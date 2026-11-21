"""
Ekstraksi POI (tempat wisata, penginapan, restoran) di Kabupaten Toba dan
Kabupaten Samosir dari OpenStreetMap melalui Overpass API.

Hasil : data/raw/osm_poi_toba_samosir.csv

Alur  : 1) ambil semua tempat di tingkat kabupaten (data lengkap),
        2) ambil tempat per kecamatan untuk mengisi kolom kecamatan,
        3) gabungkan. Tempat yang kecamatannya belum diketahui tetap disimpan
           dengan kecamatan kosong, lalu dilengkapi di tahap transform.
Cara  : python etl/extract/extract_osm.py
Lisensi data: Open Database License (ODbL), (c) OpenStreetMap contributors.

Skrip ini aman dijalankan ulang. Setiap kali dijalankan, file hasil ditimpa
dengan data terbaru dan kolom tanggal_ambil diperbarui.
"""

import argparse
import csv
import sys
import time
from collections import Counter
from datetime import date
from pathlib import Path

import requests

# ------------------------------------------------------------------ konfigurasi
ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DEFAULT = ROOT / "data" / "raw" / "osm_poi_toba_samosir.csv"

ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
USER_AGENT = "smart-traveler-kelompok13-itdel/1.0 (proyek akademik)"
JEDA_DETIK = 5          # jeda antarpermintaan agar tidak membebani server
TIMEOUT_DETIK = 300

# Nama wilayah di OSM bisa berbeda-beda, jadi dicocokkan dengan pola.
# Samosir diproses lebih dulu. Jika di OSM masih ada batas lama "Toba Samosir"
# (sebelum pemekaran 2003) yang ikut mencakup Pulau Samosir, tempat yang sama
# tetap tercatat sebagai Samosir karena duplikat dihapus dengan menyimpan
# kemunculan pertama.
KABUPATEN = {
    "Samosir": r"^(Kabupaten )?Samosir$",
    "Toba": r"^(Kabupaten )?Toba( Samosir)?$",
}

# Tag OSM yang diambil untuk setiap kategori utama.
FILTER_POI = """
  nwr(area.{a})["tourism"~"^(hotel|guest_house|hostel|motel|apartment|chalet|camp_site)$"];
  nwr(area.{a})["leisure"="resort"];
  nwr(area.{a})["amenity"~"^(restaurant|cafe|fast_food|food_court)$"];
  nwr(area.{a})["tourism"~"^(attraction|viewpoint|museum|theme_park|zoo|picnic_site)$"];
  nwr(area.{a})["natural"~"^(waterfall|beach|peak|hot_spring|cave_entrance)$"];
  nwr(area.{a})["leisure"~"^(water_park|beach_resort|nature_reserve)$"];
  nwr(area.{a})["historic"];
"""

KOLOM = [
    "osm_type", "osm_id", "nama", "kategori_utama", "subkategori",
    "kabupaten", "kecamatan", "desa", "alamat", "latitude", "longitude",
    "telepon", "website", "jam_buka_raw", "masakan_raw", "bintang_raw",
    "biaya_raw", "tag_sumber", "sumber", "lisensi", "tanggal_ambil",
]


# ------------------------------------------------------------------ query
def buat_query(pola_kabupaten: str) -> str:
    """Query Overpass: semua POI per kecamatan di dalam satu kabupaten.

    Untuk setiap kecamatan (admin_level 6), Overpass mengirim dulu elemen
    'area' kecamatan itu, lalu daftar POI di dalamnya. Urutan ini dipakai
    untuk mengisi kolom kecamatan.
    """
    return f"""
[out:json][timeout:{TIMEOUT_DETIK}];
area["boundary"="administrative"]["admin_level"="5"]["name"~"{pola_kabupaten}"]->.kab;
rel(area.kab)["boundary"="administrative"]["admin_level"="6"];
map_to_area->.semua_kec;
foreach.semua_kec->.kec(
  .kec out tags;
  ({FILTER_POI.format(a="kec")});
  out center tags;
);
"""


def buat_query_cadangan(pola_kabupaten: str) -> str:
    """Query cadangan jika batas kecamatan tidak tersedia di OSM."""
    return f"""
[out:json][timeout:{TIMEOUT_DETIK}];
area["boundary"="administrative"]["admin_level"="5"]["name"~"{pola_kabupaten}"]->.kab;
({FILTER_POI.format(a="kab")});
out center tags;
"""


