# 🎯 Como Usar o InstaVideo Studio - Guia Prático

## 🚀 OPÇÃO 1: Instalação Automática (Recomendado)

### Windows PowerShell (Recomendado)
```powershell
# 1. Abra PowerShell como Administrador
# 2. Execute:
powershell -ExecutionPolicy Bypass -File install.ps1

# A instalação fará automaticamente:
# ✅ Clone do repositório
# ✅ Virtual environment
# ✅ Instalação de dependências
# ✅ Setup do banco de dados
# ✅ Criação de atalho na Desktop
```

### Windows CMD
```cmd
# 1. Abra CMD como Administrador
# 2. Execute:
install.bat

# Segue os mesmos passos do PowerShell
```

---

## 🚀 OPÇÃO 2: Instalação Manual

Se prefere instalar passo a passo:

```bash
# 1. Clone o repositório
git clone https://github.com/NinjaDeChinelo/Ciber.git
cd Ciber

# 2. Crie virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1          # PowerShell
# ou
.\venv\Scripts\activate.bat          # CMD

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure banco de dados
python scripts/setup_database.py
```

---

## ▶️ EXECUTAR A APLICAÇÃO

### Passo 1: Abra 2 Terminais

**Terminal 1 - Backend (API)**
```bash
# Ative o virtual env
.\venv\Scripts\Activate.ps1

# Inicie o backend
cd backend
python app.py
```

Você verá:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Frontend (Interface)**
```bash
# Ative o virtual env
.\venv\Scripts\Activate.ps1

# Inicie o frontend
cd frontend
python main.py
```

A janela da aplicação abrirá! 🎉

---

## 📥 Exemplo 1: Baixar Vídeo

```
1. Clique em "Downloads" no menu
2. Cole a URL:
   https://www.instagram.com/p/ABC123XYZ/

3. Clique "+ Novo Download"
4. Selecione qualidade (720p, 1080p, etc)
5. Clique "Download"

✅ Vídeo salvo em:
   C:\Users\{seu-usuário}\.instavideo-studio\videos\
```

---

## 🎬 Exemplo 2: Editar Vídeo

```
1. Menu: "Editor" → "Novo Projeto"
2. Nome do projeto: "Meu Vídeo"
3. Arraste vídeo da biblioteca para timeline
4. Edite:
   - ✂️ Corte: Duplo clique + arraste marcadores
   - 🎨 Efeito: Menu → Aplicar Efeito
   - 🎵 Áudio: Menu → Adicionar Música
   - 📝 Texto: Menu → Adicionar Legenda

5. Preview: Pressione SPACE
6. Salvar: Ctrl+S
```

---

## 📤 Exemplo 3: Exportar para MP4

```
1. Projeto aberto no Editor
2. Menu: "Arquivo" → "Exportar"
3. Selecione:
   - Formato: MP4
   - Resolução: 1080p
   - Localização: Pasta

4. Clique "Exportar"

✅ Vídeo pronto em:
   C:\Users\{seu-usuário}\.instavideo-studio\exports\
```

---

## 📊 Estrutura de Arquivos

Todos os seus arquivos são armazenados aqui:

```
C:\Users\{seu-usuário}\.instavideo-studio\
├── videos/           # Vídeos baixados
├── projects/         # Projetos salvos
├── exports/          # Vídeos exportados
├── thumbnails/       # Cache de miniaturas
├── logs/             # Logs de debug
└── instavideo.db     # Banco de dados
```

---

## ⚙️ Configurações Importantes

Menu → **Configurações**

### Armazenamento
- Customize pasta de vídeos
- Customize pasta de exportações
- Limpar cache quando necessário

### Desempenho
- ⚡ Ativar GPU (50% mais rápido!)
- Configurar threads simultâneos
- Limitar uso de memória

### Qualidade
- Resolução padrão de preview
- Bitrate padrão de exportação

---

## 🎮 Atalhos de Teclado

```
Ctrl+S      = Salvar projeto
Ctrl+Z      = Desfazer
Ctrl+Y      = Refazer
Space       = Play/Pause
Delete      = Remover clip selecionado
Ctrl+C      = Copiar
Ctrl+V      = Colar
Ctrl+A      = Selecionar tudo
```

---

## 🔧 Troubleshooting

### ❌ FFmpeg não encontrado
```bash
# Opção 1: Instalar via Chocolatey
choco install ffmpeg

# Opção 2: Especificar caminho
# Crie/edite .env na raiz:
FFMPEG_PATH=C:\path\to\ffmpeg.exe
```

### ❌ Porta 8000 já em uso
```env
# Edite .env
API_PORT=8001
```

### ❌ Banco de dados corrompido
```bash
python scripts/setup_database.py --force
```

### ❌ PowerShell não executa scripts
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📚 Documentação

- 📖 [QUICKSTART.md](QUICKSTART.md) - Guia de 5 minutos
- 📖 [docs/USAGE_GUIDE.md](docs/USAGE_GUIDE.md) - Guia completo
- 📖 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Técnico
- 📖 [docs/BUILD.md](docs/BUILD.md) - Compilar EXE
- 💻 [docs/EXAMPLES.py](docs/EXAMPLES.py) - Exemplos de código

---

## 🆘 Precisa de Ajuda?

1. **Leia** [QUICKSTART.md](QUICKSTART.md)
2. **Consulte** [docs/USAGE_GUIDE.md](docs/USAGE_GUIDE.md)
3. **Abra uma issue**: https://github.com/NinjaDeChinelo/Ciber/issues
4. **Verifique logs**: `~/.instavideo-studio/logs/`

---

## 🌟 Dicas Úteis

### Dica 1: Download em Lote
```
Cole múltiplas URLs separadas por quebra de linha:

https://www.instagram.com/p/ABC/
https://www.instagram.com/p/DEF/
https://www.instagram.com/p/GHI/
```

### Dica 2: Presets de Exportação
```
Salve suas configurações favoritas:
1. Configure formato/resolução
2. Clique "Salvar como Preset"
3. Reutilize depois!
```

### Dica 3: Acelerar com GPU
```
Menu → Configurações → Desempenho
✅ Ativar GPU
⚡ 50% mais rápido!
```

### Dica 4: Recuperar Downloads
```
Downloads pausados? Sem problemas!
Menu → Downloads → Histórico
Clique "Retomar"
```

---

## ✅ Checklist de Primeiro Uso

- [ ] Instalação concluída
- [ ] Backend iniciado (porta 8000)
- [ ] Frontend iniciado
- [ ] Primeiro vídeo baixado
- [ ] Editor testado
- [ ] Vídeo exportado
- [ ] Configurações personalizadas

---

## 🎉 Pronto!

Agora você está pronto para:
- ✅ Baixar vídeos do Instagram
- ✅ Editar com profissionalismo
- ✅ Exportar em múltiplos formatos
- ✅ Agendar publicações

**Versão**: 1.0.0  
**Status**: ✅ Estável  
**Último update**: 2026-06-07

Boa sorte com seus vídeos! 🎬
