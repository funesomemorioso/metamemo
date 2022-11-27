# MetaMemo

## Requisitos

- Docker
- Docker compose

## Como usar

Primeiro, copie o `.env-example` para `.env` e edite o arquivo caso necessário.
Para subir todos os serviços necessários, execute `docker compose up -d` na
raiz do projeto. A primeira vez que o comando for executado irá demorar alguns
minutos, dado que o `docker compose` precisará baixar algumas imagens e gerar a
image do serviço `web`.

Quando tudo estiver rodando você poderá acompanhar os logs com `docker compose
logs -t` e quando todos os serviços tiverem subido, basta acessar
[localhost:5000](http://localhost:5000/).


## Configurações iniciais

Para criar a estrutura dos modelos no banco de dados, execute o `bash` dentro
do container `web` com `docker compose exec web bash` e, dentro do container,
execute:

```shell
python manage.py migrate
```

Para criar o usuário administrativo:

```shell
python manage.py createsuperuser
```

## Refazendo a imagem

Caso seja necessário refazer a imagem do container `web` (por ter adicionado
alguma dependência de sistema ou Python), basta executar:

```shell
docker compose stop web
docker compose rm -f web
docker compose build web  # em alguns casos, `--no-cache` pode ajudar
docker compose start web
```

## Deployment

(a fazer)
