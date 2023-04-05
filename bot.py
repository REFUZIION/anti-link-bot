import asyncio
import os
import re

import disnake
from disnake.ext import commands

with open('.env') as f:
    for line in f:
        key, value = line.strip().split('=')
        os.environ[key] = value

CHANNEL_ID = 622096446237179924
ALLOWED_KEYWORDS = [".mp4", ".gif", ".png", ".jpg", ".jpeg", "mp4", "gif", "png", "jpg", "jpeg"]


class Bot(commands.AutoShardedInteractionBot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def on_connect(self) -> None:
        print(f"Logged in as {self.user}!")

    async def on_ready(self) -> None:
        await self.change_presence(
            activity=disnake.Activity(
                name="for forbidden urls",
                type=disnake.ActivityType.watching
            ),
            status=disnake.Status.online
        )


intents = disnake.Intents.all()
client = commands.Bot(command_prefix='?', intents=intents)


@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID:
        return

    if message.author == client.user:
        return

    url_match = re.search("(?P<url>https?://[^\s]+)", message.content)
    if url_match:
        url = url_match.group("url")

        if any(keyword in url for keyword in ALLOWED_KEYWORDS):
            pass
        else:
            await message.delete()

            bot_message = await message.channel.send(
                f"{message.author.mention} Links are not allowed, except for gifs and images.")
            await asyncio.sleep(5)
            await bot_message.delete()


if __name__ == '__main__':
    client = Bot(
        intents=intents
    )

    for dirPath, dirNames, filenames in os.walk('./cogs/'):
        for file in filenames:
            if not file.endswith('.py'):
                continue

            relative_path = os.path.relpath(os.path.join(dirPath, file), './cogs')

            module_name = relative_path.replace(os.path.sep, '.')[:-3]

            client.load_extension(f"cogs.{module_name}")
            print(f"cogs.{module_name} has been loaded!")

    client.run(os.environ['TOKEN'])
