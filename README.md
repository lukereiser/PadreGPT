# PadreGPT - Catholic AI Assistant

## 🎯 Project Vision

Create **Padre GPT**, an AI assistant that answers questions from an authentically Catholic theological perspective, grounded in primary sources (Church Fathers, Papal documents, Catechisms, Aquinas). Available via:
1. **Web** - `chat.projectpio.com` (Streamlit on Railway)
2. **Telegram Bot** - For mobile/chat access
3. **API** - OpenAI Assistants API for integrations

---

## 🤖 AGENT STRATEGY

### Agent Roles & Assignments

| Agent | Focus Area | Recommended Model | Priority |
|-------|------------|-------------------|----------|
| **🏛️ Founder Agent** | Strategy, coordination, architecture | Claude Opus | Meta |
| **🚀 Deploy Agent** | Railway, domains, infrastructure | Claude Sonnet / GPT-4o | HIGH |
| **📚 Content Agent** | Finding, downloading, uploading PDFs | Claude Sonnet | HIGH |
| **🤖 Telegram Agent** | Building Telegram bot interface | Claude Sonnet / GPT-4o | MEDIUM |
| **🎨 UI/UX Agent** | Improving Streamlit web interface | Claude Sonnet | LOW |

---

### 🏛️ FOUNDER AGENT (Current)

**Role**: Strategic oversight, project coordination, README maintenance

**Responsibilities**:
- Define project architecture and vision
- Coordinate between specialized agents
- Maintain this README as source of truth
- Make high-level decisions

**Current Status**: Setting up agent strategy, preparing handoffs

---

### 🚀 DEPLOY AGENT

**Mission**: Get `chat.projectpio.com` live and working

**Current State**:
- ✅ GitHub repo created: `github.com/lukereiser/PadreGPT`
- ✅ Railway project created: `beneficial-strength`
- ✅ Environment variables set: `OPENAI_API_KEY`, `OPENAI_ASSISTANT_ID`
- 🔄 **BLOCKED**: Need to generate domain and configure DNS

**Immediate Tasks**:
1. In Railway Settings → Networking → Click "Generate Domain" with port **8501**
2. Click "+ Custom Domain" → Enter `chat.projectpio.com`
3. Copy the CNAME target Railway provides
4. In GoDaddy DNS for `projectpio.com`:
   - Add CNAME record: `chat` → `[Railway CNAME target]`
5. Wait for DNS propagation (~5-15 min)
6. Test `chat.projectpio.com`

**Files to Know**:
- `app.py` - Streamlit application (uses port 8501)
- `.env` - Contains `OPENAI_API_KEY` and `OPENAI_ASSISTANT_ID`

**Credentials Needed**:
- Railway: User is logged in at `railway.com`
- GoDaddy: User is logged in, domain is `projectpio.com`

---

### 📚 CONTENT AGENT

**Mission**: Maximize the quality and coverage of theological sources in the Assistant

**Current State**:
- ✅ 77 PDFs downloaded from Telegram (808MB)
- ✅ 16 files uploaded to Assistant (see list below)
- 🔄 More books available to upload

**Books Currently Uploaded**:
| Book | Type | Size |
|------|------|------|
| Theology for Beginners - Frank Sheed | PDF | 832KB |
| A Catechism of Christian Doctrine (Ireland 1951) | PDF | 6.1MB |
| Catechism of the Catholic Church | PDF | ~3MB |
| Contra Errores Graecorum - Aquinas | PDF | 152KB |
| How to Study - St. Thomas Aquinas | PDF | 1.1MB |
| Summa Theologica Part 1 (Prima Pars) | TXT | ~2MB |
| Summa Theologica Part 1-2 (Prima Secundae) | TXT | ~2MB |
| Summa Theologica Part 2-2 (Secunda Secundae) Vol 1 | TXT | ~2MB |
| Summa Theologica Part 3 (Tertia Pars) | TXT | ~2MB |
| Douay-Rheims Bible Complete | TXT | ~4MB |
| St. Justin Martyr - First Apology | PDF | 136KB |
| St. Justin Martyr - Second Apology | PDF | 40KB |
| First Seven Ecumenical Councils | PDF | 2.1MB |
| Practice of Humility - Pope Leo XIII | PDF | 2.1MB |
| Uniformity with God's Will - St. Alphonsus | PDF | 148KB |
| Papal Encyclicals 1958-1981 | PDF | 27MB |

