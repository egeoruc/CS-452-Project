import requests
from bs4 import BeautifulSoup
from utils.common import add_department_url

UNIVERSITY_NAME = "Yeditepe Üniversitesi"

def extract_department_from_url(url):
    if "https://med.yeditepe.edu.tr/tr/akademik-kadro" in url:
        return "Tıp"

    segments = url.rstrip('/').split('/')

    if len(segments) > 2 and segments[-1] == "akademik-kadro":
        if segments[-2] != "tr":
            return segments[-2].replace("-", " ").title()

    domain_parts = url.split("//")[1].split(".")
    if len(domain_parts) > 1:
        subdomain = domain_parts[0]
        if subdomain != "www" and subdomain != "tr":
            return subdomain.replace("-", " ").title()
    return "Unknown Department"

def scrape_layout_akademik_kadro(url, url_data):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    data = []
    faculty_name = extract_department_from_url(url)

    kadro_list = soup.find_all("div", id="akademikKadroList")
    for kadro in kadro_list:
        name_divs = kadro.find_all("div", class_="akademikListName")
        if len(name_divs) > 1:
            name_a = name_divs[1].find("a")
            full_name = name_a.get_text(strip=True) if name_a else name_divs[1].get_text(strip=True)
        else:
            full_name = "Unknown Name"

        data.append({
            "Ad": full_name,
            "Üniversite": UNIVERSITY_NAME,
            "Fakülte": faculty_name,
        })

    add_department_url(UNIVERSITY_NAME, faculty_name, url, url_data)
    return data

def scrape_col_md_9_layout(url, url_data):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    data = []
    faculty_name = extract_department_from_url(url)

    main_div = soup.find("section", class_=["col-md-9", "col-md-12"])
    if not main_div:
        print(f"Main container not found in {url}")
        return data

    academic_divs = main_div.find_all("div", class_=["views-field views-field-field-unvan-akademisyen",
                                                     "views-field views-field-field-gorevi-akademisyen", "views-field views-field-field-gorev-akademisyen"])
    for academic_div in academic_divs:
        name_tag = academic_div.find("strong").find("a")
        full_name = name_tag.get_text(strip=True) if name_tag else "Unknown Name"

        data.append({
            "Ad": full_name,
            "Üniversite": UNIVERSITY_NAME,
            "Fakülte": faculty_name,
        })

    add_department_url(UNIVERSITY_NAME, faculty_name, url, url_data)
    return data

