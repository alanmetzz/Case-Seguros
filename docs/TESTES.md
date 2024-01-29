
# Testes

## Testes unitários

Para este código, temos que criar os testes unitários para validações das nossas rotas rest

- /racas
- /raca/details
- /racas_by

Levando em consideração os cenários possíveis para a rota `/racas_by`, por suportar diferentes parametros.

Outras validações que podemos incluir é do consumo da API The Cat para carga inicial, lembrando que os testes sejam independentes e que não causem efeitos colaterais permanentes no banco (Apesar de estar sendo utilizado o SQLite3 neste cenário)

Podemos usar a biblioteca unittest para construir nossos testes unitários, um exemplo de teste para a rota /racas com validação de resposta 200 apenas:

```python
import unittest
from unittest.mock import patch
from app.routes import racas_routes

class TestRacasRoutes(unittest.TestCase):

    @patch('app.routes.request')
    def test_listar_racas(self, mock_request):
        mock_request.args.get.return_value = 1

        with racas_routes.app.test_request_context('/racas'):
            resposta = racas_routes.listar_racas()

        self.assertEqual(resposta.status_code, 200)
if __name__ == '__main__':
    unittest.main()
```

## Testes regressivos

Para os testes de regressão, devemos ter em mente a abrangência e cobertura dos testes para que as funcionalidades críticas sejam abordadas. Para isso devemos criar os cenários de teste.

Outro ponto importante será a definição destes testes na pipeline, fazendo com que toda nova implementação os testes sejam efetuados para detectar esses efeitos colaterais indesejados.

## Teste Integrado

[...]

## Teste de Performance

Para performance, podemos utilizar de ferramentas como K6 ou JMeter e configurar as requisições de rotas desejadas. Neste contexto foi gerado um script básico do K6 para gerar carga na API: [arquivo](./test-api-files/performance.js)

Para executar:

````shell
K6_PROMETHEUS_RW_SERVER_URL=http://localhost:9090/api/v1/write \
k6 run -o experimental-prometheus-rw --tag testid=<UNIC_ID> test-api-files/performance.js
````

Obs.: Alterar a tag `testid` para ID único, para assim diferenciar as execuções.

Obs.: Neste cenário, estou usando a feature de [Rw do Prometheus](https://k6.io/docs/results-output/real-time/prometheus-remote-write/) para enviar as métricas diretamente para o Prometheus e podermos validar, caso não tiver configurado o Prometheus localmente, executar somente o `k6 run` desta forma:

````shell
k6 run test-api-files/performance.js
````

# Teste de resiliência

Os testes de resiliencia consiste em introduzir falhas intencionais na sua arquitetura e garantir que o sistema se recupere da maneira mais adequada.

Podemos por exemplo usar o [Litmus](https://github.com/litmuschaos/litmus)(OpenSource) em ambientes Kubernetes para realizar experimentos variados de cenários na nossa aplicação.

Neste caso, como estamos utilizando no contexto do Docker, um tipo de experimento para validar o comportamento de resiliência da aplicação, é localmente inserir falha para o DNS do `api.thecatapi.com` e entender o comportamento da nossa aplicação durante o inicio dela, assim estamos "quebrando" a comunicação da aplicação com um endpoint externo necessário durante a inicialização.
