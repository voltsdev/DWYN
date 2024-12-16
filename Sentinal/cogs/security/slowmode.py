import discord
from discord.ext import commands

class SlowmodeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, *args):
        # -> Default values.
        seconds = 0
        channel = ctx.channel  # -> Default to current channel.
        
        # -> If two arguments are provided.
        if len(args) == 1:
            # -> Check if the first argument is a channel or seconds.
            try:
                # -> Try to interpret the first argument as a channel name.
                if args[0].startswith('#'):
                    channel_name = args[0][1:]  # Remove '#' symbol
                    channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
                    if not channel:
                        raise ValueError("Channel not found.")
                else:
                    # -> If it's not a channel name, interpret it as seconds.
                    seconds = int(args[0])
            except ValueError as e:
                embed = discord.Embed(
                    title="Error",
                    description=str(e),
                )
                await ctx.send(embed=embed)
                return

        elif len(args) == 2:
            # -> If both arguments are provided, interpret the first as channel and second as seconds.
            channel_name = args[0][1:]  # Remove '#' symbol
            channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
            seconds = int(args[1])

        # -> If channel is still None, default to current channel.
        if channel is None:
            channel = ctx.channel

        await self.apply_slowmode(ctx, channel, seconds)

    async def apply_slowmode(self, ctx, channel, seconds):
        # -> Check if the input time is valid.
        if seconds < 0:
            embed = discord.Embed(
                title="Invalid Slowmode Value",
                description="Slowmode delay cannot be negative.",
            )
            await ctx.send(embed=embed)
            return

        # -> Apply the slowmode to the specified channel.
        try:
            await channel.edit(slowmode_delay=seconds)

            # -> Provide feedback to the user.
            if seconds == 0:
                description = f"Slowmode has been **disabled** in {channel.mention}."
            else:
                description = f"Slowmode for {channel.mention} is now set to **{seconds} seconds**."

            embed = discord.Embed(
                title="Slowmode Updated",
                description=description,
            )
            embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)

        except discord.Forbidden:
            # -> Bot lacks permissions to edit the channel.
            embed = discord.Embed(
                title="Permission Denied",
                description=f"I don't have permission to edit {channel.mention}.",
            )
            await ctx.send(embed=embed)
        except Exception as e:
            # -> Catch other errors and display them.
            embed = discord.Embed(
                title="Error",
                description=f"An unexpected error occurred: {e}",
            )
            await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(SlowmodeCog(bot))