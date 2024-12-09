import requests
from bs4 import BeautifulSoup
from utils.common import add_department_url

UNIVERSITY_NAME = "Özyeğin Üniversitesi"

def scrape_ozyegin(url_data):
    urls = [
        "https://www.ozyegin.edu.tr/tr/uluslararasi-finans/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/isletme/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/ekonomi/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/uluslararasi-finans/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/uluslararasi-ticaret-ve-isletmecilik/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/yonetim-bilisim-sistemleri/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/girisimcilik/akademik-kadro",
        "https://cs.ozyegin.edu.tr/tr/akademik-kadro",
        "https://ee.ozyegin.edu.tr/tr/akademik-kadro",
        "https://ie.ozyegin.edu.tr/tr/akademik-kadro",
        "https://ce.ozyegin.edu.tr/tr/akademik-kadro",
        "https://me.ozyegin.edu.tr/tr/akademik-kadro",
        "https://math.ozyegin.edu.tr/tr/akademik-kadro",
        "https://science.ozyegin.edu.tr/tr/akademik-kadro",
        "https://ai.ozyegin.edu.tr/tr/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/psikoloji-bolumu/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/uluslararasi-iliskiler/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/insan-ve-toplum-bilimleri-bolumu/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/antropoloji/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/havacilik-yonetimi/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/pilotaj/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/hukuk-fakultesi/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/mimarlik/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/endustriyel-tasarim/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/iletisim-ve-tasarimi/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/ic-mimarlik-ve-cevre-tasarimi/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/gastronomi-ve-mutfak-sanatlari/akademik-kadro",
        "https://www.ozyegin.edu.tr/tr/otel-yoneticiligi-lisans-programi/akademik-kadro",
    ]

    author_data = []
    for url in urls:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract department name
        sag_menu_div = soup.find("div", class_="medium-3 columns sagMenu")
        department_name = sag_menu_div.find("h4").get_text(strip=True) if sag_menu_div else "Unknown Department"

        # Extract academic staff names
        for name_div in soup.find_all("div", itemprop="givenName"):
            given_name = name_div.get_text(strip=True)
            family_name_div = name_div.find_next_sibling("div", itemprop="familyName")
            family_name = family_name_div.get_text(strip=True) if family_name_div else ""
            full_name = f"{given_name} {family_name}".strip()

            author_data.append({
                "Ad": full_name,
                "Üniversite": UNIVERSITY_NAME,
                "Fakülte": department_name,
            })

        add_department_url(UNIVERSITY_NAME, department_name, url, url_data)

        print(f"Scraped {len(author_data)} entries from {url}")

    return author_data