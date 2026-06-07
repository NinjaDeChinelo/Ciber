# InstaVideo Studio

Uma aplicação profissional para desktop (Windows 10/11) para download, organização, edição e publicação de vídeos do Instagram com conteúdo autorizado.

## 📋 Funcionalidades

### Download
- ✅ Download individual de vídeos
- ✅ Download em lote (múltiplas URLs, TXT, CSV)
- ✅ Downloads simultâneos com fila
- ✅ Pausa, retomada e cancelamento
- ✅ Histórico de downloads

### Biblioteca
- ✅ Organização de vídeos em categorias
- ✅ Metadados automáticos (título, duração, tamanho)
- ✅ Pesquisa e filtros avançados
- ✅ Gerenciamento de projetos

### Editor de Vídeo
- ✅ Timeline interativa
- ✅ Corte, divisão e reordenação de cenas
- ✅ Edição de áudio (volume, fade, música)
- ✅ Adicionar textos, títulos e legendas
- ✅ Efeitos (zoom, blur, transições, cor)
- ✅ Previewização em tempo real

### Exportação
- ✅ Múltiplos formatos (MP4, MOV, AVI, MKV)
- ✅ Resoluções: 720p, 1080p, 1440p, 4K
- ✅ Fila de exportação com barra de progresso
- ✅ Otimização de CPU/GPU

### Publicação
- ✅ Agendamento de postagens
- ✅ Integração com Instagram API (conteúdo autorizado)
- ✅ Gerenciamento de múltiplas contas

## 🛠️ Tecnologias

- **Frontend**: PyQt6 / PySide6
- **Backend**: Python 3.11+
- **Desktop**: Tauri (alternativa) / PyQt
- **Banco de Dados**: SQLite3
- **Processamento de Vídeo**: FFmpeg
- **API**: FastAPI (backend services)
- **UI Framework**: Modern, Dark Mode/Light Mode

## 📁 Estrutura do Projeto

```
instavideo-studio/
├── backend/
│   ├── app.py                 # Entry point
│   ├── requirements.txt
│   ├── config/
│   │   ├── settings.py
│   │   ├── constants.py
│   │   └── database.py
│   ├── models/
│   │   ├── video.py
│   │   ├── project.py
│   │   ├── export.py
│   │   └── user.py
│   ├── services/
│   │   ├── download_service.py
│   │   ├── video_processor.py
│   │   ├── export_service.py
│   │   ├── instagram_service.py
│   │   └── ffmpeg_service.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── videos.py
│   │   │   ├── projects.py
│   │   │   ├── exports.py
│   │   │   └── downloads.py
│   │   └── schemas.py
│   ├── utils/
│   │   ├── validators.py
│   │   ├── file_handler.py
│   │   ├── logger.py
│   │   └── error_handler.py
│   └── migrations/
│
├── frontend/
│   ├── main.py              # PyQt Application entry
│   ├── requirements.txt
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── widgets/
│   │   │   ├── dashboard.py
│   │   │   ├── download_manager.py
│   │   │   ├── library.py
│   │   │   ├── video_editor.py
│   │   │   ├── export_manager.py
│   │   │   └── settings.py
│   │   ├── styles/
│   │   │   ├── dark_theme.qss
│   │   │   ├── light_theme.qss
│   │   │   └── resources.qrc
│   │   └── dialogs/
│   │       ├── download_dialog.py
│   │       ├── export_dialog.py
│   │       └── settings_dialog.py
│   ├── services/
│   │   ├── api_client.py
│   │   ├── state_manager.py
│   │   └── event_bus.py
│   └── assets/
│       ├── icons/
│       └── images/
│
├── database/
│   ├── schema.sql
│   ├── migrations/
│   └── seeds.sql
│
├── scripts/
│   ├── build.py
│   ├── install_dependencies.py
│   ├── setup_database.py
│   └── package.py
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── SETUP.md
│   ├── BUILD.md
│   └── DEPLOYMENT.md
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── .github/
│   └── workflows/
│
├── pyproject.toml
├── setup.py
└── .gitignore
```

## 🚀 Quick Start

### Pré-requisitos
- Python 3.11+
- FFmpeg instalado
- Windows 10/11
- pip/conda

### Instalação

```bash
# Clone o repositório
git clone https://github.com/NinjaDeChinelo/Ciber.git
cd Ciber

# Crie um ambiente virtual
python -m venv venv
source venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o banco de dados
python scripts/setup_database.py

# Execute a aplicação
python frontend/main.py
```

## 📝 Compliance e Segurança

- ✅ Respeita Terms of Service do Instagram
- ✅ Suporte apenas para conteúdo autorizado
- ✅ Validação de URLs e permissões
- ✅ Tratamento seguro de credenciais
- ✅ Logs de segurança
- ✅ Recuperação automática de falhas

## 📖 Documentação

- [Arquitetura](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Setup Guide](docs/SETUP.md)
- [Build Guide](docs/BUILD.md)

## 📄 Licença

MIT License - Veja LICENSE para detalhes.

## 👨‍💻 Desenvolvedor

InstaVideo Studio - Arquitetura profissional para edição de vídeos.
