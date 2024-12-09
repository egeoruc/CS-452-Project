import requests
from urllib3.exceptions import InsecureRequestWarning
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
from utils.common import add_department_url, clean_name

UNIVERSITY_NAME = "İstanbul Ticaret Üniversitesi"

def scrape_Ticaret(url_data):
    urls = [
        "https://ticaret.edu.tr/isletme-fakultesi/akademik-kadro/",
        "https://ticaret.edu.tr/muhendislik-fakultesi/akademik-kadro/",
        "https://ticaret.edu.tr/hukuk-fakultesi/akademik-kadro/",
        "https://ticaret.edu.tr/insan-ve-toplum-bilimleri-fakultesi/akademik-kadro/",
        "https://ticaret.edu.tr/mimarlik-ve-tasarim-fakultesi/akademik-kadro/",
        "https://ticaret.edu.tr/iletisim-fakultesi/akademik-kadro/"

    ]

    author_data = []

    for url in urls:
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            div_col = soup.find("div", attrs={"class": "col-md-9"})
            if not div_col:
                print(f"div_col not found: {url}")
                continue
            div_col_12 = div_col.find("div", attrs={"class": "col-md-12"})
            kaydirma = div_col_12.find("div", attrs={"class": "kaydirma"})
            big_list =  kaydirma.find("ul", class_="akademikkadro_list")
            if not big_list:
                print(f"big_list not found: {url}")
            items = big_list.find_all("li", class_="akademiklist_li")

            for item in items:
                content = item.find("div", attrs={"class": "akademik_content"})
                full_name = item.find("a").find("h4").get_text(strip=True)
                name = clean_name(full_name)
                lines = content.find_all("div", attrs={"class": "akademik-line"})
                if(len(lines) > 1):
                    department_name = lines[1].get_text(strip=True)
                else:
                    department_name = "Unknown"
                    print(f"department not found: {url}")

                author_data.append({
                    "Ad": name,
                    "Üniversite": UNIVERSITY_NAME,
                    "Fakülte": department_name,
                })
                add_department_url(UNIVERSITY_NAME,department_name, url, url_data)
            print(f"Scraped {len(items)} entries from {url}")

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return author_data