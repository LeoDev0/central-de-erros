# Central de Erros - Projeto Final AceleraDev Python 2020

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/LeoDev0/central-de-erros/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/LeoDev0/central-de-erros.svg?branch=master)](https://travis-ci.org/LeoDev0/central-de-erros)

Projeto final da aceleração de Back End com Python da [Codenation](https://github.com/codenation-dev) em parceria com a [Stone Payments](https://github.com/stone-payments). Se trata de uma API REST para gerenciamento e centralização de erros e você pode testá-la [aqui](https://errors-logger.herokuapp.com/) com as credenciais "admin@email.com" e senha "admin" para visualizar todos os endpoints.


## Tabela de Conteúdos

- [Objetivo](#Objetivo)
- [Tecnologias Utilizadas](#Tecnologias-Utilizadas)
- [Instalação e Uso](#Instalação-e-Uso)
- [Modelagem](#Modelagem)
- [Endpoints](#Endpoints)
- [Licença](#Licença)


## Objetivo

Em projetos modernos é cada vez mais comum o uso de arquiteturas baseadas em serviços ou microsserviços. Nestes ambientes complexos, erros podem surgir em diferentes camadas da aplicação (backend, frontend, mobile, desktop) e mesmo em serviços distintos. Desta forma, é muito importante que os desenvolvedores possam centralizar todos os registros de erros em um local, de onde podem monitorar e tomar decisões mais acertadas. Neste projeto vamos implementar um sistema para centralizar registros de erros de aplicações.

A arquitetura do projeto é formada por:

- Criar endpoints para serem usados pelo frontend da aplicação;
- Criar um endpoint que será usado para gravar os logs de erro em um banco de dados relacional;
- A API deve ser segura, permitindo acesso apenas com um token de autenticação válido.


## Tecnologias Utilizadas

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [JWT (JSON Web Token)](https://en.wikipedia.org/wiki/JSON_Web_Token)
- Bancos de dados relacionais ([SQLite](https://sqlite.org/index.html) localmente e [PostgreSQL](https://www.postgresql.org/) no deploy pelo [Heroku](https://www.heroku.com/))
- [Docker](https://www.docker.com/)
- [TDD (Test Driven Development)](https://en.wikipedia.org/wiki/Test-driven_development)
- [Travis-CI](https://travis-ci.org/)
- Documentação com [Swagger](https://errors-logger.herokuapp.com/api/swagger/) e [Redoc](https://errors-logger.herokuapp.com/api/redoc/)


## Instalação e Uso

### Clonando o repositório:

```bash
$ git clone https://github.com/LeoDev0/central-de-erros.git
```

### Instalação e execução automatizadas com Docker:

```bash
$ cd central-de-erros
$ docker-compose up
```

A aplicação estará rodando em ```http://localhost:8000/``` e você será redirecionado para a documentação local dos endpoints da API.

### Executando os testes da API (32 testes unitários):

```bash
$ cd central-de-erros
$ docker-compose run app sh -c "python manage.py test"
```


## Modelagem

Representação das tabelas do banco de dados usadas na aplicação.   

![models](https://raw.githubusercontent.com/LeoDev0/leodev0/master/media/codenation_models.png)

## Endpoints

### /api/logs/

*É preciso estar autenticado para visualizar*

`Métodos: GET, POST`

- Lista todos os logs;
- Cria novo log.

### /api/logs/results

*É preciso estar autenticado para visualizar*

`Método: GET`

- Pesquisa por logs pelos campos 'description' e 'details' usando o parâmetro '?search='.

### /api/logs/{id}

*É preciso estar autenticado para visualizar*

`Métodos: GET, PUT, PATCH, DELETE`

- Lista detalhes de um log através do seu id;
- Edita completamente um log;
- Edita parcialmente um log;
- Deleta um log.

### /api/register/

`Método: POST`

- Registra um novo usuário.

### /api/token/

`Método: POST`

- Requisita os tokens de acesso e refresh, além dos dados cadastrais do usuário.

### /api/token/refresh/

`Método: POST`

- Atualiza e retorna o token de acesso do usuário.

### /api/users/

*É preciso estar autenticado como super usuário para visualizar*

`Método: GET`

- Lista todos os usuários.

### /api/users/{id}

*É preciso estar autenticado como super usuário para visualizar*

`Método: GET`

- Lista dados de um usuário pelo seu id.

### /api/swagger/

Documentação com Swagger.

### /api/redoc/

Documentação com Redoc.


## Licença

[MIT © Leonardo T. Fernandes](https://github.com/LeoDev0/central-de-erros/blob/master/LICENSE)
