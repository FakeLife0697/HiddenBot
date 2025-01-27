from discord import Button, ButtonStyle, Component, Interaction, ui

class ConfirmView(ui.View):
    def __init__(self, timeout = 60):
        super().__init__(timeout = timeout)
        self.confirmation: bool = None
        
    def disable(self):
        for child in self.children:
            child.disabled = True
    
    @ui.button(
            style = ButtonStyle.success,
            label = "Confirm",
            custom_id = "confirm"
            )
    async def confirm(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message("", view = None, ephemeral = True)
        self.confirmation = True
        self.stop()
        
    @ui.button(
            style = ButtonStyle.danger,
            label = "Cancel",
            custom_id = "cancel"
            )
    async def cancel(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message("", view = None, ephemeral = True)
        self.confirmation = False
        self.stop()
        
    async def on_timeout(self):
        # Called when the timeout expires
        self.disable()
        # Optional: Update the message to indicate timeout
        # await self.message.edit(content = "Message expired. No response received.", view = None)
        
    def getConfirmation(self) -> None:
        return self.confirmation