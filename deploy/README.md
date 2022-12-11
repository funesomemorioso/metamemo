# Deploy do projeto

O deployment do projeto é realizado através do [Dokku](https://dokku.com/), que
facilita a gestão de containers Docker e outros serviços, como bancos de dados,
servidores de cache etc.

## Configurações iniciais do servidor

Para a segurança do servidor, é importante que você:

- Utilize apenas chaves SSH para login (copie suas chaves usando o comando
  `ssh-copy-id` ou coloque-as em `/root/.ssh/authorized_keys`)
- Remova a opção de login via SSH usando senha (altere a configuração editando
  o arquivo `/etc/ssh/ssh_config` e depois execude `service ssh restart`)
- Se possível, crie um outro usuário que possua acesso via `sudo` e desabilite
  o login do usuário root via SSH (edite o arquivo `/etc/ssh/ssh_config`)


## Instalação de pacotes básicos de sistema

```shell
apt update && apt upgrade -y && apt install -y wget
apt install -y $(wget -O - https://raw.githubusercontent.com/turicas/dotfiles/main/server-apt-packages.txt)
apt clean
```


## Instalação do Docker

Caso a versão do Debian seja mais nova que bullseye, verifique mudanças nos
comandos abaixo [na documentação do
Docker](https://docs.docker.com/engine/install/debian/).

```shell
apt remove docker docker-engine docker.io containerd runc
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Para testar:
docker run --rm hello-world
```

## Instalação e configuração do Dokku

Caso a versão do Debian seja mais nova que bullseye, verifique mudanças nos
comandos abaixo [na documentação do
Dokku](https://dokku.com/docs/getting-started/install/debian/).

```shell
wget -qO- https://packagecloud.io/dokku/dokku/gpgkey | tee /etc/apt/trusted.gpg.d/dokku.asc
OS_ID="$(lsb_release -cs 2>/dev/null || echo "bionic")"
echo "bionic focal jammy" | grep -q "$OS_ID" || OS_ID="bionic"
echo "deb https://packagecloud.io/dokku/dokku/ubuntu/ ${OS_ID} main" | tee /etc/apt/sources.list.d/dokku.list
apt update
apt install -y dokku
# Responda nas perguntas que quer habilitar vhost
apt clean
dokku plugin:install-dependencies --core

# Dokku plugins
dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku plugin:install https://github.com/dokku/dokku-maintenance.git
dokku plugin:install https://github.com/dokku/dokku-postgres.git
dokku plugin:install https://github.com/dokku/dokku-redis.git

# Dokku configs
dokku config:set --global DOKKU_RM_CONTAINER=1  # don't keep `run` containers around
dokku letsencrypt:cron-job --add
```

Caso você não tenha colocado sua chave SSH do Dokku durante a execução do
comando `apt install dokku`, você precisa adicioná-la com o seguinte comando:

```shell
dokku ssh-keys:add admin path/to/pub_key
```

> Nota: o arquivo deve ter apenas uma chave SSH (caso o arquivo fornecido na
> interface de configuração tenha mais de uma chave, a configuração precisará
> ser feita manualmente, com o comando acima).

Dessa forma, o usuário que possuir essa chave poderá fazer deployments via git
nesse servidor.

> **Importante:** após a instalação do Dokku, caso não tenha respondido às
> perguntas durante a instalação, será necessário acessar a interface Web
> temporária para finalizar configuração (entre em `http://ip-do-servidor/` em
> seu navegador).

Ao finalizar a instalação do Dokku e acessar http://ip-do-servidor/ você deverá
ver a mensagem "Welcome to nginx!".


## Instalação da aplicação

Antes de criar a aplicação no Dokku será necessário configurar algumas
variáveis no shell, para que elas sejam adicionadas às variáveis de ambiente do
app (assim, o Dokku irá sempre carregá-las toda vez que o app for iniciado e
não precisaremos armazenar senhas em arquivos no repositório).

```shell
# Provavelmente você precisará trocar apenas essas primeiras:
export APP_NAME="metamemo"
export APP_DOMAIN="metamemo.pythonic.cafe"  # Domínio por onde o app será acessado
export SENTRY_DSN="https://..."  # URL de acesso ao Sentry, para reporte de erros
export ADMINS="Álvaro Justen|alvaro@pythonic.cafe"
export DEFAULT_FROM_EMAIL="alvaro@pythonic.cafe"

export ALLOWED_HOSTS="$APP_DOMAIN"
export CSRF_TRUSTED_ORIGINS="https://${APP_DOMAIN}"
export DATA_DIR="/data"
export DEBUG="false"
export DEV_BUILD="false"
export LETSENCRYPT_EMAIL="$(echo $ADMINS | sed 's/^[^|]*|\([^,]*\).*$/\1/')"
export POSTGRES_NAME="postgres_${APP_NAME}"
export REDIS_NAME="redis_${APP_NAME}"
export SECRET_KEY=$(openssl rand -base64 64 | tr -d ' \n')
export STORAGE_PATH="/var/lib/dokku/data/storage/$APP_NAME"

export TWITTER_BEARER_TOKEN=xxx
export FACEBOOK_COOKIES_BASE64=xxx
export TELEGRAM_API_ID=xxx
export TELEGRAM_API_HASH=xxx
export CROWDTANGLE_FACEBOOK_API_KEY=xxx
export CROWDTANGLE_INSTAGRAM_API_KEY=xxx
export GOOGLE_BLOGGER_CREDENTIALS=xxx
export GOOGLE_YOUTUBE_CREDENTIALS=xxx
export GOOGLE_APPLICATION_CREDENTIALS_BASE64=xxx

# Opcionais:
# FACEBOOK_PAGES (default: 4)
# FACEBOOK_PPP (default: 10)
# CROWDTANGLE_POSTS_COUNT (default: 100)
# CROWDTANGLE_POSTS_INTERVAL (default: "5 DAY")
```

Depois que as variáveis foram definidas, podemos criar o app, os serviços de
banco de dados e fazer as configurações iniciais:

```shell
dokku apps:create $APP_NAME
dokku domains:add $APP_NAME $APP_DOMAIN
dokku nginx:set $APP_NAME client-max-body-size 50m

# Provisionando um volume (será útil para transportar dados do container para a
# máquina host, em tarefas de manutenção)
mkdir -p "$STORAGE_PATH"
dokku storage:mount $APP_NAME "$STORAGE_PATH:$DATA_DIR"

# Provisionando serviços de banco de dados
dokku postgres:create $POSTGRES_NAME -i postgres -I 14-bullseye --shm-size 2g
dokku postgres:stop $POSTGRES_NAME
cp deploy/postgres.prod.conf /var/lib/dokku/services/postgres/$POSTGRES_NAME/data/postgresql.conf
dokku postgres:start $POSTGRES_NAME
dokku postgres:link $POSTGRES_NAME $APP_NAME

dokku redis:create $REDIS_NAME
dokku redis:link $REDIS_NAME $APP_NAME

# Adicionando configurações iniciais
dokku config:set --no-restart $APP_NAME ADMINS="$ADMINS"
dokku config:set --no-restart $APP_NAME ALLOWED_HOSTS="$ALLOWED_HOSTS"
dokku config:set --no-restart $APP_NAME CSRF_TRUSTED_ORIGINS="$CSRF_TRUSTED_ORIGINS"
dokku config:set --no-restart $APP_NAME DATA_DIR="$DATA_DIR"
dokku config:set --no-restart $APP_NAME DEBUG="$DEBUG"
dokku config:set --no-restart $APP_NAME DEFAULT_FROM_EMAIL="$DEFAULT_FROM_EMAIL"
dokku config:set --no-restart $APP_NAME DEV_BUILD="$DEV_BUILD"
dokku config:set --no-restart $APP_NAME DOKKU_LETSENCRYPT_EMAIL="$LETSENCRYPT_EMAIL"
dokku config:set --no-restart $APP_NAME SECRET_KEY="$SECRET_KEY"
dokku config:set --no-restart $APP_NAME SENTRY_DSN="$SENTRY_DSN"

# Configurações para mídias sociais:
dokku config:set --no-restart $APP_NAME TWITTER_BEARER_TOKEN="$TWITTER_BEARER_TOKEN"
dokku config:set --no-restart $APP_NAME FACEBOOK_COOKIES_BASE64="$FACEBOOK_COOKIES_BASE64"
dokku config:set --no-restart $APP_NAME TELEGRAM_API_ID="$TELEGRAM_API_ID"
dokku config:set --no-restart $APP_NAME TELEGRAM_API_HASH="$TELEGRAM_API_HASH"
dokku config:set --no-restart $APP_NAME CROWDTANGLE_FACEBOOK_API_KEY="$CROWDTANGLE_FACEBOOK_API_KEY"
dokku config:set --no-restart $APP_NAME CROWDTANGLE_INSTAGRAM_API_KEY="$CROWDTANGLE_INSTAGRAM_API_KEY"
dokku config:set --no-restart $APP_NAME GOOGLE_BLOGGER_CREDENTIALS="$GOOGLE_BLOGGER_CREDENTIALS"
dokku config:set --no-restart $APP_NAME GOOGLE_YOUTUBE_CREDENTIALS="$GOOGLE_YOUTUBE_CREDENTIALS"
dokku config:set --no-restart $APP_NAME GOOGLE_APPLICATION_CREDENTIALS_BASE64="$GOOGLE_APPLICATION_CREDENTIALS_BASE64"

# Opcionais:
# dokku config:set --no-restart $APP_NAME FACEBOOK_PAGES="$FACEBOOK_PAGES"
# dokku config:set --no-restart $APP_NAME FACEBOOK_PPP="$FACEBOOK_PPP"
# dokku config:set --no-restart $APP_NAME CROWDTANGLE_POSTS_COUNT="$CROWDTANGLE_POSTS_COUNT"
# dokku config:set --no-restart $APP_NAME CROWDTANGLE_POSTS_INTERVAL="$CROWDTANGLE_POSTS_INTERVAL"
```

Com o app criado e configurado, agora precisamos fazer o primeiro deployment,
para então finalizar a configuração com a criação do certificado SSL via Let's
Encrypt (precisa ser feito nessa ordem).

Em sua **máquina local**, vá até a pasta do repositório e execute:

```shell
# Troque <server-ip> pelo IP do servidor e <app-name> pelo valor colocado na
# variável $APP_NAME definida no servidor
# ATENÇÃO: execute esses comandos fora do servidor (em sua máquina local)
git remote add dokku dokku@<server-ip>:<app-name>
git checkout main
git push dokku main
```

Para finalizar as configurações iniciais, conecte novamente no servidor e
execute:

```shell
dokku letsencrypt:enable $APP_NAME
dokku checks:disable $APP_NAME
dokku ps:scale $APP_NAME web=4
dokku ps:scale $APP_NAME worker=1
```

Aplicação instalada e rodando! Para criar um superusuário no Django:

```shell
dokku run $APP_NAME python manage.py createsuperuser
```

## Instalação do MinIO (storage)

Você precisará de um servidor com [Dokku](https://dokku.com/) e
[dokku-letsencrypt](https://github.com/dokku/dokku-letsencrypt) instalados.

No servidor, crie o app e as configurações iniciais:

```shell
export APP_NAME="storage-metamemo"
export APP_DOMAIN="storage.metamemo.info"
export DATA_PATH="/mnt/storage/storage-metamemo"
export ADMIN_MAIL="metamemo@metamemo.info"

dokku apps:create $APP_NAME
dokku config:set --no-restart $APP_NAME MINIO_ROOT_USER=$(echo `openssl rand -base64 45` | tr -d \=+ | cut -c 1-32)
dokku config:set --no-restart $APP_NAME MINIO_ROOT_PASSWORD=$(echo `openssl rand -base64 45` | tr -d \=+ | cut -c 1-32)
dokku config:set --no-restart $APP_NAME NGINX_MAX_REQUEST_BODY=50M
dokku config:set --no-restart $APP_NAME MINIO_DOMAIN=$APP_DOMAIN
dokku config:set --no-restart $APP_NAME DOKKU_LETSENCRYPT_EMAIL=$ADMIN_MAIL

mkdir -p $DATA_PATH
chown 32769:32769 $DATA_PATH
dokku storage:mount $APP_NAME ${DATA_PATH}:/home/dokku/data

dokku domains:set $APP_NAME $APP_DOMAIN
dokku proxy:ports-add $APP_NAME http:80:9000
dokku proxy:ports-add $APP_NAME https:443:9000
dokku proxy:ports-add $APP_NAME https:9001:9001
dokku proxy:ports-remove $APP_NAME http:80:5000
```

Em sua máquina local, faça o deployment da aplicação:

```shell
git clone https://github.com/turicas/minio-dokku.git
cd minio-dokku
git checkout develop
git remote add dokku dokku@storage.metamemo.info:storage-metamemo
git push dokku main
```

Termine a configuração do certificado SSL no servidor:

```shell
dokku letsencrypt:enable $APP_NAME
```
