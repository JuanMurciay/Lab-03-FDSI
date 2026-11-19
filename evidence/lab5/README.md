# Evidencia real del laboratorio 5

Estos archivos fueron descargados de GitHub Actions o resumen controles consultados en GitHub. No son capturas simuladas.

- Línea base: 6a1f8839c234bbe5f4258e9868808ac3996cda35.
- Código corregido: 19de2cd598f566b54620130512de2d90f900f25a.
- SAST, secretos y regresión: https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429539772.
- CodeQL: https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429539812.
- DAST y validación manual reproducible: https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429528875.
- PR: https://github.com/JuanMurciay/Lab-03-FDSI/pull/1.

Semgrep: 2 resultados antes y 2 después. ZAP frontend: 7 tipos de alerta antes y 6 después; se eliminó la alerta 10055. Las cuentas son tipos de alertas, no una puntuación de seguridad ni el número de fallas explotadas.

Las fechas de los artefactos están en UTC. El informe usa la fecha de Colombia. results.sarif corresponde a Gitleaks; codeql-resumen.json identifica la alerta de CodeQL sin copiar información sensible. Los valores del token y de PostgreSQL no se incluyen.
