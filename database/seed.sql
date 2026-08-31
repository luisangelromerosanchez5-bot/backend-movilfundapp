-- ==============================================================================
-- Datos Iniciales (Seed Data) para Fundación Biosferas
-- ==============================================================================

-- Usuario de prueba (password: 123456)
INSERT INTO usuarios (id, nombres, apellidos, correo, password_hash, fecha_nacimiento, telefono, rol, meta_anual_horas)
VALUES (
    'a1010000-0000-0000-0000-000000000001',
    'Luis Fernando',
    'Pérez Gómez',
    'luis@correo.com',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', -- bcrypt hash de 123456
    '2001-05-02',
    '+57 312 456 7890',
    'voluntario',
    20
) ON CONFLICT (correo) DO NOTHING;

-- Actividades Ambientales
INSERT INTO actividades (id, titulo, descripcion, categoria, fecha, hora, duracion_horas, cupos_totales, cupos_ocupados, estado_cupos, ubicacion_nombre, latitud, longitud, radio_permitido_metros, puntos_impacto, tags, imagen_url)
VALUES 
(
    'b1010000-0000-0000-0000-000000000001',
    'Reforestación Río Bosque',
    'Jornada de siembra de especies nativas junto a la comunidad local. Se proveen herramientas y refrigerio. Tu aporte ayuda a proteger la cuenca hídrica.',
    'Reforestación',
    '2026-09-05',
    '08:00 AM',
    4,
    30,
    18,
    'disponible',
    'Vereda El Bosque, Cuenca Alta',
    4.711000,
    -74.072100,
    120,
    150,
    ARRAY['Siembra', 'Bosque', 'Comunidad'],
    'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=600'
),
(
    'b1010000-0000-0000-0000-000000000002',
    'Jornada de Reciclaje Urbano',
    'Separación y recolección de materiales reciclables en parques zonales para fomentar la economía circular con recicladores de oficio.',
    'Reciclaje',
    '2026-09-11',
    '09:00 AM',
    3,
    20,
    15,
    'disponible',
    'Parque Principal Simón Bolívar',
    4.658300,
    -74.093900,
    100,
    100,
    ARRAY['Reciclaje', 'Ciudad', 'CeroBasura'],
    'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=600'
),
(
    'b1010000-0000-0000-0000-000000000003',
    'Limpieza de Humedal Córdoba',
    'Recuperación ambiental del ecosistema acuático, retiro de residuos sólidos y censo básico de aves migratorias.',
    'Conservación',
    '2026-09-19',
    '07:30 AM',
    5,
    25,
    25,
    'lleno',
    'Humedal Córdoba, Entrada Norte',
    4.701200,
    -74.075400,
    150,
    200,
    ARRAY['Humedal', 'Aves', 'Conservación'],
    'https://images.unsplash.com/photo-1618477461853-cf6ed80faba5?w=600'
) ON CONFLICT DO NOTHING;
