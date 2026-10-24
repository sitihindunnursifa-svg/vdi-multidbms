import pandas as pd
df = pd.read_csv("data/Sales Transaction v.4a.csv")
print(df.head())
print(df.shape)
import pandas as pd

df = pd.read_csv("data/Sales Transaction v.4a.csv")
print("Baris awal:", len(df))

# 1. Buang transaksi batal (nomor berawalan C, atau jumlah negatif)
df = df[~df["TransactionNo"].astype(str).str.startswith("C")]
df = df[df["Quantity"] > 0]
print("Setelah buang batal:", len(df))

# 2. Cek data kosong di tiap kolom
print(df.isnull().sum())

# 3. Cek dan buang duplikat
print("Jumlah duplikat:", df.duplicated().sum())
df = df.drop_duplicates()
print("Setelah buang duplikat:", len(df))

# 4. Ubah kolom Date menjadi tanggal sungguhan
df["Date"] = pd.to_datetime(df["Date"])
print("Tanggal awal :", df["Date"].min())
print("Tanggal akhir:", df["Date"].max())

# 5. Simpan hasil bersih
df.to_csv("data/transaksi_bersih.csv", index=False)
print("Selesai, file bersih tersimpan.")
import pandas as pd

df = pd.read_csv("data/transaksi_bersih.csv", dtype={"ProductNo": str})

# 1. Satu produk = satu baris
master = df.groupby("ProductNo").agg(
    product_name=("ProductName", lambda s: s.mode().iloc[0]),
    list_price=("Price", "median"),
).reset_index()
master = master.rename(columns={"ProductNo": "product_no"})
master["product_name"] = master["product_name"].str.strip().str.upper()
master["list_price"] = master["list_price"].round(2)

# 2. Kategori diperkirakan dari kata kunci pada nama produk
aturan = {
    "Seasonal & Party": ["CHRISTMAS", "XMAS", "EASTER", "PARTY", "BALLOON", "WRAP", "RIBBON", "GIFT", "CARD"],
    "Lighting & Candles": ["LIGHT", "CANDLE", "LANTERN", "LAMP", "INCENSE"],
    "Kitchen & Dining": ["MUG", "CUP", "PLATE", "BOWL", "JAR", "TEAPOT", "CAKE", "SPOON", "KITCHEN", "LUNCH", "BOTTLE", "TRAY"],
    "Bags & Storage": ["BAG", "BOX", "TIN", "BASKET", "STORAGE", "CASE", "HOLDER", "DRAWER"],
    "Toys & Games": ["TOY", "GAME", "DOLL", "PUZZLE", "PLAYING"],
    "Stationery & Craft": ["PENCIL", "NOTEBOOK", "PAPER", "STICKER", "PEN ", "STAMP", "CRAFT", "BOOK"],
    "Garden & Outdoor": ["GARDEN", "BIRD", "PLANT", "FLOWER", "BUNTING"],
    "Home Decor": ["FRAME", "CLOCK", "MIRROR", "CUSHION", "VASE", "SIGN", "WALL", "HEART", "DECORATION", "HANGING"],
}

def tentukan_kategori(nama):
    nama = " " + str(nama).upper() + " "
    for kategori, kata_kunci in aturan.items():
        for kata in kata_kunci:
            if kata in nama:
                return kategori
    return "Other"

master["category"] = master["product_name"].apply(tentukan_kategori)

# 3. Lihat hasilnya
print(master.head(10))
print("Jumlah produk:", len(master))
print(master["category"].value_counts())

# 4. Simpan
master.to_csv("data/master_produk.csv", index=False)
print("Selesai, master produk tersimpan.")
print("Kolom transaksi:")
print(df.columns.tolist())

print("\nContoh data transaksi:")
print(df.head())

print("\nVariabel data yang tersedia:")
print([nama for nama in globals()
       if "produk" in nama.lower()
       or "master" in nama.lower()])