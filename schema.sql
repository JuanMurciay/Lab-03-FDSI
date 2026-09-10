CREATE TABLE IF NOT EXISTS alertas (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    hostname VARCHAR(100) NOT NULL,
    severidad VARCHAR(10) NOT NULL CHECK (severidad IN ('baja','media','alta','critica')),
    descripcion TEXT NOT NULL DEFAULT '',
    fuente TEXT NOT NULL DEFAULT 'CrowdStrike Falcon - SIMULADO',
    estado VARCHAR(15) NOT NULL DEFAULT 'nueva' CHECK (estado IN ('nueva','escalada','cerrada')),
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS acciones (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    alerta_id BIGINT NOT NULL REFERENCES alertas(id),
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('recibir','clasificar','enriquecer','escalar','cerrar')),
    nota TEXT NOT NULL DEFAULT '',
    actor TEXT NOT NULL DEFAULT 'anonimo',
    request_id UUID NOT NULL,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS solicitudes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    request_id UUID NOT NULL,
    origen TEXT NOT NULL,
    metodo VARCHAR(10) NOT NULL,
    ruta VARCHAR(500) NOT NULL,
    codigo INTEGER NOT NULL,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS solicitudes_deteccion ON solicitudes (origen, creado_en) WHERE codigo=404;
