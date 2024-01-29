# Infraestrutura

Neste cenário, utilizamos alguns recursos, com o Docker Swarm, são eles:

- Aplicação
- Grafana
- Promtail
- Loki
- Prometheus
- Node Exporter
- Cadivisor

![Arquitetura](images/Case.png)

## Aplicação

A aplicação está sendo iniciada com somente uma réplica e volume montado para que seja mantido a nossa database local do SQLite3.

O volume montado é no caminho:

````yaml
    volumes:
    - app-data:/app/app/database/files
````

As variáveis de ambiente disponíveis são:

Env | Descrição
--- | ---
TIMEOUT | Refere ao timeout das requisições do Flask. Default: 5.0
THECATAPI_API_KEY | API Key para consumo dos dados da The Cat API. Default: null
LOG_LEVEL | Log level que será utilizado/ Default: INFO
INITIAL_FLOW_CATS | Inicia a aplicação com o consumo da API The Cats para salvar informações no banco. Valores: 'TRUE'ou 'FALSE'. Default: 'FALSE'
INITIAL_FLOW_HATS_CATS | Inicia a aplicação com o consumo da API The Cats para salvar imagens de gatos com Chapéu e Óculos no banco. Valores: 'TRUE'ou 'FALSE'. Default: 'FALSE'

## Observabilidade

### Loki e Promtail

Optado por utilizar o Loki como datasource de logs pela facilidade e integração local. Para utilizaçõa local, não é necessário muitos ajustes, apenas apontar todos os serviços para se conectar localmente (Uma única instância, então deve inicializar com `127.0.0.1`).

````yaml
      -config.file=/etc/loki/local-config.yaml
      -boltdb.shipper.compactor.ring.instance-addr=127.0.0.1
      -distributor.ring.instance-addr=127.0.0.1
      -frontend.instance-addr=127.0.0.1
      -index-gateway.ring.instance-addr=127.0.0.1
      -ingester.lifecycler.addr=127.0.0.1
      -query-scheduler.ring.instance-addr=127.0.0.1
      -ruler.ring.instance-addr=127.0.0.1
````

Para o promtail, é necessário se atentar para que seja montado o volume o socket do docker:

````yaml
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
````

As configurações estão localizadas em `../infra/configs/loki/promtail-config.yaml`, basicamente utilizando a coleta do `docker_sd_configs` filtrando pelos containers que tenham a label `logging=promtail`. [Ref.](https://grafana.com/docs/loki/latest/send-data/promtail/configuration/#docker_sd_configs)

Se atentar então para que os containers que deseja que seja coletado os logs, iniciem com a label:  `logging=promtail` existente.

Também está sendo utilizada a label service_name para gerar a label `service` nos logs, e ajudar na agregação de logs de diferentes containers mas do mesmo serviço.

### Grafana

Para o grafana, a infra utilizada é básica, e o login está ativo com o default(admin/admin).
Também está sendo montado as datasources do Prometheus e do Loki na subida do container, junto com todas as dashboards.

Para que seja montado, é necessário adicionar em volume:

````yaml
    volumes:
      - ./configs/grafana/datasources.yml:/etc/grafana/provisioning/datasources/provisioning-datasources.yaml:ro
      - ./configs/grafana/dashboards.yml:/etc/grafana/provisioning/dashboards/main.yaml
      - ./configs/grafana/dashboards:/var/lib/grafana/dashboards
````

Onde as configs estão localizadas em `../infra/configs/grafana`.
Para adicionar novas dashboards defaults, pode ser adicionado o `.json` no caminho `../infra/configs/grafana/dashboards`

### Prometheus e Exporters

Para o prometheus, iniciado em modo padrão e com Feature `remote-write-receiver` para receber métricas do K6.

Atentar-se aos volumes montados das configurações:

````yaml
    volumes:
      - ./configs/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./configs/prometheus/recording-rules.yml:/etc/prometheus/recording-rules.yml
      - ./configs/prometheus/alerting-rules.yml:/etc/prometheus/alerting-rules.yml
````

As configurações estão localizadas em `../infra/configs/prometheus`
A configuração de scrape utilizada foi a [`static_configs`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config) apontando os serviços e portas manualmente. (Possível ajuste é utilizar o `dockerswarm_sd_configs` para discovery automático.)

Também utilizamos a `recording-rules` para criação de records de querys.
Um padrão do Node Exporter: `prometheus_node_exporter_rules` e o restante relacionado ao [Sloth](OBSERVABILITY.md#slosli).

Não foi criado alertas, mas para ser criado, é somente adicionar ao `alerting-rules.yml` seguindo os padrões do [AlertManager](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/).
