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
    DiscIRC launcher
    ----------------

    Launcher for DiscIRC app
"""

import asyncio
import os.path as op
import sys
import json

from discord_bot import DiscordWrapper
from irc_bot import IRCBot


__author__ = 'TROUVERIE Joachim'


def main():
    config = op.expanduser('cfg.json')

    with open(config, 'r') as fi:
        conf = json.load(fi)

    irc = IRCBot(conf)
    disc = DiscordWrapper(conf)

    loop = asyncio.get_event_loop()
    loop.create_task(irc.connect())
    loop.create_task(disc.run())
    loop.run_forever()

main()