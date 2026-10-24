
from pathlib import Path
import pandas as pd

folder_data = Path("data")
file_csv = list(folder_data.glob("*.csv"))

if not file_csv:
    print("Tidak ada file CSV di folder data.")
else:
    for file in file_csv:
        print("\n" + "=" * 60)
        print(f"NAMA FILE: {file.name}")
        print("=" * 60)

        try:
            df = pd.read_csv(file)

            print("Jumlah baris:", len(df))
            print("Jumlah kolom:", len(df.columns))
            print("\nNama kolom:")
            print(df.columns.tolist())

            print("\nContoh 5 baris data:")
            print(df.head().to_string(index=False))

            print("\nTipe data:")
            print(df.dtypes.to_string())

        except Exception as e:
            print("Gagal membaca CSV:", e)
