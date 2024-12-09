from scrapers.ozyeginScraper import scrape_ozyegin
from scrapers.sabanciScraper import scrape_sabanci
from scrapers.uskudarScraper import scrape_uskudar
from scrapers.yeditepeScraper import scrape_yeditepe
from scrapers.piriReisScraper import scrape_pririreis
from scrapers.mefScraper import scrape_mef
from scrapers.maltepeScraper import scrape_maltepe
from scrapers.kadirhasScraper import scrape_Khas
from  scrapers.yeniyuzyilScraper import scrape_yeniyuzyil
from scrapers.topkapiScraper import scrape_Topkapi
from scrapers.istanbul_ticaretScraper import scrape_Ticaret
from scrapers.istanbul_saglik_ve_teknolojiScraper import scrape
from scrapers.istanbul_zaimScraper import scrapeZaim
from utils.common import handle_excel_output

ACADEMIC_EXCEL_PATH = "data/kadro.xlsx"
URL_EXCEL_PATH = "data/departman_url.xlsx"

author_data = []
url_data = []

def main():

    author_data.extend(scrapeZaim(url_data))

    handle_excel_output(author_data, ACADEMIC_EXCEL_PATH)
    handle_excel_output(url_data, URL_EXCEL_PATH)

if __name__ == "__main__":
    main()