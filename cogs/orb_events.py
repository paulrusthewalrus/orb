"""
Handles event triggers and reactions
"""

import discord
import random
import sys
import datetime
import csv
import re
import traceback

from discord.ext import commands as bot_commands
from discord.ext.commands import errors
from http.client import HTTPException, HTTPResponse
from utils import repo
from utils.repo import VERSION_DATA, MESSAGE, PREFIXES
from cogs.orb_control import db


async def send_command_help(ctx):
    """
    Sends help message for specific command

    Params:
        (discord.ext.commands.Context) ctx: context
    """
    await ctx.send("That's not how you use this command! Try again, and check https://aribowe.github.io/orb/commands.html if you're not sure")
    # if ctx.invoked_subcommand:                                                         THIS IS BROKE BUT I DON'T KNOW HOW
    #     _help = await ctx.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
    # else:
    #     _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

    # for page in _help:
    #     await ctx.send(page)

class Events(bot_commands.Cog):

    def __init__(self, bot):
        self.log = open("../log.txt", mode="a")
        self.bot = bot
    # Displays boot complete message
    
    @bot_commands.Cog.listener()
    async def on_ready(self):
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.datetime.now()

        await self.bot.change_presence(status=discord.Status.online, activity=MESSAGE)
        print("\nORB Core", VERSION_DATA["Colour"], VERSION_DATA["Version"], "Build", VERSION_DATA["Build"])
        print('------------------------------------------')
        print('Bot is online and connected to Discord.')
        print(f'Currently connected to {len(self.bot.guilds)} server.' if len(self.bot.guilds) == 1
              else f'Currently connected to {len(self.bot.guilds)} servers.')
        print('------------------------------------------')
        print('Bot Name: ' + self.bot.user.name)
        print('Bot ID: ' + str(self.bot.user.id))
        print('')
        print('Discord.py Version: ' + discord.__version__)
        print('Python Version: ' + sys.version[:5])
        print('')
        print('orb.py Version: ' + str(repo.VERSION_DATA["Version"]))
        print('------------------------------------------')
        self.log.write(f"------------------------------------------ \n Boot successful. \n BOT DATA: \n Core: {VERSION_DATA['Version']}, Build {VERSION_DATA['Build']} \n Connected to {len(self.bot.guilds)} servers \n Bot name: {self.bot.user.name} \n Bot ID: {self.bot.user.id} \n Discord.py version: {discord.__version__} \n Python version: {sys.version[:5]} \n ---------------------------")

    @bot_commands.Cog.listener()
    async def on_command_error(self, ctx, error: errors):
        """
        Bot posts message when command errors occur

        Params:
            (discord.ext.commands.Context) ctx: Context
            (discord.ext.commands.errors): errors
        """
        if isinstance(error, errors.CommandNotFound):
            await ctx.send(f'Invalid command. Please type {random.choice(PREFIXES)}commands to see a list of commands, or visit https://aribowe.github.io/orb/.')

        elif isinstance(error, errors.MissingRequiredArgument) or isinstance(error, errors.BadArgument):
            await send_command_help(ctx)

        elif isinstance(error, errors.CommandOnCooldown):
            await ctx.send(f'Woah, slow down there! Retry again in {error.retry_after:.0f} seconds.')

        elif isinstance(error, errors.CommandInvokeError):

            _traceback = traceback.format_list(traceback.extract_tb(error.__traceback__))
            _traceback = ''.join(_traceback)

            error_message = f'```Python\n{_traceback}{type(error).__name__}: {error}```'

            await ctx.send(f'There was an error processing the command ;w; {error_message}')

        elif isinstance(error, errors.MissingPermissions):
            await ctx.send('You do not have the required permissions to run this command.')

        elif isinstance(error, errors.BotMissingPermissions):
            await ctx.send('I do not have permission to run this command ;w;')

        elif isinstance(error, HTTPException):
            # if HTTPResponse == 413:
            ctx.send('The file size is too large for me to send over Discord ;o;')

    async def on_command(self, ctx):
        """Prints user commands to console"""
        try:
            print(f'{ctx.guild.me} > {ctx.message.channel} > {ctx.message.author.name} > {ctx.message.clean_content}')
        except AttributeError:
            print(f'Private Message > {ctx.message.channel} > {ctx.message.author.name} > {ctx.message.clean_content}')

    @bot_commands.Cog.listener()
    async def on_message(self, message):
        # If message contains very cool, or otherwise a 1/2000 chance of reacting "very cool"
        if (re.search(r"\b(very cool)\b", message.content, re.IGNORECASE) and random.random() > 0.5) or random.randint(1, 2000) == 1:
            for emote in "🇻🇪🇷🇾🇨🇴🅾🇱": 
                await message.add_reaction(emote)
               
            if random.random() > 0.99:  #1/100 chance
                await message.add_reaction("😎")
            print("Reacted 'very cool' to message", "'" + message.content + "'", "from user", message.author.display_name)

        # Girls aren't real
        elif re.search(r"\b(girl[']?s aren[']?t real)\b", message.content, re.IGNORECASE):
            reaction = random.choice(["🇹🇷🇺🇪", "🇫🇦🇨🇹"])
            for emote in reaction:
                await message.add_reaction(emote)

                print(f"Reacted {str(reaction)} to the message '{message.content}' from user {message.author.display_name}")

        # Epic reaction time
        elif re.search(r"\b(epic)\b", message.content, re.IGNORECASE) and random.random() > 0.5:
            if random.randint(1, 15) == 1:
                reaction = "🇪🅱🇮🇨"
                for emote in reaction:
                    await message.add_reaction(emote)
                #
                # print(f"Reacted {emote}")

                print(f"Reacted {reaction} to the message '{message.content}' from user {message.author.display_name}")
            else:
                reaction = "🇪🇵🇮🇨"
                for emote in reaction:
                    await message.add_reaction(emote)
                print(f"Reacted {reaction} to the message '{message.content}' from user {message.author.display_name}")

        # Big guy react
        elif re.search(r"\b(big guy)\b", message.content, re.IGNORECASE) and random.random() > 0.75:
            await message.channel.send("For you")
            print(f"Responded with 'For you' to message {message.content} from user {message.author.display_name}")
        # Awoo react
        elif re.search(r"\b(awoo+)\b", message.content, re.IGNORECASE):
            reaction = "🇦🇼🇴🅾"
            for emote in reaction:
                await message.add_reaction(emote)

            print(f"Reacted with {reaction} to message '{message.content}' from user {message.author.display_name}")

        # 3/10
        elif re.search(r"\b(asuna)\b", message.content, re.IGNORECASE) or re.search(r"\b(sword art online)\b",
                                                                                    message.content,
                                                                                    re.IGNORECASE) or re.search(
                r"\b(SAO)\b", message.content, re.IGNORECASE):
            if random.random() > 0.9:
                await message.channel.send("3/10")
                print(f"Responded with '3/10' to message {message.content} from user {message.author.display_name}")

        # Imagine
        elif re.search(r"\b(imagine)\b", message.content, re.IGNORECASE) and random.random() > 0.9:
            await message.channel.send(random.choice(["Imagine", "> i m a g i n e"]))

            # # 40 kg
            # elif re.search(r"\b(40[ ]?kg)\b", message.content, re.IGNORECASE) and random.random() > 0.95:
            #     await message.channel.send(random.choice(["145 cm", "I M A G I N E"]))

            # # Roughly 145 cm
            # elif re.search(r"\b(145[ ]?cm)\b", message.content, re.IGNORECASE) and random.random() > 0.99:
            #     await message.channel.send(random.choice(["40 kg", "I M A G I N E", "Imagine how fun it would be to manhandle her tiny body"]))

            # elif re.search(r"\b(imagine)\b", message.content, re.IGNORECASE) and random.randint(1,1000) == 420:
            #     await message.channel.send("https://i.kym-cdn.com/photos/images/newsfeed/001/455/798/54e.jpg")

            # Level up
        elif re.search(r"(leveled up!)", message.content, re.IGNORECASE) and message.author.id == 172002275412279296:
            for emote in "🇬🇿":
                await message.add_reaction(emote)

            # OwO
        elif re.search(r"\b(owo)\b", message.content, re.IGNORECASE):
            for emote in "🇴🇼🅾":
                await message.add_reaction(emote)

            # Data are is the wrong way to say it
        elif re.search(r"\b(data are)\b", message.content, re.IGNORECASE):
            await message.add_reaction(self.bot.get_emoji(415384489733128195))

            # Owl
        elif re.search(r"\b(🦉)\b", message.content, re.IGNORECASE) and message.author.id == 243656780222038017:
            await message.add_reaction("🦉")

            # Orb
        elif re.search(r"(\b|:)(orb)(\b|:|^.)", message.content, re.IGNORECASE) and random.random() > 0.99:
            await message.add_reaction(self.bot.get_emoji(587198415348170773))

            # # Gay
            # elif re.search(r"\b(gays)\b", message.content, re.IGNORECASE) and random.random() > 0.99:
            #     await message.add_reaction("🇬")
            #     await message.add_reaction("🇦")
            #     await message.add_reaction("🇾")
        #
        # await bot.process_commands(message)
        
          # Commented out since it was interefering with command processor for o.fox
#         elif re.search(r"\b(:fox:)\b", message.content, re.IGNORECASE):
#             await message.add_reaction("🦊")

        elif re.search(r"\b(surely)\b", message.content, re.IGNORECASE):
            for emote in "🇸🇺🇷🇪🇱🇾":
                await message.add_reaction(emote)

def setup(bot):
    bot.add_cog(Events(bot))
