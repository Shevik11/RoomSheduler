# PowerShell script для запуску development environment
Write-Host "🚀 Starting development environment..." -ForegroundColor Green

# Створюємо .env файл якщо не існує
if (!(Test-Path ".env")) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
}

# Запускаємо з development налаштуваннями
Write-Host "⚡ Starting with optimized development settings..." -ForegroundColor Cyan
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

Write-Host "✅ Development environment is running!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:8080" -ForegroundColor Blue
Write-Host "🔗 Backend: http://localhost:8000" -ForegroundColor Blue
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Blue
