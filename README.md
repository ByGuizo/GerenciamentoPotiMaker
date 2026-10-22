# PotiMaker

Sistema de gestão do FabLab do IFRN Campus Canguaretama: inventário, projetos e
atividades, escala de horários do laboratório e cadastro de membros com aprovação do
coordenador.

Trabalho de Conclusão de Curso de Guizo.

## Como rodar

Precisa ter instalado: **Python 3.12 ou mais novo** e **Git**.

Os comandos abaixo são para o terminal do Windows (PowerShell ou Prompt de Comando).
No Linux/macOS, veja a observação de cada passo.

### 1. Baixar o projeto

```bash
git clone https://github.com/ByGuizo/GerenciamentoPotiMaker.git
cd GerenciamentoPotiMaker
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate
```

- Linux/macOS: `python3 -m venv venv` e `source venv/bin/activate`.
- Se o PowerShell disser que a execução de scripts está desabilitada, rode
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e tente de novo (ou use o
  Prompt de Comando).

Com o ambiente ativado, o terminal mostra `(venv)` no começo da linha. **Todos os
próximos comandos precisam dele ativado.**

### 3. Instalar o Django

```bash
pip install -r requirements.txt
```

### 4. Criar o arquivo `.env`

O sistema não inicia sem uma chave secreta. Este comando cria o `.env` com o modo de
desenvolvimento ligado e uma chave aleatória:

```bash
python -c "import secrets; open('.env', 'w').write('DJANGO_DEBUG=True\nDJANGO_SECRET_KEY=' + secrets.token_urlsafe(50) + '\n')"
```

### 5. Criar o banco de dados

```bash
python manage.py migrate
```

### 6. Criar o coordenador

```bash
python manage.py createsuperuser
```

Ele pede usuário, matrícula e senha (a senha não aparece enquanto você digita).

### 7. Rodar

```bash
python manage.py runserver
```

Abra **http://127.0.0.1:8000** no navegador e entre com o coordenador criado no passo 6.
Para parar o servidor: `Ctrl + C`.

## Da próxima vez

Basta entrar na pasta, ativar o ambiente e rodar:

```bash
venv\Scripts\activate
python manage.py runserver
```

## Erros comuns

| Mensagem | Solução |
|---|---|
| `Defina a variável DJANGO_SECRET_KEY no arquivo .env` | Faltou o passo 4 (ou o comando foi rodado fora da pasta do projeto). |
| `No module named 'django'` | O ambiente virtual não está ativado (passo 2) ou faltou o passo 3. |
| `python` não é reconhecido | No Windows, use `py` no lugar de `python`. No Linux/macOS, use `python3`. |
| `no such table` | Faltou o passo 5. |

## Colocar no servidor

Para implantar em produção (HTTPS, nginx, backup), veja `docs/IMPLANTACAO.md`.
