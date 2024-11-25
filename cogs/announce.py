import discord
from discord.ext import commands
import yaml
import os

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.announce_file = "announce.yml"

    def load_announcements(self):
        """アナウンス内容をファイルから読み込む"""
        if not os.path.exists(self.announce_file):
            return []
        
        with open(self.announce_file, 'r', encoding='utf-8') as file:
            try:
                announcements = yaml.safe_load(file)
                return announcements if isinstance(announcements, list) else []
            except yaml.YAMLError as e:
                print(f"YAMLエラー: {e}")
                return []

    @discord.app_commands.command(name="announce", description="現在のアナウンスを表示します。")
    async def announce(self, interaction: discord.Interaction):
        """アナウンスをDiscordに表示するコマンド"""
        announcements = self.load_announcements()

        if not announcements:
            await interaction.response.send_message("現在、アナウンスはありません。")
            return

        # Embed形式でアナウンスを表示
        embed = discord.Embed(
            title="📢 現在のアナウンス",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

        for idx, announcement in enumerate(announcements, start=1):
            embed.add_field(name=f"アナウンス {idx}", value=announcement, inline=False)

        await interaction.response.send_message(embed=embed)

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(Announce(bot))
