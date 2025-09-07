# PowerShell script для зупинки всіх контейнерів
Write-Host "🛑 Stopping all containers..." -ForegroundColor Yellow
docker-compose down

Write-Host "🧹 Cleaning up..." -ForegroundColor Yellow
docker system prune -f

Write-Host "✅ All containers stopped and cleaned up!" -ForegroundColor Green
