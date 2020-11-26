import asyncio
import random
from time import time

from discord.ext import commands

from lib.delete import delete_server, delete_giveaway
from lib.edit import edit_user, edit_item
from lib.request import request_item, request_if, request_giveaways

bot = commands.Bot(command_prefix='kn!')

bot.remove_command('help')


class AutoClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for i in self.bot.guilds:
            for x in request_giveaways(str(i.id)):
                if request_if(str(i.id), str(x)):
                    if request_item(str(i.id), 'activ', str(x)) is True:
                        await self.giveaway_timer(str(i.id), str(x))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        delete_server(str(guild.id))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        server_id = str(message.guild.id)
        message_id = str(message.id)
        if request_if(server_id, message_id) is True:
            delete_giveaway(server_id, message_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        bot_reaction = self.bot.get_emoji(549531102117625866)
        if payload.emoji == bot_reaction:
            server_id = str(payload.guild_id)
            message_id = str(payload.message_id)
            user_id = str(payload.user_id)
            if request_if(server_id, message_id):
                if payload.member == self.bot.user:
                    await self.giveaway_timer(server_id, message_id)
                else:
                    edit_user(server_id, message_id, user_id, 'append')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        bot_reaction = self.bot.get_emoji(549531102117625866)
        if payload.emoji == bot_reaction:
            server_id = str(payload.guild_id)
            message_id = str(payload.message_id)
            user_id = str(payload.user_id)
            if request_if(server_id, message_id):
                if payload.member == self.bot.user:
                    pass
                else:
                    edit_user(server_id, message_id, user_id, 'remove')

    async def giveaway_timer(self, server_id: str, message_id: str):
        while True:
            await asyncio.sleep(5)
            current = time()
            start = request_item(server_id, 'start', message_id)
            delay = request_item(server_id, 'time', message_id)
            if round(current - start) >= delay:
                print(round(current - start))
                print(delay)
                break
        if request_if(server_id, message_id):
            channel_id = request_item(server_id, 'channel', message_id)
            channel = self.bot.get_channel(channel_id)
            winners = int(request_item(server_id, 'winner', message_id))
            users = request_item(server_id, 'user', message_id)
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
            edit_item(server_id, message_id, 'activ', False)


def setup(bot):
    bot.add_cog(AutoClass(bot))
