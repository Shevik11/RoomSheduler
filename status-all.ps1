Param(
    [string]$ResourceGroup = "myResourceGroup",
    [string]$BackendName = "backend-container",
    [string]$FrontendName = "frontend-container",
    [string]$RedisName = "redis-container",
    [string]$DbName = "roomscheduler-db"
)

Write-Host "Fetching statuses in resource group '$ResourceGroup'..." -ForegroundColor Cyan

# Ensure Azure CLI is logged in
try { az account show 1>$null 2>$null } catch { az login | Out-Null }

function Get-ContainerStatus {
  Param([string]$name)
  $state = az container show --resource-group $ResourceGroup --name $name --query "instanceView.state" -o tsv 2>$null
  $cstate = az container show --resource-group $ResourceGroup --name $name --query "containers[0].instanceView.currentState.state" -o tsv 2>$null
  $detail = az container show --resource-group $ResourceGroup --name $name --query "containers[0].instanceView.currentState.detailStatus" -o tsv 2>$null
  $ip = az container show --resource-group $ResourceGroup --name $name --query "ipAddress.ip" -o tsv 2>$null
  $fqdn = az container show --resource-group $ResourceGroup --name $name --query "ipAddress.fqdn" -o tsv 2>$null
  [PSCustomObject]@{ Name=$name; State=$state; Current=$cstate; Detail=$detail; IP=$ip; FQDN=$fqdn }
}

$backend  = Get-ContainerStatus -name $BackendName
$frontend = Get-ContainerStatus -name $FrontendName
$redis    = Get-ContainerStatus -name $RedisName

$dbState = az postgres flexible-server show --resource-group $ResourceGroup --name $DbName --query "state" -o tsv 2>$null

Write-Host "\nContainers:" -ForegroundColor Yellow
$backend  | Format-Table -AutoSize
$frontend | Format-Table -AutoSize
$redis    | Format-Table -AutoSize

Write-Host "\nDatabase:" -ForegroundColor Yellow
Write-Host ("{0}: {1}" -f $DbName, ($dbState | ForEach-Object {$_}))

Write-Host "\nDone." -ForegroundColor Cyan


