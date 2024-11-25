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

    @discord.app_commands.command(
        name="join-message", 
        description="参加メッセージを有効化または無効化します。\n\n"
    )
    async def join_message(self, interaction: discord.Interaction, action: bool, message: str = None):
        """参加メッセージの設定を有効化または無効化"""
        # ユーザーがモデレーター権限を持っているかチェック
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("このコマンドを実行するには、メッセージ管理権限が必要です。")
            return

        server_id = interaction.guild.id
        conn = sqlite3.connect('joinmessage.db')
        c = conn.cursor()

        # プレースホルダ以外の関数が使われていないかチェック
        if not self.is_valid_message(message):
            await interaction.response.send_message("無効なプレースホルダが含まれています。")
            return

        if action:
            # メッセージを設定して有効化
            c.execute('''
            INSERT INTO join_messages (server_id, message, enabled) 
            VALUES (?, ?, ?) 
            ON CONFLICT(server_id) 
            DO UPDATE SET message = ?, enabled = ?''', (server_id, message, True, message, True))
            conn.commit()
            await interaction.response.send_message(f"参加メッセージが有効化され、メッセージは「{message}」に設定されました。")
        else:
            # 無効化
            c.execute('''
            INSERT INTO join_messages (server_id, message, enabled) 
            VALUES (?, ?, ?) 
            ON CONFLICT(server_id) 
            DO UPDATE SET enabled = ?''', (server_id, '', False, False))
            conn.commit()
            await interaction.response.send_message("参加メッセージが無効化されました。")

        conn.close()

    def is_valid_message(self, message: str) -> bool:
        """プレースホルダ以外の関数が含まれていないかチェック"""
        # {member.name} や {member.id} のようなプレースホルダのみを許可
        allowed_patterns = [r"{member\.(name|id)}"]
        pattern = "|".join(allowed_patterns)
        return bool(re.fullmatch(f"({pattern})*", message))

    def format_message(self, message: str, member: discord.Member) -> str:
        """メッセージ内のプレースホルダを解釈してフォーマットする"""
        # {member.name} や {member.id} を埋め込む
        message = message.replace("{member.name}", member.name)
        message = message.replace("{member.id}", str(member.id))
        return message

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """新規メンバーが参加したときに参加メッセージを送信"""
        server_id = member.guild.id
        conn = sqlite3.connect('joinmessage.db')
        c = conn.cursor()

        # サーバーの設定を確認
        c.execute('SELECT message, enabled FROM join_messages WHERE server_id = ?', (server_id,))
        result = c.fetchone()

        if result and result[1]:  # メッセージが設定されており、有効化されている場合
            # プレースホルダを解釈して、参加メッセージを送信
            formatted_message = self.format_message(result[0], member)
            await member.guild.system_channel.send(formatted_message)

        conn.close()

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(JoinMessage(bot))
