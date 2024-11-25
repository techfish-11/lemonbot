import discord
from discord.ext import commands

class mention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # メッセージが送信された際のイベント
    @discord.ext.commands.Cog.listener()
    async def on_message(self, message):
        # メッセージがbot自身のメンションかどうかをチェック
        if self.bot.user.mention in message.content:
            # レイテンシをミリ秒に変換
            latency_ms = round(self.bot.latency * 1000)
            # メンションがあった場合に返信
            await message.channel.send(f"LemonBotは正常に動作しています。現在のレイテンシは{latency_ms}msです。")

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(mention(bot))
