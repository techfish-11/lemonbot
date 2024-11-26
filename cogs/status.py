import discord
from discord.ext import commands
import asyncio

# Botの初期化
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

async def get_router_latency(router_ip):
    """
    ルーターレイテンシを取得するためにpingコマンドを実行します。
    :param router_ip: ルーターのIPアドレス
    :return: レイテンシの値（ms）またはエラー
    """
    try:
        # pingコマンドを非同期で実行
        process = await asyncio.create_subprocess_exec(
            'ping', '-c', '1', router_ip,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            # pingの出力を解析
            output = stdout.decode()
            for line in output.splitlines():
                if "time=" in line:
                    latency = line.split("time=")[1].split(" ")[0]
                    return f"{latency} ms"
        return "計測不可"
    except Exception as e:
        return f"エラー: {e}"

@bot.slash_command(name="status", description="Botのステータスを表示します。")
async def status(ctx):
    # Discord APIのレイテンシ
    discord_latency = round(bot.latency * 1000)  # 秒 -> ミリ秒に変換
    # ネットワークルーターレイテンシ
    router_ip = "192.168.1.1"  # 適切なIPアドレスを設定してください
    router_latency = await get_router_latency(router_ip)

    # ステータスメッセージの作成
    status_message = (
        f"**Discord APIレイテンシ**: `{discord_latency} ms`\n"
        f"**ネットワークルーターレイテンシ**: `{router_latency}`\n"
        f"ステータス詳細は、[こちら](https://status.sakana11.org)をご覧ください。\n"
        "Deploy RunnerでLemonBotは動作しています。"
    )

    # メッセージを送信
    await ctx.respond(status_message)

# Botの起動
bot.run('YOUR_BOT_TOKEN')  # あなたのBotトークンを入力