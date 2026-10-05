CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    device_id,
    ROUND(AVG(temperature), 2) AS avg_temp,
    COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY device_id
ORDER BY device_id;

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM noted_at)::INT AS hora,
    COUNT(*) AS contagem,
    ROUND(AVG(temperature), 2) AS temperatura_media
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM noted_at)
ORDER BY hora;

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    noted_at::DATE AS data,
    MAX(temperature) AS temp_max,
    MIN(temperature) AS temp_min,
    ROUND(AVG(temperature), 2) AS temp_media
FROM temperature_readings
GROUP BY noted_at::DATE
ORDER BY data;

CREATE OR REPLACE VIEW resumo_por_ambiente AS
SELECT
    location,
    COUNT(*) AS total_leituras,
    ROUND(AVG(temperature), 2) AS temperatura_media,
    MIN(temperature) AS menor_temperatura,
    MAX(temperature) AS maior_temperatura
FROM temperature_readings
GROUP BY location
ORDER BY location;
