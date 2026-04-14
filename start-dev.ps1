# Run both Frontend and Backend servers

Write-Host "🚀 Starting CrypToCare Development Servers..." -ForegroundColor Green
Write-Host ""

# Start Django Backend
Write-Host "Starting Django Backend on http://localhost:8001..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; if (Test-Path '.\venv\Scripts\Activate.ps1') { .\venv\Scripts\Activate.ps1 }; python manage.py runserver 0.0.0.0:8001"

Start-Sleep -Seconds 2

# Start Quasar Frontend
Write-Host "Starting Quasar Frontend on http://localhost:9000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; pnpm dev"

Write-Host ""
Write-Host "✅ Both servers are starting!" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: http://localhost:9000" -ForegroundColor Yellow
Write-Host "Backend:  http://localhost:8001" -ForegroundColor Yellow
Write-Host "Admin:    http://localhost:8001/admin" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
