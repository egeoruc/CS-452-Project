import requests
from bs4 import BeautifulSoup
from utils.common import add_department_url, clean_name

UNIVERSITY_NAME = "İstanbul Yeni Yüzyıl Üniversitesi"

def scrape_yeniyuzyil(url_data):
    url_function_map = {
        1: [
           "https://www.yeniyuzyil.edu.tr/Eczacilik/AkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Hukuk/AkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Tip/AkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/DisHekimligi/AkademikKadro.aspx"
        ],
        2: [
            "https://www.yeniyuzyil.edu.tr/Bolumler/IngilizDiliveEdebiyatiAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/IngilizceMutercimTercumanlikAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/MolekulerBiyolojiVeGenetikAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/PsikolojiAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/GrafikTasarimiAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/SahneSanatlariAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/SiyasetBilimiVeUluslararasiIliskilerAkademikKadro.aspx,"
            "https://www.yeniyuzyil.edu.tr/Bolumler/UluslararasiTicaretVeLojistikAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/IsletmeAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/GorselIletisimTasarimAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/HalklaIliskilerVeReklamcilikAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/RadyoTelevizyonVeSinemaAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/YeniMedyaVeIletisimAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/BiyomedikalMuhendisligiAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/ElektrikElektronikMuhendisligiAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/IcMimarlikVeCevreTasarimiAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/MimarlikAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/BeslenmeveDiyetetikAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/FizyoterapiVeRehabilitasyonAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/HemsirelikAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/IsSagligiVeGuvenligiAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/SaglikYonetimiAkademikKadro.aspx",
            "https://www.yeniyuzyil.edu.tr/Bolumler/AntrenorlukEgitimiAkademikKadro.aspx"

        ],
    }

    author_data = []

    for url_type, urls in url_function_map.items():
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                if url_type == 1:
                    # Extract department name
                    department_list = soup.find("div", class_="row detay-header-footer")
                    department_list = department_list.find("div", class_="col-md-12")
                    department_name = "Unknown Department"
                    if department_list:
                        department_name = department_list.get_text(strip=True)

                    # Get faculty members
                    member_list = soup.find("div", class_="akademik-kadro")
                    if not member_list:
                        print(f"Member list not found in {url}")
                        continue

                    members = member_list.find_all("div", class_="akademik-name")
                    for member in members:
                        name = clean_name(member.get_text(strip=True))
                        author_data.append({
                            "Ad": name,
                            "Üniversite": UNIVERSITY_NAME,
                            "Fakülte": department_name,
                        })

                elif url_type == 2:
                    department_list = soup.find("div", class_="row detay-header-footer")
                    department_list = department_list.find("div", class_="col-md-12")
                    department_name = "Unknown Department"
                    if department_list:
                        department_name = department_list.get_text(strip=True)
                        # Get faculty members
                        member_list = soup.find("div", class_="akademik-kadro")
                        if not member_list:
                            print(f"Member list not found in {url}")
                            continue

                        members = member_list.find_all("div", class_="akademik-name")
                        for member in members:
                            name = clean_name(member.get_text(strip=True))
                            author_data.append({
                                "Ad": name,
                                "Üniversite": UNIVERSITY_NAME,
                                "Fakülte": department_name,
                            })


                # Add department URL
                add_department_url(UNIVERSITY_NAME, department_name, url, url_data)
                print(f"Scraped {len(members)} entries from {url}")

            except Exception as e:
                print(f"Error scraping {url}: {e}")
    return author_data