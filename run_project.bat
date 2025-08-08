@echo off
echo 🚀 Bluehawks Security Services
echo ==========================================

cd /d "%~dp0"

if not exist "backend" (
    echo ❌ Error: backend directory not found!
    pause
    exit /b 1
)

if not exist "myenv" (
    echo ❌ Error: Virtual environment not found!
    pause
    exit /b 1
)

echo 📦 Activating virtual environment...
call myenv\Scripts\activate.bat

echo ✅ Virtual environment activated!
echo 🌐 Starting Django development server...
echo 📱 Server will be available at: http://127.0.0.1:8000
echo 🔧 Admin panel: http://127.0.0.1:8000/admin
echo.
echo ==========================================
echo Press Ctrl+C to stop the server
echo ==========================================

cd backend
python manage.py runserver

echo.
echo 🛑 Server stopped
pause
