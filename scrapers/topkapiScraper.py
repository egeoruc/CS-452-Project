import requests
from bs4 import BeautifulSoup
from utils.common import add_department_url, clean_name

UNIVERSITY_NAME = "İstanbul Topkapı Üniversitesi"

def scrape_Topkapi(url_data):
    urls = [
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/137642",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/48195",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/48216",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/152680",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/99515",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/118659",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/118666",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/99523",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/48244",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/151663",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/118673",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/118680",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/48251",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/87408",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/48258",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/48265",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/118687",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/118694",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/99539",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/119627",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/99507",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/118631",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/28076",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/27947",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/27940",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/48202",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/118638",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/118645",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/137650",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/137658",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/156800",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/99570",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/99578",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/99586",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/48237",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/99531",
        "https://www.topkapi.edu.tr/tr-TR/akademik-kadro/73344",
    ]

    broken_urls = [
        "https://www.topkapi.edu.tr/tr-TR/bolum-baskaninin-mesaji/156838",
        "https://www.topkapi.edu.tr/tr-TR/bolumler/156850"
    ]

    author_data = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            div_breadcrumb = soup.find("div", "row breadcrumb")
            div_col = div_breadcrumb.find('div', class_='column-12')
            department_name = "Unknown Department"
            if div_col:
                ul = div_col.find('ul', class_='breadcrumb mb0')
                if ul:
                    items = ul.find_all('li')
                    if len(items) > 1:
                        second_li = items[1]
                        department_name = second_li.find('a').get_text(strip=True)

            list_div = soup.find("div", class_="row university-management")
            if not list_div:
                print(f"List not found in {url}")
                continue

            # Extract academic staff entries
            items = list_div.find_all("div", class_="management-wrapper")
            for item in items:
                # Extract name
                name_h2 = item.find("h2", class_="title")
                name = clean_name(name_h2.get_text(strip=True))

                author_data.append({
                    "Ad": name,
                    "Üniversite": UNIVERSITY_NAME,
                    "Fakülte": department_name,
                })

            add_department_url(UNIVERSITY_NAME, department_name, url, url_data)
            print(f"Scraped {len(items)} entries from {url}")

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return author_data