import discord

from discord.ext import commands
from cogs.orb_control import db
from orb_core import help


slot_payouts = """Slot machine payouts:
    :two: :two: :six: Bet * 5000
    :four_leaf_clover: :four_leaf_clover: :four_leaf_clover: +1000
    :cherries: :cherries: :cherries: +800
    :two: :six: Bet * 4
    :cherries: :cherries: Bet * 3
    Three symbols: +500
    Two symbols: Bet * 2"""

class UserEconomy:
    """
    This represents a UserEconomy object with the following attributes
        name (str): name of the user
        bank (int): the amount of money the individual has
        level (int): level of the user
        xp (int): amount of xp the user has
    """
    def __init__(self, name, balance, level, xp):
        self.name = name
        self.balance = balance
        self.level = level
        self.xp = xp

    def get_name(self):
        return self.name

    def get_balance(self):
        return self.balance

    def get_level(self):
        return self.level

    def get_xp(self):
        return self.xp

    def set_balance(self, balance):
        self.balance = balance

    def set_level(self, level):
        self.level = level

    def set_xp(self, level):
        self.level = level

    def __str__(self):
        return "%s %d %d %d" % (
            self.name,
            self.balance,
            self.level,
            self.xp
        )


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def enough_money(self, ctx):
        """
        Checks if user has enough money"""
        raise NotImplementedError

    def account_check(self, ctx):
        """Checks if user has an account"""
        raise NotImplementedError

    @commands.group(name="bank")
    def _bank(self, ctx):
        """Main command"""
        if ctx.invoked_subcommand is None:
            await help(ctx)

    @_bank.command()
    async def register(self, ctx):
        """Registers a user in the Orb bank."""
        raise NotImplementedError

    @_bank.command()
    async def balance(self, user: discord.Member=None):
        """
        Checks balance of user

        Params:
            user (discord.Member): discord member, defaults to None (in which case it shows the author's balance)
        """
        raise NotImplementedError

    @commands.command()
    async def dailies(self, ctx):
        """Daily credits for users"""
        raise NotImplementedError

    @commands.command()
    async def leaderboard(self, ctx):
        """Shows the leaderboard"""
        raise NotImplementedError

    @commands.command()
    async def payouts(self, ctx):
        """Shows slot machine payouts"""
        await ctx.send(slot_payouts)

def setup(bot):
    bot.add_cogs(Economy(bot))
