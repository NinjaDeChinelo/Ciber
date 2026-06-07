# Build & Deployment Guide

## 🔨 Build para Produção

### Requisitos
- Python 3.11+
- Git
- PyInstaller (para gerar executável)
- Visual Studio Build Tools (para compilação nativa)

### 1. Preparar Ambiente de Build

```bash
# Clone o repositório
git clone https://github.com/NinjaDeChinelo/Ciber.git
cd Ciber

# Crie ambiente virtual de build
python -m venv venv_build
.\venv_build\Scripts\Activate.ps1

# Instale dependências incluindo dev
pip install -r requirements.txt
pip install pyinstaller>=6.0
```

### 2. Preparar Aplicação

```bash
# Execute testes
pytest tests/

# Otimize banco de dados
python scripts/setup_database.py

# Limpe cache
python scripts/clean_build.py
```

### 3. Gerar Executável

```bash
# Build backend como EXE
pyinstaller --onefile \
  --name "InstaVideoStudio_Backend" \
  --distpath ./dist \
  --workpath ./build \
  backend/app.py

# Build frontend como EXE
pyinstaller --onefile --windowed \
  --name "InstaVideoStudio" \
  --icon assets/icon.ico \
  --distpath ./dist \
  --workpath ./build \
  frontend/main.py

# Copie FFmpeg para dist
mkdir dist\ffmpeg
copy C:\ffmpeg\bin\ffmpeg.exe dist\ffmpeg\
copy C:\ffmpeg\bin\ffprobe.exe dist\ffmpeg\
```

### 4. Criar Installer

#### Usando NSIS:
```bash
# Crie script NSIS
makensis installer.nsi

# Resultado: InstaVideoStudio_Installer.exe
```

Arquivo `installer.nsi`:
```nsis
!include "MUI2.nsh"

Name "InstaVideo Studio"
OutFile "InstaVideoStudio_Installer.exe"
InstallDir "$PROGRAMFILES\InstaVideoStudio"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "PortugueseBR"

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "dist\*.*"
  CreateDirectory "$SMPROGRAMS\InstaVideoStudio"
  CreateShortcut "$SMPROGRAMS\InstaVideoStudio\InstaVideoStudio.lnk" "$INSTDIR\InstaVideoStudio.exe"
  CreateShortcut "$DESKTOP\InstaVideoStudio.lnk" "$INSTDIR\InstaVideoStudio.exe"
SectionEnd

Section "Uninstall"
  Delete "$SMPROGRAMS\InstaVideoStudio\InstaVideoStudio.lnk"
  Delete "$DESKTOP\InstaVideoStudio.lnk"
  RMDir /r "$INSTDIR"
SectionEnd
```

### 5. Assinar Executável (Opcional)

```bash
# Com certificado válido (recomendado para distribuição)
signtool sign /f certificate.pfx /p password /t http://timestamp.server.com /d "InstaVideo Studio" dist\InstaVideoStudio.exe
```

## 📦 Distribuição

### Versão Portável (Sem Installer)

```bash
# Crie pasta portável
mkdir InstaVideoStudio_Portable
xcopy dist\* InstaVideoStudio_Portable\ /E
xcopy database\*.db InstaVideoStudio_Portable\data\

# Compacte
7z a InstaVideoStudio_v1.0_Portable.7z InstaVideoStudio_Portable\
```

### Versão Installer (Com Registro no Windows)

```bash
# Gere MSI usando WiX
heat dir dist -o files.wxs
candle files.wxs -o files.wixobj
light files.wixobj -o InstaVideoStudio_v1.0.msi
```

## 🚀 Release Checklist

