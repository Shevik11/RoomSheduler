# PowerShell script для запуску production-like environment
Write-Host "🏭 Starting production-like environment..." -ForegroundColor Green

# Створюємо .env файл якщо не існує
if (!(Test-Path ".env")) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
}

# Зупиняємо поточні контейнери
Write-Host "🛑 Stopping current containers..." -ForegroundColor Yellow
docker-compose down

# Запускаємо оптимізовану версію
Write-Host "⚡ Starting with optimized production settings..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "✅ Production-like environment is running!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:8080" -ForegroundColor Blue
Write-Host "🔗 Backend: http://localhost:8000" -ForegroundColor Blue
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Blue
