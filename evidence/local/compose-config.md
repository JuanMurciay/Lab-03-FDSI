# Validación estática de Compose

Codex ejecutó el 23-09-2026, en Windows local:

```powershell
$env:POSTGRES_PASSWORD='VALIDACION_LOCAL_NO_USAR'
docker compose -f compose.yaml config --quiet
$LASTEXITCODE
Remove-Item Env:POSTGRES_PASSWORD
```

Resultado: código **0**. Docker avisó que no podía leer su archivo de
configuración del usuario. El daemon no estaba activo, por lo que **no se
inició Nginx ni se verificó el contenedor**. El valor mostrado es solo un
marcador de validación de sintaxis, no una credencial de despliegue.
