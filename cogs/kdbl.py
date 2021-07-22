from datetime import datetime
from typing import Optional, TYPE_CHECKING
import discord
from discord.ext import commands

if TYPE_CHECKING:
    from bot import Bot

from submits import submits, approved_submits


class KDBL(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self._submits_dict: dict[int, Bot] = {bot.id: bot for bot in submits}

    @commands.command()
    async def todo(self, ctx: commands.Context, query: Optional[int] = None):
        if not query:
            if not self._submits_dict:
                return await ctx.send(embed=discord.Embed(title="현재 대기 중인 봇이 없습니다."))
            embed = discord.Embed(title="현재 대기 중인 봇 목록")
            for i, bot in enumerate(self._submits_dict.values()):
                embed.add_field(
                    name=f"{i + 1}: {bot.id}",
                    value=f"심사 신청 일자: {datetime.fromtimestamp(bot.date)}",
                    inline=False,
                )
            return await ctx.send(embed=embed)

        if query - 1 < len(self._submits_dict):
            bot = submits[query - 1]
        else:
            if not (bot := self._submits_dict.get(query)):
                return await ctx.send(
                    embed=discord.Embed(title="해당 인덱스 또는 ID를 가진 봇을 찾지 못했습니다.")
                )

        url = "https://discord.com/oauth2/authorize?client_id={bot.id}&scope=bot&guild_id=653083797763522580"
        embed = discord.Embed(
            title=f"{bot.id}",
            description=f"[초대 링크]({url})\n심사 신청 일자: {datetime.fromtimestamp(bot.date)}",
        )
        return await ctx.send(embed=embed)

    @commands.command()
    async def approve(self, ctx: commands.Context, query: int):
        if bot := self._submits_dict.get(query):
            submits.remove(bot)
            approved_submits.append(bot)
            del self._submits_dict[query]
            return await ctx.send(embed=discord.Embed(title=f"{query} 를 승인하였습니다."))
        return await ctx.send(embed=discord.Embed(title=f"{query} 를 찾지 못했습니다."))

    @commands.command()
    async def deny(self, ctx: commands.Context, query: int):
        if bot := self._submits_dict.get(query):
            submits.remove(bot)
            del self._submits_dict[query]
            return await ctx.send(embed=discord.Embed(title=f"{query} 를 거절하였습니다."))
        return await ctx.send(embed=discord.Embed(title=f"{query} 를 찾지 못했습니다."))


def setup(bot: "Bot"):
    bot.add_cog(KDBL(bot))
