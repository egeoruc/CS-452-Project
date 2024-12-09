import requests
from bs4 import BeautifulSoup
from utils.common import add_department_url, clean_name

UNIVERSITY_NAME = "Piri Reis Üniversitesi"

def scrape_pririreis(url_data):
    url_function_map = {
        1: [
            "https://denizcilik.pirireis.edu.tr/bolumler/deniz-ulastirma-isletme-muhendisligi/bolum-kadrosu/",
            "https://muhendislik.pirireis.edu.tr/bolumler/gemi-insaati-ve-gemi-makineleri-muhendisligi/bolum-kadrosu/",
            "https://muhendislik.pirireis.edu.tr/bolumler/makine-muhendisligi/bolum-kadrosu/",
            "https://muhendislik.pirireis.edu.tr/bolumler/elektrik-elektronik-muhendisligi/bolum-kadrosu/",
            "https://muhendislik.pirireis.edu.tr/bolumler/endustri-muhendisligi/bolum-kadrosu/",
            "https://muhendislik.pirireis.edu.tr/bolumler/bilgisayar-muhendisligi/bolum-kadrosu/",
            "https://iibf.pirireis.edu.tr/bolumler/yonetim-bilisim-sistemleri/bolum-kadrosu/",
            "https://iibf.pirireis.edu.tr/bolumler/uluslararasi-ticaret-ve-isletmecilik/bolum-kadrosu/",
            "https://iibf.pirireis.edu.tr/bolumler/lojistik-yonetimi/bolum-kadrosu/",
            "https://iibf.pirireis.edu.tr/bolumler/deniz-isletmeleri-yonetimi/bolum-kadrosu/",
            "https://iibf.pirireis.edu.tr/bolumler/ekonomi-ve-finans/bolum-kadrosu/",
            "https://denizcilik.pirireis.edu.tr/bolumler/gemi-makineleri-isletme-muhendisligi/bolum-kadrosu/",


        ],
        2: [
            "https://hukuk.pirireis.edu.tr/akademik-kadro/",
        ],
        3: [
            "https://pirireis.edu.tr/akademik/fen-edebiyat-fakultesi/akademik-kadro/matematik-akademik-kadrosu/",
            "https://pirireis.edu.tr/akademik/fen-edebiyat-fakultesi/akademik-kadro/fizik-akademik-kadrosu/",
            "https://pirireis.edu.tr/akademik/fen-edebiyat-fakultesi/akademik-kadro/kimya-akademik-kadrosu/",
           "https://pirireis.edu.tr/akademik/fen-edebiyat-fakultesi/akademik-kadro/sosyal-bilimler-akademik-kadrosu/"
        ]
    }

    author_data = []

    def get_department_name(url, url_type):

        if url_type == 1:
            segments = url.split("/")
            return segments[-3].replace("-", " ").title()
        elif url_type == 2:
            domain_parts = url.split("/")[-3].split(".")
            return domain_parts[0].replace("-", " ").title()
        elif url_type == 3:
            segments = url.split("/")
            if len(segments) > 1:
                last_segment = segments[-2]
                if "akademik-kadrosu" in last_segment:
                    department_name = last_segment.replace("akademik-kadrosu", "").strip("-").replace("-", " ").title()
                    return department_name
                return last_segment.split("-")[0].replace("-", " ").title()
            return "Unknown Department"
        else:
            return "Unknown Department"

    for url_type, urls in url_function_map.items():
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                department_name = get_department_name(url, url_type)

                # Find the main staff list container
                staff_list = soup.find("div", class_=["DepartmentStaff Layout__Body", "col-12 col-md-9", "Layout__Body"])
                if not staff_list:
                    print(f"Staff list not found in {url}")
                    continue

                # Extract academic staff entries
                members = staff_list.find_all("div", class_="Person")
                for member in members:
                    # Extract name
                    name = member.find("div", class_="Person__Fullname")
                    if name:
                        full_text = name.get_text(strip=True)
                        name = clean_name(full_text)  # Use the updated clean_name function
                    else:
                        name = "Unknown Name"

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