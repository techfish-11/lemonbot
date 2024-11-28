import discord
from discord.ext import commands
import sqlite3
import re

class JoinMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.initialize_db()

    def initialize_db(self):
        """データベース初期化"""
        conn = sqlite3.connect('joinmessage.db')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS join_messages (
            server_id INTEGER PRIMARY KEY,
            message TEXT,
            enabled BOOLEAN
        )
        ''')
        conn.commit()
        conn.close()

    def sanitize_message(self, message: str) -> str:
        """メンションを防ぐため、@やeveryone、roleを無効化"""
        sanitized_message = re.sub(r'@', '＠', message)
        sanitized_message = re.sub(r'@(everyone|here)', '＠\\1', sanitized_message)
        return sanitized_message

    @discord.app_commands.command(
        name="join-message", 
        description="参加メッセージを有効化または無効化します。"
    )
    async def join_message(self, interaction: discord.Interaction, action: bool, message: str = None):
        """参加メッセージの設定を有効化または無効化"""
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("このコマンドを実行するには、メッセージ管理権限が必要です。")
            return

        server_id = interaction.guild.id
        conn = sqlite3.connect('joinmessage.db')
        c = conn.cursor()

        if message:
            sanitized_message = self.sanitize_message(message)
            if not self.is_valid_message(sanitized_message):
                await interaction.response.send_message("無効なプレースホルダまたは危険なメッセージが含まれています。")
                return

        if action:
            c.execute('''
            INSERT INTO join_messages (server_id, message, enabled) 
            VALUES (?, ?, ?) 
            ON CONFLICT(server_id) 
            DO UPDATE SET message = ?, enabled = ?''', (server_id, sanitized_message, True, sanitized_message, True))
            conn.commit()
            await interaction.response.send_message(
                f"参加メッセージが有効化されました。設定されたメッセージ: {sanitized_message}",
                allowed_mentions=discord.AllowedMentions.none()  # メンション無効化
            )
        else:
            c.execute('''
            INSERT INTO join_messages (server_id, message, enabled) 
            VALUES (?, ?, ?) 
            ON CONFLICT(server_id) 
            DO UPDATE SET enabled = ?''', (server_id, '', False, False))
            conn.commit()
            await interaction.response.send_message(
                "参加メッセージが無効化されました。",
                allowed_mentions=discord.AllowedMentions.none()  # メンション無効化
            )

        conn.close()

    def is_valid_message(self, message: str) -> bool:
        """プレースホルダ以外の無効な文字列を防ぐ"""
        allowed_patterns = [r"{member\.(name|id)}"]
        pattern = "|".join(allowed_patterns)
        message_pattern = re.compile(f"({pattern})*")
        return message_pattern.fullmatch(message) is not None

    def format_message(self, message: str, member: discord.Member) -> str:
        """プレースホルダの置換"""
        message = message.replace("{member.name}", member.name)
        message = message.replace("{member.id}", str(member.id))
        return message

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """新規メンバーが参加した際のメッセージ"""
        server_id = member.guild.id
        conn = sqlite3.connect('joinmessage.db')
        c = conn.cursor()

        c.execute('SELECT message, enabled FROM join_messages WHERE server_id = ?', (server_id,))
        result = c.fetchone()

        if result and result[1]:
            formatted_message = self.format_message(result[0], member)
            await member.guild.system_channel.send(
                formatted_message,
                allowed_mentions=discord.AllowedMentions.none()  # メンション無効化
            )

        conn.close()

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(JoinMessage(bot))
