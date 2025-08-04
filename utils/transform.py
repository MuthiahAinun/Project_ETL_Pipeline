import pandas as pd

def clean_price(price_str):
    try:
        return int(float(price_str.replace("$", "")) * 16000)
    except:
        return None

def clean_rating(rating_str):
    try:
        rating_cleaned = rating_str.replace("Rating:", "").replace("⭐", "").replace(" / 5", "").strip()
        return float(rating_cleaned)
    except:
        return None

def clean_colors(color_str):
    try:
        return int(color_str.replace(" Colors", ""))
    except:
        return None

def clean_size(size_str):
    return size_str.replace("Size: ", "").strip()

def clean_gender(gender_str):
    return gender_str.replace("Gender: ", "").strip()

def transform_data(df):
    try:
        df = df[df["Title"] != "Unknown Product"]
        df = df.drop_duplicates()
        df = df.dropna()

        df["Price"] = df["Price"].apply(clean_price)
        df["Rating"] = df["Rating"].apply(clean_rating)
        df["Colors"] = df["Colors"].apply(clean_colors)
        df["Size"] = df["Size"].apply(clean_size)
        df["Gender"] = df["Gender"].apply(clean_gender)

        df = df.dropna()
        return df
    except Exception as e:
        print(f"Error during transformation: {e}")
        return pd.DataFrame([])