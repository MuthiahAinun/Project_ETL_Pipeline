import pytest
import pandas as pd
from unittest import mock
from io import StringIO

from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql

df_valid = pd.DataFrame({'nama': ['produk1'], 'harga': [10000]})
df_empty = pd.DataFrame()

# ---------- Test load_to_csv ----------
def test_csv_success(tmp_path):
    path = tmp_path / "test.csv"
    load_to_csv(df_valid, str(path))
    assert path.exists()

def test_csv_empty_df(capfd):
    load_to_csv(df_empty, "dummy.csv")
    out, _ = capfd.readouterr()
    assert "DataFrame kosong" in out

def test_csv_exception_handling(monkeypatch, capfd):
    monkeypatch.setattr("pandas.DataFrame.to_csv", lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Simulasi error")))
    load_to_csv(df_valid, "error.csv")
    out, _ = capfd.readouterr()
    assert "Gagal menyimpan ke CSV" in out

# ---------- Test load_to_google_sheets ----------
@mock.patch("utils.load.gspread.authorize")
@mock.patch("utils.load.ServiceAccountCredentials.from_json_keyfile_name")
def test_gsheet_success(mock_creds, mock_auth):
    mock_client = mock.Mock()
    mock_sheet = mock.Mock()
    mock_ws = mock.Mock()

    mock_auth.return_value = mock_client
    mock_client.open_by_url.return_value = mock_sheet
    mock_sheet.get_worksheet.return_value = mock_ws

    with mock.patch("utils.load.set_with_dataframe") as mock_set_df:
        load_to_google_sheets(df_valid, "dummy_credentials.json", "http://dummy-sheet-url")
        mock_set_df.assert_called_once()

def test_gsheet_empty_df(capfd):
    load_to_google_sheets(df_empty, "credentials.json", "url")
    out, _ = capfd.readouterr()
    assert "Data kosong" in out

def test_gsheet_no_url(capfd):
    load_to_google_sheets(df_valid, "credentials.json", None)
    out, _ = capfd.readouterr()
    assert "URL Google Sheets tidak diberikan" in out

@mock.patch("utils.load.ServiceAccountCredentials.from_json_keyfile_name", side_effect=Exception("simulasi error"))
def test_gsheet_exception_handling(mock_creds, capfd):
    load_to_google_sheets(df_valid, "credentials.json", "http://dummy-url")
    out, _ = capfd.readouterr()
    assert "Gagal mengunggah ke Google Sheets" in out

# ---------- Test load_to_postgresql ----------
@mock.patch("utils.load.create_engine")
def test_postgres_success(mock_engine):
    mock_conn = mock.Mock()
    mock_engine.return_value = mock_conn
    with mock.patch.object(df_valid, "to_sql") as mock_to_sql:
        load_to_postgresql(df_valid, "dummy_table")
        mock_to_sql.assert_called_once()

def test_postgres_empty_df(capfd):
    load_to_postgresql(df_empty, "table")
    out, _ = capfd.readouterr()
    assert "Data kosong" in out

@mock.patch("utils.load.create_engine", side_effect=Exception("Simulasi gagal koneksi"))
def test_postgres_exception_handling(mock_engine, capfd):
    load_to_postgresql(df_valid, "table")
    out, _ = capfd.readouterr()
    assert "Gagal menyimpan ke PostgreSQL" in out
