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

@bot.event
async def on_message(message):
    if message.author == bot.user:
        # Botが送信したメッセージで、メンションを含む場合は削除
        if message.mentions or message.role_mentions or message.mention_everyone:
            await message.delete()  # メッセージを削除
            print("メンションを含むメッセージを削除しました。")
            
            # 削除したメッセージがあったチャンネルに通知を送信
            await message.channel.send(
                "⚠️ **迷惑対策のため、Botによるメッセージを削除しました。**\n"
                "Botによるメンションは許可されていません。",
                delete_after=5  # 通知を5秒後に自動削除
            )
        return
    # 他のコマンドが使えるようにする
    await bot.process_commands(message)

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
