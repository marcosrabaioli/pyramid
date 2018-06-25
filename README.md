Desafio Geru
====

Instruções Básicas
---------------

- Para rodar o projeto crie um ambiente virtual

    python3 -m venv env

- Instale as  dependências, incluindo as dependencias de teste

    env/bin/pip install -e ".[testing]"

- Rode o script de inicialização do banco de dados

    env/bin/initialize_geru_db development.ini

- Para rodar os testes execute

    env/bin/pytest

- Para rodar a api, execute

    env/bin/pserve development.ini

Estrutura do projeto
---------------
.

├── geru

│   ├── models

│   ├── scripts

│   ├── static

│   ├── templates

│   ├── views

│   └── wrapper

└── geru.egg-info

- **models**: Classes dos modelos que são utilizados no banco de dados
- **scripts**: Sripts de inicialização do banco de dados
- **static**: arquivos estáticos da aplicação
- **templates**: contém os temlates .jinja2 das páginas da aplicação
- **views**: contém todas as views da aplicação
- **wrapper**: diretório que contém os arquivos da aplicação que consome a api de quotes
- **geru.egg-info**: informações do projeto como requirements e etc

Frameworks Utilizados
---------------
**Pyramid**: framework para aplicações web
**SQLAlchemy**: ORM para manipulação dos dados do banco de dados (sqlite)
**Unittest**: biblioteca para testes
**Jinja2**: para linguagem de templates
**Outros**: localizados em geru.egg-info/requirements.txt

End Points
---------------
- **/** -> home
- get **/quotes** -> lista todas as quotes
- get **/quotes/{pk}** -> lista determinado quote
- get **/quotes/random** -> lista um quote aleatório
- get **/requests** -> lista todas as requisições feitas

Mecanismo de registro de seção
---------------

Foi criado um mecanismo de registro de seção que gera um userid único do tipo uuid para qualquer seção, esse userid não expira enquanto a seção não for reiniciada pelo servidor (aplicação reiniciar) ou o browser ser fechado.
Cada requisição feita é resgistrada no banco de dados. É guardado o id da seção, a url da requisição e o timestamp em que aconteceu.
