import random
from datetime import datetime
from time import time

import discord
from discord.ext import commands
from pytz import timezone

from lib.create import create_giveaway
from lib.edit import edit_item
from lib.request import request_item, request_giveaways, request_if

# Libery Imports

bot = commands.Bot(command_prefix='r!')

bot.remove_command('help')


class CommandClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help Menu")
        embed.add_field(name="r!create_giveaway *time:sek* winners msg", value="Start a Giveaway", inline=False)
        embed.add_field(name="r!end *message id*", value="End a Giveaway", inline=False)
        embed.add_field(name="r!list", value="List all Giveaways", inline=False)
        embed.add_field(name="r!reroll *message id*", value="Reroll a giveaway", inline=False)
        embed.set_thumbnail(url="https://neko-dev.de/img/Neko_Logo.png")
        embed.set_footer(text=ctx.message.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def create_giveaway(self, ctx, time_sec: int, winners: int, *args: str):
        if isinstance(time_sec, int) is False:
            await ctx.send("Please write the Time in Seconds next Time.")
        elif isinstance(winners, int) is False:
            await ctx.send("Please write the Winners as number next Time.")
        else:
            price = ' '.join(args)
            givemsg = ""
            if price == "":
                givemsg += "We roll for anything"
            else:
                givemsg += price
                time_var = calc(time_sec)
                date1 = datetime.now(timezone('UTC'))
                date_time = date1.astimezone(timezone('Europe/Berlin'))
                date = "{}.{}.{}".format(date_time.day, date_time.month, date_time.year)
                clock = "{}:{}:{}".format(date_time.hour, date_time.minute, date_time.second)
                embed = discord.Embed(title=givemsg,
                                      description="Hoster: {}\n"
                                                  "Winner: {}\n"
                                                  "Start: {} | {}\n"
                                                  "Time: {}".format(ctx.author, winners, date, clock, time_var))
                embed.set_thumbnail(url="https://neko-dev.de/imgstore/giveaway.jpg")
                embed.set_author(icon_url=self.bot.user.avatar_url, name=ctx.author.name)
                message = await ctx.send(embed=embed)
                server_id = str(ctx.guild.id)
                channel_id = ctx.channel.id
                create_giveaway(server_id, channel_id, str(message.id), str(ctx.author.id), time(), time_sec, winners)
                reaction = self.bot.get_emoji(549531102117625866)
                await message.add_reaction(reaction)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reroll(self, ctx, message: discord.Message):
        if not message:
            await ctx.send("Bitte gebe die Message ID des Giveaways an.")
        else:
            server_id = str(ctx.guild.id)
            message_id = str(message.id)
            channel_id = request_item(server_id, 'channel', message_id)
            channel = self.bot.get_channel(channel_id)
            winners = int(request_item(server_id, 'winner', message_id))
            users = request_item(server_id, 'user', message_id)
            if request_if(server_id, message_id) is False:
                winner_list = []
                for i in range(winners):
                    users = list(users)
                    if users:
                        print(users)
                        winner_id = random.choice(users)
                        winner = self.bot.get_user(int(winner_id))
                        if winner.mention not in winner_list:
                            winner_list.append(str(winner.mention))
                        else:
                            winners += 1
                    else:
                        break
                if not winner_list:
                    liste = "Nobody"
                else:
                    liste = ', '.join(winner_list)
                await channel.send("{} has won the giveaway".format(liste))
            else:
                await ctx.send("Giveaway is activ currently.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def end(self, ctx, message: discord.Message):
        if not message:
            await ctx.send("Bitte gebe die Message ID des Giveaways an.")
        else:
            server_id = str(ctx.guild.id)
            message_id = str(message.id)
            if request_if(server_id, message_id) is True:
                edit_item(server_id, message_id, 'time', 0)
            else:
                await ctx.send("Giveaway is currently not online.")

    @commands.command()
    async def list(self, ctx):
        server_id = str(ctx.guild.id)
        all_give = request_giveaways(server_id)
        all_givs = ""
        for i in all_give:
            state = request_item(server_id, 'activ', i)
            host = request_item(server_id, 'hoster', i)
            winner = request_item(server_id, 'winner', i)
            all_givs += "{}\n" \
                        "Hoster: {}\n" \
                        "Winner: {} | State: {}\n\n".format(i, host, winner, state)
        if not all_givs:
            all_list = "No Giveaways"
        else:
            all_list = all_givs
        embed = discord.Embed(title="Current Giveaways",
                              description=all_list, color=ctx.author.color)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CommandClass(bot))


def calc(n):
    day = n // (24 * 3600)
    n = n % (24 * 3600)
    hour = n // 3600
    n %= 3600
    minutes = n // 60
    n %= 60
    seconds = n
    return "{}d {}h {}m {}s".format(day, hour, minutes, seconds)
