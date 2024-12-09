import requests
from urllib3.exceptions import InsecureRequestWarning
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
from utils.common import add_department_url, clean_name, clear_department_name

UNIVERSITY_NAME = "İstanbul Sağlık ve Teknoloji Üniversitesi"

def scrape(url_data):
    urls = [
        "https://tip.istun.edu.tr/tr/akademik-kadro-984",
        "https://dishekimligi.istun.edu.tr/tr/akademik-kadro-988",
        "https://eczacilik.istun.edu.tr/tr/akademik-kadro-990",
        "https://muhendislik.istun.edu.tr/tr/akademik-kadro-1603",
        "https://sbf.istun.edu.tr/tr/akademik-kadro-1208",
        "https://iisbf.istun.edu.tr/tr/akademik-kadro-1683",
        "https://iisbf.istun.edu.tr/tr/ingilizce-mutercim-tercumanlik-akademik-kadrosu-1611",
    ]

    author_data = []
    titles_to_ignore = ["Dekan","Dekan V.","Dekan Vekili" ]

    for url in urls:
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")


            main_div = soup.find("div", class_="team team-sm row d-flex justify-content-center")
            if not main_div:
                print(f"main div not found: {url}")
                continue
            items = main_div.find_all("div", class_=["col-6 col-sm-6 col-md-3 col-lg-3 mb-3", "col-6 col-sm-6 col-md-3 mb-3"])
            for item in items:
                content = item.find("div", attrs={"class": "item"})
                full_name = item.find("span", class_="name").get_text(strip=True)
                name = clean_name(full_name)
                department_span = content.find("span", class_="title")
                if department_span:
                    br_tag = department_span.find("br")
                    if br_tag:
                        department_name = br_tag.next_sibling.strip() if br_tag.next_sibling else "N/A"
                    else:
                        department_name = department_span.text.strip()
                    department_name = clear_department_name(department_name)
                    if department_name in titles_to_ignore:
                        department_name = "N/A"
                else:
                    print(f"departmant span not found in: {url} , for: {name}")
                    department_name = "N/A"

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