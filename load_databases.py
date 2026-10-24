
from pathlib import Path
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

# Membaca konfigurasi dari .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Membaca master produk
produk = pd.read_csv(
    DATA_DIR / "master_produk.csv",
    dtype={"product_no": str}
)

# Membaca transaksi yang sudah dibersihkan
transaksi = pd.read_csv(
    DATA_DIR / "transaksi_bersih.csv",
    dtype={"ProductNo": str}
)

# Membersihkan spasi pada kode produk
produk["product_no"] = produk["product_no"].str.strip()
transaksi["ProductNo"] = transaksi["ProductNo"].str.strip()

# Membuat koneksi PostgreSQL / Supabase
url = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "postgres"),
)

pg_engine = create_engine(url, pool_pre_ping=True)

# Membuat database SQLite untuk transaksi
sqlite_path = DATA_DIR / "analytics.db"
sqlite_engine = create_engine(f"sqlite:///{sqlite_path}")

try:
    print("1. Mengirim master produk ke PostgreSQL...")

    produk.to_sql(
        "master_produk",
        pg_engine,
        if_exists="replace",
        index=False,
        chunksize=1000
    )

    print(f"   Berhasil: {len(produk):,} produk")

    print("2. Mengirim transaksi bersih ke SQLite...")

    transaksi.to_sql(
        "transaksi",
        sqlite_engine,
        if_exists="replace",
        index=False,
        chunksize=5000
    )

    print(f"   Berhasil: {len(transaksi):,} transaksi")

    # Memastikan data benar-benar tersimpan
    with pg_engine.connect() as conn:
        jumlah_produk = conn.exec_driver_sql(
            "SELECT COUNT(*) FROM master_produk"
        ).scalar_one()

    with sqlite_engine.connect() as conn:
        jumlah_transaksi = conn.exec_driver_sql(
            "SELECT COUNT(*) FROM transaksi"
        ).scalar_one()

    print("\n=== HASIL PEMERIKSAAN ===")
    print("Produk di PostgreSQL:", f"{jumlah_produk:,}")
    print("Transaksi di SQLite:", f"{jumlah_transaksi:,}")
    print("Lokasi database SQLite:", sqlite_path)
    print("\nProses pemuatan database selesai!")

except Exception as e:
    print("Terjadi kesalahan:", type(e).__name__)
    print("Pesan:", str(e)[:500])
    raise

finally:
    pg_engine.dispose()
    sqlite_engine.dispose()
