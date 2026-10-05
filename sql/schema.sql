CREATE TABLE IF NOT EXISTS temperature_readings (
    reading_id BIGINT PRIMARY KEY,
    device_id TEXT NOT NULL,
    room_id TEXT,
    noted_at TIMESTAMP NOT NULL,
    temperature NUMERIC(5, 2) NOT NULL,
    location TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_temperature_readings_noted_at
    ON temperature_readings (noted_at);

CREATE INDEX IF NOT EXISTS idx_temperature_readings_device
    ON temperature_readings (device_id);
