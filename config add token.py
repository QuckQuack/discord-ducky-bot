TOKEN = "bot token here"
PREFIX = "."
DB_PATH = "economy.db"

# Embed color
EMBED_COLOR = 0x5865F2

# Cooldowns (in seconds)
DAILY_COOLDOWN   = 86400   # 24 hours
WORK_COOLDOWN    = 3600    # 1 hour
BEG_COOLDOWN     = 300     # 5 minutes
FISH_COOLDOWN    = 1800    # 30 minutes
HUNT_COOLDOWN    = 1800    # 30 minutes
MINE_COOLDOWN    = 1800    # 30 minutes
ROB_COOLDOWN     = 3600    # 1 hour
CRIME_COOLDOWN   = 7200    # 2 hours
JOB_CHANGE_COOLDOWN = 86400  # 24 hours

# Economy values
DAILY_AMOUNT = 500
WORK_MIN     = 100
WORK_MAX     = 500
BEG_MIN      = 10
BEG_MAX      = 200

# Job configs
JOBS = {
    "farmer":     {"base_pay": 200, "emoji": "🌾"},
    "miner":      {"base_pay": 300, "emoji": "⛏️"},
    "hunter":     {"base_pay": 350, "emoji": "🏹"},
    "fisher":     {"base_pay": 250, "emoji": "🎣"},
    "programmer": {"base_pay": 500, "emoji": "💻"},
    "doctor":     {"base_pay": 600, "emoji": "🏥"},
    "chef":       {"base_pay": 400, "emoji": "👨‍🍳"},
    "artist":     {"base_pay": 350, "emoji": "🎨"},
}
