# InstaVideo Studio - Guia de Uso Completo

## 🚀 Quick Start (5 minutos)

### 1. Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/NinjaDeChinelo/Ciber.git
cd Ciber

# Crie ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Instale dependências
pip install -r requirements.txt

# Configure banco de dados
python scripts/setup_database.py
```

### 2. Inicie a Aplicação

**Terminal 1 - Backend (API)**
```bash
cd backend
python app.py
```
Saída esperada:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Frontend (UI)**
```bash
cd frontend
python main.py
```

## 📋 Funcionalidades Disponíveis

### ✅ Download de Vídeos

#### Interface
- Menu: **Downloads** → **+ Novo Download**

#### Como usar:
1. Cole a URL do vídeo
2. Clique em "Buscar Informações"
3. Visualize thumbnail, duração e qualidades
4. Selecione qualidade desejada
5. Clique em "Download"

#### Exemplo de URL:
```
https://www.instagram.com/p/ABC123XYZ/
https://www.instagram.com/reel/DEF456UVW/
```

### 📹 Biblioteca de Vídeos

#### Acessar
Menu: **Biblioteca**

#### Operações:
- **Visualizar**: Todos os vídeos baixados
- **Filtrar**: Por data, tamanho, projeto
- **Pesquisar**: Por título, tags
- **Renomear**: Clique duplo no vídeo
- **Deletar**: Clique direito → Remover

### ✂️ Editor de Vídeo

#### Fluxo de Edição:
1. **Criar Projeto**: Menu → Novo Projeto
2. **Adicionar Vídeos**: Arraste vídeos da biblioteca
3. **Cortar**: Timeline → Duplo clique → Drag dos marcadores
4. **Adicionar Efeitos**: 
   - Blur, Sharpen, Brightness
   - Transições: Fade, Dissolve, Wipe
5. **Adicionar Áudio**: Menu → Áudio → Adicionar Música
6. **Adicionar Texto**: Menu → Texto → Nova Legenda
7. **Preview**: Clique em Play
8. **Salvar**: Ctrl+S

#### Atalhos de Teclado:
```
Ctrl+S          = Salvar projeto
Ctrl+Z          = Desfazer
Ctrl+Y          = Refazer
Space           = Play/Pause
Delete          = Remover clip selecionado
Ctrl+C          = Copiar
Ctrl+V          = Colar
```

### 📤 Exportação de Vídeo

#### Como Exportar:
1. Projeto aberto no Editor
2. Menu: **Arquivo** → **Exportar**
3. Selecione:
   - **Formato**: MP4, MOV, AVI, MKV
   - **Resolução**: 720p, 1080p, 1440p, 4K
   - **Localização**: Pasta de saída
4. Clique "Exportar"

#### Monitorar Progresso:
Menu: **Exportações** - Veja fila e progresso em %

#### Tempos Estimados (1080p):
- 5 min de vídeo: ~3-5 minutos
- 10 min de vídeo: ~6-10 minutos
- Com GPU: 50% mais rápido

### 📅 Agendar Publicação (Beta)

#### Configurar Conta Instagram:
1. Menu: **Configurações** → **Contas do Instagram**
2. Clique: **+ Adicionar Conta**
3. Faça login com suas credenciais
4. Autorize acesso

#### Agendar Postagem:
1. Projeto exportado
2. Menu: **Publicar** → **Agendar**
3. Selecione:
   - Conta Instagram
   - Data e hora
   - Caption (legenda)
4. Clique: **Agendar**

## ⚙️ Configurações

### Localização: Menu → Configurações

#### Geral
- **Tema**: Dark Mode / Light Mode
- **Idioma**: Português, English
- **Auto-salvar**: Ativar/Desativar (padrão: ON)

#### Armazenamento
- **Pasta de Vídeos**: Customize localização
- **Pasta de Exportações**: Customize localização
- **Pasta de Projetos**: Customize localização
- **Limpar Cache**: Remove miniaturas

#### Desempenho
- **Acelerar GPU**: Ativar/Desativar
- **Threads Simultâneos**: 2-8 (padrão: 4)
- **Memória Máxima**: 1GB-8GB

#### Instagram
- **App ID**: Seu app ID (Se usar API)
- **App Secret**: Seu app secret (Se usar API)
- **Contas Conectadas**: Gerenciar

## 🐛 Troubleshooting

### Erro: "FFmpeg not found"
```bash
# Opção 1: Instalar via Chocolatey
choco install ffmpeg

