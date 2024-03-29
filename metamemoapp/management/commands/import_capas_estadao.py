import json
from datetime import datetime, timedelta
from io import BytesIO

import requests
from django.core.files.base import File
from django.core.management.base import BaseCommand

from metamemoapp.models import NewsCover, NewsSource


class Command(BaseCommand):
    help = "Importa Capas do Estadão"

    def add_arguments(self, parser):
        parser.add_argument("-n", "--number", type=int, help="Number of Days")
        parser.add_argument("-d", "--date", type=str, help="Date to search from")

    def handle(self, *args, **kwargs):
        self.days = kwargs["number"]
        self.veiculo = "estadao"
        if kwargs["date"]:
            self.actual_date = datetime.strptime(kwargs["date"], "%Y-%m-%d")
        else:
            self.actual_date = datetime.today() - timedelta(60)
        print(self.actual_date)
        self.source = NewsSource.objects.get_or_create(name="Estado de São Paulo")[0]
        self.covers = NewsCover.objects.filter(source=self.source).values_list("media", flat=True)
        for i in range(self.days):
            ano = str(self.actual_date.year)
            mes = str(self.actual_date.month)
            dia = str(self.actual_date.day)
            url = f"https://acervo.estadao.com.br/pagina/{dia.zfill(2)}/{mes.zfill(2)}/{ano}/"
            uolfilename = requests.get(url).url.split("/")[-1]
            filename = f"{self.veiculo}_{ano}_{mes}_{dia}.jpg"
            if f"cover/{filename}" in self.covers:
                print("Last cover already in DB...")
                break
            url = f"https://acervo.estadao.com.br/servicos/montaPagina.php?nome_arquivo={uolfilename}"

            data = requests.get(url)
            data = json.loads(data.content)
            print(data["imagem_reader"])
            image_data = requests.get(data["imagem_reader"])
            fp = BytesIO()
            fp.write(image_data.content)

            newscover = NewsCover()
            newscover.source = self.source
            newscover.content_date = self.actual_date
            newscover.media.save(name=filename, content=File(fp))
            newscover.save()
            self.actual_date = self.actual_date - timedelta(1)
