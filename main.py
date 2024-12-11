#app ID: 1310977643629383750

# Public key:  8af17458780d8d54fee297f109a628c6a56654921dedc8dfa152152d8d9703ac
# This example requires the 'message_content' intent.

# This example requires the 'message_content' intent.

import discord
import os
import google.generativeai as genai
import requests
from io import BytesIO

import google.generativeai as genai

genai.configure(api_key=os.environ["gemini_api"])
image = "ImageGPT"

token = os.getenv("secret_key")
st = "act as a discord bot and respond to the following conversation in the most helpful way possible. You are a helpful assistant. response should be less than or equal to 2000 characters"



class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        mentioned_users = [user.name for user in message.mentions]
        if self.user != message.author:
          if self.user in message.mentions:

            channel = message.channel
            await message.channel.send(f'Hello {message.author.mention}!')
            try:
                author = "you are responding to " + str(message.author)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(st + author + message.content)
                message_to_send = response.text
                print(f'response: {response}'
                      )  
                await channel.send(
                    message_to_send
                )
            except Exception as e:
                print(f"Error: {e}")
                await channel.send(
                    "Oops, something went wrong when processing your request."
                )

        if image in mentioned_users:
            channel = message.channel 
            await message.channel.send(f'Hello {message.author.mention}!')
            try:
                url = "https://pollinations.ai/prompt/" + message.content
                response = requests.get(url)
                if response.status_code == 200:
                      image_data = BytesIO(response.content)
                      image_data.seek(0)
                      await channel.send(file=discord.File(image_data, 'generated_image.png'))
                else:
                      await channel.send("Could not retrieve the image from the server.")

            except Exception as e:
                          # If an error occurs, log it and send an error message to the channel
                          print(f"Error: {e}")
                          await channel.send(
                              "Oops, something went wrong when processing your request."
                          )





intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
