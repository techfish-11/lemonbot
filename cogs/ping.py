import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # スラッシュコマンドの定義
    @discord.app_commands.command(name="ping", description="ボットのレスポンスを確認します")
    async def ping(self, interaction: discord.Interaction):
        """ボットのレイテンシ（応答速度）を表示します。"""
        latency = self.bot.latency * 1000  # レイテンシをミリ秒単位に変換
        await interaction.response.send_message(f"Pong! レイテンシ: {latency:.2f} ms")

# コグをセットアップ
async def setup(bot):
    await bot.add_cog(General(bot))
