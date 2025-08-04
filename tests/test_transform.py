import pytest
import pandas as pd
from utils.transform import (
    clean_price, clean_rating, clean_colors,
    clean_size, clean_gender, transform_data
)

# ---------- Tests for clean_price ----------
def test_clean_price_valid():
    assert clean_price("$10") == 160000
    assert clean_price("$0") == 0
    assert clean_price("$99.99") == 1599840

def test_clean_price_invalid():
    assert clean_price("Not a price") is None
    assert clean_price("") is None
    assert clean_price(None) is None

# ---------- Tests for clean_rating ----------
def test_clean_rating_valid():
    assert clean_rating("Rating: 4.5 / 5 ⭐") == 4.5
    assert clean_rating("Rating: 5 / 5 ⭐") == 5.0
    assert clean_rating("Rating: 3 / 5 ⭐") == 3.0

def test_clean_rating_invalid():
    assert clean_rating("Rating: - / 5 ⭐") is None
    assert clean_rating("") is None
    assert clean_rating(None) is None

# ---------- Tests for clean_colors ----------
def test_clean_colors_valid():
    assert clean_colors("3 Colors") == 3
    assert clean_colors("10 Colors") == 10

def test_clean_colors_invalid():
    assert clean_colors("Colors") is None
    assert clean_colors("") is None
    assert clean_colors(None) is None

# ---------- Tests for clean_size ----------
def test_clean_size():
    assert clean_size("Size: M") == "M"
    assert clean_size("Size: L ") == "L"
    assert clean_size("Size:   XL ") == "XL"

# ---------- Tests for clean_gender ----------
def test_clean_gender():
    assert clean_gender("Gender: Male") == "Male"
    assert clean_gender("Gender: Female ") == "Female"

# ---------- Tests for transform_data ----------
def test_transform_data_valid():
    df = pd.DataFrame({
        "Title": ["T-shirt", "Dress"],
        "Price": ["$10", "$20"],
        "Rating": ["Rating: 4.5 / 5 ⭐", "Rating: 5 / 5 ⭐"],
        "Colors": ["2 Colors", "3 Colors"],
        "Size": ["Size: M", "Size: L"],
        "Gender": ["Gender: Female", "Gender: Male"]
    })

    result = transform_data(df)

    assert len(result) == 2
    assert result["Price"].tolist() == [160000, 320000]
    assert result["Rating"].tolist() == [4.5, 5.0]
    assert result["Colors"].tolist() == [2, 3]
    assert result["Size"].tolist() == ["M", "L"]
    assert result["Gender"].tolist() == ["Female", "Male"]

def test_transform_data_handles_unknown_and_duplicates_and_nulls():
    df = pd.DataFrame({
        "Title": ["Unknown Product", "Dress", "Dress"],
        "Price": ["$10", "$20", "$20"],
        "Rating": ["Rating: 4.5 / 5 ⭐", "Rating: 5 / 5 ⭐", "Rating: 5 / 5 ⭐"],
        "Colors": ["2 Colors", "3 Colors", "3 Colors"],
        "Size": ["Size: M", "Size: L", "Size: L"],
        "Gender": ["Gender: Female", "Gender: Male", "Gender: Male"]
    })

    result = transform_data(df)
    assert len(result) == 1  # hanya 1 baris valid setelah filter

def test_transform_data_invalid_columns():
    df = pd.DataFrame({
        "Title": ["Shirt"],
        "Price": ["invalid"],
        "Rating": ["invalid"],
        "Colors": ["invalid"],
        "Size": ["Size: L"],
        "Gender": ["Gender: Male"]
    })

    result = transform_data(df)
    assert result.empty

def test_transform_data_exception(monkeypatch):
    # Simulasi kolom yang tidak ada
    df = pd.DataFrame({"WrongCol": ["X"]})
    result = transform_data(df)
    assert result.empty
