# Projeto-Empreendedor: Bora_la: app de eventos

## Introdução

Este é um guia para instalar e executar o projeto Bora_la localmente usando Docker e Docker Compose.
O projeto será construído com Django, mas não é necessário instalar o framework localmente na máquina, vamos ter tudo dentro do container da aplicação, e no container do banco de dados.

## O que é o Docker e Docker Compose?

Docker é uma plataforma que permite desenvolver, implantar e executar aplicativos em contêineres. Contêineres são ambientes isolados que empacotam um aplicativo com todas as dependências necessárias. O Docker Compose é uma ferramenta para definir e executar aplicativos multi-container usando arquivos de configuração YAML, no nosso caso, usamos ele para subir conjuntamente a aplicação e o banco de dados.

## Instalação do Docker

### Linux/Windows

Siga as instruções no site oficial do Docker para o seu respectivo SO: [Docker Installation](https://docs.docker.com/get-docker/). Nos links úteis tem artigos e guias que vão ajudar no processo!

## Instalação do Docker Compose

O Docker Compose normalmente já está incluído na instalação do Docker Desktop para Windows e macOS. Para sistemas Linux, siga as instruções no site oficial: [Docker Compose Installation](https://docs.docker.com/compose/install/).

## Instalação do Plugin Docker para Visual Studio Code

Uma ferramente legal para lidar com container é um plugin direto no VScode, principalmente se voce trabalhar com linux. No windows, o docker desktop tem uma interface que facilita o uso. Procure o plugin "Docker" da Microsoft,após a instalação, você verá um ícone de Docker na barra lateral esquerda do VS Code.

# Desenvolvimento local
## Dependências e Requisitos
Antes de subir o projeto Bora_la, certifique-se de que seu ambiente de desenvolvimento atende aos seguintes requisitos:

- Docker e Docker Compose: Instalados e configurados

As dependencias do projeto são instaladas no container a partir da configuração do Dockerfile.

## Subindo o Projeto Bora_la

1. Clone este repositório do projeto:
   ```bash
   git clone <URL do Repositório>

2. Crie um novo arquivo '.env' na raiz do projeto. Copie os dados do '.env.sample'.

3. Construa e execute os contêineres usando o Docker Compose com a opção -d para executar em segundo plano e liberar o terminal. Para isso, abra o terminal dentro da pasta do projeto que vc acabou de clonar e rode:

    ```bash
    docker-compose build
    docker-compose up -d
    P.S: dependendo da versão, pode ser sem o hifen: 'docker compose up -d'
    ```

4. Vamos precisar agora criar o banco do nosso app. Entre no shell do container "postgres:12.1" e rode os comandos

    ```
    psql -U postgres
    CREATE USER postgres WITH ENCRYPTED PASSWORD 'postgres';
    CREATE DATABASE db_bora_la;
    GRANT ALL PRIVILEGES ON DATABASE db_bora_la TO postgres;
    c
     \l
    ```

5. Agora que o banco foi criado, de um reestart no container do projeto "projeto-empreendedor-bora_la" para que ele consiga se conectar ao banco.

6. Abra o shell do container do projeto e rode os comandos:

    ```
    python manage.py makemigrations
    python manage.py migrate

    python manage.py createsuperuser --username=admin --email=admin@example.com
    use a senha padrao "admin" e digite "y" no bypass de segurança
    Por fim, inicie o servidor:
    python manage.py runserver 0.0.0.0:8000
    ```

6. Se tudo estiver certo, o projeto estará disponível em http://localhost:8000/ .
Se der erro, tente restartar ambos os containers.
Para a area admin, lembre-se de usar o user admin com a senha admin que vc recem criou. 


### Comandos úteis do Docker

1. Para ver os logs do container, utilize o seguinte comando ou o plugin do docker:

    ```bash
    docker-compose logs bora_la

    ```

2. Para parar os contêineres, use o comando:

    ```bash
    docker-compose down -v

    ```

3. Para entrar no shell do container, use o seguinte comando:

    ```bash
    docker-compose exec bora_la sh

    ```
### Links úteis Docker:

[Comandos básicos](https://stack.desenvolvedor.expert/appendix/docker/comandos.html)

[Guia para iniciantes](https://dev.to/ingresse/docker-e-docker-compose-um-guia-para-iniciantes-48k8)

### Links úteis Django:

[Documentação oficial](https://docs.djangoproject.com/pt-br/4.2/)

[Tutorial da Documentação-é bem bom](https://docs.djangoproject.com/pt-br/4.1/intro/tutorial01/)

[Tutorial básico:criando um blog](https://www.devmedia.com.br/como-criar-um-blog-com-django-e-python/33710)

[Principais comandos django](https://www.treinaweb.com.br/blog/principais-comandos-do-django-cli)

[MDN Web Docs](https://developer.mozilla.org/pt-BR/docs/Learn/Server-side/Django)
## Boas práticas, qualidade e padrão de código.

> Atenção! Para manter a qualidade do codigo, siga esses passos antes de subir suas alterações pro repositório: 
1. rode o black
2. rode os testes
3. commit usando Conventional Commits

### Padrão de commits
O Conventional Commits é um padrão para mensagens de commit que facilita a leitura e a geração automática de changelogs. Cada mensagem de commit deve seguir o seguinte formato:

`<tipo>`: `<descrição>`

O `<tipo>` pode ser um dos seguintes:

- **feat**: para novas funcionalidades
- **fix**: para correção de bugs
- **docs**: para alterações na documentação
- **style**: para alterações que não afetam o código (espaços em branco, formatação, etc)
- **refactor**: para refatoração de código
- **test**: para adicionar ou modificar testes
- **chore**: para alterações em tarefas de manutenção

A `<descrição>` deve ser clara e concisa, descrevendo o que a alteração faz e deve ser menor que 70 caracteres. Veja os exemplos:

    feat: Adicionar autenticação de usuários
    fix: Corrigir erro de digitação no formulário de login
    docs: Atualizar README com instruções de instalação
    style: aplica correcoes black
    chore: Atualizar dependências do projeto
    refactor: Dividir função grande em funções menores

### Black 

 É uma ferramenta que formata automaticamente o código Python seguindo um conjunto consistente de regras de estilo (customizado no arquivo pyproject.toml). Isso ajuda a manter um código bem formatado e de fácil leitura.**É altamente recomendado executar o Black antes de fazer o commit do código**. Para usar o Black, execute algum dos comandos no terminal do container:

        black nome_do_arquivo.py  # formata o código do arquivo especificado
        black . # formata todo o repositório
