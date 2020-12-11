"""

StarLight Company Bot
---
by Not Tani#6135

Copyright © 2020 Tani Writes Code

LICENCED UNDER THE MIT LICENCE:
https://tani.mit-license.org
"""

import discord
import os
import random

code = random.randint(0, 10000)

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

with open('text/welcome_message.txt', 'r') as w:
    welcome_message = ''.join(w.readlines())

with open('text/starlight_help.txt', 'r') as w:
    starlight_help = ''.join(w.readlines())

@client.event
async def on_ready():
    print(f"{client.user} connected to Discord!")


@client.event
async def on_member_join(member):
    await member.send(welcome_message)


# I've opted not to use the discord.ext.commands module because
# I'm implementing only one command, and so for simplicity,
# I've done it this way.
@client.event
async def on_message(message):
    if message.content.startswith("v!verify"):
        verify_message = message.content.split(" ")
        # Calculated based on user id combined with a random number.
        # Should stop simple bots very easily, didn't want fully random
        # code because Heroku's filesystem is stateless and a database
        # is a bit beyond the scope of this project
        verify_code = str(message.author.id + code)[:5]
        verify_role = discord.utils.get(message.author.guild.roles, name="verified")

        # Check if server owner has setup the `verified` role
        if not verify_role:
            await message.channel.send(f"{message.author.mention} - this server does not have a `verified` role.")
            return

        # If the message is just "v!verify" or similar
        if len(verify_message) == 1:
            await message.channel.send(
                f"{message.author.mention} - to gain the verified role, please type\n`v!verify {verify_code}`"
            )

        # A two part message means that they are entering a code as well
        elif len(verify_message) == 2:
            if verify_message[1] == verify_code:
                await message.author.add_roles(verify_role)
                await message.add_reaction("✅")
                await message.channel.send(
                    f"{message.author.mention} - you have been verified!"
                )
            else:
                await message.add_reaction("🚫")
                await message.channel.send(
                    f"{message.author.mention} - You have not been verified. Please check your code."
                )
    elif message.content.startswith("v!help"):
        await message.add_reaction("✅")
        await message.channel.send(f"")

client.run(os.environ["AUTH_TOKEN"])
