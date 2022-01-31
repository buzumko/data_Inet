from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leruaparser.spiders.leroymerlinru import  LeroymerlinruSpider
from leruaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinruSpider, search='мебель для кухни')

    process.start()
