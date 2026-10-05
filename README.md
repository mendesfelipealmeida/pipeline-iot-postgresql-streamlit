# Pipeline de Dados com IoT e Docker

Projeto desenvolvido para a disciplina **Disruptive Architectures: IoT, Big Data e IA**. Ele processa leituras de temperatura de dispositivos IoT, armazena os dados em PostgreSQL com Docker e disponibiliza um dashboard em Streamlit.

## Estrutura

```text
.
├── data/
│   └── sample_temperature_readings.csv
├── docs/
│   ├── relatorio.md
│   ├── roteiro-video.md
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

## Dataset

O dataset solicitado e **Temperature Readings: IoT Devices**, disponivel no Kaggle:

https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices

Para testes rapidos, o projeto inclui `data/sample_temperature_readings.csv`. Se usar o CSV oficial do Kaggle, coloque o arquivo em `data/IOT-temp.csv` e ajuste `DATA_FILE` no arquivo `.env`.

## Configuracao do ambiente Python

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

## Ingestao dos dados

Execute a ingestao:

```powershell
python -m src.ingest
```

Com o CSV de exemplo, a saida esperada e:

```text
18 leituras carregadas no PostgreSQL com sucesso.
```

Os dados sao carregados na tabela `temperature_readings`. Antes da insercao, o script recria a estrutura SQL necessaria e limpa a tabela para manter a execucao reprodutivel.

## Validacao opcional no PostgreSQL

Para confirmar a quantidade de registros com uma consulta somente leitura:

```powershell
docker exec postgres-iot psql -U iot_user -d iot_db -c "SELECT COUNT(*) AS total_registros FROM temperature_readings;"
```

Com o CSV de exemplo, o resultado esperado e `18`.

## Dashboard Streamlit

Execute o dashboard:

```powershell
streamlit run dashboard.py
```

O dashboard apresenta:

- total de leituras;
- quantidade de dispositivos;
- temperatura media geral;
- media de temperatura por dispositivo;
- leituras por hora do dia;
- temperaturas maximas, minimas e medias por dia;
- resumo por ambiente interno e externo.

## Banco, tabela e views

A tabela principal e `temperature_readings`, definida em `sql/schema.sql`.

As views analiticas estao em `sql/views.sql`:

- `avg_temp_por_dispositivo`: media de temperatura e total de leituras por dispositivo.
- `leituras_por_hora`: quantidade de leituras e temperatura media por hora do dia.
- `temp_max_min_por_dia`: temperatura maxima, minima e media por data.
- `resumo_por_ambiente`: estatisticas por ambiente interno ou externo.

## Documentacao e evidencias

- Relatorio final: `docs/relatorio.md`
- Roteiro do video pitch: `docs/roteiro-video.md`
- Evidencias visuais: `docs/screenshots/`

As evidencias incluem validacao do Docker/PostgreSQL, consulta com 18 registros e telas do dashboard Streamlit.
