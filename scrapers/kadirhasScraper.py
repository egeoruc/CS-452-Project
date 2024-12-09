import requests
from bs4 import BeautifulSoup
from utils.common import add_department_url, clean_name

UNIVERSITY_NAME = "Kadir Has Üniversitesi"

def scrape_Khas(url_data):
    url_function_map = {
        1: [
            "https://mis.khas.edu.tr/akademisyenlerimiz/",
            "https://itf.khas.edu.tr/akademisyenlerimiz/",
            "https://pols.khas.edu.tr/akademisyenlerimiz/",
            "https://psych.khas.edu.tr/akademisyenlerimiz/",
            "https://mgmt.khas.edu.tr/akademisyenlerimiz/",
            "https://econ.khas.edu.tr/akademisyenlerimiz/",
            "https://theatre.khas.edu.tr/akademisyenlerimiz/",
            "https://iaed.khas.edu.tr/akademisyenlerimiz/",
            "https://id.khas.edu.tr/akademisyenlerimiz/",
            "https://mbg.khas.edu.tr/akademisyenlerimiz/",
            "https://mcte.khas.edu.tr/akademisyenlerimiz/",
            "https://ce.khas.edu.tr/akademisyenlerimiz/",
            "https://ie.khas.edu.tr/akademisyenlerimiz/",
            "https://ee.khas.edu.tr/akademisyenlerimiz/",
            "https://cpe.khas.edu.tr/akademisyenlerimiz/",
            "https://nm.khas.edu.tr/akademisyenlerimiz/",
            "https://adhas.khas.edu.tr/akademisyenlerimiz/",
            "https://rtc.khas.edu.tr/akademisyenlerimiz/",
            "https://pr.khas.edu.tr/akademisyenlerimiz/",
        ],
        2: [
            "https://dev-arch.khas.edu.tr/akademik-kadro/"
        ],
    }

    author_data = []

    for url_type, urls in url_function_map.items():
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                if url_type==1:
                    # Get department name
                    department_list = soup.find("ul",
                                                class_="caf-filter-container caf-mtf-layout caf-mtf-tax-category ml-0 list-unstyled")
                    department_name = "Unknown Department"
                    if department_list:
                        labels = department_list.find_all("label")
                        for label in labels:
                            department_name = label.get_text(strip=True)

                    # Get faculty members
                    memberList = soup.find("div", class_="row academic-staff-container")
                    if not memberList:
                        print(f"Member list not found in {url}")
                        continue

                    members = memberList.find_all("h4")
                    for member in members:
                        name = member.get_text(strip=True)
                        author_data.append({
                            "Ad": name,
                            "Üniversite": UNIVERSITY_NAME,
                            "Fakülte": department_name,
                        })
                elif url_type==2:
                    department_name = "Mimarlık Fakültesi"

                    memberList = soup.find("div", class_="vp-portfolio__items vp-portfolio__items-style-fade vp-portfolio__items-show-overlay-hover")
                    if not memberList:
                        print("Member list not found in {url}")
                        continue
                    members = memberList.find_all("h2")
                    for member in members:
                        name = member.get_text(strip=True)
                        author_data.append({
                            "Ad": name,
                            "Üniversite": UNIVERSITY_NAME,
                            "Fakülte":department_name,
                        })

                # Add department URL
                add_department_url(UNIVERSITY_NAME, department_name, url, url_data)
                print(f"Scraped {len(members)} entries from {url}")

            except Exception as e:
                print(f"Error scraping {url}: {e}")
    return author_data