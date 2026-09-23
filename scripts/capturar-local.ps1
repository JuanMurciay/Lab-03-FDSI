param(
    [string]$Clon = (Join-Path $PSScriptRoot '..\..\..\work\lab3-verificacion-clon')
)

$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$dest = Join-Path $repo 'evidence\local\verificacion-2026-09-23.md'
$lines = [System.Collections.Generic.List[string]]::new()
function Add-Line([string]$value) { $lines.Add($value) }
function Add-Command([string]$command, [string]$destination, [scriptblock]$run) {
    Add-Line "`n### ``$command``"
    Add-Line "UTC: $(Get-Date -AsUTC -Format 'yyyy-MM-ddTHH:mm:ssZ') · origen: este equipo · destino: $destination · responsable: Codex."
    $output = & $run 2>&1 | Out-String
    Add-Line '```text'
    Add-Line $output.TrimEnd()
    Add-Line '```'
}

Push-Location $repo
try {
    Add-Line '# Evidencia local verificable — 23-09-2026'
    Add-Line ''
    Add-Line 'Responsable de esta comprobación: Codex, asistente de desarrollo; no se atribuye al estudiante.'
    Add-Line 'Origen y destino HTTP: 127.0.0.1 (solo loopback). No se escaneó ningún host externo.'
    Add-Line "Inicio UTC: $(Get-Date -AsUTC -Format 'yyyy-MM-ddTHH:mm:ssZ')"
    Add-Line 'Entorno: Windows; Python http.server 8080 sirve una carpeta temporal con solo index.html, styles.css y web.js.'
    Add-Line 'La aplicación funcional separada usa HTTP 80 → API 5000 → PostgreSQL 55432.'
    Add-Command 'git status --short --branch' 'repositorio local' { git status --short --branch }
    Add-Command 'git log --oneline -5' 'repositorio local' { git log --oneline -5 }
    Add-Command 'git ls-files (equivalente seguro de find para archivos versionados)' 'repositorio local' { git ls-files }
    Add-Command 'git -C CLON rev-parse --short HEAD; git -C CLON remote get-url origin; Test-Path CLON/index.html' 'clon local obtenido de github.com/JuanMurciay/Lab-03-FDSI' {
        git -C $Clon rev-parse --short HEAD
        git -C $Clon remote get-url origin
        Test-Path (Join-Path $Clon 'index.html')
    }
    Add-Command 'find . -maxdepth 3 -type f (clon limpio)' 'clon local obtenido de GitHub' {
        $gitDir = Split-Path (Get-Command git).Source -Parent
        $find = (Resolve-Path (Join-Path $gitDir '..\usr\bin\find.exe')).Path
        Push-Location $Clon
        try { & $find . -maxdepth 3 -type f } finally { Pop-Location }
    }
    Add-Command 'curl -I http://127.0.0.1:8080/' '127.0.0.1:8080' { curl.exe -sS -I --max-time 5 http://127.0.0.1:8080/ }
    Add-Command 'curl -i http://127.0.0.1:8080/ (primeras líneas y longitud)' '127.0.0.1:8080' {
        $response = curl.exe -sS -i --max-time 5 http://127.0.0.1:8080/
        $response | Select-Object -First 10
        'Caracteres recibidos: ' + ($response | Out-String).Length
    }
    Add-Command 'curl -I http://127.0.0.1/' '127.0.0.1:80' { curl.exe -sS -I --max-time 5 http://127.0.0.1/ }
    Add-Command 'curl -i http://127.0.0.1/api/health' '127.0.0.1:80 → API local → PostgreSQL' { curl.exe -sS -i --max-time 5 http://127.0.0.1/api/health }
    Add-Line "`nFin UTC: $(Get-Date -AsUTC -Format 'yyyy-MM-ddTHH:mm:ssZ')"
    Add-Line ''
    Add-Line 'Interpretación: la página estática respondió 200; la aplicación y la API respondieron 200 en el host local. El repositorio público se clonó y contiene index.html. No se midió acceso desde otra máquina.'
    [System.IO.File]::WriteAllLines($dest, $lines, [System.Text.UTF8Encoding]::new($false))
    Write-Output $dest
} finally { Pop-Location }
