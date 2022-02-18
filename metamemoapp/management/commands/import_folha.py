from django.conf import settings
from django.core.management.base import BaseCommand

from django.utils import timezone
from metamemoapp.models import MetaMemo, MemoNews
import datetime, re
from lxml import html
from urllib import request, parse

def parseDate(content_date):
    mes = {'jan':'01','fev':'02','mar':'03','abr':'04','mai':'05','jun':'06','jul':'07','ago':'08','set':'09','out':'10','nov':'11','dez':'12'}
    c = re.search("([0-9]{1,2})\.([a-z]{3})\.([0-9]{1,4}) à[s]? ([0-9]{1,2})h([0-9]{1,2})", content_date)
    return f'{c[3]}-{mes[c[2]]}-{c[1]} {c[4]}:{c[5]}:00'

class Command(BaseCommand):
    help = 'Importa Notícias da Folha de São Paulo'
    max_result = 10000
    sr = 1
    site = 'jornal'

    def scrapeFolha(self, keyword):
        keyword = parse.quote(keyword)
        soap = request.urlopen(f'https://search.folha.uol.com.br/?q={keyword}&site={self.site}&sr={self.sr}')
        soap = soap.read()
        soap = html.fromstring(soap)
        for n in soap.xpath("//li[contains(@class,'c-headline')]"):
            try:
                news = MemoNews()
                news.title = n.xpath(".//h2[contains(@class,'c-headline__title')]")[0].text.strip()
                news.text = n.xpath(".//p[contains(@class, 'c-headline__standfirst')]")[0].text_content().strip()
                news.url = n.xpath(".//div[contains(@class, 'c-headline__content')]/a")[0].get("href")
                dt = n.xpath(".//time")[0].text_content().strip().replace('º','')
                news.content_date = parseDate(dt)
                news.metamemo = self.metamemo[0]
                news.source = "Folha de São Paulo"
                news.save()
                self.sr += 1
            except:
                print(dt)

    def add_arguments(self, parser):
        parser.add_argument('-k', '--keyword', type=str, help='Palavra-chave')
        parser.add_argument('-a', '--author', type=str, help='MetaMemo Author Name')


    def handle(self, *args, **kwargs):
        keyword = kwargs['keyword']
        self.author = kwargs['author']
        self.metamemo = MetaMemo.objects.get_or_create(name=self.author)

        while self.sr < self.max_result:
            print("Starting from..." + str(self.sr))
            self.scrapeFolha(keyword)