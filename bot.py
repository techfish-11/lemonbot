import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import traceback  # エラー詳細を取得するために必要

# .envファイルから環境変数をロード
load_dotenv()

# トークンを環境変数から取得
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)  # `commands.Bot`を使用

ADMIN_USER_ID = 1310198598213963858  # 通知を受け取る管理者のユーザーID

# エラーハンドリング
@bot.event
async def on_error(event, *args, **kwargs):
    """イベントエラーを処理"""
    try:
        # チャンネルにエラーメッセージを送信
        channel = args[0].channel if args and hasattr(args[0], "channel") else None
        if channel:
            await channel.send(
                "エラーが発生したようです。bot管理者にエラーの詳細が送信されました。"
            )
        
        # 管理者にエラーの詳細をDM
        admin_user = await bot.fetch_user(ADMIN_USER_ID)
        if admin_user:
            error_details = traceback.format_exc()
            await admin_user.send(f"エラーが発生しました。\n\n```\n{error_details}\n```")
        
        # エラー詳細をコンソールに出力
        print(f"エラー発生: {traceback.format_exc()}")

    except Exception as inner_error:
        # エラーハンドリング中にエラーが発生した場合もその詳細を出力
        print(f"エラーハンドリング中にエラーが発生しました: {inner_error}")

@bot.event
async def on_command_error(ctx, error):
    """コマンド実行時のエラーハンドリング"""
    await ctx.send("エラーが発生しました。管理者に通知されました。")

    # 管理者に通知
    admin_user = await bot.fetch_user(ADMIN_USER_ID)
    if admin_user:
        error_details = traceback.format_exc()
        await admin_user.send(f"コマンドエラーが発生しました。\n\n```\n{error_details}\n```")

    # エラー詳細をコンソールに出力
    print(f"コマンドエラー発生: {traceback.format_exc()}")

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
