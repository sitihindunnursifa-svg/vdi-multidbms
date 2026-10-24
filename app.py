
import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

# Pengaturan lokasi file
BASE_DIR = Path(__file__).resolve().parent
SQLITE_PATH = BASE_DIR / "data" / "analytics.db"

load_dotenv(BASE_DIR / ".env")

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sales Analytics Dashboard")
st.write(
    "Dashboard analisis penjualan dengan integrasi "
    "PostgreSQL dan SQLite menggunakan Pandas."
)


def get_postgres_engine():
    required = ["DB_USER", "DB_PASSWORD", "DB_HOST"]
    missing = [key for key in required if not os.getenv(key)]

    if missing:
        raise ValueError(
            "Variabel berikut belum diatur di file .env: "
            + ", ".join(missing)
        )

    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "postgres"),
    )

    return create_engine(url, pool_pre_ping=True)


@st.cache_data(ttl=300)
def load_data():
    if not SQLITE_PATH.exists():
        raise FileNotFoundError(
            "File data/analytics.db tidak ditemukan. "
            "Jalankan python load_databases.py terlebih dahulu."
        )

    postgres_engine = get_postgres_engine()

    try:
        with postgres_engine.connect() as conn:
            produk = pd.read_sql(
                text(
                    """
                    SELECT product_no, product_name,
                           list_price, category
                    FROM master_produk
                    """
                ),
                conn,
            )
    finally:
        postgres_engine.dispose()

    sqlite_engine = create_engine(
        f"sqlite:///{SQLITE_PATH.as_posix()}"
    )

    try:
        with sqlite_engine.connect() as conn:
            transaksi = pd.read_sql(
                text(
                    """
                    SELECT "TransactionNo", "Date", "ProductNo",
                           "ProductName", "Price", "Quantity",
                           "CustomerNo", "Country"
                    FROM transaksi
                    """
                ),
                conn,
            )
    finally:
        sqlite_engine.dispose()

    # Menyamakan format kode produk
    produk["product_no"] = (
        produk["product_no"].astype("string").str.strip().str.upper()
    )
    transaksi["ProductNo"] = (
        transaksi["ProductNo"].astype("string").str.strip().str.upper()
    )

    # Membersihkan tipe data
    transaksi["Date"] = pd.to_datetime(
        transaksi["Date"], errors="coerce"
    )
    transaksi["Price"] = pd.to_numeric(
        transaksi["Price"], errors="coerce"
    )
    transaksi["Quantity"] = pd.to_numeric(
        transaksi["Quantity"], errors="coerce"
    )

    # Integrasi dua database menggunakan Pandas
    df = transaksi.merge(
        produk,
        left_on="ProductNo",
        right_on="product_no",
        how="left",
        indicator=True,
        validate="many_to_one",
    )

    df["Revenue"] = df["Price"] * df["Quantity"]

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data: {type(e).__name__}: {e}")
    st.info(
        "Periksa file .env, koneksi Supabase, dan database "
        "yang sudah dimuat."
    )
    st.stop()


# Filter dashboard
st.sidebar.header("🔎 Filter Dashboard")

tanggal_valid = df["Date"].dropna()

if tanggal_valid.empty:
    st.error("Tidak ada tanggal transaksi yang valid.")
    st.stop()

tanggal_awal = tanggal_valid.min().date()
tanggal_akhir = tanggal_valid.max().date()

rentang = st.sidebar.date_input(
    "Rentang tanggal",
    value=(tanggal_awal, tanggal_akhir),
    min_value=tanggal_awal,
    max_value=tanggal_akhir,
)

negara_tersedia = sorted(df["Country"].dropna().unique().tolist())
negara_pilihan = st.sidebar.multiselect(
    "Negara",
    negara_tersedia,
    default=negara_tersedia,
)

kategori_tersedia = sorted(
    df["category"].dropna().unique().tolist()
)
kategori_pilihan = st.sidebar.multiselect(
    "Kategori produk",
    kategori_tersedia,
    default=kategori_tersedia,
)

