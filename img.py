import discord
import os
import google.generativeai as genai
import requests
from io import BytesIO
from urllib.parse import quote

# Google Generative AI configuration
genai.configure(api_key=os.environ["gemini_api"])

# Environment variables
token = os.getenv("secret_key")
st = "act as a discord bot and respond to the following conversation in the most helpful way possible. You are a helpful assistant. response should be less than or equal to 2000 characters."

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

        # Check if the message is not from the bot itself
        if self.user != message.author:

            # Respond to mentions for text-based responses
            if self.user in message.mentions:
                channel = message.channel
                await channel.send(f'Hello {message.author.mention}!')
                try:
                    author = "you are responding to " + str(message.author)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(st + author + message.content)
                    message_to_send = response.text
                    print(f'Response: {response}')  
                    await channel.send(message_to_send)
                except Exception as e:
                    print(f"Error: {e}")
                    await channel.send(
                        "Oops, something went wrong when processing your request."
                    )

            # Image generation logic
            if "image" in message.content.lower():
                channel = message.channel
                await channel.send(f'Hello {message.author.mention}! Generating an image for your prompt...')
                try:
                    # Prepare the prompt for the image generation API
                    prompt = quote(message.content)
                    url = f"https://pollinations.ai/prompt/{prompt}"
                    response = requests.get(url)

                    # Check if the response contains an image
                    if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
                        image_data = BytesIO(response.content)
                        image_data.seek(0)
                        await channel.send(file=discord.File(image_data, 'generated_image.png'))
                    else:
                        await channel.send("Could not retrieve an image from the server.")
                except Exception as e:
                    print(f"Error: {e}")
                    await channel.send(
                        "Oops, something went wrong when processing your image request."
                    )

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True

# Run the bot
client = MyClient(intents=intents)
client.run(token)