def ambil(query: str) -> list:
    """Kirim query ke Overpass dengan percobaan ulang ke server cadangan."""
    pesan_error = []
    for endpoint in ENDPOINTS:
        for percobaan in range(1, 4):
            try:
                resp = requests.post(
                    endpoint,
                    data={"data": query},
                    headers={"User-Agent": USER_AGENT},
                    timeout=TIMEOUT_DETIK + 30,
                )
                if resp.status_code == 200:
                    return resp.json().get("elements", [])
                pesan_error.append(f"{endpoint} percobaan {percobaan}: HTTP {resp.status_code}")
            except requests.RequestException as e:
                pesan_error.append(f"{endpoint} percobaan {percobaan}: {e}")
            time.sleep(JEDA_DETIK * percobaan)
    raise RuntimeError("Gagal mengambil data dari Overpass:\n  " + "\n  ".join(pesan_error))


# ------------------------------------------------------------------ olah tag
def tentukan_kategori(tags: dict):
    """Kembalikan (kategori_utama, subkategori, tag_sumber) dari tag OSM."""
    t = tags.get
    if t("tourism") in {"hotel", "guest_house", "hostel", "motel", "apartment", "chalet", "camp_site"}:
        return "penginapan", t("tourism"), f"tourism={t('tourism')}"
    if t("leisure") == "resort":
        return "penginapan", "resort", "leisure=resort"
    if t("amenity") in {"restaurant", "cafe", "fast_food", "food_court"}:
        return "restoran", t("amenity"), f"amenity={t('amenity')}"
    if t("natural") in {"waterfall", "beach", "peak", "hot_spring", "cave_entrance"}:
        return "wisata", t("natural"), f"natural={t('natural')}"
    if t("tourism") in {"attraction", "viewpoint", "museum", "theme_park", "zoo", "picnic_site"}:
        return "wisata", t("tourism"), f"tourism={t('tourism')}"
    if t("leisure") in {"water_park", "beach_resort", "nature_reserve"}:
        return "wisata", t("leisure"), f"leisure={t('leisure')}"
    if t("historic"):
        return "wisata", f"historic_{t('historic')}", f"historic={t('historic')}"
    return None, None, None


def susun_alamat(tags: dict) -> str:
    if tags.get("addr:full"):
        return tags["addr:full"]
    bagian = [
        " ".join(x for x in [tags.get("addr:street"), tags.get("addr:housenumber")] if x),
        tags.get("addr:village") or tags.get("addr:hamlet"),
        tags.get("addr:subdistrict"),
        tags.get("addr:city") or tags.get("addr:district"),
    ]
    return ", ".join(b for b in bagian if b)


def koordinat(el: dict):
    if "lat" in el and "lon" in el:
        return el["lat"], el["lon"]
    if "center" in el:
        return el["center"]["lat"], el["center"]["lon"]
    return None, None


def bersihkan_nama_kecamatan(nama: str) -> str:
    for awalan in ("Kecamatan ", "Kec. ", "Kec "):
        if nama.startswith(awalan):
            return nama[len(awalan):]
    return nama


def ke_baris(el: dict, kabupaten: str, kecamatan: str, tanggal: str):
    tags = el.get("tags", {})
    kategori, sub, tag_sumber = tentukan_kategori(tags)
    if kategori is None:
        return None
    lat, lon = koordinat(el)
    return {
        "osm_type": el.get("type"),
        "osm_id": el.get("id"),
        "nama": tags.get("name", "").strip(),
        "kategori_utama": kategori,
        "subkategori": sub,
        "kabupaten": kabupaten,
        "kecamatan": kecamatan,
        "desa": tags.get("addr:village") or tags.get("addr:hamlet") or "",
        "alamat": susun_alamat(tags),
        "latitude": lat,
        "longitude": lon,
        "telepon": tags.get("phone") or tags.get("contact:phone") or "",
        "website": tags.get("website") or tags.get("contact:website") or "",
        "jam_buka_raw": tags.get("opening_hours", ""),
        "masakan_raw": tags.get("cuisine", ""),
        "bintang_raw": tags.get("stars", ""),
        "biaya_raw": tags.get("charge") or tags.get("fee") or "",
        "tag_sumber": tag_sumber,
        "sumber": "osm",
        "lisensi": "ODbL (c) OpenStreetMap contributors",
        "tanggal_ambil": tanggal,
    }


def proses_elemen(elements: list, kabupaten: str, tanggal: str) -> list:
    """Ubah elemen Overpass menjadi baris CSV, mengikuti urutan area kecamatan."""
    baris, kecamatan = [], ""
    for el in elements:
        if el.get("type") == "area":
            kecamatan = bersihkan_nama_kecamatan(el.get("tags", {}).get("name", ""))
            continue
        b = ke_baris(el, kabupaten, kecamatan, tanggal)
        if b:
            baris.append(b)
    return baris


