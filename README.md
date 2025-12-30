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
- ✅ 77+ PDFs downloaded from Telegram (808MB)
- ✅ 20 files uploaded to Assistant (see list below)
- ✅ Added Augustine, Kempis works from Project Gutenberg

**Books Currently Uploaded (20 files)**:
| Book | Type | Size |
|------|------|------|
| **Core Theology** |  |  |
| Theology for Beginners - Frank Sheed | PDF | 832KB |
| A Catechism of Christian Doctrine (Ireland 1951) | PDF | 6.1MB |
| Catechism of the Catholic Church | PDF | ~3MB |
| **Thomas Aquinas** |  |  |
| Contra Errores Graecorum - Aquinas | PDF | 152KB |
| How to Study - St. Thomas Aquinas | PDF | 1.1MB |
| Summa Theologica Part 1 (Prima Pars) | TXT | ~2.9MB |
| Summa Theologica Part 1-2 (Prima Secundae) | TXT | ~2.9MB |
| Summa Theologica Part 2-2 (Secunda Secundae) Vol 1 | TXT | ~4.2MB |
| Summa Theologica Part 3 (Tertia Pars) | TXT | ~2.8MB |
| **Sacred Scripture** |  |  |
| Douay-Rheims Bible Complete | TXT | ~5.6MB |
| **Church Fathers** |  |  |
| St. Justin Martyr - First Apology | PDF | 136KB |
| St. Justin Martyr - Second Apology | PDF | 40KB |
| First Seven Ecumenical Councils | PDF | 2.1MB |
| **St. Augustine** |  |  |
| City of God - Volume I | TXT | ~1.3MB |
| City of God - Volume II | TXT | ~1.4MB |
| Confessions | TXT | ~617KB |
| **Spiritual Classics** |  |  |
| Imitation of Christ - Thomas à Kempis | TXT | ~375KB |
| **Papal & Spiritual** |  |  |
| Practice of Humility - Pope Leo XIII | PDF | 2.1MB |
| Uniformity with God's Will - St. Alphonsus | PDF | 148KB |
| Papal Encyclicals 1958-1981 | PDF | 27MB |

**Priority Books to Find/Add**:
| Book | Status | Source |
|------|--------|--------|
| RSV-CE Bible | ❌ Copyrighted | Cannot find free legal source |
| The Fathers Know Best | ❌ Not found | Check Amazon/Catholic publishers |
| City of God - St. Augustine | ✅ Added | Project Gutenberg |
| Confessions - St. Augustine | ✅ Added | Project Gutenberg |
| Imitation of Christ - Thomas à Kempis | ✅ Added | Project Gutenberg |
| More Papal Encyclicals | ✅ Have 1958-1981 | Consider adding pre-1958 |

**Tasks**:
1. ✅ Downloaded Augustine & Kempis from Project Gutenberg
2. ✅ Updated `PRIORITY_FILES` in `scripts/create_assistant.py`
3. ✅ Created new assistant with 20 files
4. ✅ Updated `.env` with new `ASSISTANT_ID`
5. 🔄 Consider adding: earlier Encyclicals (pre-1958), Didache, Letter to Diognetus

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
- ✅ Bot script created: `telegram_bot.py`
- ✅ Persistent thread storage (JSON)
- ✅ Procfile for Railway deployment
- 🔄 Need to create bot with @BotFather and add token

**Architecture**:
```
User → Telegram Bot → OpenAI Assistants API → Response
```

**Features Implemented**:
- `/start` — Welcome message with usage instructions
- `/new` — Clear conversation and start fresh
- `/help` — Show help and rate limit info
- Message handler → OpenAI Assistant with typing indicator
- Thread IDs persisted to `state/telegram_threads.json`
- Rate limiting (60 msg/hour default)
- Long message chunking (4000 char limit)

**Setup Instructions**:

1. **Create bot with @BotFather**:
   - Open Telegram, message `@BotFather`
   - Send `/newbot`
   - Name: `Padre GPT`
   - Username: `PadreGPTBot` (or available alternative)
   - Copy the bot token

