# 🦆 Discord Economy Bot

A full-featured Discord economy bot with jobs, gambling games, investing, fishing/hunting/mining, and more.

---

## 🚀 Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your bot token
Open `config.py` and replace `bot token here` with your actual bot token from the [Discord Developer Portal](https://discord.com/developers/applications).

```python
TOKEN = "your_real_token_here"
```

### 3. Run the bot
```bash
python bot.py
```

---

## 📁 File Structure

```
discord_economy_bot/
├── bot.py            # Main entry point
├── config.py         # All settings & cooldowns (edit here)
├── database.py       # SQLite async helpers
├── requirements.txt
└── cogs/
    └── economy.py    # All commands
```

The bot creates `economy.db` automatically on first run.

---

## ⚙️ Configuration (`config.py`)

| Setting | Default | Description |
|---|---|---|
| `PREFIX` | `.` | Command prefix |
| `DAILY_AMOUNT` | 500 | Daily reward coins |
| `DAILY_COOLDOWN` | 86400 | 24 hours (seconds) |
| `WORK_COOLDOWN` | 3600 | 1 hour |
| `BEG_COOLDOWN` | 300 | 5 minutes |
| `FISH/HUNT/MINE_COOLDOWN` | 1800 | 30 minutes each |
| `ROB_COOLDOWN` | 3600 | 1 hour |
| `CRIME_COOLDOWN` | 7200 | 2 hours |

---

## 💰 Commands Reference

### Page 1 — Basics
| Command | Description |
|---|---|
| `.balance` / `.bal [@user]` | Check wallet & bank balance |
| `.daily` | Claim daily coins (24h cooldown) |
| `.work` | Earn coins from your job (1h cooldown) |
| `.beg` | Beg strangers for coins (5m cooldown) |
| `.deposit` / `.dep <amount\|all>` | Move coins to bank |
| `.withdraw` / `.with <amount\|all>` | Move coins from bank |
| `.shop` | View all items for sale |
| `.buy <item>` | Purchase an item |
| `.use <item>` | Activate a usable item |
| `.inventory` / `.inv [@user]` | View your items |

### Page 2 — Social & Gambling
| Command | Description |
|---|---|
| `.give` / `.pay @user <amount>` | Transfer coins |
| `.leaderboard` / `.lb` | Server richest users |
| `.coinflip` / `.cf <amount\|all>` | 50/50 coin flip |
| `.fish` | Fish (requires Fishing Rod) |
| `.rob` / `.steal @user` | Rob someone's wallet (45% success) |
| `.lottery` | View pool; draws at 5+ participants |
| `.choosejob [job]` | Pick a career |
| `.jobstatus` | XP, level & promotion info |
| `.crime <bank\|shoplift\|payroll>` | High-risk crimes |
| `.sell <item> <amount>` | Sell inventory items |

### Page 3 — Advanced
| Command | Description |
|---|---|
| `.invest [company] [amount]` | Invest in companies |
| `.investstatus` | Check returns |
| `.hunt` | Hunt animals (requires Hunting Bow) |
| `.mine` | Mine ores (requires Pickaxe) |
| `.doorgame <amount>` | Pick a door: 1/3 wins up to x3 |
| `.ducktowers <amount>` | Climb floors for multipliers |
| `.mines <amount> [mine_count]` | Minesweeper gambling game |
| `.passive` | Toggle robbery protection |

---

## 🛒 Shop Items

| Item | Price | Effect |
|---|---|---|
| Fishing Rod | 500 | Unlock `.fish` |
| Hunting Bow | 800 | Unlock `.hunt` |
| Pickaxe | 600 | Unlock `.mine` |
| Bank Upgrade | 5,000 | Doubles bank limit |
| Lucky Charm | 2,000 | +50% income for 1 hour |
| Padlock | 1,500 | Rob protection for 24h |
| Lottery Ticket | 100 | Enter the lottery pool |

---

## 🏢 Investment Companies

| Company | Risk | Return Range | Duration |
|---|---|---|---|
| WaterWing Inc | 🟢 Low | 103–115% | 30 min |
| DuckTech | 🟢 Low | 105–120% | 1 hour |
| QuackCorp | 🟡 Medium | 90–150% | 2 hours |
| Mallard Markets | 🟡 Medium | 85–180% | 3 hours |
| PondStocks | 🔴 High | 50–300% | 4 hours |

---

## 🎮 Games

### Door Game
Pick one of 3 doors. One hides a prize worth x1.5–x3 your bet. No prize = full loss.

### Duck Towers
Climb 5 floors. Each floor multiplies your bet (x1.2 → x5.0). Hit a trap and lose everything. Cash out anytime with 💰.

### Mines (3×3 grid)
Bet coins, choose how many mines (1–8). Reveal safe tiles to increase your multiplier. Hit a mine = lose. React 💰 anytime to cash out.

---

## 🔒 Required Bot Permissions

- Read Messages / Send Messages
- Add Reactions
- Manage Messages (for reaction cleanup)
- Embed Links
- Read Message History
