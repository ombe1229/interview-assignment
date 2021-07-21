from datetime import datetime
from typing import Optional, TYPE_CHECKING
import discord
from discord.embeds import Embed
from discord.ext import commands

if TYPE_CHECKING:
    from bot import Bot

from submits import submits, approved_submits


class KDBL(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def todo(self, ctx: commands.Context, query: Optional[int] = None):
        if not query:
            if not submits:
                return await ctx.send(embed=discord.Embed(title="현재 대기 중인 봇이 없습니다."))
            embed = discord.Embed(title="현재 대기 중인 봇 목록")
            for i, bot in enumerate(submits):
                embed.add_field(
                    name=f"{i + 1}: {bot.id}",
                    value=datetime.fromtimestamp(bot.date),
                    inline=False,
                )
            return await ctx.send(embed=embed)

        if query <= 0:
            return await ctx.send(embed=discord.Embed(title="인자는 1 이상의 숫자여야 합니다."))

        if query > len(submits):
            for i in submits:
                if i.id == query:
                    bot = i
                    break
        else:
            bot = submits[query - 1]

        if "bot" not in locals() or not bot:
            return await ctx.send(
                embed=discord.Embed(title="해당 인덱스 또는 ID를 가진 봇이 없습니다.")
            )
        url = "https://discord.com/oauth2/authorize?client_id={bot.id}&scope=bot&guild_id=653083797763522580"
        embed = discord.Embed(
            title=f"{bot.id}",
            description=f"{url}\n{datetime.fromtimestamp(bot.date)}",
        )
        return await ctx.send(embed=embed)

    @commands.command()
    async def approve(self, ctx: commands.Context, query: int):
        for i in submits:
            if i.id == query:
                approved_submits.append(submits.pop(submits.index(i)))
                return await ctx.send(embed=discord.Embed(title=f"{query} 를 승인하였습니다."))
        return await ctx.send(embed=discord.Embed(title=f"{query} 를 찾지 못했습니니다."))

    @commands.command()
    async def deny(self, ctx: commands.Context, query: int):
        for i in submits:
            if i.id == query:
                submits.pop(submits.index(i))
                return await ctx.send(embed=discord.Embed(title=f"{query} 를 거절하였습니다."))
        return await ctx.send(embed=discord.Embed(title=f"{query} 를 찾지 못했습니다."))


def setup(bot: "Bot"):
    bot.add_cog(KDBL(bot))
