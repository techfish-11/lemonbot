import discord
from discord.ext import commands

class AboutLemonCoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="about-lemoncoin", description="レモンコインについて説明します。")
    async def about_lemoncoin(self, interaction: discord.Interaction):
        """レモンコインの説明を表示"""
        
        # 埋め込みメッセージを作成
        embed = discord.Embed(
            title="レモンコインとは？",
            description="レモンコインは、LemonBotを導入している全サーバー内で使用できる仮想通貨です。"
                        "ユーザーはコインを使って様々なアクションを実行できます。\n\n"
                        "**主な機能**:\n"
                        "・ログインボーナス: 2時間ごとにレモンコインが貯まります。\n"
                        "・コインの譲渡: 他のユーザーにレモンコインを譲渡できます。\n"
                        "・ガチャ: ガチャを回して、レモンコインやアイテムをゲットできます。\n"
                        "・コインの確認: 自分の所持コインを確認できます。\n\n"
                        "レモンコインは特定のアクションやガチャを通じて手に入れることができます！"
                        "コインを賢く使って、楽しい体験をお楽しみください！\n"
                        "コインは、５分毎に自動的に監視され、小数があった場合自動的に切り捨てられるようになっています。その場合、BOTからDMが送信されます。\n\n"
                        "レモンコインは、Discord上での活動の幅を広げるために開発されています。"
                        "そのため、現実のお金を巻き込んだり、違法な取引に使用することは、絶対に禁止されています。",
            color=discord.Color.green()
        )

        try:
            # メッセージを送信
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message("レモンコインに関する説明の送信中にエラーが発生しました。")
            print(f"Error: {e}")

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(AboutLemonCoin(bot))
