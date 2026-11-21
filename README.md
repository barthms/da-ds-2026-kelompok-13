# Smart Traveler: Sistem Jelajah dan Rencana Wisata Berbasis Budget di Kabupaten Toba dan Samosir

## Deskripsi Proyek

Smart Traveler merupakan proyek Data Analytics dan Data Science yang bertujuan membantu wisatawan mengeksplorasi destinasi wisata dan merencanakan perjalanan berdasarkan anggaran yang dimiliki.

Sistem ini berfokus pada Kabupaten Toba dan Kabupaten Samosir. Pengguna dapat mencari informasi tempat wisata, penginapan, restoran, dan transportasi, serta memperoleh rekomendasi rencana perjalanan yang disesuaikan dengan budget, jumlah orang, durasi perjalanan, dan preferensi wisata.

## Latar Belakang

Kabupaten Toba dan Kabupaten Samosir memiliki berbagai potensi wisata yang menarik untuk dikunjungi. Namun, wisatawan sering menghadapi kesulitan dalam memperoleh informasi terintegrasi mengenai destinasi wisata, penginapan, restoran, transportasi, dan perkiraan biaya perjalanan.

Informasi yang tersebar di berbagai sumber membuat proses perencanaan perjalanan menjadi kurang praktis. Wisatawan juga perlu mempertimbangkan anggaran agar perjalanan yang direncanakan sesuai dengan kemampuan finansial.

Oleh karena itu, Smart Traveler dirancang untuk mengintegrasikan pengolahan data pariwisata, analisis data, dan pendekatan Data Science dalam membantu wisatawan mengeksplorasi destinasi serta menyusun rencana perjalanan berdasarkan budget.

## Tujuan Proyek

1. Mengintegrasikan informasi pariwisata di Kabupaten Toba dan Kabupaten Samosir.
2. Mempermudah wisatawan menemukan tempat wisata, penginapan, restoran, dan transportasi.
3. Membantu wisatawan menyusun rencana perjalanan berdasarkan anggaran.
4. Menerapkan Data Analytics untuk mengolah dan menganalisis data pariwisata.
5. Menerapkan pendekatan Data Science untuk mendukung analisis ulasan dan pemeringkatan rekomendasi wisata.

## Cakupan Data

**Wilayah**

- Kabupaten Toba, Sumatera Utara.
- Kabupaten Samosir, Sumatera Utara.

Data destinasi wisata, penginapan, dan restoran dibatasi pada kedua kabupaten tersebut. Kabupaten Simalungun tidak termasuk, sehingga Parapat dan Tigaras juga tidak termasuk. Wilayah di luar cakupan hanya digunakan sebagai titik asal perjalanan untuk kebutuhan perhitungan transportasi, misalnya Medan atau Pematangsiantar.

**Periode**

Data yang digunakan berasal dari periode 2024 sampai 2026, termasuk tanggal ulasan dan tanggal berlaku harga.

## Fitur Utama

### 1. Jelajah

Fitur Jelajah membantu pengguna menemukan dan mengeksplorasi informasi pariwisata berdasarkan lokasi dan preferensi.

Kategori informasi yang direncanakan meliputi:

- **Wisata:** destinasi dan tempat rekreasi.
- **Penginapan:** hotel, homestay, dan jenis akomodasi lainnya.
- **Restoran:** tempat makan beserta informasi harga dan kategori makanan.
- **Transportasi:** pilihan transportasi dan informasi biaya perjalanan.

Pengguna dapat melakukan pencarian dan penyaringan berdasarkan kabupaten, kecamatan, kategori, kisaran harga, rating, jenis makanan, dan tipe perjalanan.

Hasil pencarian direncanakan ditampilkan dalam bentuk daftar dan peta.

### 2. Rencana Budget

Fitur Rencana Budget membantu pengguna menyusun alternatif perjalanan berdasarkan anggaran yang dimiliki.

Informasi yang dapat dimasukkan pengguna meliputi:

- Kota asal perjalanan.
- Total anggaran.
- Jumlah orang (dewasa dan anak).
- Jenis perjalanan (solo, pasangan, keluarga, atau rombongan).
- Durasi perjalanan.
- Minat atau preferensi wisata.
- Moda transportasi.
- Preferensi makanan.
- Jenis penginapan.

Berdasarkan informasi tersebut, sistem dirancang untuk menghasilkan 1 sampai 3 alternatif paket perjalanan yang disesuaikan dengan anggaran pengguna.

Perhitungan biaya direncanakan mencakup:

1. Transportasi perjalanan pergi dan pulang.
2. Biaya penyeberangan apabila tujuan berada di Pulau Samosir.
3. Biaya penginapan.
4. Biaya makan.
5. Tiket masuk destinasi wisata (dewasa dan anak), aktivitas, dan parkir.

Perhitungan penginapan mempertimbangkan jumlah orang, kapasitas kamar, jumlah kamar yang dibutuhkan, dan lama menginap. Perhitungan makanan mempertimbangkan harga per orang, jumlah orang, dan jumlah waktu makan. Sarapan tidak dihitung kembali apabila sudah termasuk dalam harga penginapan.

Informasi harga transportasi dan penginapan perlu disertai tanggal berlaku atau tanggal menginap karena dapat berubah berdasarkan waktu.

## Integrasi Data Analytics dan Data Science

