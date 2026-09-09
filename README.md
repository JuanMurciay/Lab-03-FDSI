# MuvAutomation Secure Product Challenge

## Laboratorio 3: entrega inicial

**Estado: preparación local. No desplegado ni evaluado en un servidor autorizado.**

Este repositorio inicia una aplicación estática por HTTP y sin autenticación para
el ejercicio académico Red Team + Blue Team. Su contenido es completamente ficticio.
La solución se conservará para los siguientes laboratorios.

| Dato | Valor |
|---|---|
| Integrante(s) | Juan Sebstian Murcia Yanquen |
| Asignatura / grupo | PENDIENTE de completar |
| Docente | PENDIENTE de completar |
| IP, URL y CIDR autorizados | PENDIENTES; ver docs/alcance.md |
| Ventana autorizada | PENDIENTE |
| Versión inicial | lab-3-inicial |
| Versión final lab-3 | PENDIENTE; no creada |

## Contenido

- [Resumen de entrega inicial](docs/entrega-inicial.md).
- [Alcance y responsabilidades](docs/alcance.md).
- [Procedimiento de preparación y despliegue](docs/procedimiento.md).
- [DFD](diagrams/dfd-lab3.png) y [explicación de límites de confianza](diagrams/README.md).
- [Hipótesis STRIDE](docs/stride.md).
- [Registro de riesgos](risk-register.md).
- [Bitácora y comparación](docs/bitacora.md).
- [Reflexión individual pendiente](docs/reflexion-individual.md).

```text
app/                         Sitio e inventario ficticio
nginx/                       Configuración inicial del virtual host
diagrams/                    DFD y explicación
docs/                        Alcance, procedimiento y documentación inicial
evidence/red/                Instrucciones para evidencias ofensivas pendientes
evidence/blue/               Instrucciones para evidencias defensivas pendientes
evidence/retest/             Instrucciones para comparación pendiente
reports/zap-passive/          Reporte ZAP pendiente
risk-register.md             Riesgos previstos, aún no validados
README.md                    Punto de entrada
```

## Arquitectura prevista

Kali / navegador → red autorizada → Ubuntu Server / Nginx (80/TCP) → archivos del sitio.
Blue Team observa el host mediante logs y capturas controladas.
HTTP se permitirá únicamente desde el CIDR autorizado. HTTPS y autenticación se
reservan para el laboratorio 4. El inventario no representa servicios desplegados:
los nombres WEB-LAB-01, API-LAB-01 y DB-LAB-01 son datos de demostración.

## Reproducción

Requisitos del entorno definitivo: Ubuntu Server LTS, sudo autorizado, Nginx,
Git y herramientas de prueba indicadas por la guía. No se requiere base de datos.

1. Completar y validar [el alcance](docs/alcance.md) con el docente.
2. Seguir [el procedimiento](docs/procedimiento.md) desde Ubuntu y Kali según el rol.
3. Conservar la línea base antes de aplicar hardening.
4. Obtener autorización del docente para las pruebas.
5. Ejecutar las fases Red, Blue, corrección y retest; completar sus evidencias.
6. Revisar los entregables finales y crear `lab-3` solo cuando estén completos.

Para una vista previa local con Python 3, desde la raíz del repositorio:

```bash
python -m http.server 8080 --bind 127.0.0.1 --directory app
```

Abrir http://127.0.0.1:8080 y detener con Ctrl+C. Esta vista previa no verifica Nginx,
el firewall ni el despliegue exigido por el laboratorio.

## Evidencias y trazabilidad

Las carpetas de evidencias contienen instrucciones, no resultados de pruebas.
Cada hallazgo deberá incluir hipótesis, comando/acción, hora UTC, origen, destino,
responsable, resultado real, interpretación, corrección y retest.
Los estados PENDIENTE no constituyen evidencias de logro.

No incluir secretos, datos reales ni tráfico ajeno. `.gitignore` excluye capturas
PCAP y logs crudos por defecto: conservar los originales controlados localmente y
entregar únicamente la evidencia revisada por el canal autorizado del curso.
Ver evidence/blue/README.md para incorporar un PCAP revisado cuando corresponda.

## Cierre requerido por la guía

- [ ] Sitio HTTP accesible desde el segmento permitido.
- [ ] Alcance y autorización documentados.
- [ ] Hipótesis contrastadas con Nmap, curl y ZAP pasivo.
- [ ] PCAP exclusivamente del ejercicio y al menos tres eventos correlacionados.
- [ ] Regla de cinco 404 por IP en cinco minutos evaluada.
- [ ] Hardening, reducción de contenido y comparación antes/después.
- [ ] Registro de riesgos actualizado.
- [ ] Reflexión individual de máximo 250 palabras.
- [ ] README reproducible y etiqueta final `lab-3`.

## Referencias

- Guía docente: Laboratorio_3_HTTP_Red_Blue_Team.pdf, 11 páginas, proporcionada por el estudiante.
- [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/).
- [Documentación Threat Dragon](https://www.threatdragon.com/docs/).
- [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/).

La guía es la fuente del alcance. Juice Shop y CrowdStrike Falcon no son requisitos
de la implementación mínima descrita en ella.
