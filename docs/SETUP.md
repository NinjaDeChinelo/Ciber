"""
Setup instructions and installation guide
"""

# InstaVideo Studio - Setup Guide

## 📋 Pré-requisitos

### Windows 10/11
- Python 3.11 ou superior
- FFmpeg instalado ou disponível no PATH
- 4GB RAM mínimo (8GB recomendado)
- 500MB espaço livre para aplicação + espaço para vídeos

## 🚀 Instalação Rápida

### 1. Clone o Repositório
```bash
git clone https://github.com/NinjaDeChinelo/Ciber.git
cd Ciber
```

### 2. Crie um Ambiente Virtual
```bash
python -m venv venv
source venv\Scripts\activate  # Windows
# ou
.\venv\Scripts\Activate.ps1  # PowerShell
```

### 3. Instale Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados
```bash
python scripts/setup_database.py
```

### 5. Configure Variáveis de Ambiente
Crie arquivo `.env` na raiz do projeto:
```env
DEBUG=False
LOG_LEVEL=INFO
FFMPEG_PATH=C:\path\to\ffmpeg.exe
INSTAGRAM_APP_ID=seu_app_id
INSTAGRAM_APP_SECRET=seu_app_secret
```

### 6. Execute a Aplicação

**Backend (em um terminal):**
```bash
cd backend
python app.py
```

**Frontend (em outro terminal):**
```bash
cd frontend
python main.py
```

## 📦 Instalação do FFmpeg

### Windows

#### Opção 1: Usando Chocolatey (Recomendado)
```bash
choco install ffmpeg
```

#### Opção 2: Download Manual
1. Acesse https://ffmpeg.org/download.html
2. Download a versão Windows (Full/Static)
3. Extraia para `C:\ffmpeg`
4. Adicione `C:\ffmpeg\bin` ao PATH do Windows

#### Verificar Instalação
```bash
ffmpeg -version
ffprobe -version
```

## 🗄️ Banco de Dados

### Inicializar
```bash
python scripts/setup_database.py
```

### Localização
- Windows: `C:\Users\{user}\.instavideo-studio\instavideo.db`

### Backup
```bash
python scripts/backup_database.py
```

## 🔧 Configuração Avançada

### Usar GPU para Exportação
```env
ENABLE_GPU=True
GPU_ACCELERATION=cuda  # ou dxva2, qsv
```

### Alterar Diretórios
```env
DATA_DIR=D:\InstaVideo
VIDEOS_DIR=D:\InstaVideo\Videos
EXPORTS_DIR=D:\InstaVideo\Exports
```

## 🐛 Troubleshooting

### FFmpeg não encontrado
```bash
# Verifique se está no PATH
where ffmpeg

# Ou especifique o caminho em .env
FFMPEG_PATH=C:\path\to\ffmpeg.exe
```

### Erro de Banco de Dados
```bash
# Recrie o banco de dados
python scripts/setup_database.py --force
```

### Porta 8000 já em uso
```env
# Mude a porta em .env
API_PORT=8001
```

## 📚 Estrutura de Diretórios

```
Ciber/
├── backend/              # API e lógica
│   ├── app.py           # Entry point
│   ├── config/          # Configurações
│   ├── models/          # ORM models
│   ├── services/        # Business logic
│   ├── api/             # Rotas API
│   └── utils/           # Utilitários
├── frontend/            # Interface PyQt
│   ├── main.py         # Entry point
│   ├── ui/             # Componentes UI
│   ├── services/       # Serviços frontend
│   └── assets/         # Recursos
├── database/           # Schemas e migrations
├── scripts/            # Scripts utilitários
├── docs/              # Documentação
└── tests/             # Testes
```

## ✅ Verificação de Instalação

```bash
# Teste o backend
curl http://localhost:8000/api/health

# Teste o frontend
python frontend/main.py

# Execute testes
pytest tests/
```

## 📖 Próximos Passos

1. Leia [ARCHITECTURE.md](docs/ARCHITECTURE.md) para entender a arquitetura
2. Consulte [API.md](docs/API.md) para documentação da API
3. Comece com [BUILD.md](docs/BUILD.md) para compilar executável

---

**Suporte**: Para problemas, abra uma issue no GitHub
**Versão**: 1.0.0
**Última atualização**: 2026-06-07
