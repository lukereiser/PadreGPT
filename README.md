# PadreGPT - Catholic AI Assistant

## 🎯 Project Goal

Create an AI assistant called "Padre GPT" that answers questions from a Catholic theological perspective, grounded in authentic Catholic sources. The assistant is designed to embody the role of a Catholic theologian with expertise on Thomas Aquinas.

---

## 📊 Current Status

### ✅ Completed
- [x] Telegram API credentials configured
- [x] Session string generated (no interactive login needed)
- [x] PDF download script working
- [x] **77 PDFs downloaded** from "Catholic library - books & documents" Telegram channel
- [x] **OpenAI Assistant created** with file search enabled
- [x] **10 priority PDFs uploaded** to the Assistant
- [x] **Streamlit web app** created for interacting with the assistant

### 🔄 In Progress
- [ ] Download more priority books from Telegram (Douay-Rheims, Catechism, Summa selections)
- [ ] Upload additional books to Assistant

### ❌ Not Found in Telegram Channel
- RSV-CE Bible (only partial books available)
- The Fathers Know Best (someone requested it, not uploaded)

---

## 🚀 Quick Start

### Run the Web App
```bash
cd /Users/lukereiser/PadreGPT
source .venv/bin/activate
streamlit run app.py --server.port 8501
```
Then open http://localhost:8501

### Test the Assistant
Ask questions like:
- "What does St. Thomas Aquinas say about humility?"
- "Explain the doctrine of the Trinity according to Catholic teaching"
- "What are the first principles of natural law?"

---

## 📁 Project Structure

```
PadreGPT/
├── .env                          # API credentials (gitignored)
├── .venv/                        # Python virtual environment
├── app.py                        # Streamlit web interface
├── downloads/
│   └── telegram_pdfs/
│       └── 2025-12/              # Downloaded PDFs (77 files, 808MB total)
├── scripts/
│   ├── telegram_pdf_downloader.py    # Downloads PDFs from Telegram channels
│   ├── print_telegram_session_string.py  # Generates session string
│   └── create_assistant.py           # Creates OpenAI Assistant with files
├── state/
│   └── telegram_downloader_state.json  # Tracks download progress
├── requirements.txt
└── README.md
```

---

## 🔑 Credentials & Configuration

### Environment Variables (in `.env`)
```
# Telegram API credentials from https://my.telegram.org
TELEGRAM_API_ID=30284703
TELEGRAM_API_HASH=0ef7193213c48e0777e72b8bb026eae4
TELEGRAM_SESSION_STRING=1AZWarz...  (long string)

# OpenAI API Key
OPENAI_API_KEY=sk-proj-843d...

# OpenAI Assistant ID (created by create_assistant.py)
OPENAI_ASSISTANT_ID=asst_OXwLslMwFGOTBgLBgi82CWvd
```

---

## 📚 Books Currently in Assistant

| Book | Author/Source | Size |
|------|---------------|------|
| Theology for Beginners | Frank Sheed | 832KB |
| A Catechism of Christian Doctrine | Ireland 1951 | 6.1MB |
| Contra Errores Graecorum | St. Thomas Aquinas | 152KB |
| How to Study | Letter of St. Thomas Aquinas | 1.1MB |
| The Practice of Humility | Pope Leo XIII | 2.1MB |
| Uniformity with God's Will | St. Alphonsus de Liguori | 148KB |
| The First Apology | St. Justin Martyr | 136KB |
| The Second Apology | St. Justin Martyr | 40KB |
| The First Seven Ecumenical Councils | (325-787 AD) | 2.1MB |
| Papal Encyclicals 1958-1981 | Various Popes | 27MB |

**Total: ~40MB**

---

## 📥 Priority Books to Add

Found in Telegram channel (need to download):

