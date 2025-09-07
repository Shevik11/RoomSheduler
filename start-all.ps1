Param(
    [string]$ResourceGroup = "myResourceGroup",
    [string]$BackendName = "backend-container",
    [string]$FrontendName = "frontend-container",
    [string]$RedisName = "redis-container",
    [string]$DbName = "roomscheduler-db",
    [string]$Location = "uksouth",
    [string]$AcrName = "roomscheduler"
)

Write-Host "Starting Azure resources in resource group '$ResourceGroup'..." -ForegroundColor Cyan

# Ensure Azure CLI is logged in
try { az account show 1>$null 2>$null } catch { az login | Out-Null }

# Start PostgreSQL first (it takes time to wake)
Write-Host "Starting PostgreSQL Flexible Server '$DbName'..." -ForegroundColor Yellow
az postgres flexible-server start --resource-group $ResourceGroup --name $DbName 2>$null | Out-Null

# Optional: wait until DB is 'Ready'
Write-Host "Waiting for DB to be Ready (timeout ~5 min)..." -ForegroundColor Yellow
$deadline = (Get-Date).AddMinutes(5)
do {
  Start-Sleep -Seconds 10
  $state = az postgres flexible-server show --resource-group $ResourceGroup --name $DbName --query "state" -o tsv 2>$null
  Write-Host "DB state: $state"
} while ($state -ne "Ready" -and (Get-Date) -lt $deadline)

# Start containers (ACI)
Write-Host "Starting containers..." -ForegroundColor Yellow
az container start --resource-group $ResourceGroup --name $RedisName   2>$null | Out-Null
az container start --resource-group $ResourceGroup --name $BackendName 2>$null | Out-Null
az container start --resource-group $ResourceGroup --name $FrontendName 2>$null | Out-Null

# Ensure ACR login (helps on image refresh)
Write-Host "Logging into ACR '$AcrName'..." -ForegroundColor Yellow
az acr login --name $AcrName 2>$null | Out-Null

# Show current public endpoints
Write-Host "Current public endpoints:" -ForegroundColor Green
try {
  $bIp = az container show --resource-group $ResourceGroup --name $BackendName  --query "ipAddress.fqdn" -o tsv 2>$null
  $fIp = az container show --resource-group $ResourceGroup --name $FrontendName --query "ipAddress.fqdn" -o tsv 2>$null
  Write-Host ("Backend:  http://{0}:8000" -f $bIp)
  Write-Host ("Frontend: http://{0}:8080" -f $fIp)
} catch {}

Write-Host "Done." -ForegroundColor Cyan