# ------------------------------------------------------------------ utama
def main():
    parser = argparse.ArgumentParser(description="Ekstraksi POI OpenStreetMap Toba dan Samosir")
    parser.add_argument("--output", default=str(OUTPUT_DEFAULT), help="lokasi file CSV hasil")
    args = parser.parse_args()

    tanggal = date.today().isoformat()
    semua = []

    for kabupaten, pola in KABUPATEN.items():
        # 1) Semua POI di tingkat kabupaten, agar tidak ada tempat yang terlewat
        #    walaupun batas kecamatannya belum tersedia di OSM.
        print(f"[{kabupaten}] mengambil semua tempat di tingkat kabupaten ...")
        baris_kab = proses_elemen(ambil(buat_query_cadangan(pola)), kabupaten, tanggal)
        time.sleep(JEDA_DETIK)

        # 2) POI per kecamatan, hanya dipakai untuk mengisi kolom kecamatan.
        print(f"[{kabupaten}] mencocokkan kecamatan dari batas wilayah OSM ...")
        elemen_kec = ambil(buat_query(pola))
        baris_kec = proses_elemen(elemen_kec, kabupaten, tanggal)
        nama_kec = sorted({e.get("tags", {}).get("name", "") for e in elemen_kec if e.get("type") == "area"})
        peta_kec = {(b["osm_type"], b["osm_id"]): b["kecamatan"] for b in baris_kec if b["kecamatan"]}
        time.sleep(JEDA_DETIK)

        # 3) Gabungkan: data lengkap dari langkah 1, kecamatan dari langkah 2.
        kunci_kab = set()
        for b in baris_kab:
            kunci = (b["osm_type"], b["osm_id"])
            kunci_kab.add(kunci)
            b["kecamatan"] = peta_kec.get(kunci, "")
        tambahan = [b for b in baris_kec if (b["osm_type"], b["osm_id"]) not in kunci_kab]
        baris = baris_kab + tambahan

        terisi = sum(1 for b in baris if b["kecamatan"])
        print(f"[{kabupaten}] {len(baris)} tempat, kecamatan terisi {terisi}, "
              f"batas kecamatan di OSM: {len(nama_kec)}")
        if nama_kec:
            print(f"[{kabupaten}] kecamatan yang punya batas di OSM: {', '.join(bersihkan_nama_kecamatan(k) for k in nama_kec)}")
        if not baris:
            print(f"[{kabupaten}] PERINGATAN: tidak ada data. Cek nama kabupaten di OSM.")
        semua.extend(baris)

    # Hapus duplikat (elemen yang sama bisa muncul di dua query)
    unik, terlihat = [], set()
    for b in semua:
        kunci = (b["osm_type"], b["osm_id"])
        if kunci not in terlihat:
            terlihat.add(kunci)
            unik.append(b)

    tanpa_nama = sum(1 for b in unik if not b["nama"])

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=KOLOM)
        w.writeheader()
        w.writerows(unik)

    print("\n=== Ringkasan ===")
    print(f"File       : {out}")
    print(f"Total baris: {len(unik)} (tanpa nama: {tanpa_nama}, tetap disimpan untuk dicek di tahap transform)")
    hitung = Counter((b["kabupaten"], b["kategori_utama"]) for b in unik)
    for (kab, kat), jml in sorted(hitung.items()):
        print(f"  {kab:<8} {kat:<11} {jml}")

    print("\nPemeriksaan wilayah (rentang koordinat per kabupaten):")
    for kab in KABUPATEN:
        titik = [(b["latitude"], b["longitude"]) for b in unik
                 if b["kabupaten"] == kab and b["latitude"] is not None]
        if titik:
            lats = [t[0] for t in titik]
            lons = [t[1] for t in titik]
            kosong = sum(1 for b in unik if b["kabupaten"] == kab and not b["kecamatan"])
            print(f"  {kab:<8} lat {min(lats):.3f} s.d. {max(lats):.3f} | lon {min(lons):.3f} s.d. {max(lons):.3f}"
                  f" | kecamatan kosong: {kosong} (diisi di tahap transform)")

    if not unik:
        print("\nPERINGATAN: tidak ada data. Cek nama kabupaten di OSM atau koneksi internet.")
        sys.exit(1)


if __name__ == "__main__":
    main()
