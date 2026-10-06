# Pipeline de Dados com IoT e Docker

Projeto desenvolvido para a disciplina **Disruptive Architectures: IoT, Big Data e IA**. Ele processa leituras reais de temperatura de dispositivos IoT, armazena os dados em PostgreSQL com Docker e disponibiliza indicadores em um dashboard Streamlit.

## Estrutura

```text
.
├── data/
│   └── sample_temperature_readings.csv
├── docs/
│   └── screenshots/
├── sql/
│   ├── schema.sql
│   └── views.sql
├── src/
│   ├── config.py
│   └── ingest.py
├── dashboard.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Tecnologias

- Python 3.12.10, versao validada no projeto.
- PostgreSQL 16 via Docker.
- Pandas para tratamento do CSV.
- SQLAlchemy e psycopg2-binary para conexao com o banco.
- Streamlit e Plotly para dashboard.

## Dataset Oficial

O projeto utiliza como fonte principal o dataset **Temperature Readings: IoT Devices**, disponivel no Kaggle:

https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices

O arquivo esperado pelo pipeline e:

```text
data/IOT-temp.csv
```

Como o arquivo oficial nao deve ser enviado ao GitHub, `data/IOT-temp.csv` esta protegido pelo `.gitignore`. Para reproduzir o projeto, baixe o dataset no Kaggle, extraia somente o arquivo `IOT-temp.csv` e coloque-o dentro da pasta `data/`.

O CSV oficial possui:

- 97.606 registros originais.
- 1 `reading_id` duplicado.
- 97.605 registros unicos apos deduplicacao.
- Temperaturas entre 21 °C e 51 °C.
- Temperatura media de 35,053860 °C.
- Periodo de 28/07/2018 07:06 ate 08/12/2018 09:30.
- 20.345 leituras `In`.
- 77.260 leituras `Out`.
- 1 room/dispositivo normalizado como `room_admin`.

O projeto tambem mantem `data/sample_temperature_readings.csv` apenas como amostra pequena de referencia estrutural. A base principal do projeto final e o arquivo oficial `IOT-temp.csv`.

## Configuracao do Ambiente Python

No Windows, crie o ambiente virtual com Python 3.12:

```powershell
py -3.12 -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Confirme a versao:

```powershell
python --version
```

Instale as dependencias:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copie o arquivo de exemplo de variaveis de ambiente:

```powershell
copy .env.example .env
```

Configure o arquivo `.env` para usar o dataset oficial:

```env
DATA_FILE=data/IOT-temp.csv
```

Nao envie o arquivo `.env` para o GitHub. Ele esta protegido pelo `.gitignore`.

## PostgreSQL com Docker

Suba o banco:

```powershell
docker compose up -d
```

Valide o container:

```powershell
docker compose ps
```

O esperado e que o container `postgres-iot` esteja `Up` e com health `healthy`, publicando a porta `5432`.

## Ingestao dos Dados

Execute a ingestao oficial:

```powershell
python -m src.ingest
```

Com `DATA_FILE=data/IOT-temp.csv`, a saida esperada e:

```text
97605 leituras carregadas no PostgreSQL com sucesso.
```

Antes da insercao, o script valida e normaliza o CSV. O pipeline remove registros invalidos, preserva `reading_id` como texto, remove duplicados por `reading_id` e so substitui a tabela se houver dados normalizados validos.

## Validacao no PostgreSQL

Para confirmar a carga oficial:

```powershell
docker exec postgres-iot psql -U iot_user -d iot_db -c "SELECT COUNT(*) AS total_registros, COUNT(DISTINCT reading_id) AS ids_unicos, MIN(temperature) AS temp_min, MAX(temperature) AS temp_max, ROUND(AVG(temperature), 6) AS temp_media, MIN(noted_at) AS primeira_leitura, MAX(noted_at) AS ultima_leitura FROM temperature_readings;"
```

Resultado validado no projeto:

- total de registros: 97.605
- IDs unicos: 97.605
- temperatura minima: 21 °C
- temperatura maxima: 51 °C
- temperatura media: 35,053860 °C
- primeira leitura: 2018-07-28 07:06:00
- ultima leitura: 2018-12-08 09:30:00

## Schema

A tabela principal e `temperature_readings`, definida em `sql/schema.sql`:

- `reading_id TEXT PRIMARY KEY`: identificador unico da leitura.
- `device_id TEXT NOT NULL`: identificador normalizado a partir do room.
- `room_id TEXT`: room original do dataset.
- `noted_at TIMESTAMP NOT NULL`: data e hora da leitura.
- `temperature NUMERIC(5, 2) NOT NULL`: temperatura registrada.
- `location TEXT NOT NULL`: ambiente da leitura (`In` ou `Out`).
- `created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP`: data de insercao no banco.

## Views Analiticas

As views estao em `sql/views.sql`:

- `avg_temp_por_dispositivo`: calcula a temperatura media e o total de leituras por dispositivo.
- `leituras_por_hora`: agrupa as leituras por hora do dia e calcula a temperatura media por hora.
- `temp_max_min_por_dia`: mostra temperatura maxima, minima e media por data.
- `resumo_por_ambiente`: resume quantidade, media, minima e maxima por ambiente `In` e `Out`.

Todas as quatro views foram validadas com o dataset oficial carregado no PostgreSQL.

## Dashboard Streamlit

Execute o dashboard:

```powershell
streamlit run dashboard.py
```

O dashboard validado com o dataset oficial apresenta:

- 97.605 leituras.
- 1 dispositivo/room.
- temperatura media geral de aproximadamente 35,1 °C.
- grafico de media de temperatura por dispositivo.
- grafico de leituras por hora do dia.
- grafico de temperaturas maximas, minimas e medias por dia.
- tabela de resumo por ambiente:
  - `In`: 20.345 leituras, media 30,45 °C.
  - `Out`: 77.260 leituras, media 36,27 °C.

## Insights dos Dados

- As leituras externas sao maioria no dataset oficial.
- A media de temperatura `Out` e superior a media `In`.
- As temperaturas variam de 21 °C a 51 °C.
- Apos a remocao de 1 duplicado, existem 97.605 leituras validas.
- O dataset possui apenas um room/dispositivo identificado como `room_admin`.

## Documentacao e Evidencias

As evidencias visuais atualizadas estao em `docs/screenshots/`:

- `01-docker-postgres-healthy.png`: Docker/PostgreSQL em execucao.
- `02-postgresql-97605-registros.png`: validacao SQL com 97.605 registros e estatisticas oficiais.
- `03-dashboard-visao-geral.png`: visao geral do dashboard com 97.605 leituras.
- `04-dashboard-leituras-por-hora.png`: grafico de leituras por hora.
- `05-dashboard-temperaturas-por-dia.png`: grafico de temperaturas por dia.
- `06-dashboard-resumo-ambiente.png`: resumo por ambiente `In` e `Out`.

## Seguranca e Arquivos Ignorados

O `.gitignore` protege arquivos locais e sensiveis:

- `.env`: credenciais e configuracoes locais.
- `.venv/`: ambiente virtual Python.
- `.streamlit/secrets.toml`: segredos locais do Streamlit.
- `data/IOT-temp.csv`: dataset oficial baixado do Kaggle.
- `data/*.sqlite`: bases locais auxiliares, se existirem.

Assim, nenhum segredo local nem o arquivo grande do dataset oficial devem ser enviados ao repositorio.