| Book | Status | Notes |
|------|--------|-------|
| **Douay-Rheims Bible** | ✅ Found | 4 volumes (Vulgate, Latin-English I-III.pdf) |
| **Catechism of the Catholic Church** | ✅ Found | 4 parts in EPUB format |
| **Summa Theologica** | ⚠️ Partial | Catechism of Summa, Nature and Grace Selections |
| **RSV-CE Bible** | ❌ Not found | Only partial books (Chronicles, Mark) |
| **The Fathers Know Best** | ❌ Not found | Someone requested it, not uploaded |

---

## 🔧 Key Scripts

### 1. Download PDFs from Telegram
```bash
cd /Users/lukereiser/PadreGPT
source .venv/bin/activate
python scripts/telegram_pdf_downloader.py --channel "-1001802265936" --limit 5000
```

### 2. Create/Update Assistant
```bash
python scripts/create_assistant.py
```
This script:
- Uploads PDFs from `downloads/telegram_pdfs/2025-12/`
- Creates an OpenAI Assistant with file_search enabled
- Saves the Assistant ID to `.env`

### 3. Generate Telegram Session String
```bash
python scripts/print_telegram_session_string.py
```
Note: User has 2FA enabled - password "Novice945*" required.

---

## 🌐 Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Telegram       │     │   Local Files   │     │    OpenAI       │
│  Channel        │────>│   (PDFs)        │────>│   Assistants    │
│  @cathlib       │     │   downloads/    │     │   API           │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         v
                                                ┌─────────────────┐
                                                │   Streamlit     │
                                                │   Web App       │
                                                │   (app.py)      │
                                                └─────────────────┘
```

### Why Assistants API instead of Custom GPT?
1. **Full automation** - Can upload files programmatically (Custom GPTs require manual drag-and-drop due to native file dialogs)
2. **Web accessible** - Streamlit app can be deployed publicly
3. **More control** - Can customize the assistant behavior, manage threads, etc.

---

## 📞 User Info

- **Phone**: +1 415 312 4656 (for Telegram verification)
- **Telegram 2FA Password**: Novice945*
- **Telegram Channel ID**: -1001802265936

---

## 🔗 Useful Links

- **Streamlit App**: http://localhost:8501 (when running)
- **OpenAI Platform**: https://platform.openai.com/assistants
- **Telegram Channel**: https://t.me/cathlib
- **Telegram API Portal**: https://my.telegram.org/apps

---

## ⚠️ Known Issues & Solutions

### Telegram Download Script
The script requires the channel ID as an integer:
```bash
# Correct:
python scripts/telegram_pdf_downloader.py --channel "-1001802265936"

# Wrong (username doesn't work):
python scripts/telegram_pdf_downloader.py --channel "@cathlib"
```

### Session Expiry
If Telegram session expires, regenerate with:
```bash
python scripts/print_telegram_session_string.py
```

### File Limits
- OpenAI Assistants: No hard limit like Custom GPTs (512MB)
- But larger files take longer to index
- Recommend keeping total under 100MB for best performance

---

## 🛠️ Development Notes

### Dependencies
```
openai>=1.0.0
streamlit
telethon
python-dotenv
tqdm
```

### Streamlit App Features
- Chat interface with message history
- Thread management (new conversation button)
- Catholic-themed styling (parchment background, etc.)
- Spinner while waiting for responses

### Adding More Books
1. Download PDFs to `downloads/telegram_pdfs/2025-12/`
2. Add filenames to `PRIORITY_FILES` list in `scripts/create_assistant.py`
3. Run `python scripts/create_assistant.py` (creates new assistant)
4. Update `OPENAI_ASSISTANT_ID` in `.env` with new ID

---

## 📝 Session History

### Session 1 (Initial Setup)
- Set up Telegram API credentials
- Created PDF download script
- Downloaded 77 PDFs

### Session 2 (OpenAI Integration)
- Switched from Custom GPT to Assistants API
- Created Assistant with 10 priority books
- Built Streamlit web interface
- Successfully tested chat functionality

### Session 3 (Current - Book Search)
- Searched Telegram for priority books
- Found: Douay-Rheims Bible, Catechism of Catholic Church, Summa selections
- Not found: RSV-CE Bible, The Fathers Know Best
- Download in progress
