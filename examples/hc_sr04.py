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
 """

import asyncio
import sys
import time

from tmx_pico_aio import tmx_pico_aio

"""
This is an example program for HC-SR04 type distance sensors.

A single device was tested attaching  a device to pins 16 and  17 
Pins  2, 3, 4, 5, 6,  7  have no HC-SR04 attached, but demonstrate
 that multiple device may be attached simultaneously. 
"""

# some globals
TRIGGER_PIN = 16
ECHO_PIN = 17

# indices into callback data
TRIGGER = 1
DISTANCE_IN_CENTIMETERS = 2
TIME_STAMP = 3


async def the_callback(data):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[TIME_STAMP]))

    print(f'{date}\t Trigger Pin::\t{data[TRIGGER]}\t Distance(cm):\t'
          f'{data[DISTANCE_IN_CENTIMETERS]}')


async def get_distance(the_board):
    # await the_board.set_pin_mode_sonar(2, 3, the_callback)
    # await the_board.set_pin_mode_sonar(4, 5, the_callback)
    await the_board.set_pin_mode_sonar(TRIGGER_PIN, ECHO_PIN, the_callback)
    # await the_board.set_pin_mode_sonar(6, 7, the_callback)

    while True:
        # do nothing but sleep while the reports come in.
        await asyncio.sleep(1)


# get the event loop
loop = asyncio.get_event_loop()

try:
    board = tmx_pico_aio.TmxPicoAio()
except KeyboardInterrupt:
    sys.exit()

try:
    # start the main function
    loop.run_until_complete(get_distance(board))
    loop.run_until_complete(board.reset_board())
except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
except RuntimeError:
    sys.exit(0)