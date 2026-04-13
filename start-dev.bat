@echo off
echo.
echo Starting CrypToCare Development Servers...
echo.

echo Starting Django Backend on http://localhost:8001...
start cmd /k "cd backend && venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8001"

timeout /t 2 /nobreak >nul

echo Starting Quasar Frontend on http://localhost:9000...
start cmd /k "pnpm dev"

echo.
echo Both servers are starting!
echo.
echo Frontend: http://localhost:9000
echo Backend:  http://localhost:8000
echo Admin:    http://localhost:8000/admin
echo.
pause
