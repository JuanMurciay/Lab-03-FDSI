# Riesgos iniciales — Falcon simulado

Hipótesis de diseño, pendientes de comprobar con evidencias reales del laboratorio.

| Riesgo | Tratamiento previsto | Estado |
|---|---|---|
| Alertas y hostnames visibles por HTTP | Datos ficticios y alcance limitado ahora; HTTPS en Lab 4 | Pendiente |
| Consulta y enumeración sin autenticación | Documentar exposición; identidad y roles en Lab 4 | Pendiente |
| Ingreso de alertas falsas y falta de integridad HTTP | Validación básica de campos ya en código; autenticación y TLS en Lab 4 | Pendiente de validar |
| Trazabilidad insuficiente | Registro básico UTC; correlacionar con access.log de Nginx | Pendiente de validar |
| Logs consultables y configuraciones inseguras | Revisar exposición y endurecimiento en la fase Blue Team | Pendiente |

El registro de solicitudes no identifica usuarios y puede alterarse en disco. Las alertas
no persisten al reiniciar. Son limitaciones explícitas del prototipo inicial.
