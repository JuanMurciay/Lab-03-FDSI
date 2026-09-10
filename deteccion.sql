-- Ventana móvil: cinco o más respuestas 404 de una IP en los últimos cinco minutos.
-- Requiere ejecutar la consulta en PostgreSQL con acceso del defensor.
SELECT origen, count(*) AS errores_404, min(creado_en) AS primero, max(creado_en) AS ultimo
FROM solicitudes
WHERE codigo = 404 AND creado_en >= now() - interval '5 minutes'
GROUP BY origen
HAVING count(*) >= 5;
