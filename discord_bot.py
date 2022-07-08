import math
from typing_extensions import Self
from config import Config
from utils import clean_text

import string
import discord
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
from discord.ext import tasks
import torch
import time
import re
import threading
import asyncio
COOLDOWN_AMOUNT_SECONDS = 60
last_executed = {}


class Discord_Bot(discord.Client):
    # print(Config.HUGGINGFACE_KEY)

    def __init__(self, intents):
        super().__init__(intents = intents)
        
        self.CHANNEL_ID = int(989976603243188227)
        self.GUILD_ID = int(989976603243188224)
        self.TOKEN_AUTH = Config.TOKEN
        self.MODEL = AutoModelForCausalLM.from_pretrained("Gods/discord_test")
        self.TOKENIZER = AutoTokenizer.from_pretrained("Gods/discord_test")
        self.count = 0
        self.chat_history_ids = None
        # self.USER = 
        self.current_time = time.time()
        self.check = True

    async def on_ready(self):

            guilds = list(self.guilds)
            server = None
            for guild in guilds:
                if guild.id == self.GUILD_ID:
                    server = guild
                    channel = server.get_channel(self.CHANNEL_ID)

            if server and channel:
                logging.info('Server and channel are found')            
            else:
                raise Exception(f"Channel ID {self.CHANNEL_ID} or Server ID {self.GUILD_ID} not exists.")
            # logging.info('Ready')
            print('ready')


    def generateResponse(self, message) -> string:
        # print(message.content)
        text = clean_text(" ".join(str(message.content).split()))
        # print(text)
        if not text: 
            print('Only emoji')
            return "I'm tired"
        input_ids = self.TOKENIZER.encode(text + self.TOKENIZER.eos_token, return_tensors='pt')
        new_chat_history_ids =  input_ids if self.count == 0 else torch.cat([self.chat_history_ids, input_ids], dim=-1)
        if self.count > 5:
            new_chat_history_ids = input_ids
            self.count = 0

        self.chat_history_ids = self.MODEL.generate(
            new_chat_history_ids, max_length=500,
            pad_token_id=self.TOKENIZER.eos_token_id,
            no_repeat_ngram_size=2,       
            do_sample=True, 
            top_k=100, 
            top_p=0.7,
            temperature = 0.8
        )
        self.count +=1

        text = self.TOKENIZER.decode(self.chat_history_ids[:, new_chat_history_ids.shape[-1]:][0], skip_special_tokens=True).replace("\n", ' ')
        text = re.sub(r'[^\w\s]','',text)
        return text


    def mention_message(self, message):
        reference = None
        if self.user in message.mentions:
            print('You are mentioned')
            try:
                reference = message.to_reference()

            except discord.HTTPException: 
                print("Message has been deleted or can't be found")
    
        return reference


    async def reply(self, message, reference=None):
        async with message.channel.typing():
                response = self.generateResponse(message)
                # logging.info(response)
            # logging.info("sentence")
                print(response)
                if not response:
                    self.check = True
                    return
        await message.channel.send(response, reference=reference, mention_author=False)
        if not self.check:
            self.check = True
        self.current_time = time.time()

    async def on_message(self, message):
        # answering mentioned msg is the top priority
        reference = self.mention_message(message)
        # print(reference)
        if reference:
            asyncio.create_task(self.reply(message, reference))
            print("Done")
# https://stackoverflow.com/questions/72118914/cooldown-on-an-on-message-event-discord-py
        if last_executed.get(self.user.id, 1.0) + COOLDOWN_AMOUNT_SECONDS < time.time():
            
            print("You are not mentioned")
# https://stackoverflow.com/questions/67339174/discord-api-soft-ban-for-selfbot-it-can-only-read-its-own-messages
            async for message in message.channel.history(limit=1):
                
                print(message.content)


            isSelf = message.author == self.user
            isBot = message.author.bot == True

            if message.channel.id != self.CHANNEL_ID:
                print('different channel')
                return

            # terminate the bot
            # if isSelf and ('!' in message.content):
            #     print('Special char found.. Terminating...')
            #     await self.close()

    # don't talk to 1) myself 2) server bot that pops up when you level up..
            if isSelf or isBot:
                return
            

            asyncio.create_task(self.reply(message, reference))

            last_executed[self.user.id] = time.time()
        else:
            await asyncio.sleep(5)


if __name__ == '__main__':
    # intents = discord.Intents(messages=True, typing=True)
    # required to fire on_message()
    intents = discord.Intents.all()

    dc = Discord_Bot(intents=intents)
# https://github.com/Rapptz/discord.py/issues/918
    logging.info('Starting....')
    # dc.intents = intents
    dc.run(dc.TOKEN_AUTH, bot=False)


#  Additional rss
# https://github.com/Rapptz/discord.py/issues/192
# https://www.reddit.com/r/Discord_selfbots/comments/n3b907/change_in_api_that_prevents_selfbots_from_seeing/
# https://code.visualstudio.com/docs/python/python-tutorial#_install-and-use-packages