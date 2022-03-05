# MetaMemo

## Requisitods

- Django

## Como usar

Primeiro, copie o .env-example para .env e atualize com as informações do seu banco de dados.
Não se esqueça de, na hora de criar o banco de dados, configurar character set e collation.
Exemplo (no MariaDB 10.3.34):

    CREATE DATABASE metamemo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Para criar o banco de dados:

```shell
python manage.py makemigrations
python manage.py makemigrations metamemoapp
python manage.py migrate
```

Para criar o usuário administrativo:

    python manage createsuperuser

Depois de instalado o django no seu venv preferido:

    python manage.py runserver

Para colocar em produção a gente usa o mod_wsgi mas não precisamos nos preocupar com isso agora.
