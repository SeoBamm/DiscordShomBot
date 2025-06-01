from discord import ui, Interaction, ButtonStyle

class FishBiteView(ui.View):
    def __init__(self, owner_id: int, embedList, timeout=5):
        super().__init__(timeout=timeout)
        self.owner_id = owner_id
        self.embedList = embedList
        self.fished = False

    @ui.button(label="🎣 낚싯대 당기기!", style=ButtonStyle.primary)
    async def fish_button(self, button: ui.Button, interaction: Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message("이건 당신의 낚시가 아니에요!", ephemeral=True)
            return

        self.fished = True
        await interaction.response.edit_message(content="🐟 잡았다!", view=None)
        self.stop()