filtered = df.copy()

if isinstance(rentang, (tuple, list)) and len(rentang) == 2:
    mulai = pd.Timestamp(rentang[0])
    selesai = pd.Timestamp(rentang[1]) + pd.Timedelta(days=1)

    filtered = filtered[
        filtered["Date"].ge(mulai)
        & filtered["Date"].lt(selesai)
    ]

filtered = filtered[
    filtered["Country"].isin(negara_pilihan)
    & filtered["category"].isin(kategori_pilihan)
]


# Ringkasan angka
total_penjualan = filtered["Revenue"].sum()
total_transaksi = filtered["TransactionNo"].nunique()
total_unit = filtered["Quantity"].sum()
total_produk = filtered["ProductNo"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Penjualan", f"{total_penjualan:,.2f}")
c2.metric("Nomor Transaksi", f"{total_transaksi:,.0f}")
c3.metric("Unit Terjual", f"{total_unit:,.0f}")
c4.metric("Produk Terjual", f"{total_produk:,.0f}")

tingkat_cocok = (
    filtered["_merge"].eq("both").mean() * 100
    if len(filtered)
    else 0
)

st.caption(
    f"Baris transaksi: {len(filtered):,} | "
    f"Kecocokan produk: {tingkat_cocok:.2f}%"
)

st.divider()


# Grafik tren bulanan
kiri, kanan = st.columns(2)

with kiri:
    st.subheader("📈 Tren Penjualan Bulanan")

    tren = (
        filtered.dropna(subset=["Date"])
        .assign(
            Bulan=lambda x: x["Date"].dt.to_period("M").astype(str)
        )
        .groupby("Bulan", as_index=False)["Revenue"]
        .sum()
    )

    fig_tren = px.line(
        tren,
        x="Bulan",
        y="Revenue",
        markers=True,
        title="Total penjualan per bulan",
    )

    st.plotly_chart(fig_tren, use_container_width=True)

with kanan:
    st.subheader("🌍 Penjualan per Negara")

    negara = (
        filtered.groupby("Country", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    fig_negara = px.bar(
        negara,
        x="Country",
        y="Revenue",
        title="10 negara dengan penjualan tertinggi",
    )

    st.plotly_chart(fig_negara, use_container_width=True)


# Grafik kategori dan produk
kiri, kanan = st.columns(2)

with kiri:
    st.subheader("📦 Penjualan per Kategori")

    kategori = (
        filtered.groupby("category", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )

    fig_kategori = px.pie(
        kategori,
        names="category",
        values="Revenue",
        title="Proporsi penjualan per kategori",
    )

    st.plotly_chart(fig_kategori, use_container_width=True)

with kanan:
    st.subheader("🏆 Produk Terlaris")

    terlaris = (
        filtered.groupby("ProductName", as_index=False)
        .agg(
            Unit_Terjual=("Quantity", "sum"),
            Penjualan=("Revenue", "sum"),
        )
        .sort_values("Unit_Terjual", ascending=False)
        .head(10)
        .sort_values("Unit_Terjual")
    )

    fig_produk = px.bar(
        terlaris,
        x="Unit_Terjual",
        y="ProductName",
        orientation="h",
        title="10 produk berdasarkan jumlah unit terjual",
    )

    st.plotly_chart(fig_produk, use_container_width=True)


# Tabel transaksi
st.divider()
st.subheader("📋 Detail Transaksi Terintegrasi")

kolom = [
    "TransactionNo",
    "Date",
    "ProductNo",
    "ProductName",
    "category",
    "Price",
    "Quantity",
    "Revenue",
    "CustomerNo",
    "Country",
]

st.dataframe(
    filtered[kolom].head(1000),
    use_container_width=True,
    hide_index=True,
)

csv = filtered[kolom].to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Unduh data hasil filter (CSV)",
    data=csv,
    file_name="hasil_analisis_penjualan.csv",
    mime="text/csv",
)
