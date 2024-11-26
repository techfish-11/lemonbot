import discord
from discord.ext import commands
from discord import app_commands

class MojiBake(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="moji-bake", description="文字をわざと文字化けさせます")
    async def moji_bake(self, interaction: discord.Interaction, content: str):
        # 文字列をUTF-8でエンコードし、さらにISO-8859-1でデコードして文字化けを発生させる
        try:
            # UTF-8にエンコード → ISO-8859-1でデコード（わざと文字化けさせる）
            content_baked = content.encode('utf-8').decode('iso-8859-1')

            # 英語も文字化けさせるために、もう一段階Shift_JISに変換するなど、さらに文字化けを加える
            content_baked = content_baked.encode('utf-8').decode('shift_jis', errors='ignore')  # Shift_JISでもデコード

        except Exception as e:
            content_baked = f"エラーが発生しました: {str(e)}"
        
        # 文字化けさせた内容を返す
        await interaction.response.send_message(content_baked)

async def setup(bot: commands.Bot):
    """Cogを非同期で追加"""
    await bot.add_cog(MojiBake(bot))
