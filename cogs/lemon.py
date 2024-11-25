import discord
from discord.ext import commands
import random
import json

class Lemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /lemonコマンドの定義
    @discord.app_commands.command(name="lemon", description="ランダムにレモンの品種を表示します。")
    async def lemon_command(self, interaction: discord.Interaction):
        # JSONファイルを読み込む
        with open('lemons.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # レモンの品種リストを取得
        lemon_varieties = data["varieties"]

        # ランダムに選ぶ
        random_lemon = random.choice(lemon_varieties)

        # 結果をDiscordに送信
        await interaction.response.send_message(f"ランダムに選ばれたレモンの品種: {random_lemon}")

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(Lemon(bot))
