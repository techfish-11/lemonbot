import discord
from discord.ext import commands
import sqlite3
import re

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def sanitize_message(self, message: str) -> str:
        """メンションを無効化するため、@を全角＠に変換するか、他の方法でメンションを防ぐ。"""
        return re.sub(r'@', '＠', message)  # メンション無効化

    @discord.app_commands.command(name="afk-start", description="AFK状態にする。通知したいことを設定できます。")
    async def afk_start(self, interaction: discord.Interaction, message: str):
        """ユーザーをAFK状態に設定し、メッセージを保存する"""
        user_id = interaction.user.id
        conn = sqlite3.connect("AFK.db")
        cursor = conn.cursor()

        # AFKテーブルがなければ作成
        cursor.execute('''CREATE TABLE IF NOT EXISTS afk_users (
                            user_id INTEGER PRIMARY KEY,
                            message TEXT)''')
        
        sanitized_message = self.sanitize_message(message)
        cursor.execute('INSERT OR REPLACE INTO afk_users (user_id, message) VALUES (?, ?)', 
                       (user_id, sanitized_message))
        conn.commit()
        conn.close()

        await interaction.response.send_message(
            f"{interaction.user.name}さんはAFK状態になりました。メッセージ: {sanitized_message}",
            allowed_mentions=discord.AllowedMentions.none()  # メンション無効化
        )

    @discord.app_commands.command(name="afk-end", description="AFK状態を解除します。")
    async def afk_end(self, interaction: discord.Interaction):
        """AFK状態を解除"""
        user_id = interaction.user.id
        conn = sqlite3.connect("AFK.db")
        cursor = conn.cursor()

        cursor.execute('DELETE FROM afk_users WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()

        await interaction.response.send_message(
            f"{interaction.user.name}さんのAFK状態が解除されました。",
            allowed_mentions=discord.AllowedMentions.none()  # メンション無効化
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """メンションされたAFKユーザーに自動で反応"""
        if message.author.bot:
            return  # botには反応しない

        mentioned_users = message.mentions
        conn = sqlite3.connect("AFK.db")
        cursor = conn.cursor()

        for user in mentioned_users:
            cursor.execute('SELECT message FROM afk_users WHERE user_id = ?', (user.id,))
            result = cursor.fetchone()

            if result:
                afk_message = result[0]
                sanitized_message = self.sanitize_message(afk_message)
                await message.channel.send(
                    f"**{user.name}さんは現在AFK中です。**\n"
                    f"ユーザーからのお手紙：\n{sanitized_message}",
                    allowed_mentions=discord.AllowedMentions.none()  # メンション無効化
                )

        conn.close()

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(AFK(bot))