Proyek Smart Traveler mengintegrasikan Data Analytics dan Data Science untuk mendukung pengolahan data serta pengembangan rekomendasi wisata.

### Data Analytics

Proses Data Analytics direncanakan mencakup:

1. **Data Collection:** mengumpulkan data destinasi wisata, lokasi, penginapan, restoran, transportasi, harga, dan ulasan.
2. **ETL:** melakukan proses Extract, Transform, dan Load untuk membersihkan, mengintegrasikan, serta menyiapkan data.
3. **Data Warehouse:** menyusun data warehouse menggunakan pendekatan star schema.
4. **Exploratory Data Analysis (EDA):** mengeksplorasi karakteristik dan pola data pariwisata.
5. **Dashboard Analytics:** menyajikan informasi dan hasil analisis data pariwisata melalui visualisasi.

Rancangan data warehouse mencakup tabel fakta `fact_ulasan` serta tabel dimensi seperti `dim_tempat`, `dim_lokasi`, `dim_waktu`, dan `dim_sumber`.

Arti setiap kolom data dijelaskan dalam kamus data di [`docs/data_dictionary.md`](docs/data_dictionary.md).

### Data Science

Pendekatan Data Science direncanakan untuk menganalisis sentimen ulasan wisata ke dalam tiga kategori:

- Positif.
- Netral.
- Negatif.

Rencana pengembangan model mencakup penggunaan minimal tiga algoritma untuk membandingkan performa model klasifikasi sentimen.

Hasil analisis sentimen direncanakan menjadi salah satu pertimbangan dalam pemeringkatan rekomendasi tempat wisata.

**Catatan:** Rancangan analisis sentimen dan penggunaan beberapa algoritma masih menunggu konfirmasi dosen sehingga belum dinyatakan sebagai ketetapan akhir proyek.

## Sumber Data dan Atribusi

Data Smart Traveler direncanakan diperoleh dari beberapa sumber, antara lain:

- OpenStreetMap untuk informasi lokasi dan data geografis.
- Dinas Pariwisata dan instansi terkait untuk informasi pariwisata.
- Badan Pusat Statistik (BPS) untuk data pendukung wilayah dan pariwisata.
- Sumber informasi harga dan transportasi dari penyedia layanan terkait.
- Pengumpulan data secara manual dari sumber yang dapat dipertanggungjawabkan.

Dataset yang diberikan dosen hanya digunakan sebagai contoh format data dan tidak digunakan sebagai sumber data proyek. Sumber data ulasan masih menunggu izin dosen.

Penggunaan data dari setiap sumber akan memperhatikan ketentuan akses, lisensi, atribusi, dan izin yang berlaku.

Atribusi OpenStreetMap:

> © OpenStreetMap contributors. Data tersedia di bawah Open Database License (ODbL). Informasi lengkap: https://www.openstreetmap.org/copyright

Data ulasan yang digunakan untuk analisis memperhatikan privasi pengguna. Nama pemberi ulasan tidak disimpan dan diganti dengan kode anonim (`reviewer_kode`), sesuai Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi.

## Struktur Repositori

```text
.
├── README.md
├── app/                 # Area pengembangan aplikasi
├── data/
│   ├── raw/             # Data mentah dari setiap sumber
│   ├── processed/       # Data hasil olah
│   └── reference/       # Data referensi
├── docs/                # Dokumentasi, kamus data, dan kualitas data
├── etl/                 # Skrip Extract, Transform, dan Load
├── models/              # Model Machine Learning dan model card
├── notebooks/           # Notebook EDA dan eksperimen model
├── paper/               # Penulisan dan dokumentasi jurnal
├── reports/
│   └── weekly/          # Laporan perkembangan mingguan
└── warehouse/           # Skema data warehouse dan ERD
```

## Teknologi yang Digunakan

Teknologi yang sudah digunakan:

- Python 3 dan library `requests` untuk pengambilan data.
- Overpass API untuk mengambil data OpenStreetMap.
- Git dan GitHub untuk pengelolaan kode sumber dan pelacakan pekerjaan.

Teknologi untuk tahap berikutnya (pengolahan data, data warehouse, model Machine Learning, aplikasi, dan visualisasi) akan dicantumkan setelah ditetapkan dan digunakan dalam implementasi proyek.

## Instalasi dan Penggunaan

Repositori ini masih berada pada tahap pengumpulan data. Komponen yang sudah dapat dijalankan adalah skrip pengambilan data tempat dari OpenStreetMap.

```bash
pip install requests
python etl/extract/extract_osm.py
```

Hasilnya tersimpan di `data/raw/osm_poi_toba_samosir.csv`, berisi daftar tempat wisata, penginapan, dan restoran di Kabupaten Toba dan Kabupaten Samosir.

Petunjuk instalasi dan penggunaan untuk aplikasi, pipeline ETL lengkap, data warehouse, dan model akan ditambahkan setelah komponen tersebut tersedia.

## Anggota Kelompok

| Nama | NIM | Tanggung Jawab |
|---|---|---|
| Win Grace Sitanggang | 41424023 | Project Manager |
| Lastri Hutagalung | 41424019 | Data Engineer |
| Hizkia Siahaan | 41424003 | Data Analyst |
| David Sinurat | 41424004 | ML Engineer |
| Andika Purba | 41424001 | Deployment Engineer |

---

**Smart Traveler**

Proyek Data Analytics dan Data Science, Kelompok 13
Institut Teknologi Del
