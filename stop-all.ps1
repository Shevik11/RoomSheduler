Param(
    [string]$ResourceGroup = "myResourceGroup",
    [string]$BackendName = "backend-container",
    [string]$FrontendName = "frontend-container",
    [string]$RedisName = "redis-container",
    [string]$DbName = "roomscheduler-db"
)

Write-Host "Stopping Azure resources in resource group '$ResourceGroup'..." -ForegroundColor Cyan

# Ensure Azure CLI is logged in
try { az account show 1>$null 2>$null } catch { az login | Out-Null }

# Stop containers (ACI)
Write-Host "Stopping containers..." -ForegroundColor Yellow
az container stop --resource-group $ResourceGroup --name $FrontendName 2>$null | Out-Null
az container stop --resource-group $ResourceGroup --name $BackendName 2>$null | Out-Null
az container stop --resource-group $ResourceGroup --name $RedisName   2>$null | Out-Null

# Stop PostgreSQL Flexible Server (saves most cost)
Write-Host "Stopping PostgreSQL Flexible Server '$DbName'..." -ForegroundColor Yellow
az postgres flexible-server stop --resource-group $ResourceGroup --name $DbName 2>$null | Out-Null

Write-Host "Requested stop for containers and database. Current states:" -ForegroundColor Green
try {
  $b = az container show --resource-group $ResourceGroup --name $BackendName   --query "instanceView.state" -o tsv 2>$null
  $f = az container show --resource-group $ResourceGroup --name $FrontendName  --query "instanceView.state" -o tsv 2>$null
  $r = az container show --resource-group $ResourceGroup --name $RedisName     --query "instanceView.state" -o tsv 2>$null
  $d = az postgres flexible-server show --resource-group $ResourceGroup --name $DbName --query "state" -o tsv 2>$null
  Write-Host ("Backend:  {0}" -f ($b | ForEach-Object {$_}))
  Write-Host ("Frontend: {0}" -f ($f | ForEach-Object {$_}))
  Write-Host ("Redis:    {0}" -f ($r | ForEach-Object {$_}))
  Write-Host ("DB:       {0}" -f ($d | ForEach-Object {$_}))
} catch {}

Write-Host "Done." -ForegroundColor Cyan

# PowerShell script для зупинки всіх контейнерів
Write-Host "🛑 Stopping all containers..." -ForegroundColor Yellow
docker-compose down

Write-Host "🧹 Cleaning up..." -ForegroundColor Yellow
docker system prune -f

Write-Host "✅ All containers stopped and cleaned up!" -ForegroundColor Green
