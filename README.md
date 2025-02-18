# ftc-product-service

Repositorio de microservico de pedidos e gerenciamento do produto para projeto do modulo 4 da fiap

# Tests

Resultado do coverage
![Coverage Result](/docs/image.png)
![Sonar Result](/docs/Screenshot%202025-02-18%20at%2012.35.25.png)

## Configuração do Ambiente

1. Instale [Poetry](https://python-poetry.org/docs/) para gerenciamento de dependências.
2. Clone o repositório e navegue até a pasta do projeto.
3. Crie e ative um ambiente virtual:

   ```shell
   poetry shell
   ```

4. Instale as dependências:

   ```shell
   poetry install
   ```

   Para instalar apenas as dependências de produção, use:

   ```shell
   poetry install --no-dev
   ```

## Execução do Projeto

Utilize o Makefile fornecido para executar o projeto. Certifique-se de ter o Make instalado em seu sistema.

1. Para compilar e executar o projeto:

   ```shell
   make start-up
   ```

2. Para limpar os arquivos gerados durante a compilação:

   ```shell
   make clean-up
   ```
