import discord
from discord.ext import commands
from discord import app_commands
import os
from PIL import Image
import aiohttp
from io import BytesIO

class AA(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="image-to-aa", description="画像をASCIIアートに変換します。")
    @app_commands.describe(image="画像を添付してください")
    async def image_to_aa(self, interaction: discord.Interaction, image: discord.Attachment):
        # 画像URLを取得
        image_url = image.url

        try:
            # 画像をダウンロード
            image_path = "temp_image.jpg"
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        with open(image_path, 'wb') as f:
                            f.write(image_data)

            try:
                # 画像をASCIIアートに変換
                ascii_art = self.image_to_ascii(image_path)

                # 400文字以内に収めるために切り取る
                ascii_art = ascii_art[:400]

                # ASCIIアートをtxtファイルに保存
                txt_file_path = "ascii_art.txt"
                with open(txt_file_path, 'w') as f:
                    f.write(ascii_art)

                # txtファイルを送信
                await interaction.response.send_message("画像のASCIIアートを`txt`ファイルとして送信します。", file=discord.File(txt_file_path))

            except Exception as e:
                await interaction.response.send_message(f"画像の変換に失敗しました: {str(e)}")

            # 一時的な画像ファイルを削除
            if os.path.exists(image_path):
                os.remove(image_path)
            if os.path.exists(txt_file_path):
                os.remove(txt_file_path)

        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: {str(e)}")

    def image_to_ascii(self, image_path):
        """画像をASCIIアートに変換する"""
        try:
            # 画像を開く
            img = Image.open(image_path)
            img = img.convert("L")  # グレースケールに変換
            img.thumbnail((100, 100))  # サイズを小さくする（必要に応じて調整）

            # 画像をASCIIアートに変換
            ascii_art = ''
            for y in range(img.height):
                for x in range(img.width):
                    pixel = img.getpixel((x, y))
                    ascii_art += '@' if pixel < 128 else ' '  # 明るい部分は空白、暗い部分は@記号
                ascii_art += '\n'

            return ascii_art
        except Exception as e:
            return f"画像の変換に失敗しました: {str(e)}"

async def setup(bot: commands.Bot):
    """Cogを非同期で追加"""
    await bot.add_cog(AA(bot))
