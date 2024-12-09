import requests
from bs4 import BeautifulSoup
from utils.common import add_department_url

UNIVERSITY_NAME = "Üsküdar Üniversitesi"

def clean_name(full_text):
    parts = full_text.split(".")
    name_part = parts[-1].strip()

    if "Üyesi" in name_part:
        name_part = name_part.replace("Üyesi", "").strip()

    return name_part



def scrape_uskudar(url_data):
    urls = [
        "https://uskudar.edu.tr/iletisim-fakultesi/cizgi-film-ve-animasyon-akademik-kadro",
        "https://uskudar.edu.tr/iletisim-fakultesi/dijital-oyun-tasarimi-akademik-kadro",
        "https://uskudar.edu.tr/iletisim-fakultesi/gazetecilik-akademik-kadro",
        "https://uskudar.edu.tr/iletisim-fakultesi/gorsel-iletisim-tasarimi-akademik-kadro",
        "https://uskudar.edu.tr/iletisim-fakultesi/halkla-iliskiler-ve-tanitim-akademik-kadro",
        "https://uskudar.edu.tr/iletisim-fakultesi/radyo-televizyon-ve-sinema-akademik-kadro",
        "https://uskudar.edu.tr/iletisim-fakultesi/reklamcilik-akademik-kadro",
        "https://uskudar.edu.tr/iletisim-fakultesi/yeni-medya-ve-gazetecilik-akademik-kadro",
        "https://uskudar.edu.tr/iletisim-fakultesi/medya-ve-iletisim-akademik-kadro",
        "https://uskudar.edu.tr/iletisim-fakultesi/yeni-medya-ve-iletisim-ingilizce-akademik-kadro",
        "https://uskudar.edu.tr/itbf/felsefe-akademik-kadro",
        "https://uskudar.edu.tr/itbf/ingilizce-mutercim-ve-tercumanlik-akademik-kadro",
        "https://uskudar.edu.tr/itbf/psikoloji-akademik-kadro",
        "https://uskudar.edu.tr/itbf/psikoloji-ingilizce-akademik-kadro",
        "https://uskudar.edu.tr/itbf/siyaset-bilimi-ve-uluslararasi-iliskiler-turkce-akademik-kadro",
        "https://uskudar.edu.tr/itbf/siyaset-bilimi-ve-uluslararasi-iliskiler-akademik-kadro",
        "https://uskudar.edu.tr/itbf/sosyoloji-akademik-kadro",
        "https://uskudar.edu.tr/itbf/tarih-akademik-kadro",
        "https://uskudar.edu.tr/mdbf/adli-bilimler-akademik-kadro",
        "https://uskudar.edu.tr/mdbf/bilgisayar-muhendisligi-akademik-kadro",
        "https://uskudar.edu.tr/mdbf/biyomuhendislik-akademik-kadro",
        "https://uskudar.edu.tr/mdbf/elektrik-elektronik-muhendisligi-akademik-kadro",
        "https://uskudar.edu.tr/mdbf/endustri-muhendisligi-akademik-kadro",
        "https://uskudar.edu.tr/mdbf/kimya-muhendisligi-akademik-kadro",
        "https://uskudar.edu.tr/mdbf/molekuler-biyoloji-ve-genetik-ingilizce-akademik-kadro",
        "https://uskudar.edu.tr/mdbf/molekuler-biyoloji-ve-genetik-turkce-akademik-kadro",
        "https://uskudar.edu.tr/mdbf/yazilim-muhendisligi-akademik-kadro",
        "https://uskudar.edu.tr/dis-hekimligi-fakultesi/akademik-kadro",
        "https://uskudar.edu.tr/tip-fakultesi/akademik-kadro"
    ]

    author_data = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract department name
            department_h1 = soup.find("h1")
            department_name = department_h1.get_text(strip=True).replace("Akademik Kadro", "").strip() if department_h1 else "Unknown Department"

            # Find the main staff list container
            staff_list = soup.find("div", class_="row mx-0 staff-list")
            if not staff_list:
                print(f"Staff list not found in {url}")
                continue

            # Extract academic staff entries
            staff_items = staff_list.find_all("div", class_="col-md-6 staff-item")
            for staff_item in staff_items:
                # Extract name
                name_h2 = staff_item.find("h2")
                if name_h2:
                    full_text = name_h2.get_text(strip=True)
                    name = clean_name(full_text)  # Use the updated clean_name function
                else:
                    name = "Unknown Name"

                # Append faculty data
                author_data.append({
                    "Ad": name,
                    "Üniversite": UNIVERSITY_NAME,
                    "Fakülte": department_name,
                })

            # Append department URL
            add_department_url(UNIVERSITY_NAME, department_name, url, url_data)
            print(f"Scraped {len(staff_items)} entries from {url}")

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return author_data