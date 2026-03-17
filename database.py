import aiosqlite
import time
from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id    INTEGER,
                guild_id   INTEGER,
                wallet     INTEGER DEFAULT 0,
                bank       INTEGER DEFAULT 0,
                bank_limit INTEGER DEFAULT 10000,
                total_earned INTEGER DEFAULT 0,
                job        TEXT    DEFAULT NULL,
                job_level  INTEGER DEFAULT 1,
                job_xp     INTEGER DEFAULT 0,
                passive_mode INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, guild_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                user_id   INTEGER,
                guild_id  INTEGER,
                item_name TEXT,
                quantity  INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, guild_id, item_name)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS cooldowns (
                user_id   INTEGER,
                guild_id  INTEGER,
                command   TEXT,
                last_used REAL,
                PRIMARY KEY (user_id, guild_id, command)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS investments (
                user_id     INTEGER,
                guild_id    INTEGER,
                company     TEXT,
                amount      INTEGER,
                invested_at REAL,
                returns_at  REAL,
                PRIMARY KEY (user_id, guild_id, company)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS lottery (
                guild_id INTEGER,
                user_id  INTEGER,
                tickets  INTEGER DEFAULT 1,
                PRIMARY KEY (guild_id, user_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS lottery_pool (
                guild_id INTEGER PRIMARY KEY,
                pool     INTEGER DEFAULT 0
            )
        """)
        await db.commit()


# ─── User helpers ────────────────────────────────────────────────────────────

async def get_user(user_id: int, guild_id: int) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM users WHERE user_id=? AND guild_id=?",
            (user_id, guild_id)
        )
        row = await cur.fetchone()
        if row is None:
            await db.execute(
                "INSERT OR IGNORE INTO users (user_id, guild_id) VALUES (?,?)",
                (user_id, guild_id)
            )
            await db.commit()
            cur = await db.execute(
                "SELECT * FROM users WHERE user_id=? AND guild_id=?",
                (user_id, guild_id)
            )
            row = await cur.fetchone()
        return dict(row)


async def update_wallet(user_id: int, guild_id: int, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET wallet = wallet + ? WHERE user_id=? AND guild_id=?",
            (amount, user_id, guild_id)
        )
        if amount > 0:
            await db.execute(
                "UPDATE users SET total_earned = total_earned + ? WHERE user_id=? AND guild_id=?",
                (amount, user_id, guild_id)
            )
        await db.commit()


async def update_bank(user_id: int, guild_id: int, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET bank = bank + ? WHERE user_id=? AND guild_id=?",
            (amount, user_id, guild_id)
        )
        await db.commit()


async def set_passive_mode(user_id: int, guild_id: int, active: bool):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET passive_mode=? WHERE user_id=? AND guild_id=?",
            (1 if active else 0, user_id, guild_id)
        )
        await db.commit()


async def update_bank_limit(user_id: int, guild_id: int, multiplier: float = 2.0):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET bank_limit = CAST(bank_limit * ? AS INTEGER) WHERE user_id=? AND guild_id=?",
            (multiplier, user_id, guild_id)
        )
        await db.commit()


# ─── Cooldown helpers ────────────────────────────────────────────────────────

async def get_cooldown(user_id: int, guild_id: int, command: str) -> float:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT last_used FROM cooldowns WHERE user_id=? AND guild_id=? AND command=?",
            (user_id, guild_id, command)
        )
        row = await cur.fetchone()
        return row[0] if row else 0.0


async def set_cooldown(user_id: int, guild_id: int, command: str, timestamp: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO cooldowns (user_id, guild_id, command, last_used) VALUES (?,?,?,?)",
            (user_id, guild_id, command, timestamp)
        )
        await db.commit()


# ─── Inventory helpers ───────────────────────────────────────────────────────

async def get_inventory(user_id: int, guild_id: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM inventory WHERE user_id=? AND guild_id=? AND quantity > 0",
            (user_id, guild_id)
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def add_item(user_id: int, guild_id: int, item_name: str, quantity: int = 1):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO inventory (user_id, guild_id, item_name, quantity) VALUES (?,?,?,?)
               ON CONFLICT(user_id, guild_id, item_name) DO UPDATE SET quantity = quantity + ?""",
            (user_id, guild_id, item_name, quantity, quantity)
        )
        await db.commit()


async def remove_item(user_id: int, guild_id: int, item_name: str, quantity: int = 1) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT quantity FROM inventory WHERE user_id=? AND guild_id=? AND item_name=?",
            (user_id, guild_id, item_name)
        )
        row = await cur.fetchone()
        if not row or row[0] < quantity:
            return False
        await db.execute(
            "UPDATE inventory SET quantity = quantity - ? WHERE user_id=? AND guild_id=? AND item_name=?",
            (quantity, user_id, guild_id, item_name)
        )
        await db.commit()
        return True


async def has_item(user_id: int, guild_id: int, item_name: str) -> bool:
    inv = await get_inventory(user_id, guild_id)
    return any(i['item_name'] == item_name and i['quantity'] > 0 for i in inv)


# ─── Leaderboard helpers ─────────────────────────────────────────────────────

async def get_leaderboard(guild_id: int, limit: int = 10) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT user_id, wallet+bank AS total FROM users WHERE guild_id=? ORDER BY total DESC LIMIT ?",
            (guild_id, limit)
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def get_rank(user_id: int, guild_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """SELECT COUNT(*)+1 FROM users
               WHERE guild_id=? AND (wallet+bank) > (
                   SELECT wallet+bank FROM users WHERE user_id=? AND guild_id=?
               )""",
            (guild_id, user_id, guild_id)
        )
        row = await cur.fetchone()
        return row[0] if row else 1


# ─── Lottery helpers ─────────────────────────────────────────────────────────

async def add_lottery_ticket(user_id: int, guild_id: int, cost: int = 100):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO lottery (guild_id, user_id, tickets) VALUES (?,?,1)
               ON CONFLICT(guild_id, user_id) DO UPDATE SET tickets = tickets + 1""",
            (guild_id, user_id)
        )
        await db.execute(
            """INSERT INTO lottery_pool (guild_id, pool) VALUES (?,?)
               ON CONFLICT(guild_id) DO UPDATE SET pool = pool + ?""",
            (guild_id, cost, cost)
        )
        await db.commit()


async def get_lottery_pool(guild_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT pool FROM lottery_pool WHERE guild_id=?", (guild_id,))
        row = await cur.fetchone()
        return row[0] if row else 0


async def get_lottery_participants(guild_id: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT user_id, tickets FROM lottery WHERE guild_id=?", (guild_id,))
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def clear_lottery(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM lottery WHERE guild_id=?", (guild_id,))
        await db.execute("DELETE FROM lottery_pool WHERE guild_id=?", (guild_id,))
        await db.commit()


# ─── Job helpers ─────────────────────────────────────────────────────────────

async def update_job(user_id: int, guild_id: int, job: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET job=?, job_level=1, job_xp=0 WHERE user_id=? AND guild_id=?",
            (job, user_id, guild_id)
        )
        await db.commit()


async def add_job_xp(user_id: int, guild_id: int, xp: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET job_xp = job_xp + ? WHERE user_id=? AND guild_id=?",
            (xp, user_id, guild_id)
        )
        cur = await db.execute(
            "SELECT job_xp, job_level FROM users WHERE user_id=? AND guild_id=?",
            (user_id, guild_id)
        )
        row = await cur.fetchone()
        if row:
            total_xp, level = row
            xp_needed = level * 100
            if total_xp >= xp_needed:
                await db.execute(
                    "UPDATE users SET job_level = job_level + 1, job_xp = 0 WHERE user_id=? AND guild_id=?",
                    (user_id, guild_id)
                )
        await db.commit()


# ─── Investment helpers ──────────────────────────────────────────────────────

async def get_investments(user_id: int, guild_id: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM investments WHERE user_id=? AND guild_id=?",
            (user_id, guild_id)
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def add_investment(user_id: int, guild_id: int, company: str,
                         amount: int, invested_at: float, returns_at: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT OR REPLACE INTO investments
               (user_id, guild_id, company, amount, invested_at, returns_at)
               VALUES (?,?,?,?,?,?)""",
            (user_id, guild_id, company, amount, invested_at, returns_at)
        )
        await db.commit()


async def remove_investment(user_id: int, guild_id: int, company: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM investments WHERE user_id=? AND guild_id=? AND company=?",
            (user_id, guild_id, company)
        )
        await db.commit()
