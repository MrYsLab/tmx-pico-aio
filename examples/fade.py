"""
 Copyright (c) 2021 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,f
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

 DHT support courtesy of Martyn Wheeler
 Based on the DHTNew library - https://github.com/RobTillaart/DHTNew
"""

import sys
import asyncio

from tmx_pico_aio import tmx_pico_aio

"""
Setup a pin for output and fade its intensity
"""

# some globals
# make sure to select a PWM pin
DIGITAL_PIN = 25


async def fade(the_board):
    # Set the DIGITAL_PIN as an output pin
    await the_board.set_pin_mode_pwm_output(DIGITAL_PIN)

    # try:
    # use raw values for a fade
    for level in range(0, 19999, 10):
        await the_board.pwm_write(DIGITAL_PIN, level, raw=True)
    for level in range(19999, 0, -10):
        await the_board.pwm_write(DIGITAL_PIN, level, raw=True)

    await asyncio.sleep(.5)
    # use percentages for a fade
    for level in range(0, 99):
        await the_board.pwm_write(DIGITAL_PIN, level)
        await asyncio.sleep(.01)
    for level in range(99, 0, -1):
        await the_board.pwm_write(DIGITAL_PIN, level)
        await asyncio.sleep(.01)

# get the event loop
loop = asyncio.get_event_loop()
try:
    board = tmx_pico_aio.TmxPicoAio()
except KeyboardInterrupt:
    sys.exit()

try:
    # start the main function
    loop.run_until_complete(fade(board))
    loop.run_until_complete(board.reset_board())
except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
except RuntimeError:
    sys.exit(0)
