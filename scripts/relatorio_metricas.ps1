# Uso: .\scripts\relatorio_metricas.ps1 -Milestone 1
# Gera relatorio de metricas de codigo para a milestone indicada.

param(
    [Parameter(Mandatory=$true)]
    [int]$Milestone
)

$pasta = "metricas\milestone_$Milestone"
New-Item -ItemType Directory -Force -Path $pasta | Out-Null

Write-Host "Gerando metricas para milestone $Milestone em '$pasta'..."

radon raw  apps/ -s      | Out-File "$pasta\raw.txt"      -Encoding utf8
radon cc   apps/ -s -a   | Out-File "$pasta\cc.txt"       -Encoding utf8
radon hal  apps/         | Out-File "$pasta\halstead.txt"  -Encoding utf8
radon mi   apps/ -s      | Out-File "$pasta\mi.txt"       -Encoding utf8
pylint     apps/         | Out-File "$pasta\pylint.txt"   -Encoding utf8

Write-Host "Pronto. Arquivos em '$pasta':"
Get-ChildItem $pasta | Select-Object Name
