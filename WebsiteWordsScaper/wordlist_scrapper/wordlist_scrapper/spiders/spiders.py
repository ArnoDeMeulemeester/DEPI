from io import StringIO
from functools import partial
from scrapy.http import Request
from scrapy.spiders import BaseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item
#TODO Replace "allowed_domains", "start_urls" and "wordlist" with your own data. 
def find_all_substrings(string, sub):

    import re
    starts = [match.start() for match in re.finditer(re.escape(sub), string)]
    return starts

class WebsiteSpider(CrawlSpider):

    name = "webcrawler"
    allowed_domains = ["http://www.quartes.com/"]
    start_urls = ["http://www.quartes.com/"]
    rules = [Rule(LinkExtractor(), follow=True, callback="check_buzzwords")]

    crawl_count = 0
    words_found = 0                                 

    def check_buzzwords(self, response):

        self.__class__.crawl_count += 1

        crawl_count = self.__class__.crawl_count

        wordlist = [
            "energiebron", "energie vermindering", "energie reductie", "energie-intensiteit", "energiegebruik", "energieverbruik",
            "waterverbruik", "waterbron", "wateronttrekking", "waterafvoer", "watergebruik", "afvalwater", "grondwater", 
            "broeikasgas", "CO2", "CO²", "CO2", 
            "emissie", "uitstoot", "vervuiling", "zure regen", "uitstoot", "fijnstof", "fijn stof", "vervuilende stof", "filtertechniek", "luchtzuiverheid", "zuiveringstechnologie",
            "impact", "milieu-impact", "impact op het milieu", "milieu impact", "milieu", "mobiliteit", "vervoer", "verplaatsing", "fiets", "auto", "staanplaatsen", "parking", "openbaar vervoer", "klimaatimpact", "impact op het klimaat", "klimaatsverandering", "green deal", 
            "gezondheid", "reclyclage", "recycleren", "biodiversiteit", "afval", "afvalproductie", "vervuiling", 
            "klimaat", "klimaatsverandering", "klimaatopwarming", "opwarming", "scope",
             "milieubeleid", "hernieuwbare energie", "verspilling", "milieucriteria", "planeet", "klimaatsbeleid", "milieunormen", 
             "schoon water en sanitair","betaalbare en duurzame energie", "duurzame steden en gemeenschappen", "verantwoorde consumptie en productie", "klimaatactie", "leven in het water", 'leven op het land',
            "duurzaamheidsdoelstellingen", "ontwikkelingsdoelen", "ontwikkelingsdoelstelling", "duurzaamheidsrapportering", 
            ]

        url = response.url
        contenttype = response.headers.get("content-type", "").decode('utf-8').lower()
        data = response.body.decode('utf-8')

        for word in wordlist:
                substrings = find_all_substrings(data, word)
                for pos in substrings:
                        ok = False
                        if not ok:
                                self.__class__.words_found += 1
                                print(word + ";" + url + ";")
        return Item()

    def _requests_to_follow(self, response):
        if getattr(response, "encoding", None) != None:
                return CrawlSpider._requests_to_follow(self, response)
        else:
                return []