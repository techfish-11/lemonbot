import discord
from discord.ext import commands, tasks
import sqlite3
from datetime import datetime

# データベース接続
def get_db_connection():
    conn = sqlite3.connect('lemoncoin.db')
    conn.row_factory = sqlite3.Row
    return conn

class CoinAdjustment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.adjust_coins.start()  # 5分ごとにコインを監視するタスクを開始

    def cog_unload(self):
        """Cogがアンロードされる際にタスクを停止"""
        self.adjust_coins.cancel()

    @tasks.loop(minutes=5)  # 5分ごとに実行
    async def adjust_coins(self):
        """ユーザーのコインを監視し、必要に応じて調整"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # ユーザーのコイン残高を全件取得
        cursor.execute('SELECT user_id, coins FROM users')
        users = cursor.fetchall()

        for user in users:
            user_id = user['user_id']
            coins = user['coins']

            # 小数が含まれているか確認し、含まれていれば切り捨てる
            if coins != int(coins):
                # コインが小数の場合、整数に切り捨てて保存
                new_coins = int(coins)
                cursor.execute('UPDATE users SET coins = ? WHERE user_id = ?', (new_coins, user_id))
                conn.commit()

                # ユーザーに通知
                user = await self.bot.fetch_user(user_id)
                await user.send(f"こんにちは！あなたのレモンコイン残高に小数が含まれていたため、コインの数が調整されました。"
                                 f"現在のコイン残高は {new_coins} コインです。ご確認ください。")

        conn.close()

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(CoinAdjustment(bot))
