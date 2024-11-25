import discord
from discord.ext import commands
import aiohttp
import io

class FiveThousand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /5000コマンドの定義
    @discord.app_commands.command(name="5000", description="5000兆円ほしいジェネレータです。")
    async def generate_5000(self, interaction: discord.Interaction, top: str, bottom: str):
        # APIエンドポイントのURL
        url = f"https://gsapi.cbrx.io/image?top={top}&bottom={bottom}"
        
        # HTTPリクエストを送る
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    # 画像データを取得
                    image_data = await response.read()

                    # メモリ上にバイトデータをファイルのように扱う
                    image_file = io.BytesIO(image_data)
                    image_file.seek(0)  # ファイルポインタを先頭に戻す

                    # 画像をDiscordに送信
                    file = discord.File(image_file, filename="5000.png")
                    credit_text = (
                        "画像は[5000兆円ジェネレータAPI](https://github.com/CyberRex0/5000choyen-api)を使用して生成されました。"
                    )
                    await interaction.response.send_message(content=credit_text, file=file)
                else:
                    # エラー処理
                    await interaction.response.send_message("画像の生成に失敗しました。もう一度試してください。")

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(FiveThousand(bot))
