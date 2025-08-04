import pandas as pd
import os

# Google Sheets
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# PostgreSQL
from sqlalchemy import create_engine

def load_to_csv(df, file_path="products.csv"):
    try:
        if df.empty:
            print("⚠️ DataFrame kosong, tidak ada data yang disimpan.")
            return

        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        df.to_csv(file_path, index=False)
        print(f"✅ Data berhasil disimpan ke '{file_path}' ({len(df)} baris).")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke CSV: {e}")


def load_to_google_sheets(df, credentials_path="credentials.json", sheet_url=None):
    try:
        if df.empty:
            print("⚠️ Data kosong, tidak dikirim ke Google Sheets.")
            return

        if not sheet_url:
            print("❌ URL Google Sheets tidak diberikan.")
            return

        # Setup credential
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(creds)

        # Buka Google Sheet
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.get_worksheet(0)

        # Clear & upload data
        worksheet.clear()
        set_with_dataframe(worksheet, df)

        print(f"✅ Data berhasil dikirim ke Google Sheets ({len(df)} baris).")

    except Exception as e:
        print(f"❌ Gagal mengunggah ke Google Sheets: {e}")
        print("🔍 Pastikan akses EDITOR diberikan dan file 'credentials.json' tersedia.")


def load_to_postgresql(df, table_name="fashion_products"):
    try:
        if df.empty:
            print("⚠️ Data kosong, tidak dikirim ke PostgreSQL.")
            return

        # Ganti sesuai konfigurasi PostgreSQL kamu
        db_url = "postgresql+psycopg2://postgres:123@localhost:5432/postgres"
        engine = create_engine(db_url)

        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"✅ Data berhasil dikirim ke PostgreSQL → tabel '{table_name}' ({len(df)} baris).")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke PostgreSQL: {e}")