# Opção 2: Especificar caminho manual
# Crie/edite .env na raiz:
FFMPEG_PATH=C:\caminho\para\ffmpeg.exe
```

### Erro: "Banco de dados corrompido"
```bash
# Recrie o banco
python scripts/setup_database.py --force
```

### Aplicação lenta
1. Reduza resolução de preview (720p)
2. Feche outras aplicações
3. Ative GPU acceleration em Configurações
4. Reduza número de threads

### Download parado
1. Verifique conexão de internet
2. URL é válida?
3. Reinicie o download
4. Verifique espaço em disco

## 📊 Dashboard

### Informações Exibidas:
- **Total de Vídeos**: Quantidade na biblioteca
- **Espaço Utilizado**: MB/GB em uso
- **Downloads Recentes**: Últimos 5 downloads
- **Projetos Recentes**: Últimos 5 projetos
- **Status das Exportações**: Fila atual

## 📁 Estrutura de Dados

### Localização dos Arquivos:
```
Windows: C:\Users\{usuario}\.instavideo-studio\
├── videos/              # Vídeos baixados
├── projects/            # Arquivos de projeto
├── exports/             # Vídeos exportados
├── thumbnails/          # Miniaturas em cache
├── logs/                # Arquivos de log
└── instavideo.db        # Banco de dados SQLite
```

## 🔐 Segurança e Privacidade

- ✅ Credenciais do Instagram armazenadas com criptografia
- ✅ Nenhum dado enviado para servidores externos
- ✅ Logs locais apenas para debugging
- ✅ Compatível com Windows Defender

## 📞 Suporte e Reportar Problemas

### Coletar Logs:
1. Menu: **Ajuda** → **Abrir Pasta de Logs**
2. Copie conteúdo dos arquivos .log

### Reportar Bug:
1. Acesse: https://github.com/NinjaDeChinelo/Ciber/issues
2. Clique: **New Issue**
3. Descreva o problema
4. Anexe logs se relevante

## 📚 Recursos Adicionais

- **Documentação Técnica**: [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **API Reference**: [API.md](docs/API.md)
- **Build Guide**: [BUILD.md](docs/BUILD.md)

## 🎥 Exemplos de Workflow

### Exemplo 1: Download e Publicar
```
1. Download vídeo (Menu → Downloads)
2. Abrir na Biblioteca
3. Adicionar efeitos rápidos (Menu → Editor)
4. Exportar para MP4 1080p
5. Agendar publicação (Menu → Publicar)
```

### Exemplo 2: Compilação de Reels
```
1. Baixar 3-5 vídeos curtos
2. Criar novo projeto
3. Arrastar vídeos para timeline
4. Adicionar transições
5. Adicionar música de fundo
6. Adicionar texto introdutório
7. Exportar e publicar
```

### Exemplo 3: Edição Profissional
```
1. Importar vídeo principal
2. Adicionar clips secundários
3. Aplicar effects (color correction, blur)
4. Adicionar sobreposições de texto
5. Sincronizar áudio
6. Exportar em 4K
7. Salvar como preset de projeto
```

---

**Versão**: 1.0.0  
**Última atualização**: 2026-06-07  
**Próximas features**: 
- [ ] Mais filtros e efeitos
- [ ] Suporte a livestream
- [ ] Integração com TikTok, YouTube
- [ ] Plugins de terceiros
