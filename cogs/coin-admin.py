import discord
from discord.ext import commands
import sqlite3

class CoinAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_db_connection(self):
        """データベース接続を取得"""
        conn = sqlite3.connect('lemoncoin.db')
        conn.row_factory = sqlite3.Row
        return conn

    async def is_admin(self, interaction: discord.Interaction) -> bool:
        """ユーザーが管理者か確認"""
        return interaction.user.id == 1241397634095120438

    @discord.app_commands.command(name="coin-admin", description="レモンコイン管理用コマンドです（管理者専用）。")
    async def coin_admin(self, interaction: discord.Interaction, action: str, target_user: discord.User = None, amount: int = None):
        """
        管理者専用のコマンドで、以下の操作が可能：
        - 情報照会
        - システム送金
        - ユーザーコインリセット
        """
        # 管理者チェック
        if not await self.is_admin(interaction):
            await interaction.response.send_message("このコマンドは管理者専用です。", ephemeral=True)
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            if action == "info":
                # 情報照会: 対象ユーザーのコイン状況を表示
                if target_user is None:
                    await interaction.response.send_message("ユーザーを指定してください。", ephemeral=True)
                    return

                cursor.execute("SELECT coins FROM users WHERE user_id = ?", (target_user.id,))
                result = cursor.fetchone()
                if result:
                    coins = result["coins"]
                    await interaction.response.send_message(
                        f"**{target_user.name}** のレモンコイン情報:\n"
                        f"- 残高: {coins} レモンコイン\n"
                    )
                else:
                    await interaction.response.send_message(f"ユーザー {target_user.name} の情報が見つかりません。")

            elif action == "send":
                # システムから送金: 指定したユーザーにコインを送る
                if target_user is None or amount is None or amount <= 0:
                    await interaction.response.send_message("有効なユーザーと金額を指定してください。", ephemeral=True)
                    return

                # ユーザーが存在しない場合は作成
                cursor.execute("INSERT OR IGNORE INTO users (user_id, coins, invested) VALUES (?, 0, 0)", (target_user.id,))
                # コインを追加
                cursor.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (amount, target_user.id))
                conn.commit()

                await interaction.response.send_message(f"{target_user.name} に {amount} レモンコインを送金しました！")

            elif action == "reset":
                # ユーザーのコインをリセット
                if target_user is None:
                    await interaction.response.send_message("ユーザーを指定してください。", ephemeral=True)
                    return

                cursor.execute("UPDATE users SET coins = 0, invested = 0 WHERE user_id = ?", (target_user.id,))
                conn.commit()
                await interaction.response.send_message(f"{target_user.name} のレモンコイン情報をリセットしました。")

            else:
                await interaction.response.send_message(
                    "無効な操作です。利用可能な操作: `info`, `send`, `reset`", ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: {e}", ephemeral=True)
        finally:
            conn.close()

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(CoinAdmin(bot))