**Priority Books to Find/Add**:
| Book | Status | Source |
|------|--------|--------|
| RSV-CE Bible | ❌ Copyrighted | Cannot find free legal source |
| The Fathers Know Best | ❌ Not found | Check Amazon/Catholic publishers |
| City of God - St. Augustine | 🔍 Search | Telegram or Internet Archive |
| Confessions - St. Augustine | 🔍 Search | Telegram or Internet Archive |
| Imitation of Christ - Thomas à Kempis | 🔍 Search | Public domain |
| More Papal Encyclicals | 🔍 Search | Vatican.va has many |

**Tasks**:
1. Search Telegram channel for Augustine, Kempis works
2. Search Internet Archive / Project Gutenberg for public domain texts
3. Download Vatican.va encyclicals as PDF
4. Update `PRIORITY_FILES` in `scripts/create_assistant.py`
5. Run script to create new assistant with more files
6. Update `.env` with new `ASSISTANT_ID`
7. Notify Deploy Agent to redeploy

**How to Upload New Books**:
```bash
cd /Users/lukereiser/PadreGPT
source .venv/bin/activate

# 1. Add files to downloads/telegram_pdfs/2025-12/
# 2. Edit scripts/create_assistant.py - add to PRIORITY_FILES list
# 3. Run:
python scripts/create_assistant.py

# 4. Copy new ASSISTANT_ID from output
# 5. Update .env with new ASSISTANT_ID
# 6. Commit and push to trigger Railway redeploy
```

---

### 🤖 TELEGRAM AGENT

**Mission**: Create a Telegram bot interface for Padre GPT

**Current State**:
- ❌ Not started
- ✅ Telegram API credentials exist in `.env`
- ✅ `telethon` library installed

**Architecture Options**:

**Option A: python-telegram-bot (Recommended)**
```
User → Telegram Bot → OpenAI Assistants API → Response
```
- Simple, direct integration
- Use `python-telegram-bot` library
- Store thread IDs per user for conversation continuity

**Option B: Telethon User Bot**
- More complex, uses user account
- Can access channels/groups
- Overkill for simple bot

**Tasks**:
1. Create new Telegram bot via @BotFather
2. Get bot token
3. Create `telegram_bot.py` script
4. Implement:
   - `/start` command - Welcome message
   - Message handler - Forward to OpenAI Assistant
   - Thread management per user (store in SQLite or JSON)
5. Deploy alongside Streamlit (or separate Railway service)
6. Add bot token to `.env`

**Files to Create**:
- `telegram_bot.py` - Main bot script
- `bot_config.py` - Bot settings and prompts

---

### 🎨 UI/UX AGENT

**Mission**: Make the Streamlit interface beautiful and user-friendly

**Current State**:
- ✅ Basic Streamlit app working
- ⚠️ Generic styling (needs Catholic aesthetic)
- ⚠️ Missing features

**Current `app.py` Features**:
- Chat interface with history
- New conversation button
- Basic Catholic-themed colors (beige/brown)

**Improvements Needed**:
1. **Visual Design**:
   - Add Padre GPT logo/icon
   - Better typography (serif fonts for Catholic feel)
   - Stained glass or parchment backgrounds
   - Cross/religious iconography (tasteful)

2. **UX Features**:
   - Source citations with expandable sections
   - "Ask about..." suggestion chips
   - Export conversation as PDF
   - Dark mode toggle
   - Mobile responsiveness

3. **Content**:
   - About page explaining the assistant
   - List of source documents
   - Disclaimer about AI limitations

**Files to Edit**:
- `app.py` - Main Streamlit application

---

## 📊 PROJECT STATUS DASHBOARD

