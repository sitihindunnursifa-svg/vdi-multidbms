
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

load_dotenv()

url = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "postgres"),
)

engine = create_engine(url, pool_pre_ping=True)

try:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT current_database(), version()")
        )
        database, version = result.fetchone()

        print("Koneksi Supabase berhasil!")
        print("Database:", database)
        print("Versi PostgreSQL:", version)

except Exception as e:
    print("Koneksi gagal.")
    print("Jenis error:", type(e).__name__)
    print("Periksa konfigurasi .env dan koneksi Supabase.")

finally:
    engine.dispose()
