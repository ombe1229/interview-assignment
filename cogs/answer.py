from discord.ext import commands
from typing import TYPE_CHECKING
from submits import *
import discord

if TYPE_CHECKING:
    from bot import Bot


class Answer(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def todo(self, ctx, query=0):
        def add_submitted(i, submitted):
            embed.add_field(
                name=f"**{i+1}. {submitted.id}**",
                value=f"{datetime.fromtimestamp(submitted.date)}\n[초대 링크](https://discord.com/oauth2/authorize?client_id={submitted.id}&scope=bot&guild_id=653083797763522580)",
                inline=False,
            )

        embed = discord.Embed(
            title=":rocket: ToDo List", color=discord.Color.green(), description="_ _"
        )

        if not query:
            for i, submitted in enumerate(submits):
                add_submitted(i, submitted)

        else:
            for i, submitted in enumerate(submits):
                if submitted.id == query:
                    break
                if i == len(submits):  # query가 일치하는 id가 없을 경우 인덱스로 인식
                    add_submitted(i, submits[query - 1])

            add_submitted(i, submitted)

        await ctx.send(embed=embed)

    @commands.command()
    async def approve(self, ctx, query=0):
        for i, submitted in enumerate(submits):
            if submitted.id == query:
                approved_submits.append(submitted)
                del submits[i]
                await ctx.send(f"**{i+1}. {query}**가 정상적으로 승인되었습니다.")
                break

            if i == len(submits):
                await ctx.send(f"{query}를 찾을 수 없습니다.")

    @commands.command()
    async def deny(self, ctx, query=0):
        for i, submitted in enumerate(submits):
            if submitted.id == query:
                del submits[i]
                await ctx.send(f"**{i+1}. {query}**가 정상적으로 거부되었습니다.")
                break

            if i == len(submits):
                await ctx.send(f"{query}를 찾을 수 없습니다.")


def setup(bot: "Bot"):
    bot.add_cog(Answer(bot))
