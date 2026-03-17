import discord
from discord.ext import commands
import asyncio
from config import TOKEN, PREFIX

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None,          # We use our own .help
    case_insensitive=True
)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"   Prefix: {PREFIX}")
    await bot.change_presence(activity=discord.Game(name=f"{PREFIX}help"))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(
            description=f"❌ Missing argument: `{error.param.name}`\nUse `.help` to see correct usage.",
            color=discord.Color.red()
        ))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=discord.Embed(
            description="❌ Invalid argument. Check `.help` for correct usage.",
            color=discord.Color.red()
        ))
    elif isinstance(error, commands.CommandNotFound):
        pass  # Silently ignore unknown commands
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(embed=discord.Embed(
            description="❌ User not found!",
            color=discord.Color.red()
        ))
    else:
        raise error


async def main():
    async with bot:
        await bot.load_extension("cogs.economy")
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
