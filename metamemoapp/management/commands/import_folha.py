from urllib import parse, request

from django.core.management.base import BaseCommand
from lxml import html

from metamemoapp.models import MetaMemo, NewsItem, NewsSource
from metamemoapp.utils import parse_date


class Command(BaseCommand):
    help = "Importa Notícias da Folha de São Paulo"
    max_result = 10000
    sr = 1
    site = "jornal"

    def checkWords(self, list_words, text):
        if not list_words:
            return True
        for word in list_words.split(","):
            if word.lower() in text.lower():
                return True
        return False

    def scrapeFolha(self, keyword):
        all_news = NewsItem.objects.filter(source=self.source, metamemo=self.metamemo[0]).values_list("url", flat=True)

        keyword = parse.quote(keyword)
        soap = request.urlopen(f"https://search.folha.uol.com.br/?q={keyword}&site={self.site}&sr={self.sr}")
        soap = soap.read()
        soap = html.fromstring(soap)
        for n in soap.xpath("//li[contains(@class,'c-headline')]"):
            news = NewsItem()
            news.title = n.xpath(".//h2[contains(@class,'c-headline__title')]")[0].text.strip()
            news.text = n.xpath(".//p[contains(@class, 'c-headline__standfirst')]")[0].text_content().strip()
            news.url = n.xpath(".//div[contains(@class, 'c-headline__content')]/a")[0].get("href")
            dt = n.xpath(".//time")[0].text_content().strip().replace("º", "")
            news.content_date = parse_date(dt)
            news.metamemo = self.metamemo[0]
            news.source = self.source
            if news.url in all_news:
                print(f"[News already in DB] {news.title}")
                if not self.update:
                    self.sr = self.max_result
                    break
            elif self.checkWords(self.filter_words, news.title):
                print(f"[Saving] {news.title}")
                news.save()
            else:
                print(f"[Skipping] {news.title}")

            self.sr += 1

    def add_arguments(self, parser):
        parser.add_argument("-k", "--keyword", type=str, help="Palavra-chave")
        parser.add_argument("-f", "--filter", type=str, help="Filtra resultados com palavras no headline")
        parser.add_argument("-a", "--author", type=str, help="MetaMemo Author Name")
        parser.add_argument("-u", "--update", action="store_true")

    def handle(self, *args, **kwargs):
        self.keyword = kwargs["keyword"]
        self.author = kwargs["author"]
        self.filter_words = kwargs["filter"]
        self.metamemo = MetaMemo.objects.get_or_create(name=self.author)
        self.source = NewsSource.objects.get_or_create(name="Folha de São Paulo")[0]
        self.update = kwargs["update"]

        while self.sr < self.max_result:
            print("Starting from..." + str(self.sr))
            self.scrapeFolha(self.keyword)
