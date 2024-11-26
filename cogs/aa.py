import discord
from discord.ext import commands
from discord import app_commands
import pywhatkit as kit
import os

class AA(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="image-to-aa", description="画像をASCIIアートに変換します。")
    async def image_to_aa(self, interaction: discord.Interaction, image_url: str):
        # 画像URLをダウンロードしてローカルに保存
        image_path = "temp_image.jpg"
        async with discord.http.get(image_url) as response:
            if response.status == 200:
                with open(image_path, 'wb') as f:
                    f.write(await response.read())

        try:
            # 画像をASCIIアートに変換
            ascii_art = kit.image_to_ascii(image_path)

            # 200文字以内に収めるために切り取る
            ascii_art = ascii_art[:200]

            # ASCIIアートを返す
            await interaction.response.send_message(f"こちらが画像のASCIIアートです:\n```\n{ascii_art}\n```")

        except Exception as e:
            await interaction.response.send_message(f"画像の処理中にエラーが発生しました")

        # 一時的な画像ファイルを削除
        if os.path.exists(image_path):
            os.remove(image_path)

async def setup(bot: commands.Bot):
    """Cogを非同期で追加"""
    await bot.add_cog(AA(bot))
