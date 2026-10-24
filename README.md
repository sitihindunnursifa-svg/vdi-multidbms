
# Sales Analytics Dashboard — Multi-DBMS Data Pipeline

## 1. Deskripsi Proyek

Proyek ini merupakan aplikasi visualisasi data penjualan berbasis web menggunakan Python. Aplikasi mengintegrasikan data dari dua sistem manajemen basis data (DBMS), yaitu PostgreSQL dan SQLite.

Data diolah menggunakan Pandas dan ditampilkan melalui dashboard interaktif menggunakan Streamlit dan Plotly.

## 2. Tujuan

- Mengimplementasikan integrasi minimal dua DBMS.
- Mengolah dan menggabungkan data menggunakan Pandas.
- Menyajikan informasi penjualan melalui visualisasi interaktif.
- Menyediakan filter data dan fitur unduh hasil analisis.
- Menerapkan pengelolaan kredensial melalui environment variables.

## 3. Teknologi yang Digunakan

- Python
- PostgreSQL melalui Supabase
- SQLite
- Pandas
- SQLAlchemy
- Streamlit
- Plotly
- python-dotenv

## 4. Arsitektur Sistem

Proyek menggunakan dua database dengan peran berikut:

1. **PostgreSQL (Supabase):** menyimpan data master produk pada tabel `master_produk`.
2. **SQLite:** menyimpan data transaksi yang telah dibersihkan pada tabel `transaksi`.
3. **Pandas:** membaca data dari kedua database dan menggabungkannya berdasarkan kode produk.
4. **Streamlit dan Plotly:** menampilkan ringkasan, grafik, filter, dan tabel transaksi dalam dashboard web.

### Alur Data

```text
Data CSV
   |
   v
prepare_data.py
   |
   v
load_databases.py
   |
   +--------------------------+
   |                          |
   v                          v
PostgreSQL (Supabase)       SQLite
master_produk               transaksi
   |                          |
   +------------+-------------+
                |
                v
             Pandas
        Integrasi dan analisis
                |
                v
       Streamlit + Plotly
                |
                v
       Dashboard Penjualan
```

## 5. Fitur Dashboard

- Ringkasan total penjualan.
- Jumlah nomor transaksi unik.
- Total unit terjual.
- Jumlah produk yang terjual.
- Filter berdasarkan rentang tanggal.
- Filter berdasarkan negara.
- Filter berdasarkan kategori produk.
- Grafik tren penjualan bulanan.
- Grafik penjualan berdasarkan negara.
- Grafik penjualan berdasarkan kategori.
- Grafik produk terlaris.
- Tabel detail transaksi terintegrasi.
- Unduh hasil filter ke format CSV.

## 6. Struktur Proyek

```text
vdi-multidbms/
├── data/
│   ├── master_produk.csv
│   ├── Sales Transaction v.4a.csv
│   ├── transaksi_bersih.csv
│   └── analytics.db
├── app.py
├── prepare_data.py
├── load_databases.py
├── inspect_data.py
├── test_db.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

Catatan: file `.env` digunakan secara lokal dan tidak boleh diunggah ke repositori publik. File database dan CSV juga perlu ditinjau sebelum diunggah karena dapat berukuran besar atau mengandung data yang tidak boleh dipublikasikan.

## 7. Persiapan Lingkungan

Pastikan Python telah terpasang di komputer.

Buat dan aktifkan virtual environment jika belum tersedia:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instal dependensi:

```powershell
python -m pip install -r requirements.txt
```

## 8. Konfigurasi Database

Buat file `.env` di folder utama proyek dan isi dengan kredensial PostgreSQL milik sendiri:

```text
DB_USER=isi_username_database
DB_PASSWORD=isi_password_database
DB_HOST=isi_host_database
DB_PORT=5432
DB_NAME=postgres
```

Ganti nilai contoh tersebut dengan kredensial yang benar. Jangan mengunggah file `.env` atau membagikan kredensial database.

## 9. Menyiapkan Data

Pastikan file sumber CSV tersedia di folder `data/`.

Periksa data:

```powershell
python inspect_data.py
```

Uji koneksi PostgreSQL:

```powershell
python test_db.py
```

Muat data ke kedua database:

```powershell
python load_databases.py
```

Perhatian: skrip pemuatan data saat ini menggunakan penggantian tabel (`replace`). Jalankan hanya jika memang ingin mengganti isi tabel yang ada.

## 10. Menjalankan Aplikasi

Jalankan perintah berikut dari folder utama proyek:

```powershell
python -m streamlit run app.py
```

Buka alamat lokal yang ditampilkan oleh Streamlit, biasanya:

http://localhost:8501

## 11. Sumber Dataset

Cantumkan tautan asli sumber dataset yang digunakan di bagian ini sebelum publikasi.

- Dataset transaksi: **[Tambahkan URL sumber dataset transaksi]**
- Dataset master produk: **[Tambahkan URL sumber master produk]**

Nama file lokal bukan pengganti URL sumber asli. Pastikan sumber dataset benar-benar sesuai dengan data yang digunakan.

## 12. Referensi Kode dan Dokumentasi

- Python: https://docs.python.org/3/
- Pandas: https://pandas.pydata.org/docs/
- Streamlit: https://docs.streamlit.io/
- Plotly: https://plotly.com/python/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Supabase: https://supabase.com/docs

## 13. Deployment

Aplikasi dapat dipublikasikan melalui layanan hosting yang mendukung Streamlit, misalnya Streamlit Community Cloud.

Sebelum deployment:

1. Unggah kode aplikasi ke GitHub.
2. Pastikan `requirements.txt` tersedia.
3. Konfigurasikan kredensial database melalui fitur secrets pada layanan hosting.
4. Jangan mengunggah `.env`, kata sandi, atau kredensial pribadi ke GitHub.
5. Pastikan database dapat diakses dari lingkungan hosting.
6. Uji aplikasi setelah dipublikasikan.

## 14. Tautan Pengumpulan

- **GitHub Repository:** [https://github.com/sitihindunnursifa-svg/vdi-multidbms]
- **Live Dashboard:** [https://vdi-multidbms-syifa.streamlit.app/]
- **Sumber Dataset:** [https://www.kaggle.com/datasets/gabrielramos87/an-online-shop-business]
- **Referensi Kode:** [https://plotly.com/python/]

