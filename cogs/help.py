import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help", description="主要なコマンド一覧を表示します。")
    async def help_command(self, interaction: discord.Interaction):
        """主要なコマンドの一覧を表示する"""
        embed = discord.Embed(
            title="LemonBot コマンド一覧",
            description=(
                "以下は、主要なコマンドの概要です。詳細は各コマンドを実行するか、"
                "[全コマンド詳細](https://lemon.sakana11.org/lemon/command-use.html)をご覧ください。"
            ),
            color=discord.Color.yellow()
        )

        embed.add_field(
            name="レモンコイン系コマンド",
            value=(
                "**`/about-lemoncoin`**: Lemoncoinについて確認します。\n"
                "**`/login-bonus`**: 2時間ごとにログインボーナスを獲得します。\n"
                "**`/coin-balance`**: 現在のレモンコイン残高を確認します。\n"
                "**`/transfer-coin recipient:<ユーザー名> amount:<金額>`**: 他のユーザーにレモンコインを譲渡します。\n"
                "**`/coin-ranking`**: レモンコインランキングの上位5人を表示します。\n"
            ),
            inline=False
        )

        embed.add_field(
            name="便利系コマンド",
            value=(
                "**`/help`**: 主要なコマンド一覧を表示します。\n"
                "**`/base64 action:<encode/decode> content:<内容>`**: Base64エンコードまたはデコードを行います。\n"
                "**`/ping`**: Botの応答速度を確認します。\n"
                "**`/join-message action:<True/False> message:<メッセージ>`**: 参加メッセージを設定します。\n"
            ),
            inline=False
        )

        embed.add_field(
            name="ネタ系コマンド",
            value=(
                "**`/lemon`**: ランダムにレモンの品種を出力します。\n"
                "**`/5000 top:<文字列> bottom:<文字列>`**: 5000兆円ほしいジェネレーターです。\n"
            ),
            inline=False
        )

        embed.set_footer(
            text="詳細を知りたい場合は、各コマンドを直接実行するか、全コマンド詳細をご確認ください！"
        )

        await interaction.response.send_message(embed=embed)

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(Help(bot))