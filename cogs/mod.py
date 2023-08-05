from discord import Embed, Guild, Member, Message
from discord.ext import commands, tasks

class mod(commands.Cog, name = "Mod", description = "For moderating purposes"):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Mod cog is ready')

    @commands.command(name = "purge", description = "Delete recent messages (mod only)", hidden = False)
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, limit1: int = 0):
        await ctx.channel.purge(limit = limit1 + 1 if limit1 <= 100 and limit1 >= 1 else 1);
    
    '''
    # Coming Soon
    @commands.command()
    @commands.has_permissions(moderate_members = True)
    async def timeout(self, ctx, user: Member = None, time: float = 0, reason: str = None):
        embed = Embed(colour = user.top_role.color, timestamp = ctx.message.created_at)
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar)
        if not Member:
            embed.add_field(value = "Invalid Member. No Actions.", inline = False)
            await ctx.send(embed = embed)
        elif time == 0:
            embed.add_field(value = "Invalid Duration. No Actions.", inline = False)
            await ctx.send(embed = embed)
        else:
            hour = int(time)
            minute = time - int(time)
            minute = minute * 60
            second = minute - int(minute)
            minute = int(minute)
            second = int(second * 60)
            duration = datetime.timedelta(hours = hour, minutes = minute, seconds = second)
            embed.set_thumbnail(url = user.avatar)
            embed.add_field(name = "Timeout User: ", value = user.id, inline = False)
            embed.add_field(name = "Username: ", value = user.display_name, inline = False)
            embed.add_field(name = "Duration: ", value = f"{hour} hours {minute} minutes {second} seconds.", inline = False)
            embed.add_field(name = "Reason: ", value = f"{reason}" if reason is not None else "No reason given.", inline = False)
            await user.timeout(duration, reason = reason)
            await ctx.send(embed = embed)
    '''
        
async def setup(client):
    await client.add_cog(mod(client))