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

    @commands.command()
    async def todo(self, ctx: commands.Context, query: Optional[int] = None):
        if not query:
            if not self.bot.submits_manager.items:
                return await ctx.send(embed=discord.Embed(title="현재 대기 중인 봇이 없습니다."))
            embed = discord.Embed(title="현재 대기 중인 봇 목록")
            for i, info in enumerate(self.bot.submits_manager.items):
                embed.add_field(
                    name=f"{i + 1}: {info['id']}",
                    value=f"심사 신청 일자: {datetime.fromtimestamp(info['timestamp'])}",
                    inline=False,
                )
            return await ctx.send(embed=embed)

        if query - 1 < len(self.bot.submits_manager.items):
            bot = self.bot.submits_manager.items[query - 1]
        else:
            if not (
                bot := list(
                    filter(
                        lambda item: item["id"] == query, self.bot.submits_manager.items
                    )
                )[0]
            ):
                return await ctx.send(
                    embed=discord.Embed(title="해당 인덱스 또는 ID를 가진 봇을 찾지 못했습니다.")
                )

        url = discord.utils.oauth_url(
            self.bot.user.id,
            guild=self.bot.get_guild(653083797763522580),
        )
        embed = discord.Embed(
            title=f"{bot['id']}",
            description=f"[초대 링크]({url})\n심사 신청 일자: {datetime.fromtimestamp(bot['timestamp'])}",
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
