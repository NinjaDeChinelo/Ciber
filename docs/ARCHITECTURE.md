# InstaVideo Studio - Arquitetura Técnica

## 🏗️ Visão Geral da Arquitetura

O InstaVideo Studio segue uma arquitetura em camadas com separação clara entre backend (lógica de negócio) e frontend (interface do usuário).

```
┌─────────────────────────────────────────────┐
│         PyQt6 Frontend (UI/UX)              │
│   Dashboard | Downloads | Library | Editor  │
└────────────────────┬────────────────────────┘
                     │ HTTP/REST
┌────────────────────┴────────────────────────┐
│      FastAPI Backend (Business Logic)       │
├──────────────────────────────────────────────┤
│  • Download Manager                          │
│  • Video Processor (FFmpeg)                  │
│  • Project Manager                           │
│  • Export Queue                              │
│  • Instagram Integration (OAuth2)            │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────┴────────────────────────┐
│         SQLite Database Layer                │
├──────────────────────────────────────────────┤
│  • Videos Metadata                           │
│  • Projects                                  │
│  • Exports History                           │
│  • Download Queue                            │
│  • User Settings                             │
└──────────────────────────────────────────────┘
```

## 🔄 Fluxo de Dados

### Download de Vídeo
```
User Input (URL) 
  → Validation 
  → Instagram Service (OAuth2/API)
  → FFmpeg Extraction
  → Storage
  → Database Update
  → Library UI Refresh
```

### Edição de Vídeo
```
Load Project
  → Timeline Initialization
  → Clip Management (Add/Remove/Reorder)
  → Effects Application
  → Audio Processing
  → Text/Subtitle Overlay
  → Preview Rendering
  → Export Queue
```

### Exportação
```
Export Request
  → Queue Management
  → FFmpeg Processing
  → Resource Monitoring (CPU/GPU)
  → Progress Tracking
  → Output Delivery
  → Database Update
```

## 📦 Componentes Principais

### Backend (Python)
- **FastAPI**: Framework web leve e rápido
- **SQLAlchemy**: ORM para banco de dados
- **Pydantic**: Validação de dados
- **python-instagram**: SDK Instagram (conteúdo autorizado)
- **FFmpeg-python**: Wrapper para FFmpeg
- **Celery** (opcional): Processamento async de vídeos

### Frontend (PyQt6)
- **PyQt6**: Framework GUI moderna
- **QThread**: Multi-threading para operações pesadas
- **QGraphicsView**: Timeline do editor
- **Matplotlib**: Gráficos e visualizações

## 🗄️ Modelo de Dados

### Videos Table
```sql
- id (PK)
- title
- url_source
- thumbnail_path
- file_path
- duration (segundos)
- resolution
- file_size
- date_downloaded
- project_id (FK)
- tags
- metadata (JSON)
- created_at
- updated_at
```

### Projects Table
```sql
- id (PK)
- name
- description
- thumbnail_path
- date_created
- date_modified
- exported (bool)
- status (draft|processing|completed)
```

### Exports Table
```sql
- id (PK)
- project_id (FK)
- format (mp4|mov|avi|mkv)
- resolution (720p|1080p|1440p|4k)
- file_path
- file_size
- status (pending|processing|completed|failed)
- progress (%)
- date_started
- date_completed
- error_message
```

## 🔐 Segurança

### Validação
- URL validation (regex + Instagram API verification)
- File type validation (whitelist)
- Size limits enforcement
- Malware scanning integration (optional)

### Autenticação
- OAuth2 para Instagram API
- Credenciais armazenadas em keyring (Windows Credential Manager)
- Session management com JWT

### Logs & Audit
- Todos os downloads/exports registrados
- Rastreamento de erros
- Recuperação automática de falhas

## 🚀 Fluxo de Inicialização

```
1. Application Start
   ↓
2. Database Check/Initialization
   ↓
3. FFmpeg Availability Check
   ↓
4. Settings Load
   ↓
5. Backend Service Start (FastAPI + Uvicorn)
   ↓
6. Frontend Window Creation
   ↓
7. Dashboard Load
   ↓
8. Ready for User Interaction
```

## 📊 Performance

### Otimizações
- **Multi-threading**: UI responsiva
- **Queue System**: Downloads/Exports gerenciados
- **Caching**: Thumbnails e metadados em cache
- **GPU Support**: FFmpeg com CUDA/NVENC quando disponível
- **Lazy Loading**: Biblioteca carrega sob demanda

### Requisitos de Sistema
- RAM: 4GB mínimo (8GB recomendado)
- Disk: 500MB para app + espaço para vídeos
- GPU: Recomendado para exportações rápidas
- CPU: 4+ cores para processamento paralelo

---

**Última atualização**: 2026-06-07
**Versão**: 1.0.0
