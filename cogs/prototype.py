from discord import Embed, Interaction, app_commands
import asyncio

# Prototype  
@app_commands.command(name = "", description = "")
async def slash_(self, interaction: Interaction):
    await interaction.response.defer(ephemeral = True)
    await asyncio.sleep(delay = 0)
    embed = Embed(title = "", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)

    embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
    await interaction.followup.send(embed = embed)