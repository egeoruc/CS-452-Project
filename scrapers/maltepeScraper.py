import requests
from bs4 import BeautifulSoup
from utils.common import add_department_url, clean_name


UNIVERSITY_NAME = "Maltepe Üniversitesi"


def scrape_maltepe(url_data):
    urls = [
        "https://www.maltepe.edu.tr/egitim/tr/akademik-kadro",
        "https://www.maltepe.edu.tr/gsf/tr/akademik-kadrow",
        "https://www.maltepe.edu.tr/hukuk/tr/akademik-kadro",
        "https://www.maltepe.edu.tr/iletisim/tr/akademik-kadro-o",
        "https://www.maltepe.edu.tr/itb/tr/akademik-kadro",
        "https://www.maltepe.edu.tr/iybf/tr/akademik-kadro-o",
        "https://www.maltepe.edu.tr/mimarlik/tr/akademik-kadro-o",
        "https://www.maltepe.edu.tr/mf/tr/akademik-kadro",
        "https://www.maltepe.edu.tr/tip-fakultesi/tr/akademik-kadro"

    ]

    author_data = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract department name
            department = soup.find("div" , class_="faculty-top-title")
            department_name = department.get_text(strip=True).strip() if department else "Unknown Department"
            if url == "https://www.maltepe.edu.tr/gsf/tr/akademik-kadrow":
                department_name ="Güzel Sanatlar Fakültesi"

            # Find the main staff list container
            member_list = soup.find("div", class_=["rectorship", "person-list"])
            if not member_list:
                print(f"List not found in {url}")
                continue

            # Extract academic staff entries
            members = member_list.find_all("div", class_=["rectorship-text", "pli-inner"])
            for member in members:
                # Extract name
                name = member.find("div", class_=["rectorship-name", "pli-name"])
                name = clean_name(name.get_text(strip=True).strip())

                author_data.append({
                    "Ad": name,
                    "Üniversite": UNIVERSITY_NAME,
                    "Fakülte": department_name,
                })

            # Append department URL
            add_department_url(UNIVERSITY_NAME, department_name, url, url_data)
            print(f"Scraped {len(members)} entries from {url}")

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return author_data