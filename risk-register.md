# Registro preliminar de riesgos

**Evaluación de diseño, sin hallazgos técnicos confirmados.** No se declara ningún
riesgo corregido, mitigado o aceptado antes de contar con evidencia y responsable.

| ID | Hipótesis | Riesgo previsto | Control o tratamiento propuesto | Estado inicial | Evidencia / responsable |
|---|---|---|---|---|---|
| R1 | H1 | Lectura de contenido HTTP en tránsito | Datos ficticios y red limitada en Lab 3; HTTPS en Lab 4 | Pendiente de validar; tratamiento definitivo en Lab 4 | PENDIENTE |
| R2 | H2 | Exposición de tecnología y contenido innecesario | Ocultar versión, reducir inventario y restringir rutas ocultas | Pendiente de validar y mitigar en Lab 3 | PENDIENTE |
| R3 | H3 | Trazabilidad insuficiente de solicitudes | Hora UTC, bitácora, logs y correlación | Pendiente de validar y mitigar en Lab 3 | PENDIENTE |
| R4 | H4 | Falta de integridad del transporte HTTP | TLS/HTTPS en Lab 4; sin prueba MITM en Lab 3 | Pendiente de validación documental; tratamiento en Lab 4 | PENDIENTE |

Tras el retest, registrar estado (corregido, mitigado, aceptado o pendiente para Lab 4),
evidencia, riesgo residual, responsable y justificación. La aceptación requiere una
decisión explícita del responsable; no se presume por dejar de probar.
