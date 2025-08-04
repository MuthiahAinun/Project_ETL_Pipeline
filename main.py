from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql

def main():
    df = extract_data()
    df_clean = transform_data(df)
    load_to_csv(df_clean)
    load_to_google_sheets(df_clean,
                          credentials_path="fiery-topic-433913-q3-3b7fa3a8e0e9.json",
                          sheet_url="https://docs.google.com/spreadsheets/d/1f83u8QaFKaJPBxP0p-oKlYMXA67BhRaS_wKGuJdNaW4/edit?usp=sharing")
    load_to_postgresql(df_clean)

if __name__ == "__main__":
    main()