```
Antes de publicar:

□ Executar testes completos
  pytest tests/ --cov

□ Verificar versão
  Atualizar em:
  - pyproject.toml
  - backend/config/settings.py
  - frontend/main.py
  - CHANGELOG.md

□ Testar build completo
  - Instalar como novo usuário
  - Verificar funcionalidades core
  - Testar downloads
  - Testar exportação

□ Criar tag Git
  git tag -a v1.0.0 -m "Release v1.0.0"
  git push origin v1.0.0

□ Atualizar documentação
  - README.md
  - CHANGELOG.md
  - Release Notes

□ Gerar hashes SHA256
  certutil -hashfile InstaVideoStudio_v1.0.exe SHA256

□ Publicar em GitHub Releases
  - Upload de arquivos
  - Descrever mudanças
  - Marcar como pre-release se beta

□ Notificar usuários
  - Email newsletter
  - Social media
  - Website
```

## 🐳 Docker (Opcional)

### Dockerfile
```dockerfile
FROM python:3.11-slim-windows

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "backend/app.py"]
```

### Build Docker
```bash
docker build -t instavideo-studio:1.0 .
docker run -p 8000:8000 -v %APPDATA%\.instavideo-studio:/app/data instavideo-studio:1.0
```

## ⚙️ Configuração de Produção

### .env.production
```env
DEBUG=False
LOG_LEVEL=WARNING
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=False
SECRET_KEY=seu-secret-key-aleatorio-seguro
DATABASE_URL=sqlite:///C:\ProgramData\InstaVideoStudio\instavideo.db
FFMPEG_PATH=C:\Program Files\ffmpeg\bin\ffmpeg.exe
ENABLE_GPU=True
```

### Windows Defender Exclusão
```powershell
# Adicione pasta à exclusão do Defender
Add-MpPreference -ExclusionPath "C:\Users\$env:USERNAME\.instavideo-studio"
Add-MpPreference -ExclusionPath "C:\Program Files\InstaVideoStudio"
```

## 🔄 Update Mechanism

### Criar Updater (Python)
```python
# updater.py
import requests
import subprocess
import zipfile
from pathlib import Path

def check_updates():
    """Check for new versions"""
    response = requests.get("https://api.github.com/repos/NinjaDeChinelo/Ciber/releases/latest")
    latest = response.json()["tag_name"]
    current = "1.0.0"  # from settings
    
    if latest > current:
        return True, latest
    return False, None

def download_update(version):
    """Download and install update"""
    url = f"https://github.com/NinjaDeChinelo/Ciber/releases/download/{version}/InstaVideoStudio_{version}.zip"
    
    # Download
    response = requests.get(url)
    with open("update.zip", "wb") as f:
        f.write(response.content)
    
    # Extract
    with zipfile.ZipFile("update.zip", "r") as z:
        z.extractall("./update")
    
    # Replace files
    import shutil
    shutil.rmtree("./dist_old")
    shutil.move("./dist", "./dist_old")
    shutil.move("./update/dist", "./dist")

if __name__ == "__main__":
    has_update, version = check_updates()
    if has_update:
        print(f"Atualizando para {version}...")
        download_update(version)
        print("Atualização concluída!")
```

## 📊 Monitoramento de Releases

### GitHub Actions (CI/CD)
```yaml
# .github/workflows/build.yml
name: Build & Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build executable
      run: |
        pyinstaller --onefile frontend/main.py
        pyinstaller --onefile backend/app.py
    
    - name: Create release
      uses: actions/create-release@v1
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
```

## 🔐 Code Signing

```bash
# Gerar certificado auto-assinado
New-SelfSignedCertificate -CertStoreLocation Cert:\CurrentUser\My -DnsName "InstaVideoStudio" -FriendlyName "InstaVideoStudio Code Signing"

# Assinar todos os executáveis
Set-AuthenticodeSignature dist\InstaVideoStudio.exe cert.cer -Force
Set-AuthenticodeSignature dist\InstaVideoStudio_Backend.exe cert.cer -Force
```

---

**Próximas etapas após build:**
1. Testar em ambiente limpo
2. Coletar feedback
3. Iterar para v1.1
4. Adicionar mais recursos

**Suporte**: https://github.com/NinjaDeChinelo/Ciber/issues
