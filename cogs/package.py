import discord
from discord.ext import commands
from discord import app_commands
import requests
import json

class PackageSearch(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="package", description="npm or pipパッケージを検索します")
    @app_commands.describe(package_name="検索したいパッケージ名", manager="検索するパッケージマネージャーを選択")
    async def package(self, interaction: discord.Interaction, package_name: str, manager: str):
        if manager not in ["npm", "pip"]:
            await interaction.response.send_message("`npm`か`pip`のいずれかを指定してください。")
            return

        try:
            if manager == "npm":
                result = self.search_npm_package(package_name)
            elif manager == "pip":
                result = self.search_pip_package(package_name)

            if result:
                await interaction.response.send_message(f"検索結果:\n{result}")
            else:
                await interaction.response.send_message(f"{manager}パッケージ `{package_name}` に関連する情報が見つかりませんでした。")

        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: {str(e)}")

    def search_npm_package(self, package_name):
        """npmパッケージを検索 (npm registry APIを使用)"""
        try:
            # npm registry APIを使用してパッケージを検索
            url = f"https://registry.npmjs.org/{package_name}"
            response = requests.get(url)
            if response.status_code == 200:
                package_info = response.json()
                latest_version = package_info.get("dist-tags", {}).get("latest", "不明")
                description = package_info.get("description", "説明なし")
                homepage = package_info.get("homepage", "情報なし")
                return f"**{package_name}**\nバージョン: {latest_version}\n説明: {description}\nURL: {homepage}"
            else:
                return None
        except Exception as e:
            return f"npmパッケージの検索中にエラーが発生しました: {str(e)}"

    def search_pip_package(self, package_name):
        """pipパッケージを検索 (PyPI APIを使用)"""
        try:
            # PyPI APIを使用してパッケージを検索
            url = f"https://pypi.org/pypi/{package_name}/json"
            response = requests.get(url)
            if response.status_code == 200:
                package_info = response.json()
                version = package_info.get("info", {}).get("version", "不明")
                summary = package_info.get("info", {}).get("summary", "説明なし")
                home_page = package_info.get("info", {}).get("home_page", "情報なし")
                return f"**{package_name}**\nバージョン: {version}\n説明: {summary}\nURL: {home_page}"
            else:
                return None
        except Exception as e:
            return f"pipパッケージの検索中にエラーが発生しました: {str(e)}"

async def setup(bot: commands.Bot):
    """Cogを非同期で追加"""
    await bot.add_cog(PackageSearch(bot))
