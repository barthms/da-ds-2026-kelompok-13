# Kamus Data Smart Traveler Toba dan Samosir

Dokumen ini menjelaskan arti setiap kolom pada semua file data proyek, mulai dari data mentah yang diambil dari tiap sumber sampai tabel akhir yang dipakai aplikasi. Setiap anggota tim yang mengisi atau mengolah CSV wajib mengikuti nama kolom, satuan, dan format yang ada di sini, supaya data dari semua orang bisa digabungkan tanpa perlu diperbaiki satu per satu.

- **Kelompok:** 13 (Data Analitik dan Data Science, IT Del)
- **Wilayah:** Kabupaten Toba dan Kabupaten Samosir. Simalungun tidak termasuk, jadi Parapat dan Tigaras juga tidak termasuk.
- **Periode data:** 2024 sampai 2026
- **Acuan:** Daftar Variabel Final Smart Traveler versi 1.1
- **Issue:** #7

> Catatan: `Dataset_Tourism.xlsx` dan `Gabungan(waktu operasional destinasi).csv` dari dosen hanya contoh format data dan tidak dipakai sebagai sumber data proyek, sesuai arahan dosen pada 21 November 2026.

## Daftar isi

1. [Aturan umum penulisan data](#1-aturan-umum-penulisan-data)
2. [Daftar file data](#2-daftar-file-data)
3. [Kolom data yang sudah terkumpul](#3-kolom-data-yang-sudah-terkumpul)
4. [Format CSV untuk pengumpulan manual](#4-format-csv-untuk-pengumpulan-manual)
5. [Kolom tabel akhir (gudang data)](#5-kolom-tabel-akhir-gudang-data)
6. [Pemetaan kolom sumber ke tabel akhir](#6-pemetaan-kolom-sumber-ke-tabel-akhir)
7. [Nilai baku](#7-nilai-baku)
8. [Riwayat perubahan](#8-riwayat-perubahan)

---

## 1. Aturan umum penulisan data

| Hal | Aturan | Contoh benar | Contoh salah |
|---|---|---|---|
| Nama kolom | huruf kecil, kata dipisah garis bawah (snake_case) | `harga_per_malam_min` | `Harga Per Malam`, `hargaPerMalam` |
| Harga dan tarif | angka bulat dalam Rupiah, tanpa "Rp", titik, atau koma | `25000` | `Rp25.000`, `25.000`, `25rb` |
| Rentang harga | selalu dua kolom, `_min` dan `_max`. Kalau harganya tunggal, isi keduanya dengan angka yang sama | `5000` dan `10000` | `5.000 - 10.000` dalam satu kolom |
| Gratis | ditulis `0` | `0` | `gratis`, `free` |
| Tidak diketahui | dibiarkan kosong. Jangan diisi `0`, karena 0 berarti gratis | (kosong) | `0`, `-`, `NA`, `tidak tahu` |
| Tanggal | format `YYYY-MM-DD` | `2026-11-22` | `22/11/2026`, `22 Nov 2026` |
| Jam | format 24 jam `HH:MM`. Buka 24 jam ditulis `00:00` sampai `23:59` | `08:00`, `17:30` | `8 pagi`, `08.00` |
| Ya/Tidak | ditulis `ya` atau `tidak` | `ya` | `Y`, `true`, `1` |
| Daftar beberapa nilai | dipisah titik koma dan spasi (`; `) | `toilet; parkir; mushala` | `toilet, parkir, mushala` |
| Angka desimal | memakai titik | `4.5`, `2.3493` | `4,5` |
| Kabupaten | hanya `Toba` atau `Samosir` | `Toba` | `Kab. Toba`, `Tobasa`, `Toba Samosir` |
| Kecamatan | nama baku pada bagian 7.1 | `Sianjur Mula-Mula` | `Sianjur Mula Mula`, `Kec. Sianjur` |
| Sumber | setiap baris wajib punya kolom sumber (`sumber` atau `sumber_url`) dan `tanggal_ambil` | `https://...`, `2026-11-22` | (kosong) |
| Data pribadi | nama pengulas tidak boleh disimpan. Diganti kode anonim sesuai UU 27/2022 tentang Pelindungan Data Pribadi | `R00001` | nama asli pengulas |
| Encoding file | UTF-8, pemisah kolom koma. Teks yang mengandung koma diapit tanda kutip ganda | `"Jl. Pemandian, Balige"` | |

Keterangan kolom **W/O** dan **Fungsi** pada bagian 5:

- **W** = wajib diisi, **O** = opsional (diisi kalau datanya ada).
- **Fungsi:** K = kunci atau identitas, B = dipakai menghitung budget, S = dipakai menyaring (filter), U = dipakai mengurutkan rekomendasi, T = hanya ditampilkan, M = dipakai model Data Science.
- Sumber bertanda **\*** (Google Maps dan situs travel) hanya dipakai setelah ada izin dosen.

---

## 2. Daftar file data

| File | Isi | Sumber | Issue | Status |
|---|---|---|---|---|
| `data/raw/osm_poi_toba_samosir.csv` | Daftar tempat wisata, penginapan, dan restoran | OpenStreetMap (Overpass API) | #6 | Sudah ada, 428 baris |
| CSV harga tiket dan jam buka wisata | Lihat bagian 4.1 | Situs dinas pariwisata | #8 | Sedang dikumpulkan |
| CSV data BPS | Lihat bagian 4.2 | BPS Kabupaten Toba dan Samosir | #9 | Sedang dikumpulkan |
| CSV tarif transportasi | Lihat bagian 4.3 | Situs operator, ASDP, KAI | #10 | Sedang dikumpulkan |
| CSV harga penginapan | Lihat bagian 4.4 | Cek manual | #12 | Sedang dikumpulkan |
| CSV harga dan label makanan restoran | Lihat bagian 4.5 | Cek manual | #16 | Sedang dikumpulkan |
| CSV ulasan tempat | Lihat bagian 4.6 | Belum ditentukan | #13 | Menunggu izin dosen |

Nama file untuk pengumpulan manual mengikuti yang tertulis di issue masing-masing.

---

## 3. Kolom data yang sudah terkumpul

### 3.1 `osm_poi_toba_samosir.csv` (21 kolom)

Dibuat oleh `etl/extract/extract_osm.py`. Satu baris = satu tempat di OpenStreetMap. Kolom berakhiran `_raw` masih berupa nilai asli dari OSM dan baru diseragamkan di tahap transform.

| No | Kolom | Arti | Tipe | Contoh atau nilai |
|---|---|---|---|---|
| 1 | `osm_type` | Jenis objek di OSM | Kategori | `node` (titik), `way` (garis atau area), `relation` |
| 2 | `osm_id` | Nomor objek di OSM. Bersama `osm_type` menjadi kunci unik | Angka | nomor dari OSM |
| 3 | `nama` | Nama tempat. Bisa kosong kalau di OSM belum diberi nama | Teks | `Bukit Holbung` |
| 4 | `kategori_utama` | Kelompok tempat | Kategori | `wisata`, `penginapan`, `restoran` |
| 5 | `subkategori` | Jenis tempat menurut tag OSM | Kategori | `hotel`, `guest_house`, `restaurant`, `cafe`, `waterfall`, `viewpoint`, `historic_monument` |
| 6 | `kabupaten` | Kabupaten lokasi | Kategori | `Toba`, `Samosir` |
| 7 | `kecamatan` | Kecamatan lokasi. Bisa kosong kalau batas kecamatan di OSM belum lengkap | Kategori | `Balige` |
| 8 | `desa` | Desa atau dusun dari tag `addr:village` atau `addr:hamlet` | Teks | `Lumban Silintong` |
| 9 | `alamat` | Alamat dari tag `addr:*` | Teks | `Jl. Pemandian, Balige` |
| 10 | `latitude` | Garis lintang. Untuk area dipakai titik tengahnya | Desimal | `2.3493` |
| 11 | `longitude` | Garis bujur | Desimal | `99.0733` |
| 12 | `telepon` | Nomor telepon dari tag `phone` atau `contact:phone` | Teks | |
| 13 | `website` | Situs web dari tag `website` atau `contact:website` | Teks (URL) | |
| 14 | `jam_buka_raw` | Jam buka asli dari tag `opening_hours` | Teks | `Mo-Su 08:00-17:00` |
| 15 | `masakan_raw` | Jenis masakan asli dari tag `cuisine` | Teks | `regional`, `chinese` |
| 16 | `bintang_raw` | Kelas bintang asli dari tag `stars` | Teks | `3` |
| 17 | `biaya_raw` | Biaya masuk asli dari tag `charge` atau `fee` | Teks | `yes`, `10000 IDR` |
| 18 | `tag_sumber` | Tag OSM yang menentukan kategori | Teks | `tourism=hotel`, `amenity=restaurant` |
| 19 | `sumber` | Asal data | Kategori | `osm` |
| 20 | `lisensi` | Lisensi data | Teks | `ODbL (c) OpenStreetMap contributors` |
| 21 | `tanggal_ambil` | Tanggal skrip dijalankan | Tanggal | `2026-11-21` |

---

## 4. Format CSV untuk pengumpulan manual

Bagian ini berisi header CSV yang dipakai anggota tim saat mengumpulkan data secara manual. Salin baris header persis seperti di bawah, termasuk urutannya. Arti setiap kolom sama dengan kolom bernama sama di bagian 5.

### 4.1 Harga tiket dan jam buka wisata (#8)

```
nama,kabupaten,kecamatan,kategori_wisata,tiket_dewasa_min,tiket_dewasa_max,tiket_anak,parkir_motor,parkir_mobil,hari_buka,jam_buka,jam_tutup,fasilitas,sumber_url,tanggal_ambil
```

### 4.2 Data BPS (#9)

```
kabupaten,tahun,indikator,nilai,satuan,sumber_url,tanggal_ambil
```

| Kolom | Arti | Contoh |
|---|---|---|
| `tahun` | Tahun data | `2024` |
| `indikator` | Nama indikator persis seperti di tabel BPS | `Jumlah wisatawan nusantara` |
| `nilai` | Angka indikator, tanpa titik pemisah ribuan | `125000` |
| `satuan` | Satuan angka | `orang`, `unit`, `kamar` |

### 4.3 Tarif dan jadwal transportasi (#10)

```
jenis_perjalanan,moda,operator,kelas,jenis_kendaraan,kapasitas_penumpang,asal,tujuan,titik_naik,tarif_min,tarif_max,satuan_tarif,golongan_kendaraan,durasi_menit,jadwal_berangkat,tanggal_berlaku,sumber_url
```

### 4.4 Harga penginapan hari biasa dan akhir pekan (#12)

```
nama,tipe_penginapan,kabupaten,kecamatan,tipe_kamar,kapasitas_per_kamar,harga_per_malam_min,harga_per_malam_max,tanggal_menginap,akhir_pekan,termasuk_sarapan,rating,sumber,tanggal_ambil
```

Tanggal cek harga yang disepakati: Rabu 2 Desember 2026 (hari biasa) dan Sabtu 5 Desember 2026 (akhir pekan).

### 4.5 Harga makanan dan label halal restoran (#16)

```
nama,kabupaten,kecamatan,jenis_tempat_makan,jenis_masakan,label_makanan,harga_per_orang_min,harga_per_orang_max,menu_andalan,hari_buka,jam_buka,jam_tutup,rating,sumber,tanggal_ambil
```

### 4.6 Data ulasan (#13), format target

Sumber ulasan masih menunggu izin dosen. Apa pun sumbernya nanti, file ulasan wajib memakai format ini supaya bisa langsung masuk ke tabel fakta ulasan (bagian 5.6).

```
review_id,reviewer_kode,nama_tempat,kategori_utama,kabupaten,kecamatan,rating_ulasan,teks_ulasan,ada_teks,waktu_relatif_raw,tanggal_ulasan,tipe_pengunjung,sumber,tanggal_ambil
```

| Kolom | Arti | Contoh |
|---|---|---|
| `review_id` | Kode unik ulasan | `UL000001` |
| `reviewer_kode` | Kode pengganti nama pengulas. Satu nama yang sama selalu mendapat kode yang sama, dan tabel padanan nama ke kode tidak disimpan | `R00001` |
| `nama_tempat` | Nama tempat yang diulas, sama persis dengan nama di tabel tempat | `Bukit Holbung` |
| `rating_ulasan` | Bintang dari pengulas, bilangan bulat 1 sampai 5 | `5` |
| `teks_ulasan` | Isi ulasan. Kosong kalau pengulas hanya memberi bintang | `Pantainya bersih dan indah` |
| `ada_teks` | `1` kalau ulasan berisi teks, `0` kalau tidak | `1` |
| `waktu_relatif_raw` | Waktu ulasan apa adanya dari sumber | `a year ago`, `3 bulan lalu` |
| `tanggal_ulasan` | Perkiraan tanggal ulasan = `tanggal_ambil` dikurangi waktu relatif. Hanya ulasan tahun 2024 sampai 2026 yang disimpan | `2025-11-22` |
| `tipe_pengunjung` | Tipe perjalanan pengulas kalau tersedia (nilai baku di bagian 7.4) | `keluarga` |
| `sumber` | Asal data | `gmaps` |
| `tanggal_ambil` | Tanggal data diambil | `2026-11-22` |

Kolom `kategori_utama`, `kabupaten`, dan `kecamatan` sama artinya dengan kolom di tabel tempat.

Aturan konversi waktu relatif: `a year ago` atau `setahun lalu` dihitung 12 bulan sebelum `tanggal_ambil`, `3 months ago` dihitung 3 bulan sebelumnya, dan seterusnya. Di Google Maps, label "a year ago" berarti ulasan berumur 1 sampai 2 tahun, sehingga tanggal aslinya bisa lebih awal. Hal ini dicatat sebagai keterbatasan data.

---

## 5. Kolom tabel akhir (gudang data)

Bagian ini adalah 93 variabel final (60 wajib dan 33 opsional) dari Daftar Variabel Final versi 1.1. Kolom inilah yang akan ada di gudang data setelah tahap transform, berapa pun sumbernya.

### 5.1 Kolom bersama semua tempat (wisata, penginapan, restoran)

| No | Kolom | Arti | Tipe / satuan | Contoh atau kategori | Fungsi | W/O | Sumber |
|---|---|---|---|---|---|---|---|
| 1 | `place_id` | Kode unik tempat | Teks | WIS-0001, PNG-0001, RST-0001 | K | W | Dibuat saat ETL |
| 2 | `nama` | Nama tempat | Teks | Bukit Holbung | T | W | OSM, situs dinas, cek manual |
| 3 | `kategori_utama` | Kelompok tempat | Kategori | wisata, penginapan, restoran | S | W | Ditetapkan saat ETL |
| 4 | `kabupaten` | Kabupaten lokasi tempat | Kategori | Toba, Samosir (selain itu ditolak ETL) | S | W | OSM, alamat, koordinat |
| 5 | `kecamatan` | Kecamatan lokasi tempat | Kategori | Balige, Ajibata, Pangururan, Simanindo | S | W | Alamat, koordinat |
| 6 | `desa` | Desa atau kelurahan | Teks | Lumban Silintong | T | O | Alamat |
| 7 | `alamat` | Alamat lengkap | Teks | Jl. Pemandian No. 94, Balige | T | W | OSM, Google Maps* |
| 8 | `latitude` | Garis lintang | Desimal (derajat) | 2.3493 | S, U, T | W | OSM, Google Maps* |
| 9 | `longitude` | Garis bujur | Desimal (derajat) | 99.0733 | S, U, T | W | OSM, Google Maps* |
| 10 | `rating` | Rata-rata rating pengunjung | Desimal (1,0 sampai 5,0) | 4.6 | U, T | W | Google Maps* |
| 11 | `jumlah_ulasan` | Banyaknya ulasan | Angka | 1250 | U | W | Google Maps*, dihitung dari ulasan |
| 12 | `status_operasional` | Status tempat | Kategori | beroperasi, tutup sementara, tutup permanen | S | W | Google Maps*, cek manual |
| 13 | `hari_buka` | Hari operasional | Teks terstruktur | Sen-Min / Sel-Jum | S | W | Google Maps*, situs dinas, OSM |
| 14 | `jam_buka` | Jam mulai operasional | Waktu (HH:MM) | 08:00 (24 jam ditulis 00:00) | S | W | Google Maps*, situs dinas, OSM |
| 15 | `jam_tutup` | Jam selesai operasional | Waktu (HH:MM) | 17:00 (24 jam ditulis 23:59) | S | W | Google Maps*, situs dinas, OSM |
| 16 | `fasilitas` | Daftar fasilitas yang tersedia | Daftar teks | toilet; parkir; mushala; wifi | S, T | O | OSM, situs dinas, situs travel* |
| 17 | `cocok_untuk` | Tipe perjalanan yang cocok | Daftar kategori | solo, pasangan, keluarga, rombongan | S, U | O | Tipe pengulas, fasilitas, kategori |
| 18 | `kontak` | Telepon atau media sosial | Teks | 0812xxxx, @akun | T | O | OSM, Google Maps* |
| 19 | `deskripsi` | Deskripsi singkat tempat | Teks | Bukit savana dengan pemandangan danau | T | O | Situs dinas |
| 20 | `sumber` | Asal data baris ini | Kategori | osm, disbudpar, gmaps, manual | K | W | Dicatat saat ETL |
| 21 | `tanggal_ambil` | Tanggal data diambil | Tanggal | 2026-11-22 | K | W | Dicatat saat pengambilan |

### 5.2 Tempat wisata (tambahan dari kolom bersama)

| No | Kolom | Arti | Tipe / satuan | Contoh atau kategori | Fungsi | W/O | Sumber |
|---|---|---|---|---|---|---|---|
| 22 | `kategori_wisata` | Jenis wisata, dipakai untuk minat pengguna | Kategori | alam, budaya/sejarah, religi, buatan, desa wisata | S | W | OSM, situs dinas, diseragamkan |
| 23 | `subkategori` | Jenis objek yang lebih spesifik | Kategori | air terjun, bukit, pantai, museum, makam, gereja | S, T | W | OSM, situs dinas |
| 24 | `tiket_dewasa_min` | Harga tiket dewasa terendah | Angka (Rp/orang) | 5000 (gratis = 0) | B | W | Situs dinas, Google Maps* |
| 25 | `tiket_dewasa_max` | Harga tiket dewasa tertinggi | Angka (Rp/orang) | 10000 | B | W | Situs dinas |
| 26 | `tiket_anak` | Harga tiket anak | Angka (Rp/orang) | 3000 (kosong = sama dengan dewasa) | B | O | Situs dinas |
| 27 | `parkir_motor` | Biaya parkir sepeda motor | Angka (Rp/kendaraan) | 2000 | B | O | Situs dinas, ulasan |
| 28 | `parkir_mobil` | Biaya parkir mobil | Angka (Rp/kendaraan) | 5000 | B | O | Situs dinas, ulasan |
| 29 | `aktivitas` | Aktivitas yang bisa dilakukan | Daftar teks | berenang; sunset; paralayang; sewa kapal | S, T | O | Situs dinas, situs pengelola |
| 30 | `biaya_aktivitas` | Biaya aktivitas tambahan | Angka (Rp/orang) | paralayang 450000; tubing 50000 | B | O | Situs pengelola, situs dinas |
| 31 | `durasi_kunjungan_jam` | Perkiraan lama berkunjung | Desimal (jam) | 2 | B (jadwal) | W | Ditetapkan per subkategori |
| 32 | `waktu_terbaik` | Waktu terbaik berkunjung | Kategori | pagi, sunrise, sunset, malam | T | O | Ulasan, situs dinas |
| 33 | `perlu_menyeberang` | Apakah perlu menyeberang danau untuk sampai | Ya/Tidak | ya (lokasi di Pulau Samosir) | B | W | Dihitung dari kabupaten dan koordinat |
| 34 | `ramah_anak` | Cocok untuk anak-anak | Ya/Tidak | ya | S | O | Fasilitas dan ulasan |
| 35 | `tingkat_akses` | Kemudahan akses ke lokasi | Kategori | mudah, sedang, sulit | S | O | Ulasan |
| 36 | `kepemilikan` | Pengelola tempat | Kategori | pemerintah, swasta, masyarakat | T | O | Situs dinas, cek manual |
| 37 | `label_bpodt` | Penanda dari BPODT | Kategori | unggulan, hidden gem | U, T | O | Situs resmi BPODT (perlu dicek) |

### 5.3 Penginapan (tambahan dari kolom bersama)

| No | Kolom | Arti | Tipe / satuan | Contoh atau kategori | Fungsi | W/O | Sumber |
|---|---|---|---|---|---|---|---|
| 38 | `tipe_penginapan` | Jenis penginapan | Kategori | hotel, resort, villa, homestay, guest house | S | W | OSM, situs travel* |
| 39 | `kelas_bintang` | Klasifikasi bintang hotel | Angka (0 sampai 5) | 3 (non-bintang = 0) | S, U | O | Situs travel* |
| 40 | `tipe_kamar` | Jenis kamar yang dicatat harganya | Teks | Standard, Deluxe, Family | T | W | Situs travel*, cek manual |
| 41 | `harga_per_malam_min` | Harga kamar per malam terendah | Angka (Rp/kamar/malam) | 250000 | B, S | W | Situs travel*, cek manual |
| 42 | `harga_per_malam_max` | Harga kamar per malam tertinggi | Angka (Rp/kamar/malam) | 400000 | B, S | W | Situs travel*, cek manual |
| 43 | `tanggal_menginap` | Tanggal yang dicek harganya | Tanggal | 2026-11-28 | B | W | Dicatat saat cek harga |
| 44 | `akhir_pekan` | Apakah tanggal menginap jatuh di akhir pekan | Ya/Tidak | ya | B | W | Dihitung dari tanggal_menginap |
| 45 | `kapasitas_per_kamar` | Jumlah orang per kamar | Angka (orang) | 2 | B | W | Situs travel*, cek manual |
| 46 | `boleh_extra_bed` | Bisa menambah kasur | Ya/Tidak | ya | B | O | Situs travel* |
| 47 | `ada_kamar_keluarga` | Tersedia kamar keluarga | Ya/Tidak | ya | S | O | Situs travel* |
| 48 | `termasuk_sarapan` | Harga sudah termasuk sarapan | Ya/Tidak | ya (mengurangi biaya makan) | B | W | Situs travel*, cek manual |
| 49 | `view_danau` | Pemandangan Danau Toba | Ya/Tidak | ya | S, U | O | Situs travel*, ulasan |
| 50 | `jam_check_in` | Jam mulai menginap | Waktu (HH:MM) | 14:00 | T | O | Situs travel*, cek manual |
| 51 | `jam_check_out` | Jam akhir menginap | Waktu (HH:MM) | 12:00 | T | O | Situs travel*, cek manual |
| 52 | `jarak_ke_pelabuhan_km` | Jarak ke pelabuhan terdekat | Desimal (km) | 1.2 | U | O | Dihitung dari koordinat |

### 5.4 Restoran (tambahan dari kolom bersama)

| No | Kolom | Arti | Tipe / satuan | Contoh atau kategori | Fungsi | W/O | Sumber |
|---|---|---|---|---|---|---|---|
| 53 | `jenis_tempat_makan` | Jenis tempat makan | Kategori | restoran, rumah makan, kafe, lapo, warung | S | W | OSM, Google Maps* |
| 54 | `jenis_masakan` | Jenis masakan utama | Kategori | Batak, Nusantara, Chinese, Western, seafood | S | W | OSM, Google Maps* |
| 55 | `label_makanan` | Status kehalalan menu | Kategori | halal, non-halal, campur, tidak diketahui | S | W | Google Maps*, ulasan, cek manual |
| 56 | `harga_per_orang_min` | Kisaran harga makan per orang terendah | Angka (Rp/orang/makan) | 25000 | B, S | W | Google Maps*, cek manual (#16) |
| 57 | `harga_per_orang_max` | Kisaran harga makan per orang tertinggi | Angka (Rp/orang/makan) | 50000 | B, S | W | Google Maps*, cek manual (#16) |
| 58 | `menu_andalan` | Menu yang direkomendasikan | Daftar teks | arsik; naniura; mie gomak | T | O | Ulasan, cek manual (#16) |
| 59 | `waktu_makan` | Waktu makan yang dilayani | Daftar kategori | sarapan, siang, malam | S | O | Dihitung dari jam buka |
| 60 | `cocok_rombongan` | Bisa menampung rombongan | Ya/Tidak | ya | S | O | Fasilitas, ulasan |

### 5.5 Transportasi (satu baris = satu rute + moda + golongan)

| No | Kolom | Arti | Tipe / satuan | Contoh atau kategori | Fungsi | W/O | Sumber |
|---|---|---|---|---|---|---|---|
| 61 | `transport_id` | Kode unik rute | Teks | TRP-0001 | K | W | Dibuat saat ETL |
| 62 | `jenis_perjalanan` | Bagian perjalanan | Kategori | antarkota, penyeberangan, lokal | B | W | Ditetapkan |
| 63 | `moda` | Jenis kendaraan | Kategori | travel, bus, kereta, ferry, kapal kayu, sewa motor, sewa mobil | S | W | Situs operator, ASDP, KAI |
| 64 | `operator` | Penyedia layanan | Teks | KBT, KPT, ASDP, KAI | T | W | Situs atau media sosial operator |
| 65 | `kelas` | Kelas layanan | Kategori | reguler, eksekutif, ekspres | S | O | Situs operator |
| 66 | `jenis_kendaraan` | Jenis unit kendaraan | Teks | L300, Hiace, KMP Ihan Batak | T | O | Situs operator |
| 67 | `kapasitas_penumpang` | Jumlah kursi | Angka (orang) | 8 | B (carter) | O | Situs operator |
| 68 | `asal` | Kota atau titik keberangkatan | Teks | Medan, Pematangsiantar, Ajibata | S | W | Situs operator |
| 69 | `tujuan` | Kota atau titik tujuan | Teks | Balige, Tomok | S | W | Situs operator |
| 70 | `kecamatan_tujuan` | Kecamatan tujuan (untuk filter jelajah) | Kategori | Ajibata, Simanindo | S | W | Dihitung dari tujuan |
| 71 | `titik_naik` | Lokasi naik kendaraan | Teks | Loket KBT Amplas, Pelabuhan Ajibata | T | O | Situs operator |
| 72 | `tarif_min` | Tarif terendah | Angka (Rp) | 80000 | B | W | Situs operator, ASDP, berita resmi |
| 73 | `tarif_max` | Tarif tertinggi | Angka (Rp) | 100000 | B | W | Situs operator, ASDP, berita resmi |
| 74 | `satuan_tarif` | Cara menghitung tarif | Kategori | per orang, per kendaraan, per hari | B | W | Ditetapkan dari sumber |
| 75 | `golongan_kendaraan` | Golongan tiket ferry | Kategori | penumpang, II (motor), IVA (mobil) | B | W (ferry) | Tarif ASDP |
| 76 | `durasi_menit` | Lama perjalanan | Angka (menit) | 240 | B (jadwal) | W | Situs operator, ASDP |
| 77 | `jadwal_berangkat` | Jam keberangkatan | Daftar waktu | 05:30; 08:40; 10:40 | S | O | ASDP, situs operator |
| 78 | `jarak_km` | Jarak tempuh (untuk mobil pribadi) | Desimal (km) | 176 | B | O | Dihitung dari koordinat |
| 79 | `tanggal_berlaku` | Tanggal tarif berlaku (hanya 2024 sampai 2026) | Tanggal | 2026-11-01 | K | W | Dicatat dari sumber |
| 80 | `sumber_url` | Tautan sumber tarif | Teks (URL) | https://... | K | W | Dicatat dari sumber |

### 5.6 Ulasan (tabel fakta, minimal 5.000 baris)

| No | Kolom | Arti | Tipe / satuan | Contoh atau kategori | Fungsi | W/O | Sumber |
|---|---|---|---|---|---|---|---|
| 81 | `review_id` | Kode unik ulasan | Teks | UL000001 | K | W | Dibuat saat ETL |
| 82 | `place_id` | Tempat yang diulas | Teks (kunci tamu) | WIS-0001 | K | W | Dicocokkan saat ETL |
| 83 | `reviewer_kode` | Pengganti nama pengulas (anonim) | Teks | R00001 | K | W | Dibuat saat ETL (UU PDP) |
| 84 | `rating_ulasan` | Bintang yang diberikan pengulas | Angka (1 sampai 5) | 5 | M (label) | W | Google Maps* (#13) |
| 85 | `teks_ulasan` | Isi ulasan | Teks | Pantainya bersih dan indah | M (input) | W | Google Maps* (#13) |
| 86 | `ada_teks` | Apakah ulasan berisi teks | Ya/Tidak | tidak (hanya bintang) | M (saring) | W | Dihitung saat ETL |
| 87 | `tanggal_ulasan` | Perkiraan tanggal ulasan (hanya 2024 sampai 2026) | Tanggal | 2025-11-22 (dari "a year ago") | S, T | W | Dikonversi dari waktu relatif (lihat keputusan g) |
| 88 | `tipe_pengunjung` | Tipe perjalanan pengulas | Kategori | keluarga, pasangan, teman, solo, bisnis | S | O | Google Maps* (#13) |
| 89 | `sentimen` | Hasil model analisis sentimen | Kategori | positif, netral, negatif | U, T | W | Hasil model DS |
| 90 | `skor_sentimen` | Keyakinan model | Desimal (0 sampai 1) | 0.94 | U | O | Hasil model DS |

### 5.7 Variabel turunan per tempat (dihitung dari ulasan)

| No | Kolom | Arti | Tipe / satuan | Contoh atau kategori | Fungsi | W/O | Sumber |
|---|---|---|---|---|---|---|---|
| 91 | `persen_ulasan_positif` | Proporsi ulasan positif di tempat itu | Persen | 92 | U, T | W | Agregasi hasil model |
| 92 | `jumlah_ulasan_teks` | Banyaknya ulasan yang berisi teks | Angka | 640 | U | W | Agregasi tabel ulasan |
| 93 | `skor_rekomendasi` | Skor gabungan untuk mengurutkan pilihan | Desimal (0 sampai 1) | gabungan rating, sentimen, jumlah ulasan, jarak | U | W | Rumus sistem |

---

## 6. Pemetaan kolom sumber ke tabel akhir

Tabel ini menunjukkan kolom mentah mana yang menjadi kolom akhir, dan apa yang perlu dilakukan di tahap transform.

### 6.1 Dari OpenStreetMap

| Kolom OSM | Kolom akhir | Pengolahan |
|---|---|---|
| `nama` | `nama` | Tempat tanpa nama dibuang atau dilengkapi dari sumber lain |
| `kategori_utama` | `kategori_utama` | Langsung |
| `subkategori` | `subkategori`, `kategori_wisata`, `tipe_penginapan`, `jenis_tempat_makan` | Diterjemahkan ke nilai baku (bagian 7) |
| `kecamatan`, `desa`, `alamat` | `kecamatan`, `desa`, `alamat` | Kecamatan yang kosong dilengkapi dari koordinat |
| `latitude`, `longitude` | `latitude`, `longitude` | Langsung |
| `telepon`, `website` | `kontak` | Digabung |
| `jam_buka_raw` | `hari_buka`, `jam_buka`, `jam_tutup` | Dipecah. Contoh `Mo-Su 08:00-17:00` menjadi `Sen-Min`, `08:00`, `17:00` |
| `masakan_raw` | `jenis_masakan` | Diterjemahkan ke nilai baku |
| `bintang_raw` | `kelas_bintang` | Diubah ke angka |
| `biaya_raw` | `tiket_dewasa_min`, `tiket_dewasa_max` | Hanya dipakai kalau berisi angka |

### 6.2 Dari file ulasan (#13)

| Kolom file ulasan (#13) | Kolom akhir | Pengolahan |
|---|---|---|
| `nama_tempat` | `place_id` | Dicocokkan dengan tabel tempat |
| `review_id`, `reviewer_kode`, `rating_ulasan`, `teks_ulasan`, `ada_teks`, `tanggal_ulasan` | kolom bernama sama | Langsung |
| `tipe_pengunjung` | `tipe_pengunjung` | Diseragamkan (bagian 7.4) |
| (belum ada) | `sentimen`, `skor_sentimen` | Diisi dari hasil model DS (#11) |

---

## 7. Nilai baku

### 7.1 Kecamatan

| Kabupaten | Kecamatan (nama baku) |
|---|---|
| Toba (16) | Ajibata, Balige, Bonatua Lunasi, Bor-Bor, Habinsaran, Laguboti, Lumban Julu, Nassau, Parmaksian, Pintu Pohan Meranti, Porsea, Siantar Narumonda, Sigumpar, Silaen, Tampahan, Uluan |
| Samosir (9) | Harian, Nainggolan, Onan Runggu, Palipi, Pangururan, Ronggur Nihuta, Sianjur Mula-Mula, Simanindo, Sitio-tio |

### 7.2 Kategori tempat

| Kolom | Nilai yang boleh dipakai |
|---|---|
| `kategori_utama` | `wisata`, `penginapan`, `restoran` |
| `kategori_wisata` | `alam`, `budaya/sejarah`, `religi`, `buatan`, `desa wisata` |
| `tipe_penginapan` | `hotel`, `resort`, `villa`, `homestay`, `guest house` |
| `jenis_tempat_makan` | `restoran`, `rumah makan`, `kafe`, `lapo`, `warung` |
| `label_makanan` | `halal`, `non-halal`, `campur`, `tidak diketahui` |
| `status_operasional` | `beroperasi`, `tutup sementara`, `tutup permanen` |
| `cocok_untuk` | `solo`, `pasangan`, `keluarga`, `rombongan` |

### 7.3 Aturan awal kategori wisata dari tag OSM

| `subkategori` OSM | `kategori_wisata` |
|---|---|
| `waterfall`, `beach`, `peak`, `hot_spring`, `cave_entrance`, `viewpoint`, `nature_reserve`, `picnic_site` | `alam` |
| `museum`, semua yang berawalan `historic_` | `budaya/sejarah` |
| `theme_park`, `zoo`, `water_park` | `buatan` |
| `attraction` | ditentukan manual per tempat |

Gereja, makam tokoh agama, dan patung bertema agama dimasukkan ke `religi` secara manual.

### 7.4 Tipe pengunjung

Nilai yang boleh dipakai: `keluarga`, `pasangan`, `teman`, `solo`, `bisnis`. Kalau sumber hanya menulis tujuan perjalanan tanpa pendamping (misalnya "Liburan"), kolom ini dikosongkan.

### 7.5 Transportasi

| Kolom | Nilai yang boleh dipakai |
|---|---|
| `jenis_perjalanan` | `antarkota`, `penyeberangan`, `lokal` |
| `moda` | `travel`, `bus`, `kereta`, `ferry`, `kapal kayu`, `sewa motor`, `sewa mobil` |
| `satuan_tarif` | `per orang`, `per kendaraan`, `per hari` |
| `golongan_kendaraan` | `penumpang`, `II` (motor), `IVA` (mobil) |

Penyeberangan yang dipakai hanya Ajibata-Tomok, Ajibata-Ambarita, dan Balige-Onan Runggu. Tigaras tidak dipakai karena masuk Simalungun.

---

## 8. Riwayat perubahan

| Versi | Tanggal | Perubahan |
|---|---|---|
| 1.0 | 2026-11-21 | Versi pertama. Berisi kolom OSM (#6), format CSV manual (#8, #9, #10, #12, #16), format target data ulasan (#13), dan 93 variabel final dari Daftar Variabel Final v1.1. Perbedaan dengan v1.1: (1) dataset dari dosen tidak dicantumkan sebagai sumber karena hanya contoh format, (2) format `review_id` dan `reviewer_kode` menjadi `UL000001` dan `R00001`. |
