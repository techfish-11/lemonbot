import discord
from discord.ext import commands
import random
import sqlite3
from datetime import datetime

# コインのデータベース接続
def get_db_connection():
    conn = sqlite3.connect('lemoncoin.db')
    conn.row_factory = sqlite3.Row
    return conn

class Gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="gacha", description="レモンコイン1000でガチャを引きます。")
    async def gacha(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        conn = get_db_connection()
        cursor = conn.cursor()

        # ユーザーの現在のコイン数を取得
        cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()

        if user_data is None:
            await interaction.response.send_message("あなたはまだ登録されていません。")
            return

        current_coins = user_data['coins']

        # ガチャに必要なコインがあるかチェック
        if current_coins < 1000:
            await interaction.response.send_message("レモンコインが足りません。ガチャを引くには1000レモンコインが必要です。")
            return

        # 1000レモンコインを引く
        new_coins = current_coins - 1000
        cursor.execute("UPDATE users SET coins = ? WHERE user_id = ?", (new_coins, user_id))
        conn.commit()

        # ガチャ結果の計算（1000分の1の確率で2000レモンコイン）
        result = random.choices(
            ['2000_coins', '300_coins', '500_coins', 'item', 'nothing'],
            weights=[1, 400, 400, 100, 100],
            k=1
        )[0]

        # ガチャ結果に応じた処理
        if result == '2000_coins':
            reward = 2000
            new_coins += reward
            cursor.execute("UPDATE users SET coins = ? WHERE user_id = ?", (new_coins, user_id))
            conn.commit()
            result_message = f"おめでとうございます！2000レモンコインを獲得しました！現在のレモンコインは {new_coins} です。"
        elif result == '300_coins':
            reward = 300
            new_coins += reward
            cursor.execute("UPDATE users SET coins = ? WHERE user_id = ?", (new_coins, user_id))
            conn.commit()
            result_message = f"300レモンコインを獲得しました！現在のレモンコインは {new_coins} です。"
        elif result == '500_coins':
            reward = 500
            new_coins += reward
            cursor.execute("UPDATE users SET coins = ? WHERE user_id = ?", (new_coins, user_id))
            conn.commit()
            result_message = f"500レモンコインを獲得しました！現在のレモンコインは {new_coins} です。"
        elif result == 'item':
            # アイテムをランダムで出す（例: 限定アイテム、ボーナス）
            item = random.choice(["限定レモン", "レモンジュース", "レモンケーキ"])
            result_message = f"アイテム「{item}」を獲得しました！"
        else:
            result_message = "残念！今回は何も獲得できませんでした。またチャレンジしてください。"

        # 結果を埋め込みメッセージで送信
        embed = discord.Embed(title="ガチャ結果", description=result_message, color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(Gacha(bot))
