import requests
from bs4 import BeautifulSoup
from utils.common import add_department_url, clean_name

UNIVERSITY_NAME = "MEF Üniversitesi"

def scrape_mef(url_data):
    url_function_map = {
        1: [
            "https://www.mef.edu.tr/en/fakulteler/egitim-fakultesi/bolumler/ilkogretim-matematik-ogretmenligi/akademik-kadro/tam-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/egitim-fakultesi/bolumler/ilkogretim-matematik-ogretmenligi/akademik-kadro/yari-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/egitim-fakultesi/bolumler/rehberlik-ve-psikolojik-danismanlik/akademik-kadro/tam-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/egitim-fakultesi/bolumler/rehberlik-ve-psikolojik-danismanlik/akademik-kadro/yari-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/egitim-fakultesi/bolumler/ingilizce-ogretmenligi/akademik-kadro/ingilizce-ogretmenligi-tam-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/egitim-fakultesi/bolumler/ingilizce-ogretmenligi/akademik-kadro/ingilizce-ogretmenligi-yari-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/iktisadi-idari-ve-sosyal-bilimler-fakultesi/bolumler/ekonomi/akademik-kadro/tam-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/iktisadi-idari-ve-sosyal-bilimler-fakultesi/bolumler/ekonomi/akademik-kadro/yari-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/iktisadi-idari-ve-sosyal-bilimler-fakultesi/bolumler/isletme/akademik-kadro/tam-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/iktisadi-idari-ve-sosyal-bilimler-fakultesi/bolumler/isletme/akademik-kadro/yari-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/iktisadi-idari-ve-sosyal-bilimler-fakultesi/bolumler/psikoloji/akademik-kadro/tam-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/iktisadi-idari-ve-sosyal-bilimler-fakultesi/bolumler/psikoloji/akademik-kadro/yari-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/iktisadi-idari-ve-sosyal-bilimler-fakultesi/bolumler/siyaset-bilimi-ve-uluslararasi-iliskiler/akademik-kadro/tam-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/iktisadi-idari-ve-sosyal-bilimler-fakultesi/bolumler/siyaset-bilimi-ve-uluslararasi-iliskiler/akademik-kadro/yari-zamanli",
            "https://www.mef.edu.tr/en/fakulteler/muhendislik-fakultesi/bolumler/bilgisayar-muhendisligi/akademik-kadro/tam-zamanli-ogretim-uyeleri",
            "https://www.mef.edu.tr/en/fakulteler/muhendislik-fakultesi/bolumler/bilgisayar-muhendisligi/akademik-kadro/misafir-ogretim-uyeleri",
            "https://www.mef.edu.tr/en/fakulteler/muhendislik-fakultesi/bolumler/elektrik-elektronik-muhendisligi/akademik-kadro/tam-zamanli-ogretim-uyeleri",
            "https://www.mef.edu.tr/en/fakulteler/muhendislik-fakultesi/bolumler/elektrik-elektronik-muhendisligi/akademik-kadro/misafir-ogretim-uyeleri",
            "https://www.mef.edu.tr/en/fakulteler/muhendislik-fakultesi/bolumler/endustri-muhendisligi/akademik-kadro/tam-zamanli-ogretim-uyeleri",
            "https://www.mef.edu.tr/en/fakulteler/muhendislik-fakultesi/bolumler/endustri-muhendisligi/akademik-kadro/misafir-ogretim-uyeleri",
            "https://www.mef.edu.tr/en/fakulteler/muhendislik-fakultesi/bolumler/insaat-muhendisligi/akademik-kadro/tam-zamanli-ogretim-uyeleri",
            "https://www.mef.edu.tr/en/fakulteler/muhendislik-fakultesi/bolumler/insaat-muhendisligi/akademik-kadro/misafir-ogretim-uyeleri",
            "https://www.mef.edu.tr/en/fakulteler/muhendislik-fakultesi/bolumler/makine-muhendisligi/akademik-kadro/tam-zamanli-ogretim-uyeleri",
            "https://www.mef.edu.tr/en/fakulteler/muhendislik-fakultesi/bolumler/makine-muhendisligi/akademik-kadro/misafir-ogretim-uyeleri",
        ],
        2: [
            "https://www.mef.edu.tr/tr/fakulteler/hukuk-fakultesi/hakkimizda/akademik-kadro",
        ],
    }

    author_data = []

    def get_department_name(url, url_type):
        if url_type == 1:
            segments = url.split("/")
            return segments[-3].replace("-", " ").title()
        elif url_type == 2:
            segments = url.split("/")[-3]
            return segments.replace("-", " ").title()
        else:
            return "Unknown Department"

    for url_type, urls in url_function_map.items():
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                department_name = get_department_name(url, url_type)

                # Find all faculty members
                members = soup.find_all("a", class_="w-full")
                for member in members:
                    name_tag = member.find("h3")
                    name = name_tag.get_text(strip=True) if name_tag else "Unknown Name"

                    author_data.append({
                        "Ad": name,
                        "Üniversite": UNIVERSITY_NAME,
                        "Fakülte": department_name,
                    })

                add_department_url(UNIVERSITY_NAME, department_name, url, url_data)
                print(f"Scraped {len(members)} entries from {url}")

            except Exception as e:
                print(f"Error scraping {url}: {e}")
    return author_data