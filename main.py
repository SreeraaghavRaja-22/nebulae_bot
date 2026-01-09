import os
import discord
from discord.ext import commands 
from discord import app_commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# these are like the default intents for discord 
# assign all intents before creating the bot with the client
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

class Client(commands.Bot): # used to be discord.Client
    # pre-defined function when discord bot runs
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        try: 
            guild =  discord.Object(id = 1069104601724375140)
            synced = await self.tree.sync(guild = guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')

    
    async def on_message(self, message):
        if(message.author == self.user):
            return # stops the bot from replying to itself
        
        if message.content.startswith('hello'):
            await message.channel.send(f'Hi there {message.author}')
        
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        
        # check if there was a reaction in the server and check if it corresponded to the message id
        guild = reaction.message.guild
        if not guild:
            return
        if hasattr(self, "color_role_message_id") and reaction.message.id != self.color_role_message_id:
            return
        
        emoji = str(reaction.emoji)

        reaction_role_map = {
        '🩵' : 'Light Blue',
        '💚' : 'Green',
        '❤️' : 'Red',
        '💜' : 'Purple',
        '💛' : 'Yellow'
        } 

        if emoji in reaction_role_map:
            role_name = reaction_role_map[emoji]
            role = discord.utils.get(guild.roles, name = role_name)
            
            # if role and user exits
            if role and user:
                await user.add_roles(role)
                await reaction.message.channel.send(f'Assigned {role_name} to {user}')

    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return
        
        # check if there was a reaction in the server and check if it corresponded to the message id
        guild = reaction.message.guild
        if not guild:
            return
        if hasattr(self, "color_role_message_id") and reaction.message.id != self.color_role_message_id:
            return
        
        emoji = str(reaction.emoji)

        reaction_role_map = {
        '🩵' : 'Light Blue',
        '💚' : 'Green',
        '❤️' : 'Red',
        '💜' : 'Purple',
        '💛' : 'Yellow'
        } 

        if emoji in reaction_role_map:
            role_name = reaction_role_map[emoji]
            role = discord.utils.get(guild.roles, name = role_name)
            
            # if role and user exits
            if role and user:
                await user.remove_roles(role)
                await reaction.message.channel.send(f'Removed {role_name} from {user}')
                
    async def on_message_edit(self, before, after):
        if before.author == client.user:
            return 
        
        if before.content == after.content:
            return 
        
        await after.channel.send(f"{before.author.mention} edited a message \n"
                                 f"Before: {before.content} \n"
                                 f"After: {after.content}")
            
        


client = Client(command_prefix="!", intents=intents)

# client = Client(intents=intents)

# specify server when doing slash commands or else it takes forever#
GUILD_ID = discord.Object(id = 1069104601724375140)

# create a slash command / name cannot be capitalized
@client.tree.command(name="hellooo", description="Say hello!", guild = GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there")

@client.tree.command(name="printer", description="I will print whatever you give me!", guild = GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str, num: int):
    await interaction.response.send_message(f"{printer}, {num}")

@client.tree.command(name="embed", description="Embed demo!", guild = GUILD_ID)
async def printer(interaction: discord.Interaction):
    embed = discord.Embed(title="I am a Titan", url = "https://en.wikipedia.org/wiki/Hyperion_(Titan)", description="Hyperion", color=discord.Colour.fuchsia())
    # display an image
    embed.set_thumbnail(url="https://www.quartertothree.com/fp/wp-content/uploads/2018/08/Hyperion_review.jpg")
    # add a field (information) into the embed
    embed.add_field(name="Information", value = "Known as the Titan of Light", inline = False)
    embed.add_field(name="Descendents", value = "Helios: God of the Sun\n Selene: Goddess of the Moon\n Anemoi: Notus, Zephyrus, Eurus, and Boreas")
    # footer
    embed.set_footer(text="Thank you for reading!")
    # author
    embed.set_author(name=interaction.user.name, url="https://en.wikipedia.org/wiki/Hyperion_(Titan)", icon_url="https://static.wikia.nocookie.net/gintama/images/b/b3/Bby.png/revision/latest/scale-to-width/360?cb=20160506220450")
    # need to tell discord what channel to send embed to 
    await interaction.response.send_message(embed=embed)


# create a class for the ui and configure the button
class View(discord.ui.View):
    @discord.ui.button(label="Learn More!", style = discord.ButtonStyle.red, emoji = "🤑")
    async def button_callback(self, button, interaction):
        # can put anything in this button function to configure the button function
        await button.response.send_message("You're going to learn more!")

    @discord.ui.button(label="Learn More 2!", style = discord.ButtonStyle.green, emoji = "😈")
    async def button_callback2(self, button, interaction):
        # can put anything in this button function to configure the button function
        await button.response.send_message("You're so evil!") 
    
    @discord.ui.button(label="Learn More 3!", style = discord.ButtonStyle.blurple, emoji = "🐐")
    async def button_callback3(self, button, interaction):
        # can put anything in this button function to configure the button function
        await button.response.send_message("You're the goat!") 

@client.tree.command(name="button", description="Displaying a button", guild = GUILD_ID)
async def my_button(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())


# class for the menu select
class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label = "Euryale",
                description = "Gorgon 1",
                emoji="🦇"
            ),
            discord.SelectOption(
                label = "Stheno",
                description = "Gorgon 2",
                emoji = "👙"
            ),
            discord.SelectOption(
                label = "Medusa",
                description = "Gorgon 3",
                emoji = "🗿"
            )
        ]

        # min and max values are how many options we want a user to select
        # access the parent class
        super().__init__(placeholder="Please choose an option", min_values=1, max_values = "1", options=options)

    # must be called callback
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Euryale": 
            await interaction.response.send_message(f'You picked {self.values[0]}')
        elif self.values[0] == "Stheno":
            await interaction.response.send_message(f'You are correct')
        else:
            await interaction.response.send_message(f'MEDUSA', view = View())


# creating a class to display the dropdown menu
class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__() # initialize the parent class
        self.add_item(Menu())


# create a / command to display the dropdown menu
@client.tree.command(name="menu", description="Displaying a dropdown menu", guild = GUILD_ID)
async def my_menu(interaction: discord.Interaction):
    await interaction.response.send_message(view=MenuView())

# create a / command to get a specific role
@client.tree.command(name="color_roles", description="Lets users pick a color role", guild = GUILD_ID)
async def color_roles(interaction: discord.Interaction):
    # check admin
    if not interaction.user.guild_permissions.administrator: # ephemeral = true, only a certain user can see that role
        await interaction.respond.send_message("You must be an admin to run this command", ephemeral = True)
        return 

    # acknowledge that the bot needs to send a response / ignores the 3 second rule because for loop would make it take too long
    await interaction.response.defer(ephemeral = True)
    
    description = (
        "React to this message to get your color role!\n\n"
        "🩵 Light-Blue\n"
        "💚 Green\n"
        "❤️ Red\n"
        "💜 Purple\n"
        "💛 Yellow\n"
    )

    # embed 
    embed = discord.Embed(title="Pick your color!", description=description, color = discord.Color.blurple())
    message = await interaction.channel.send(embed=embed)

    emojis = ['🩵', '💚', '❤️', '💜', '💛']

    # add emojis to that react to the bot's message
    for emoji in emojis:
        await message.add_reaction(emoji)
    
    # detect 
    client.color_role_message_id = message.id

    # followup to the defer
    await interaction.followup.send("Color role message created!", ephemeral = True)



# need to add the unique token for the discord bot
client.run(TOKEN)