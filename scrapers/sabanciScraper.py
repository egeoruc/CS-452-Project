import requests
from bs4 import BeautifulSoup
from utils.common import add_department_url, clean_name

UNIVERSITY_NAME = "Sabancı Üniversitesi"

def scrape_sabanci(url_data):
    url_function_map = {
        1: [
            "https://cs.sabanciuniv.edu/tr/kisiler/fakulte",
            "https://cs.sabanciuniv.edu/tr/kisiler/ogretim-gorevlileri",
            "https://cs.sabanciuniv.edu/tr/kisiler/arastirma-gorevlileri",
            "https://cs.sabanciuniv.edu/tr/kisiler/emeritus-ogretim-uyeleri",
            "https://ee.sabanciuniv.edu/tr/kisiler/fakulte",
            "https://ee.sabanciuniv.edu/tr/kisiler/arastirmacilar",
            "https://ee.sabanciuniv.edu/tr/people/research-assistants",
            "https://ie.sabanciuniv.edu/tr/kisiler/fakulte",
            "https://ie.sabanciuniv.edu/tr/kisiler/emeritus-ogretim-uyeleri",
            "https://ie.sabanciuniv.edu/tr/kisiler/ogretim-gorevlileri",
            "https://ie.sabanciuniv.edu/tr/kisiler/arastirma-gorevlileri",
            "https://mat.sabanciuniv.edu/tr/kisiler/fakulte",
            "https://mat.sabanciuniv.edu/tr/kisiler/doktoraustu-arastirmacilar",
            "https://mat.sabanciuniv.edu/tr/kisiler/arastirma-gorevlileri",
            "https://me.sabanciuniv.edu/tr/kisiler/fakulte",
            "https://me.sabanciuniv.edu/tr/kisiler/emeritus-ogretim-uyeleri",
            "https://me.sabanciuniv.edu/tr/kisiler/ogretim-gorevlileri",
            "https://me.sabanciuniv.edu/tr/kisiler/arastirma-gorevlileri",
            "https://bio.sabanciuniv.edu/tr/kisiler/fakulte",
            "https://bio.sabanciuniv.edu/tr/kisiler/doktoraustu-arastirmacilar",
            "https://bio.sabanciuniv.edu/tr/kisiler/arastirma-gorevlileri",
            "https://bio.sabanciuniv.edu/tr/kisiler/associated-researchers",
            "https://phys.sabanciuniv.edu/tr/kisiler/fakulte",
            "https://phys.sabanciuniv.edu/tr/kisiler/emeritus-ogretim-uyeleri",
            "https://math.sabanciuniv.edu/tr/kisiler/fakulte",
            "https://math.sabanciuniv.edu/tr/kisiler/emeritus-ogretim-uyeleri",
            "https://math.sabanciuniv.edu/tr/kisiler/doktoraustu-arastirmacilar",
            "https://mfg.sabanciuniv.edu/tr/kisiler/fakulte",
            "https://chem.sabanciuniv.edu/tr/kisiler/fakulte",
            "https://energy-minor.sabanciuniv.edu/tr/ogretim-uyeleri",
        ],
        2: [
            "https://msit.sabanciuniv.edu/tr/egitmenlerimiz",
            "https://da.sabanciuniv.edu/tr/content/akademik-kadro"
        ],
        3: [
            "https://sl.sabanciuniv.edu/en/faculty-members"
        ]
    }

    author_data = []

    for layout_type, urls in url_function_map.items():
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                if layout_type == 1:
                    program_div = soup.find("div", class_="program")
                    department_name = program_div.find("a").get_text(strip=True) if program_div else "Unknown Department"
                    faculty_wrapper = soup.find("div", attrs={"id": ["faculty-old-wrapper", "faculty-members-wrapper"]})
                    if not faculty_wrapper:
                        print(f"Faculty wrapper not found in {url}")
                        continue

                    faculty_items = faculty_wrapper.find_all("div", class_="four columns su-item omega isotope-item")
                    for faculty_item in faculty_items:
                        name_h5 = faculty_item.find("h5")
                        name = clean_name(name_h5.text) if name_h5 else "Unknown Name"
                        author_data.append({
                            "Ad": name,
                            "Üniversite": UNIVERSITY_NAME,
                            "Fakülte": department_name,
                        })

                elif layout_type == 2:
                    program_div = soup.find("div", class_="program")
                    department_name = program_div.find("a").get_text(strip=True) if program_div else "Unknown Department"

                    faculty_members = soup.find("div", attrs={"id": "faculty-members-wrapper"})
                    if not faculty_members:
                        print(f"Faculty members wrapper not found in {url}")
                        continue

                    faculty_names = faculty_members.find_all("h5")
                    for faculty_name in faculty_names:
                        name_a = faculty_name.find("a")
                        name = name_a.get_text(strip=True) if name_a else faculty_name.get_text(strip=True)
                        author_data.append({
                            "Ad": clean_name(name),
                            "Üniversite": UNIVERSITY_NAME,
                            "Fakülte": department_name,
                        })

                elif layout_type == 3:
                    branding_div = soup.find("div", class_="branding")
                    if branding_div:
                        site_name_a = branding_div.find("a", class_="site_name")
                        department_name = site_name_a.get_text(strip=True) if site_name_a else "Unknown Department"
                    else:
                        department_name = "Unknown Department"

                    main_container = soup.find("div", class_="row mb-3")
                    if not main_container:
                        print(f"Main container not found in {url}")
                        continue

                    name_spans = main_container.find_all("span", class_="card-title")
                    for name_span in name_spans:
                        name = name_span.get_text(strip=True)
                        author_data.append({
                            "Ad": clean_name(name),
                            "Üniversite": UNIVERSITY_NAME,
                            "Fakülte": department_name,
                        })

                add_department_url(UNIVERSITY_NAME, department_name, url, url_data)
                print(f"Scraped {len(author_data)} entries from {url}")

            except Exception as e:
                print(f"Error scraping {url}: {e}")

    return author_data