2. **Add token to `.env`**:
   ```bash
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

3. **Run locally**:
   ```bash
   cd /Users/lukereiser/PadreGPT
   source .venv/bin/activate
   python telegram_bot.py
   ```

4. **Deploy to Railway**:
   - The Procfile includes both `web` and `bot` processes
   - Add `TELEGRAM_BOT_TOKEN` to Railway environment variables
   - Scale up the `bot` process in Railway dashboard

**Files**:
- `telegram_bot.py` — Main bot script (project root)
- `state/telegram_threads.json` — Persisted user threads
- `Procfile` — Railway process definitions

---

### 🎨 UI/UX AGENT

**Mission**: Make the Streamlit interface beautiful and user-friendly

**Current State**:
- ✅ Complete redesign implemented
- ✅ Medieval manuscript aesthetic
- ✅ All planned features added

**Implemented Features** (as of 2024-12-29):

1. **Visual Design** ✅:
   - Chi-Rho (☧) logo with Cinzel font
   - EB Garamond & Cormorant Garamond typography (elegant serifs)
   - Parchment/cream background with subtle cross pattern
   - Deep burgundy (#5C1A1B) & gold (#D4AF37) color palette
   - Gold-bordered decorative dividers
   - Medieval manuscript-inspired aesthetics

2. **UX Features** ✅:
   - **Suggestion chips**: 8 clickable topic buttons for new users
   - **Source citations**: Expandable sections showing referenced documents
   - **Tabbed interface**: "Ask Padre GPT" and "About & Sources" tabs
   - **Quick Topics sidebar**: One-click navigation to common topics
   - **Mobile responsive**: Optimized for all screen sizes
   - **Loading states**: Random reverent messages ("Consulting the sources...")

3. **Content** ✅:
   - Welcome message: "Welcome, Seeker of Truth" intro explaining capabilities
   - Source library: Complete list of available theological texts
   - AI disclaimer: Clear warnings about limitations and need for spiritual direction
   - How-to guide: Instructions for using the assistant
   - Footer: "Built with faith and code" + Magisterium disclaimer

**Design Inspiration**:
- Medieval illuminated manuscripts
- Vatican document aesthetics
- Stained glass color palettes
- Traditional Catholic typography

**Files**:
- `app.py` - Complete Streamlit application with all UI features

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
| Telegram Bot | 🔄 Code Ready (need token) | Telegram Agent |
| Content Updates | ✅ Functional | Content Agent |
| UI Improvements | ✅ Complete | UI/UX Agent |

---

## 📁 Project Structure

```
PadreGPT/
├── .env                          # API credentials (gitignored)
├── .venv/                        # Python virtual environment
├── app.py                        # Streamlit web interface
├── telegram_bot.py               # Telegram bot interface
├── Procfile                      # Railway process definitions
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
    ├── telegram_downloader_state.json
    └── telegram_threads.json     # Persisted bot conversations
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

### 2024-12-29 - Content Agent Session
- Downloaded 4 new books from Project Gutenberg:
  - City of God (Volumes I & II) - St. Augustine
  - Confessions - St. Augustine  
  - Imitation of Christ - Thomas à Kempis
- Updated `PRIORITY_FILES` to include 20 total files
- Created new Assistant (ID: `asst_QXrmyfNZoMzFPE42EbYLPZXK`)
- Updated `.env` with new Assistant ID

### 2024-12-29 - UI/UX Agent Session
- **Complete UI redesign** of `app.py` with Catholic/medieval aesthetic
- Added Chi-Rho (☧) logo with Cinzel font branding
- Implemented EB Garamond & Cormorant Garamond typography
- Created parchment background with subtle cross pattern
- Deep burgundy (#5C1A1B) & gold (#D4AF37) color palette
- Added 8 suggestion chips for new users
- Implemented expandable source citations
- Created "About & Sources" tab with full source library
- Added Quick Topics sidebar with one-click navigation
- Mobile responsive CSS for all screen sizes
- AI disclaimer and usage instructions

### 2024-12-29 - Telegram Agent Session
- Created `telegram_bot.py` with OpenAI Assistants API integration
- Added persistent thread storage (JSON) for conversation continuity
- Implemented /start, /new, /help commands
- Added rate limiting (60 msg/hour default)
- Created Procfile for Railway deployment (web + bot processes)
- Updated README with bot setup instructions

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
1. ✅ Added Augustine (City of God, Confessions) from Project Gutenberg
2. ✅ Added Imitation of Christ (Thomas à Kempis)
3. ✅ 20 files now uploaded to Assistant
4. 🔄 Consider adding: Didache, Letter to Diognetus, more Church Fathers

### 🟢 LOW - Telegram Agent
1. ✅ Bot script created with persistent storage
2. 🔄 Create bot with @BotFather and get token
3. Add token to `.env` and test locally
4. Deploy bot process on Railway

### 🔵 COMPLETE - UI/UX Agent
1. ✅ Medieval manuscript aesthetic with serif fonts
2. ✅ Source citations with expandable sections
3. ✅ Mobile responsive design
4. ✅ Suggestion chips for new users
5. ✅ About page with source library

---

*Last updated: 2024-12-29 by Content Agent*
