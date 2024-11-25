import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio


# .envファイルから環境変数をロード
load_dotenv()

# トークンを環境変数から取得
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)  # `commands.Bot`を使用

# コグ（モジュール）をロード
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    # コグを非同期で並行してロード
    tasks = []
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            # コグを非同期でロードするタスクを追加
            tasks.append(bot.load_extension(f'cogs.{filename[:-3]}')) 

    # コグを全てロード
    await asyncio.gather(*tasks)

    # コマンドを一度だけ同期
    await bot.tree.sync()

    print("All cogs loaded and commands synced!")

# Botの起動
bot.run(TOKEN)
