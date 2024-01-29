# Case seguros

Aplicação para trazer informações de gatos baseados na API The Cat API.

## Estrutura do diretório

Diretório | Descrição | O que contém
--- | --- | ---
/docs | Documentações relacionadas ao projeto | Arquivos md para documentação
/infra | Criação da infraestrutura | Arquivos de configuração e docker-compose
/test-api-files | Testes relacionados a API |Arquivos relacionados a testes externos (Performance, Consumo de API)
/src | Source da aplicação | Código fonte da aplicação

## Documentação do projeto

- [Como subir local](./docs/START.md)
- [Aplicação](./docs/APP.md)
- [Infraestrutura](./docs/INFRA.md)
- [Observabilidade](./docs/OBSERVABILITY.md)
- [Testes](./docs/TESTES.md)

## Projeto construído baseado no desafio/case

Case The Cat API

1. Crie uma aplicação na linguagem que desejar para coletar as seguintes informações da [API
de Gatos](https://thecatapi.com/):

    - Para cada uma das raças de gatos disponíveis, armazenar as informações de
    origem, temperamento e descrição em uma base de dados. (se disponível)
    - Para cada uma das raças acima, salvar o endereço de 3 imagens em uma base de
    dados. (se disponível)
    - Salvar o endereço de 3 imagens de gatos com chapéu.
    - Salvar o endereço de 3 imagens de gatos com óculos.

2. Use uma base de dados para armazenar as informações (pode ser um banco de dados em
memória como H2 ou HSQLDB)

3. Utilizando a linguagem Java, crie 4 APIs REST:

    - API capaz de listar todas as raças
    - API capaz de listar as informações de uma raça
    - API capaz de a partir de um temperamento listar as raças
    - API capaz de a partir de uma origem listar as raças

4. As APIs acima deverão expor métricas de execução.

5. Crie uma coleção no postman ou insomnia para consumir as APIs criadas.

6. Utilizando uma ferramenta de logging (exemplos: Elastic Search, Splunk, Graylog ou
similar), crie uma query que mostre em tempo real os eventos que acontecem na
execução da API criada no item 6, exemplos (Warning, Erro, Debug, Info, etc).

7. Utilizando uma ferramenta de métricas (exemplos: Prometheus, Zabbix, cloudwatch ou
similar), crie 3 dashboards que mostre em tempo real a quantidade de execução, a latência
(tempo de execução) e quantidade de erros da API criada acima.

8. Utilize técnicas ou descreva formas de aplicar os temas qualidade e teste na sua
aplicação (teste unitário, teste regressivo, teste integrado, teste de performance, teste de
resiliência etc)

9. Publique o projeto no Github e documentar em um README.md os itens abaixo:

    - Documentação do projeto
    - Documentação das APIs
    - Documentação de arquitetura
    - Documentação de como podemos subir uma cópia deste ambiente localmente
    - Manual com prints dos Logs (item 6) e os 3 Dashboards (item 7).
