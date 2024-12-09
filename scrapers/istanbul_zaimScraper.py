from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils.common import add_department_url, title_end_clean_name
import re

# University Name
UNIVERSITY_NAME = "İstanbul Zaim Üniversitesi"

# Function to scrape faculty data
def scrapeZaim(url_data):
    urls = [
        "https://www.izu.edu.tr/akademik/fakulteler/egitim-fakultesi/bolumler/egitim-bilimleri-bolumu/rehberlik-ve-psikolojik-danismanlik-anabilim-dali/rehberlik-ve-psikolojik-danismanlik",
        "https://www.izu.edu.tr/akademik/fakulteler/egitim-fakultesi/bolumler/matematik-ve-fen-bilimleri-egitim-bolumu/ilkogretim-matematik-egitimi-anabilim-dali/ilkogretim-matematik-ogretmenligi",
        "https://www.izu.edu.tr/akademik/fakulteler/egitim-fakultesi/bolumler/ozel-egitim-bolumu/ozel-egitim-anabilim-dali/ozel-egitim-ogretmenligi",
        "https://www.izu.edu.tr/akademik/fakulteler/egitim-fakultesi/bolumler/temel-egitim-bolumu/okul-oncesi-egitimi-anabilim-dali/okul-oncesi-ogretmenligi",
        "https://www.izu.edu.tr/akademik/fakulteler/egitim-fakultesi/bolumler/temel-egitim-bolumu/sinif-egitimi-anabilim-dali/sinif-ogretmenligi",
        "https://www.izu.edu.tr/akademik/fakulteler/egitim-fakultesi/bolumler/turkce-ve-sosyal-bilimler-egitimi-bolumu/turkce-egitimi-anabilim-dali/turkce-ogretmenligi",
        "https://www.izu.edu.tr/akademik/fakulteler/egitim-fakultesi/bolumler/yabanci-diller-egitimi-bolumu/arap-dili-egitimi-anabilim-dali/arapca-%C3%B6gretmenligi-yuzde-30-arapca",
        "https://www.izu.edu.tr/akademik/fakulteler/egitim-fakultesi/bolumler/yabanci-diller-egitimi-bolumu/ingiliz-dili-egitimi-anabilim-dali/ingilizce-ogretmenligi",
        "https://www.izu.edu.tr/akademik/fakulteler/egitim-fakultesi/bolumler/guzel-sanatlar-egitimi-bolumu/muzik-egitimi-anabilim-dali/muzik-ogretmenligi",
        "https://www.izu.edu.tr/akademik/fakulteler/hukuk-fakultesi/bolumler/hukuk",
        "https://www.izu.edu.tr/akademik/fakulteler/insan-ve-toplum-bilimleri-fakultesi/bolumler/psikoloji",
        "https://www.izu.edu.tr/akademik/fakulteler/insan-ve-toplum-bilimleri-fakultesi/bolumler/psikoloji-ingilizce",
        "https://www.izu.edu.tr/akademik/fakulteler/insan-ve-toplum-bilimleri-fakultesi/bolumler/siyaset-bilimi-ve-uluslararasi-iliskiler-ingilizce",
        "https://www.izu.edu.tr/akademik/fakulteler/insan-ve-toplum-bilimleri-fakultesi/bolumler/sosyoloji-yuzde-30-ingilizce",
        "https://www.izu.edu.tr/akademik/fakulteler/insan-ve-toplum-bilimleri-fakultesi/bolumler/tarih",
        "https://www.izu.edu.tr/akademik/fakulteler/insan-ve-toplum-bilimleri-fakultesi/programlar/turk-dili-ve-edebiyati",
        "https://www.izu.edu.tr/akademik/fakulteler/insan-ve-toplum-bilimleri-fakultesi/programlar/gosel-iletisim-tasarimi",
        "https://www.izu.edu.tr/akademik/fakulteler/islami-ilimler-fakultesi/bolumler/islami-ilimler-yuzde-30-arapca",
        "https://www.izu.edu.tr/akademik/fakulteler/islami-ilimler-fakultesi/bolumler/islami-ilimler-arapca",
        "https://www.izu.edu.tr/akademik/fakulteler/isletme-ve-yonetim-bilimleri-fakultesi/bolumler/iktisat-yuzde-30-ingilizce",
        "https://www.izu.edu.tr/akademik/fakulteler/isletme-ve-yonetim-bilimleri-fakultesi/bolumler/islam-iktisadi-finans",
        "https://www.izu.edu.tr/akademik/fakulteler/isletme-ve-yonetim-bilimleri-fakultesi/bolumler/islam-iktisadi-finans-ingilizce",
        "https://www.izu.edu.tr/akademik/fakulteler/isletme-ve-yonetim-bilimleri-fakultesi/bolumler/isletme-yuzde-30-ingilizce",
        "https://www.izu.edu.tr/akademik/fakulteler/isletme-ve-yonetim-bilimleri-fakultesi/bolumler/uluslararasi-ticaret-finansman",
        "https://www.izu.edu.tr/akademik/fakulteler/isletme-ve-yonetim-bilimleri-fakultesi/bolumler/uluslararasi-ticaret-finansman-ingilizce",
        "https://www.izu.edu.tr/akademik/fakulteler/muhendislik-ve-doga-bilimleri-fakultesi/bolumler/bilgisayar-muhendisligi",
        "https://www.izu.edu.tr/akademik/fakulteler/muhendislik-ve-doga-bilimleri-fakultesi/bolumler/elektrik-elektronik-muhendisligi-yuzde-30-ingilizce)",
        "https://www.izu.edu.tr/akademik/fakulteler/muhendislik-ve-doga-bilimleri-fakultesi/bolumler/endustri-muhendisligi-yuzde-30-ingilizce)",
        "https://www.izu.edu.tr/akademik/fakulteler/muhendislik-ve-doga-bilimleri-fakultesi/bolumler/g%c4%b1da-m%c3%bchendisli%c4%9fi-(-30-i-ngilizce)",
        "https://www.izu.edu.tr/akademik/fakulteler/muhendislik-ve-doga-bilimleri-fakultesi/bolumler/ic-mimarlik-ve-cevre-tasarimi",
        "https://www.izu.edu.tr/akademik/fakulteler/muhendislik-ve-doga-bilimleri-fakultesi/bolumler/mimarlik",
        "https://www.izu.edu.tr/akademik/fakulteler/muhendislik-ve-doga-bilimleri-fakultesi/bolumler/molekuler-biyoloji-genetik-ingilizce",
        "https://www.izu.edu.tr/akademik/fakulteler/muhendislik-ve-doga-bilimleri-fakultesi/bolumler/yazilim-muhendisligi-yuzde-30-ingilizce",
        "https://www.izu.edu.tr/akademik/fakulteler/saglik-bilimleri-fakultesi/bolumler/beslenme-ve-diyetetik",
        "https://www.izu.edu.tr/akademik/fakulteler/saglik-bilimleri-fakultesi/bolumler/hemsirelik",
        "https://www.izu.edu.tr/akademik/fakulteler/saglik-bilimleri-fakultesi/bolumler/saglik-yonetimi",
        "https://www.izu.edu.tr/akademik/fakulteler/saglik-bilimleri-fakultesi/bolumler/sosyal-hizmet",
        "https://www.izu.edu.tr/akademik/fakulteler/sporbilimleri/bolumler/beden-egitimi-ve-spor-ogretmenligi",
        "https://www.izu.edu.tr/akademik/fakulteler/sporbilimleri/bolumler/spor-yoneticiligi",
    ]

    author_data = []

    driver_service = Service("/Users/egeoruc/Downloads/chromedriver-mac-arm64/chromedriver")
    driver = webdriver.Chrome(service=driver_service)

    try:
        for url in urls:
            try:
                driver.get(url)


                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "profile-listing"))
                )

                soup = BeautifulSoup(driver.page_source, "html.parser")

                # Get faculty members
                main_div = soup.find("div", class_="profile-listing")
                if not main_div:
                    print(f"main div not found: {url}")
                    continue

                items = main_div.find_all("div", class_="listing")
                for item in items:
                    full_name = item.find("h4").find("a")
                    if full_name:
                        full_name = full_name.get_text().strip()
                        name = title_end_clean_name(full_name)

                        # Get department name
                        nav = soup.find("section", class_="nav-inside")
                        if not nav:
                            print(f"department not found: {url}")
                            department_name = "Unknown"
                        else:
                            raw_department_name = nav.find("h2").find("a").get_text(strip=True)
                            department_name = re.sub(r"\(.*?\)", "", raw_department_name).strip().title()

                        author_data.append({
                            "Ad": name,
                            "Üniversite": UNIVERSITY_NAME,
                            "Fakülte": department_name,
                        })
                        add_department_url(UNIVERSITY_NAME, department_name, url, url_data)

                print(f"Scraped {len(items)} entries from {url}")

            except Exception as e:
                print(f"Error scraping {url}: {e}")

    finally:
        driver.quit()

    return author_data