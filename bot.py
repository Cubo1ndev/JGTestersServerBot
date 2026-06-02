import asyncio
import discord
from discord.ext import commands

import config
import database

COGS = [
    "cogs.admin",
    "cogs.user",
    "cogs.history",
]

intents = discord.Intents.default()
intents.members = True


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        database.set_path(config.DB_PATH)
        await database.init_db()

        for cog in COGS:
            await self.load_extension(cog)

        if config.GUILD_ID:
            guild = discord.Object(id=config.GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print(f"Guild ID: {config.GUILD_ID or 'global'}")
        print("------")


def main() -> None:
    bot = Bot()
    bot.run(config.TOKEN)


if __name__ == "__main__":
    main()
