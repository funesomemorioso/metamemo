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

É necessário fazer a autenticação por 2 fatores no Telegram na primeira vez (o
arquivo de sessão ficará salvo em `settings.DATA_DIR` e será reutilizado nas
outras vezes que o programa rodar). Para isso, execute manualmente qualquer um
dos comandos `import_telegram` e responda com o telefone e o código.

## Refazendo a imagem

Caso seja necessário refazer a imagem do container `web` (por ter adicionado
alguma dependência de sistema ou Python), basta executar:

```shell
docker compose stop web
docker compose rm -f web
docker compose build web  # em alguns casos, `--no-cache` pode ajudar
docker compose start web
```

## Backup/restore do banco local

Para criar um backup da base de dados PostgreSQL local, execute dentro do container `web`:

```shell
# Para executar o bash no container, rode: docker compose exec web bash
pg_dump -F c -d $DATABASE_URL -f "metamemo-$(date +'%Y-%m-%d').dump"
```

Para restaurar usando o arquivo `YYYY-MM-DD-metamemo.dump`, execute dentro do container `web`:

```shell
# Para executar o bash no container, rode: docker compose exec web bash
pg_restore -d $DATABASE_URL YYY-MM-DD-metamemo.dump
```

## Deployment

Acesse [deploy/README.md](deploy/README.md).
