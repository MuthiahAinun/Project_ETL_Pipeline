import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from urllib.parse import urljoin
import time

BASE_URL = "https://fashion-studio.dicoding.dev"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extract_data(pages=50):
    data = []

    for page in range(1, pages + 1):
        url = BASE_URL if page == 1 else urljoin(BASE_URL, f"/page{page}")
        print(f"📄 Mengambil halaman ke-{page}: {url}")

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            products = soup.find_all("div", class_="collection-card")
            if not products:
                print(f"⚠️ Tidak ditemukan produk di halaman {page}.")
                continue

            for product in products:
                try:
                    title_tag = product.find("h3", class_="product-title")
                    price_tag = product.find("span", class_="price")
                    details = product.find_all("p")

                    # Skip jika elemen penting tidak ditemukan
                    if not title_tag or not price_tag:
                        print(f"⚠️ Produk tanpa title atau price di halaman {page}, dilewati.")
                        continue

                    title = title_tag.text.strip()
                    price = price_tag.text.strip()

                    # Inisialisasi default
                    rating = colors = size = gender = None
                    for p in details:
                        text = p.get_text(strip=True)
                        if "Rating:" in text:
                            rating = text.replace("Rating:", "").strip()
                        elif "Colors" in text:
                            colors = text.strip()
                        elif "Size:" in text:
                            size = text.replace("Size:", "").strip()
                        elif "Gender:" in text:
                            gender = text.replace("Gender:", "").strip()

                    data.append({
                        "Title": title,
                        "Price": price,
                        "Rating": rating,
                        "Colors": colors,
                        "Size": size,
                        "Gender": gender,
                        "Timestamp": datetime.now().isoformat()
                    })

                except Exception as e:
                    print(f"❌ Gagal parsing produk di halaman {page}: {e}")

            time.sleep(0.5)  # opsional: mencegah diblok

        except Exception as e:
            print(f"❌ Gagal mengambil halaman {page}: {e}")

    if not data:
        print("⚠️ Tidak ada data berhasil diambil.")
    else:
        print(f"✅ Total data berhasil diambil: {len(data)} produk")

    return pd.DataFrame(data)
