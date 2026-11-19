# Integración del laboratorio 5 en este proyecto

El kit del profesor se adaptó al proyecto Python, JavaScript y PostgreSQL, sin cambiar de lenguaje.

1. La rama de trabajo es security/lab-fsi y los cambios se revisan en https://github.com/JuanMurciay/Lab-03-FDSI/pull/1.
2. Semgrep y Gitleaks están en .github/workflows/seguridad-estatica.yml. Ese workflow también ejecuta la regresión y Dependency Review en PR.
3. CodeQL usa .github/workflows/codeql.yml, con Python y JavaScript. No activar Default setup a la vez que este workflow.
4. Dependabot alerts y secret scanning nativos están habilitados. .github/dependabot.yml configura actualizaciones semanales de pip y Actions; deben llegar a main para comenzar el calendario.
5. Se usó .github/workflows/dast-local.yml porque no se proporcionó staging HTTPS. Compara el commit original y el corregido con Docker y localhost. No modificarlo para escanear un dominio ajeno.
6. El workflow dast-staging.yml del kit queda como alternativa opcional. No se ejecutó. Su configuración inicial no bloquea por todos los fallos, así que el estado verde por sí solo tampoco sirve como evidencia.
7. Para Docker Compose, copiar .env.example a .env y definir dos valores locales diferentes y largos: POSTGRES_PASSWORD y LAB_API_TOKEN. No publicar .env. Ejecutar docker compose up --build y usar el token en el campo de la interfaz.
8. Para el lanzador local de Windows, definir LAB_API_TOKEN en el entorno de la misma terminal antes de ejecutar INICIAR.cmd. Si falta, las consultas siguen disponibles pero la escritura responde 503.
9. Regresión: python -m unittest discover -s tests -v. Las pruebas HTTP completas con PostgreSQL y los reportes ZAP se encuentran en el workflow DAST.
10. El informe está en docs/SECURITY.md, el detalle en docs/REPORTE_HALLAZGOS.md y los resultados en evidence/lab5.

No hace falta configurar una credencial real de CrowdStrike ni un token de Semgrep. Los valores de la ejecución automática son efímeros y no se entregan en los reportes.