### Deployment Status
| Component | Status | URL |
|-----------|--------|-----|
| GitHub Repo | ✅ Live | github.com/lukereiser/PadreGPT |
| Railway Project | ✅ Created | railway.com (beneficial-strength) |
| Railway Domain | 🔄 Pending | Need to generate |
| Custom Domain | 🔄 Pending | chat.projectpio.com |
| GoDaddy DNS | 🔄 Pending | CNAME record needed |

### Feature Status
| Feature | Status | Owner |
|---------|--------|-------|
| Web Chat | 🔄 Deploying | Deploy Agent |
| Telegram Bot | ❌ Not Started | Telegram Agent |
| Content Updates | ✅ Functional | Content Agent |
| UI Improvements | ❌ Not Started | UI/UX Agent |

---

## 📁 Project Structure

```
PadreGPT/
├── .env                          # API credentials (gitignored)
├── .venv/                        # Python virtual environment
├── app.py                        # Streamlit web interface
├── requirements.txt              # Python dependencies
├── README.md                     # This file (source of truth)
├── downloads/
│   └── telegram_pdfs/
│       └── 2025-12/              # Downloaded PDFs (77 files, 808MB)
├── scripts/
│   ├── create_assistant.py       # Creates OpenAI Assistant
│   ├── telegram_pdf_downloader.py    # Downloads from Telegram
│   └── print_telegram_session_string.py
└── state/
    └── telegram_downloader_state.json
```

---

## 🔑 Credentials Reference

### Environment Variables (`.env`)
```bash
# Telegram API
TELEGRAM_API_ID=30284703
TELEGRAM_API_HASH=0ef7193213c48e0777e72b8bb026eae4
TELEGRAM_SESSION_STRING=1AZWarz...

# OpenAI
OPENAI_API_KEY=sk-proj-843d...
OPENAI_ASSISTANT_ID=asst_IPSDeTq1kitWzQucX3m5g5uz

# Future: Telegram Bot Token
# TELEGRAM_BOT_TOKEN=...
```

### External Accounts
- **Railway**: User logged in, project `beneficial-strength`
- **GoDaddy**: User logged in, domain `projectpio.com`
- **GitHub**: Repo at `lukereiser/PadreGPT`
- **Telegram**: Phone +1 415 312 4656, 2FA: Novice945*

---

## 🚀 Quick Start for Agents

### Local Development
```bash
cd /Users/lukereiser/PadreGPT
source .venv/bin/activate
streamlit run app.py --server.port 8501
# Open http://localhost:8501
```

### Download More Telegram PDFs
```bash
python scripts/telegram_pdf_downloader.py --channel "-1001802265936" --limit 100
```

### Create New Assistant (after adding books)
```bash
python scripts/create_assistant.py
# Update OPENAI_ASSISTANT_ID in .env with new ID
```

### Deploy Changes
```bash
git add .
git commit -m "Description of changes"
git push origin main
# Railway auto-deploys from main branch
```

---

## 📝 Changelog

### 2024-12-30 - Founder Agent Session
- Created agent strategy with 5 specialized roles
- Documented deployment blockers (Railway domain + GoDaddy DNS)
- Updated README as coordination hub
- Defined tasks for Deploy, Content, Telegram, UI/UX agents

### Previous Sessions
- Set up Telegram API and downloaded 77 PDFs
- Switched from Custom GPT to Assistants API
- Created Streamlit web interface
- Uploaded 16 theological texts to Assistant
- Set up Railway deployment (pending domain)

---

## 🎯 Next Actions by Priority

### 🔴 HIGH - Deploy Agent
1. Generate Railway domain (port 8501)
2. Add custom domain `chat.projectpio.com`
3. Configure GoDaddy CNAME
4. Verify site is live

### 🟡 MEDIUM - Content Agent
1. Search for Augustine & Kempis works
2. Add more source documents
3. Optimize file selection for quality

### 🟢 LOW - Telegram Agent
1. Create bot with @BotFather
2. Implement basic chat functionality
3. Deploy as separate service

### 🔵 LOW - UI/UX Agent
1. Improve visual design
2. Add source citations
3. Mobile optimization

---

*Last updated: 2024-12-30 by Founder Agent*
