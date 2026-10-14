# Implantação do PotiMaker

Guia curto para colocar o sistema no servidor do campus (Linux com nginx e HTTPS).

## 1. Requisitos

- Python 3.12 ou mais novo, com `venv`.
- nginx com certificado HTTPS para o domínio do sistema.
- `sqlite3` (linha de comando) para o backup: `sudo apt install sqlite3`.

## 2. Instalação

```bash
sudo mkdir -p /srv/potimaker
sudo chown $USER /srv/potimaker
git clone https://github.com/ByGuizo/<repositorio>.git /srv/potimaker
cd /srv/potimaker
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

## 3. Configuração (`.env`)

Copie o exemplo e preencha:

```bash
cp .env.exemplo .env
venv/bin/python -c "import secrets; print(secrets.token_urlsafe(50))"
```

No `.env`:

| Variável | Valor |
|---|---|
| `DJANGO_DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | a chave gerada pelo comando acima |
| `DJANGO_ALLOWED_HOSTS` | o domínio, ex.: `potimaker.cang.ifrn.edu.br` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | o domínio com `https://` na frente |
| `DJANGO_HSTS_SECONDS` | `0` no começo; depois que o HTTPS estiver estável, `31536000` |

Sem `DJANGO_SECRET_KEY` o sistema não inicia (de propósito).

## 4. Banco, arquivos estáticos e coordenador

```bash
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic
venv/bin/python manage.py createsuperuser
venv/bin/python manage.py check --deploy
```

O `createsuperuser` cria o primeiro coordenador. O `check --deploy` deve mostrar só o
aviso de HSTS (enquanto `DJANGO_HSTS_SECONDS` for `0`).

## 5. Servidor da aplicação

Em produção o Django precisa de um servidor WSGI (o `runserver` é só para
desenvolvimento). O projeto não traz nenhum: a escolha fica com o NIC. O ponto de
entrada é `sistemapotimaker.wsgi:application`, e o servidor escolhido deve:

- escutar só em `127.0.0.1:8000` (o nginx fica na frente);
- rodar com **um único processo** (pode ter várias threads): o limite de tentativas de
  login fica guardado na memória do processo, então todos os acessos precisam passar
  pelo mesmo processo;
- rodar com um usuário que possa escrever no `db.sqlite3` e na pasta do projeto
  (ex.: `sudo chown -R www-data:www-data /srv/potimaker`);
- reiniciar sozinho se cair (ex.: como serviço do systemd).

## 6. nginx

```nginx
server {
    listen 80;
    server_name potimaker.cang.ifrn.edu.br;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name potimaker.cang.ifrn.edu.br;

    ssl_certificate     /caminho/do/certificado.pem;
    ssl_certificate_key /caminho/da/chave.pem;

    location /static/ {
        alias /srv/potimaker/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

O `X-Real-IP` é usado no limite de tentativas de login, e o `X-Forwarded-Proto` avisa ao
Django que o acesso veio por HTTPS. O servidor da aplicação escuta só em `127.0.0.1`,
então ninguém consegue falar com ele sem passar pelo nginx.

## 7. Backup diário

```bash
sudo mkdir -p /srv/potimaker/backups
sudo crontab -u www-data -e
```

Linha do cron (todo dia às 02:00):

```
0 2 * * * cd /srv/potimaker && sqlite3 db.sqlite3 ".backup backups/db_$(date +\%F).sqlite3"
```

## 8. Atualizar o sistema

```bash
cd /srv/potimaker
sqlite3 db.sqlite3 ".backup backups/antes_da_atualizacao.sqlite3"
git pull
venv/bin/pip install -r requirements.txt
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic --noinput
```

Depois, reinicie o servidor da aplicação.
