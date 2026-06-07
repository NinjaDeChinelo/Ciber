# ============================================
# InstaVideo Studio - Instalador PowerShell
# Windows 10/11 (Recomendado)
# ============================================

param(
    [switch]$Force = $false,
    [string]$PythonVersion = "3.11"
)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "InstaVideo Studio - Installer" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# ============ Função: Verificar Python ============
function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Python não encontrado!" -ForegroundColor Red
        Write-Host "Baixe em: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "Certifique-se de marcar 'Add Python to PATH'" -ForegroundColor Yellow
        return $false
    }
}

# ============ Função: Verificar Git ============
function Test-Git {
    try {
        $gitVersion = git --version 2>&1
        Write-Host "✅ Git encontrado: $gitVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Git não encontrado!" -ForegroundColor Red
        Write-Host "Baixe em: https://git-scm.com/download/win" -ForegroundColor Yellow
        return $false
    }
}

# ============ Função: Clonar repositório ============
function Install-Repository {
    param([string]$Path)
    
    if (Test-Path "Ciber") {
        if ($Force) {
            Write-Host "🗑️  Removendo pasta 'Ciber' existente..." -ForegroundColor Yellow
            Remove-Item -Recurse -Force "Ciber"
        }
        else {
            $response = Read-Host "Pasta 'Ciber' já existe. Remover? (S/N)"
            if ($response -eq "S" -or $response -eq "s") {
                Remove-Item -Recurse -Force "Ciber"
            }
            else {
                Write-Host "Usando pasta existente" -ForegroundColor Yellow
                Set-Location "Ciber"
                return $true
            }
        }
    }
    
    Write-Host "[1/7] Clonando repositório..." -ForegroundColor Cyan
    git clone https://github.com/NinjaDeChinelo/Ciber.git
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Falha ao clonar repositório" -ForegroundColor Red
        return $false
    }
    
    Set-Location "Ciber"
    return $true
}

# ============ Função: Criar virtual env ============
function Install-VirtualEnv {
    Write-Host "[2/7] Criando ambiente virtual..." -ForegroundColor Cyan
    
    if (Test-Path "venv") {
        Write-Host "⚠️  Ambiente virtual já existe" -ForegroundColor Yellow
    }
    else {
        python -m venv venv
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Falha ao criar venv" -ForegroundColor Red
            return $false
        }
    }
    
    return $true
}

# ============ Função: Ativar virtual env ============
function Activate-VirtualEnv {
    Write-Host "[3/7] Ativando ambiente virtual..." -ForegroundColor Cyan
    
    & ".\venv\Scripts\Activate.ps1"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Falha ao ativar venv" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# ============ Função: Instalar dependências ============
function Install-Dependencies {
    Write-Host "[4/7] Atualizando pip..." -ForegroundColor Cyan
    python -m pip install --upgrade pip | Out-Null
    
    Write-Host "[5/7] Instalando dependências..." -ForegroundColor Cyan
    
    if (-not (Test-Path "requirements.txt")) {
        Write-Host "❌ requirements.txt não encontrado" -ForegroundColor Red
        return $false
    }
    
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Falha ao instalar dependências" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# ============ Função: Setup banco de dados ============
function Setup-Database {
    Write-Host "[6/7] Configurando banco de dados..." -ForegroundColor Cyan
    
    python scripts/setup_database.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Aviso ao configurar database" -ForegroundColor Yellow
    }
    
    return $true
}

# ============ Função: Criar atalhos ============
function Create-Shortcuts {
    Write-Host "[7/7] Criando atalhos..." -ForegroundColor Cyan
    
    # Desktop shortcut
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
    $ShortcutPath = "$DesktopPath\InstaVideo Studio.lnk"
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
        $Shortcut.TargetPath = "cmd.exe"
        $Shortcut.Arguments = "/k cd /d $PSScriptRoot && venv\Scripts\activate.bat && cd frontend && python main.py"
        $Shortcut.WorkingDirectory = $PSScriptRoot
        $Shortcut.Save()
        
        Write-Host "✅ Atalho criado na Desktop" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  Não foi possível criar atalho" -ForegroundColor Yellow
    }
}

# ============ Função: Exibir instruções finais ============
function Show-Instructions {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "  ✅ Instalação Concluída!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "📖 Próximas Etapas:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Abra 2 terminais (PowerShell):" -ForegroundColor White
    Write-Host ""
    
    Write-Host "Terminal 1 - Backend (API):" -ForegroundColor Yellow
    Write-Host "  cd $PSScriptRoot" -ForegroundColor Gray
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "  cd backend" -ForegroundColor Gray
    Write-Host "  python app.py" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "Terminal 2 - Frontend (UI):" -ForegroundColor Yellow
    Write-Host "  cd $PSScriptRoot" -ForegroundColor Gray
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "  cd frontend" -ForegroundColor Gray
    Write-Host "  python main.py" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "Documentação:" -ForegroundColor Cyan
    Write-Host "  📖 QUICKSTART.md - Guia rápido" -ForegroundColor Gray
    Write-Host "  📖 docs/USAGE_GUIDE.md - Guia completo" -ForegroundColor Gray
    Write-Host "  📖 docs/ARCHITECTURE.md - Arquitetura técnica" -ForegroundColor Gray
    Write-Host ""
}

# ============ MAIN ============
try {
    # Verificações iniciais
    if (-not (Test-Python)) { exit 1 }
    if (-not (Test-Git)) { exit 1 }
    
    # Execução
    if (-not (Install-Repository)) { exit 1 }
    if (-not (Install-VirtualEnv)) { exit 1 }
    if (-not (Activate-VirtualEnv)) { exit 1 }
    if (-not (Install-Dependencies)) { exit 1 }
    if (-not (Setup-Database)) { exit 1 }
    
    # Criar atalhos
    Create-Shortcuts
    
    # Instruções finais
    Show-Instructions
    
    Write-Host "🎉 Pronto para editar vídeos incríveis!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Erro durante instalação: $_" -ForegroundColor Red
    exit 1
}
