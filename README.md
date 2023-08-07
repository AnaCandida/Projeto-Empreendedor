# Projeto-Empreendedor


## Desenvolvimento local

### Python

Certifique-se de ter o Python3 instalado em sua máquina.

### Venv

Usamos ambientes virtuais do python para  isolar as dependências do projeto . Isso permite que diferentes projetos tenham suas próprias bibliotecas e evita conflitos entre versões.Veja a[documentação](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) para mais detalhes.  

Primeiro você deve criar o ambiente e depois ativá-lo.

```
python3 -m venv env | py -m venv env  #criar um ambiente com nome 'env'
env\Scripts\Activate  # ativar Windows
source env/bin/activate #ativar linux
deactivate # desativa o ambiente virtual
```
### Requirements

Depois de ativar o ambiente virtual, instale as dependências do projeto. No ambiente de desenvolvimento, contamos com as bibliotecas de formatação de código, por isso também é necessário um segundo conjunto de dependências. Para instalar todas as dependências, utilize os seguintes comandos:

```
pip install -r requirements.txt  # instala as dependências do projeto
pip install -r requirements.dev.txt  # instala as dependências de desenvolvimento

```

### Rodando o servidor Django

> **Atenção:** Antes de rodar o servidor Django localmente, é necessário configurar o arquivo `.env` com as variáveis de ambiente corretas.

Para rodar o servidor Django, certifique-se de estar no diretório raiz do projeto (onde o arquivo manage.py está localizado). Use o seguinte comando para iniciar o servidor:

```
python manage.py runserver
```

Isso iniciará o servidor de desenvolvimento do Django e você poderá acessar o aplicativo em http://localhost:8000/ em seu navegador.





### Banco de dados

Para configurar o banco de dados localmente usando o PostgreSQL, você pode seguir os seguintes passos:

1. Instale o PostgreSQL em sua máquina. Você pode baixar o instalador apropriado para o seu sistema operacional em: https://www.postgresql.org/download/

2. Após a instalação, certifique-se de que o serviço do PostgreSQL esteja em execução.

3. No arquivo .env do seu projeto, preencha as informações sensíveis do banco de dados, como nome do banco de dados (DB_NAME), usuário do banco de dados (DB_USER), senha do usuário (DB_PASSWORD), host (DB_HOST) e porta (DB_PORT).

4. Crie um banco de dados no PostgreSQL com o mesmo nome que você definiu em DB_NAME no arquivo .env.

5. Crie e execute as migrações para criar as tabelas do Django no banco de dados:
```
python manage.py makemigrations
python manage.py migrate

```


Pode tbm rodar o banco  postgress usando docker

```
docker run --name db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres

```

## Boas práticas, qualidade e padrão de código.

> Atenção! Para manter a qualidade do codigo, siga esses passos antes de subir suas alterações pro repositório: 
1. rode o black
2. rode o flake8
3. rode os testes
4. commit usando Conventional Commits

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
    ```
    feat: Adicionar autenticação de usuários
    fix: Corrigir erro de digitação no formulário de login
    docs: Atualizar README com instruções de instalação
    style: aplica correcoes black
    chore: Atualizar dependências do projeto
    refactor: Dividir função grande em funções menores

    ```

### Black + Flake8

O Black e o Flake8 são ferramentas de formatação e linting de código em Python, usadas juntas para melhorar a qualidade do código e a experiência de desenvolvimento. Primeiro, você pode executar o Black para formatar o código e garantir a consistência. Em seguida, pode usar o Flake8 para verificar se o código está seguindo as convenções recomendadas e identificar quaisquer problemas adicionais que não sejam abordados pelo Black.

 - **Black**:  é uma ferramenta que formata automaticamente o código Python seguindo um conjunto consistente de regras de estilo (customizado no arquivo pyproject.toml). Isso ajuda a manter um código bem formatado e de fácil leitura.**É altamente recomendado executar o Black antes de fazer o commit do código**. Para usar o Black, execute o seguinte comando:

        ```
        black nome_do_arquivo.py  # formata o código do arquivo especificado
        black . # formata todo o repositório
        ```


  - **Flake**: O Flake8 é uma ferramenta de linting que verifica o código em busca de problemas, erros ou más práticas. Ele analisa o código em busca de possíveis erros de sintaxe, uso inadequado de variáveis, entre outros problemas. Para usar o Flake8, execute o seguinte comando:

        ```
            flake8 nome_do_arquivo.py  # verifica o código do arquivo especificado
            flake8  # verifica todo o projeto
        ```