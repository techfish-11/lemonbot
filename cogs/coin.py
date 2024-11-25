import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta

# データベース接続
def get_db_connection():
    conn = sqlite3.connect('lemoncoin.db')
    conn.row_factory = sqlite3.Row
    return conn

class Coin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="login-bonus", description="ログインボーナスを受け取ります。")
    async def login_bonus(self, interaction: discord.Interaction):
        """ログインボーナスの受け取り"""
        user_id = interaction.user.id
        conn = get_db_connection()
        cursor = conn.cursor()

        # 最後のログインボーナスの受取時刻を確認
        cursor.execute('SELECT last_bonus FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            # ミリ秒まで含めてパース
            try:
                last_bonus = datetime.strptime(result['last_bonus'], '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                last_bonus = datetime.strptime(result['last_bonus'], '%Y-%m-%d %H:%M:%S')  # フォーマットが異なる場合

            # 2時間以内であれば残り時間を表示
            time_diff = datetime.now() - last_bonus
            if time_diff < timedelta(hours=2):
                remaining_time = timedelta(hours=2) - time_diff
                minutes_remaining = remaining_time.total_seconds() // 60  # 残り時間を分に変換
                await interaction.response.send_message(f"まだボーナスを受け取ることができません。{int(minutes_remaining)}分後に受け取れます。")
                conn.close()
                return
        else:
            cursor.execute('INSERT INTO users (user_id, coins) VALUES (?, ?)', (user_id, 0))
            conn.commit()

        # ボーナスを付与
        cursor.execute('UPDATE users SET coins = coins + 500, last_bonus = ? WHERE user_id = ?', 
                    (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), user_id))  # ミリ秒まで含めて保存
        conn.commit()
        conn.close()

        await interaction.response.send_message(f"おめでとう！ 500レモンコインのログインボーナスを受け取りました！")

    # コイン残高を確認するコマンド
    @discord.app_commands.command(name="coin-balance", description="自分のレモンコイン残高を確認します。")
    async def coin_balance(self, interaction: discord.Interaction):
        """自分のレモンコイン残高を確認"""
        user_id = interaction.user.id
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            await interaction.response.send_message(f"あなたのレモンコイン残高は {result['coins']} コインです。")
        else:
            await interaction.response.send_message("まだレモンコインを受け取っていません。")

        conn.close()

    @discord.app_commands.command(name="transfer-coin", description="他のユーザーにレモンコインを譲渡します。")
    async def transfer_coin(self, interaction: discord.Interaction, recipient: discord.User, amount: int):
        """他のユーザーにレモンコインを譲渡"""
        user_id = interaction.user.id
        recipient_id = recipient.id

        if amount <= 0:
            await interaction.response.send_message("譲渡するコインは1以上にしてください。")
            return

        conn = get_db_connection()
        cursor = conn.cursor()

        # 自分のコイン残高を取得
        cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result and result['coins'] >= amount:
            # コインの譲渡（手数料なし）
            cursor.execute('UPDATE users SET coins = coins - ? WHERE user_id = ?', (amount, user_id))
            # 受取人がすでに登録されている場合、コインを追加、されていない場合は新規登録
            cursor.execute('INSERT INTO users (user_id, coins) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET coins = coins + ?', 
                        (recipient_id, amount, amount))
            conn.commit()
            conn.close()

            # 結果のメッセージ
            await interaction.response.send_message(
                f"{recipient.name}さんに {amount} レモンコインを譲渡しました！"
            )
        else:
            conn.close()
            await interaction.response.send_message("コインが不足しています。")


    # コインランキングを表示するコマンド
    @discord.app_commands.command(name="coin-ranking", description="レモンコインランキングを表示します。")
    async def coin_ranking(self, interaction: discord.Interaction):
        """レモンコインランキングを表示"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # コイン残高順に並べて上位5人を取得
        cursor.execute('SELECT user_id, coins FROM users ORDER BY coins DESC LIMIT 5')
        results = cursor.fetchall()

        # 埋め込みメッセージを作成
        embed = discord.Embed(title="レモンコインランキング", description="上位5人のレモンコイン所持者", color=discord.Color.green())

        # 上位5人のデータを埋め込む
        rank = 1
        for row in results:
            user = await self.bot.fetch_user(row['user_id'])
            embed.add_field(name=f"順位 {rank}", value=f"{user.name}: {row['coins']} コイン", inline=False)
            rank += 1

        # メッセージを送信
        await interaction.response.send_message(embed=embed)

        conn.close()

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(Coin(bot))
