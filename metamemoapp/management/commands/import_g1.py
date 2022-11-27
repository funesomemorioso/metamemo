from urllib import parse, request

from django.core.management.base import BaseCommand
from lxml import html

from metamemoapp.models import MemoNews, MetaMemo
from metamemoapp.utils import parse_date


class Command(BaseCommand):
    help = "Importa Notícias do G1"
    max_result = 10000
    sr = 1
    site = "jornal"

    def scrapeFolha(self, keyword):
        keyword = parse.quote(keyword)
        soap = request.urlopen(f"https://search.folha.uol.com.br/?q={keyword}&site={self.site}&sr={self.sr}")
        soap = soap.read()
        soap = html.fromstring(soap)
        for n in soap.xpath("//li[contains(@class,'c-headline')]"):
            try:
                news = MemoNews()
                news.title = n.xpath(".//h2[contains(@class,'c-headline__title')]")[0].text.strip()
                news.text = n.xpath(".//p[contains(@class, 'c-headline__standfirst')]")[0].text_content().strip()
                news.url = n.xpath(".//div[contains(@class, 'c-headline__content')]/a")[0].get("href")
                dt = n.xpath(".//time")[0].text_content().strip().replace("º", "")
                news.content_date = parse_date(dt)
                news.metamemo = self.metamemo[0]
                news.source = "Folha de São Paulo"
                news.save()
                self.sr += 1
            except:
                print(dt)

    def add_arguments(self, parser):
        parser.add_argument("-k", "--keyword", type=str, help="Palavra-chave")
        parser.add_argument("-a", "--author", type=str, help="MetaMemo Author Name")

    def handle(self, *args, **kwargs):
        keyword = kwargs["keyword"]
        self.author = kwargs["author"]
        self.metamemo = MetaMemo.objects.get_or_create(name=self.author)

        while self.sr < self.max_result:
            print("Starting from..." + str(self.sr))
            self.scrapeFolha(keyword)
