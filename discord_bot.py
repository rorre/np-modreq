#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
    Discord bot
    -----------

    Discord bot for DiscIRC app
"""

import re
import math
import requests
import asyncio
import discord
import signals as SIGNALNAMES

from asyncblink import signal
from message import Message

__author__ = 'TROUVERIE Joachim'


class DiscordWrapper(object):
    """Discord bot wrapper

    :param config: config for bot
    :type config: dict
    """

    def __init__(self, config):
        self.config = config
        self.bot = discord.Client()
        self.token = config['discordToken']
        self.command_chars = config.get('commandChars', [])

        # signals
        self.discord_signal = signal(SIGNALNAMES.DISCORD_MSG)
        self.irc_signal = signal(SIGNALNAMES.IRC_MSG)
        self.irc_signal.connect(self.on_irc_message)

        self.bot.event(self.on_message)

    def run(self):
        """Run discord bot"""
        self.bot.run(self.token)

    async def on_message(self, message):
        """Event on discord message received

        :param message: Discord message
        """
        pass

    async def on_irc_message(self, sender, **kwargs):
        """Event on IRC message received

        :param message: IRC message
        """
        message = kwargs['data']
        private = kwargs['private']
        regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        links = re.findall(regex, message.content)
        domain = "https://osu.ppy.sh/"
        setlink = None

        if private:
            target = self.bot.get_user(self.config['owner'])

        for link in links:
            if link.startswith(domain + "b"):
                setlink = link
                setid = link.split("/")[-1]
                break

        if not setlink:
            return

        res = requests.get("https://osu.ppy.sh/api/get_beatmaps?k={}&b={}".format(self.config['osukey'], setid))
        beatmap = res.json()[0]
        if not beatmap:
            return
        length = ':'.join([str(math.floor(int(beatmap['total_length']) / 60)), str(int(beatmap['total_length']) % 60)])
        
        res = requests.get("https://osu.ppy.sh/api/get_user?k={}&u={}".format(self.config['osukey'], message.source)).json()[0]
        uid = res['user_id']

        if target:
            print("target")
            embed = discord.Embed(title="Mod Request", url=setlink)
            embed.set_author(name=message.source, url="https://osu.ppy.sh/u/" + message.source,
                             icon_url="https://a.ppy.sh/{}_15485582934872985707.jpeg".format(uid))
            embed.set_thumbnail(url="https://b.ppy.sh/thumb/{}l.jpg".format(beatmap['beatmapset_id']))
            embed.add_field(name="Artist", value=beatmap['artist'], inline=True)
            embed.add_field(name="Title", value=beatmap['title'], inline=True)
            embed.add_field(name="Length", value=length, inline=False)
            embed.add_field(name="BPM", value=beatmap['bpm'], inline=False)
            await target.send(embed=embed)
