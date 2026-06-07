@echo off
REM ============================================
REM InstaVideo Studio - Instalador Automático
REM Windows PowerShell/CMD
REM ============================================

setlocal enabledelayedexpansion

echo.
echo ================================
echo  InstaVideo Studio Installer
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não está instalado ou não está no PATH
    echo Baixe em: https://www.python.org/downloads/
    echo Certifique-se de marcar "Add Python to PATH" durante instalação
    pause
    exit /b 1
)

REM Get the repository directory
cd /d "%~dp0"
set REPO_DIR=%cd%

echo [1/7] Verificando diretório...
if exist "Ciber" (
    echo [AVISO] Pasta 'Ciber' já existe
    set /p CLEANUP="Deseja remover a pasta existente? (S/N): "
    if /i "!CLEANUP!"=="S" (
        echo Removendo pasta existente...
        rmdir /s /q Ciber
    ) else (
        echo Usando pasta existente
        cd Ciber
        set REPO_DIR=!cd!
    )
)

if not exist "Ciber" (
    echo [2/7] Clonando repositório...
    git clone https://github.com/NinjaDeChinelo/Ciber.git
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao clonar repositório
        pause
        exit /b 1
    )
    cd Ciber
    set REPO_DIR=!cd!
) else (
    cd Ciber
    set REPO_DIR=!cd!
    echo [2/7] Usando repositório existente
)

echo [3/7] Criando ambiente virtual...
if exist "venv" (
    echo Ambiente virtual já existe
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao criar venv
        pause
        exit /b 1
    )
)

echo [4/7] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao ativar venv
    pause
    exit /b 1
)

REM Update pip
echo [5/7] Atualizando pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [AVISO] Erro ao atualizar pip, continuando...
)

echo [6/7] Instalando dependências...
if not exist "requirements.txt" (
    echo [ERRO] requirements.txt não encontrado em !REPO_DIR!
    pause
    exit /b 1
)

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependências
    pause
    exit /b 1
)

echo [7/7] Configurando banco de dados...
python scripts/setup_database.py
if %errorlevel% neq 0 (
    echo [AVISO] Erro ao setup database, mas continuar...
)

echo.
echo ================================
echo  ✅ Instalação Concluída!
echo ================================
echo.
echo Próximas etapas:
echo.
echo 1. Abra 2 terminais (PowerShell/CMD):
echo.
echo Terminal 1 - Backend (API):
echo   cd !REPO_DIR!
echo   venv\Scripts\activate.bat
echo   cd backend
echo   python app.py
echo.
echo Terminal 2 - Frontend (UI):
echo   cd !REPO_DIR!
echo   venv\Scripts\activate.bat
echo   cd frontend
echo   python main.py
echo.
echo.
pause