def scrape_yeditepe(url_data):
    url_function_map = {
        scrape_layout_akademik_kadro: [
            "https://yabancidiller.yeditepe.edu.tr/tr/almanca/akademik-kadro",
            "https://yabancidiller.yeditepe.edu.tr/tr/cince/akademik-kadro",
            "https://yabancidiller.yeditepe.edu.tr/tr/fransizca/akademik-kadro",
            "https://yabancidiller.yeditepe.edu.tr/tr/ispanyolca/akademik-kadro",
            "https://yabancidiller.yeditepe.edu.tr/tr/ingilizce/akademik-kadro",
            "https://yabancidiller.yeditepe.edu.tr/tr/korece/akademik-kadro",
            "https://yabancidiller.yeditepe.edu.tr/tr/rusca/akademik-kadro"
        ],
        scrape_col_md_9_layout: [
             "https://saglik.yeditepe.edu.tr/tr/beslenme-ve-diyetetik-bolumu/akademik-kadro",
        "https://fenedebiyat.yeditepe.edu.tr/tr/antropoloji/akademik-kadro",
        "https://bbbf.yeditepe.edu.tr/tr/bilgi-guvenligi-teknolojisi-bolumu/akademik-kadro",
        "https://eng.yeditepe.edu.tr/tr/bilgisayar-muhendisligi-bolumu/akademik-kadro",
        "https://egitim.yeditepe.edu.tr/tr/bilgisayar-ve-ogretim-teknolojileri-ogretmenligi-programi/akademik-kadro",
        "https://bbbf.yeditepe.edu.tr/tr/bilisim-sistemleri-ve-teknolojileri-bolumu/akademik-kadro",
        "https://eng.yeditepe.edu.tr/tr/biyomedikal-muhendisligi-bolumu/akademik-kadro",
        "https://fenedebiyat.yeditepe.edu.tr/tr/ceviribilim/akademik-kadro",
        "https://dishekimligi.yeditepe.edu.tr/tr/akademik-kadro",
        "https://eczacilik.yeditepe.edu.tr/tr/akademik-kadro",
        "https://egitim.yeditepe.edu.tr/tr/ozel-egitim-ogretmenligi-programi/akademik-kadro",
        "https://egitim.yeditepe.edu.tr/tr/ilkogretim-matematik-ogretmenligi-programi/akademik-kadro",
        "https://egitim.yeditepe.edu.tr/tr/ingilizce-ogretmenligi-programi/akademik-kadro",
        "https://egitim.yeditepe.edu.tr/tr/rehberlik-ve-psikolojik-danismanlik-programi/akademik-kadro",
        "https://egitim.yeditepe.edu.tr/tr/turk-dili-ve-edebiyati-ogretmenligi-programi/akademik-kadro",
        "https://iibf.yeditepe.edu.tr/tr/ekonomi/akademik-kadro",
        "https://eng.yeditepe.edu.tr/tr/elektrik-ve-elektronik-muhendisligi-bolumu/akademik-kadro",
        "https://myo.yeditepe.edu.tr/tr/elektronik-teknolojisi-programi/akademik-kadro",
        "https://iibf.yeditepe.edu.tr/tr/elektronik-ticaret-ve-yonetimi-bolumu/akademik-kadro",
        "https://eng.yeditepe.edu.tr/tr/endustri-muhendisligi-bolumu/akademik-kadro",
        "https://mimarlik.yeditepe.edu.tr/tr/endustriyel-tasarim-bolumu/akademik-kadro",
        "https://saglik.yeditepe.edu.tr/tr/fizyoterapi-ve-rehabilitasyon-bolumu/akademik-kadro",
        "https://fenedebiyat.yeditepe.edu.tr/tr/fizik/akademik-kadro",
        "https://fenedebiyat.yeditepe.edu.tr/tr/felsefe/akademik-kadro",
        "https://gsf.yeditepe.edu.tr/tr/gastronomi-ve-mutfak-sanatlari-bolumu/akademik-kadro",
        "https://uygulamalibilimler.yeditepe.edu.tr/tr/gayrimenkul-gelistirme-ve-yonetimi-bolumu/akademik-kadro",
        "https://iletisimfakultesi.yeditepe.edu.tr/tr/gazetecilik-bolumu/akademik-kadro",
        "https://eng.yeditepe.edu.tr/tr/genetik-ve-biyomuhendisligi-bolumu/akademik-kadro",
        "https://eng.yeditepe.edu.tr/tr/gida-muhendisligi-bolumu/akademik-kadro",
        "https://gsf.yeditepe.edu.tr/tr/grafik-tasarimi-bolumu/akademik-kadro",
        "https://uygulamalibilimler.yeditepe.edu.tr/tr/gumruk-isletme-bolumu/akademik-kadro",
        "https://iletisimfakultesi.yeditepe.edu.tr/tr/halkla-iliskiler-ve-tanitim-bolumu/akademik-kadro",
        "https://saglik.yeditepe.edu.tr/tr/hemsirelik-bolumu/akademik-kadro",
        "https://law.yeditepe.edu.tr/tr/akademik-kadro",
        "https://iibf.yeditepe.edu.tr/tr/isletme/akademik-kadro",
        "https://myo.yeditepe.edu.tr/tr/internet-ve-ag-teknolojileri-programi/akademik-kadro",
        "https://uygulamalibilimler.yeditepe.edu.tr/tr/insan-kaynaklari-yonetimi-bolumu/akademik-kadro",
        "https://eng.yeditepe.edu.tr/tr/insaat-muhendisligi-bolumu/akademik-kadro",
        "https://egitim.yeditepe.edu.tr/tr/ingilizce-ogretmenligi-programi/akademik-kadro",
        "https://egitim.yeditepe.edu.tr/tr/ilkogretim-matematik-ogretmenligi-programi/akademik-kadro",
        "https://mimarlik.yeditepe.edu.tr/tr/ic-mimarlik-bolumu/akademik-kadro",
        "https://iibf.yeditepe.edu.tr/tr/kamu-yonetimi/akademik-kadro",
        "https://mimarlik.yeditepe.edu.tr/tr/kentsel-tasarim-ve-peyzaj-mimarligi-bolumu/akademik-kadro",
        "https://eng.yeditepe.edu.tr/tr/kimya-muhendisligi-bolumu/akademik-kadro",
        "https://iibf.yeditepe.edu.tr/tr/lojistik-yonetimi-bolumu/akademik-kadro",
        "https://eng.yeditepe.edu.tr/tr/makine-muhendisligi-bolumu/akademik-kadro",
        "https://eng.yeditepe.edu.tr/tr/malzeme-bilimi-ve-nanoteknoloji-muhendisligi-bolumu/akademik-kadro",
        "https://fenedebiyat.yeditepe.edu.tr/tr/matematik/akademik-kadro",
        "https://mimarlik.yeditepe.edu.tr/tr/mimarlik-bolumu/akademik-kadro",
        "https://egitim.yeditepe.edu.tr/tr/ozel-egitim-ogretmenligi-programi/akademik-kadro",
        "https://fenedebiyat.yeditepe.edu.tr/tr/psikoloji/akademik-kadro",
        "https://gsf.yeditepe.edu.tr/tr/plastik-sanatlar-ve-resim/akademik-kadro",
        "https://iletisimfakultesi.yeditepe.edu.tr/tr/radyotelevizyon-ve-sinema-bolumu/akademik-kadro",
        "https://egitim.yeditepe.edu.tr/tr/rehberlik-ve-psikolojik-danismanlik-programi/akademik-kadro",
        "https://iletisimfakultesi.yeditepe.edu.tr/tr/reklam-tasarimi-ve-iletisimi-bolumu/akademik-kadro",
        "https://fenedebiyat.yeditepe.edu.tr/tr/rus-dili-ve-edebiyati/akademik-kadro",
        "https://gsf.yeditepe.edu.tr/tr/sanat-ve-kultur-yonetimi-bolumu/akademik-kadro",
        "https://iibf.yeditepe.edu.tr/tr/siyaset-bilimi-ve-uluslararasi-iliskiler-fr/akademik-kadro",
        "https://fenedebiyat.yeditepe.edu.tr/tr/sosyoloji/akademik-kadro",
        "https://fenedebiyat.yeditepe.edu.tr/tr/tarih/akademik-kadro",
        "https://iibf.yeditepe.edu.tr/tr/tarim-ticareti-ve-isletmeciligi-bolumu/akademik-kadro",
        "https://gsf.yeditepe.edu.tr/tr/moda-ve-tekstil-tasarimi-bolumu/akademik-kadro",
        "https://gsf.yeditepe.edu.tr/tr/tiyatro-bolumu/akademik-kadro",
        "https://iibf.yeditepe.edu.tr/tr/turizm-isletmeciligi-bolumu/akademik-kadro",
        "https://fenedebiyat.yeditepe.edu.tr/tr/turk-dili-ve-edebiyati/akademik-kadro",
        "https://egitim.yeditepe.edu.tr/tr/turk-dili-ve-edebiyati-ogretmenligi-programi/akademik-kadro",
        "https://iibf.yeditepe.edu.tr/tr/uluslararasi-finans-bolumu/akademik-kadro",
        "https://iibf.yeditepe.edu.tr/tr/uluslararasi-isletme-yonetimi-de/akademik-kadro",
        "https://iibf.yeditepe.edu.tr/tr/uluslararasi-ticaret-ve-isletmecilik-bolumu/akademik-kadro",
        "https://bbbf.yeditepe.edu.tr/tr/yazilim-gelistirme-bolumu/akademik-kadro",
        "https://bbbf.yeditepe.edu.tr/tr/yonetim-bilisim-sistemleri-bolumu/akademik-kadro",
        "https://med.yeditepe.edu.tr/tr/akademik-kadro"
        ],
    }

    author_data = []
    for scrape_function, urls in url_function_map.items():
        for url in set(urls):  # Use set to remove duplicate URLs
            try:
                scraped_data = scrape_function(url, url_data)
                print(f"Scraped {len(scraped_data)} entries from {url}")
                author_data.extend(scraped_data)
            except Exception as e:
                print(f"Error scraping {url}: {e}")

    return author_data