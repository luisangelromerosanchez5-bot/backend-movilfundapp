-- ==============================================================================
-- Esquema de Base de Datos FundAPP (Fundación Biosferas)
-- Compatible con Supabase (PostgreSQL 15+)
-- Compartido entre Plataforma Web y Aplicación Móvil
-- ==============================================================================

-- 1. EXTENSIONES
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. TABLA: USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE,
    telefono VARCHAR(20),
    rol VARCHAR(50) DEFAULT 'voluntario', -- 'voluntario', 'coordinador', 'admin'
    foto_url TEXT,
    meta_anual_horas INTEGER DEFAULT 20,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. TABLA: ACTIVIDADES AMBIENTALES
CREATE TABLE IF NOT EXISTS actividades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    categoria VARCHAR(100) NOT NULL, -- 'Reforestación', 'Reciclaje', 'Conservación', 'Educación'
    fecha DATE NOT NULL,
    hora VARCHAR(50) NOT NULL,
    duracion_horas INTEGER NOT NULL DEFAULT 2,
    cupos_totales INTEGER NOT NULL DEFAULT 20,
    cupos_ocupados INTEGER NOT NULL DEFAULT 0,
    estado_cupos VARCHAR(20) DEFAULT 'disponible', -- 'disponible', 'lleno'
    ubicacion_nombre VARCHAR(255) NOT NULL,
    latitud NUMERIC(9,6) NOT NULL,
    longitud NUMERIC(9,6) NOT NULL,
    radio_permitido_metros INTEGER NOT NULL DEFAULT 100,
    puntos_impacto INTEGER DEFAULT 100,
    tags TEXT[] DEFAULT '{}',
    imagen_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. TABLA: POSTULACIONES
CREATE TABLE IF NOT EXISTS postulaciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actividad_id UUID NOT NULL REFERENCES actividades(id) ON DELETE CASCADE,
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    estado VARCHAR(50) DEFAULT 'aprobada', -- 'pendiente', 'aprobada', 'cancelada'
    notas TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(actividad_id, usuario_id)
);

-- 5. TABLA: ASISTENCIAS (GPS Geofencing y Podómetro)
CREATE TABLE IF NOT EXISTS asistencias (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    postulacion_id UUID REFERENCES postulaciones(id) ON DELETE SET NULL,
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    actividad_id UUID NOT NULL REFERENCES actividades(id) ON DELETE CASCADE,
    lat_registrada NUMERIC(9,6) NOT NULL,
    lng_registrada NUMERIC(9,6) NOT NULL,
    distancia_metros INTEGER NOT NULL,
    precision_gps VARCHAR(50) NOT NULL DEFAULT 'Alta',
    check_in_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    check_out_at TIMESTAMPTZ,
    pasos_sesion INTEGER DEFAULT 0,
    distancia_km NUMERIC(5,2) DEFAULT 0.0,
    calorias INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. TABLA: DONACIONES
CREATE TABLE IF NOT EXISTS donaciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    monto NUMERIC(12,2) NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL, -- 'creditCard', 'pse', 'nequiDaviplata'
    estado VARCHAR(50) DEFAULT 'completada', -- 'completada', 'pendiente', 'fallida'
    codigo_transaccion VARCHAR(100) UNIQUE NOT NULL,
    proyecto_destino VARCHAR(255) DEFAULT 'Fondo General de Conservación',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. TABLA: CERTIFICADOS
CREATE TABLE IF NOT EXISTS certificados (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    actividad_id UUID REFERENCES actividades(id) ON DELETE SET NULL,
    donacion_id UUID REFERENCES donaciones(id) ON DELETE SET NULL,
    tipo VARCHAR(50) NOT NULL, -- 'voluntariado', 'donacion'
    titulo VARCHAR(200) NOT NULL,
    actividad_titulo VARCHAR(255) NOT NULL,
    horas INTEGER,
    monto NUMERIC(12,2),
    fecha_emision DATE NOT NULL DEFAULT CURRENT_DATE,
    estado VARCHAR(50) DEFAULT 'aprobado', -- 'aprobado', 'en_proceso'
    codigo_verificacion VARCHAR(100) UNIQUE NOT NULL,
    firmado_por VARCHAR(255) NOT NULL DEFAULT 'Dra. Elena Ramos - Directora Ejecutiva',
    destinatario VARCHAR(255) NOT NULL,
    documento_identidad VARCHAR(50) NOT NULL DEFAULT '1.098.765.432',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. ÍNDICES DE RENDIMIENTO
CREATE INDEX IF NOT EXISTS idx_actividades_fecha ON actividades(fecha);
CREATE INDEX IF NOT EXISTS idx_postulaciones_usuario ON postulaciones(usuario_id);
CREATE INDEX IF NOT EXISTS idx_asistencias_usuario ON asistencias(usuario_id);
CREATE INDEX IF NOT EXISTS idx_certificados_usuario ON certificados(usuario_id);
CREATE INDEX IF NOT EXISTS idx_donaciones_usuario ON donaciones(usuario_id);
