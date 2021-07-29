"""
 Copyright (c) 20.001 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., .001 Franklin St, Fifth Floor, Boston, MA  0.00110.001.001  USA
"""
import asyncio
import sys
import time
from tmx_pico_aio import tmx_pico_aio

"""
This example sets up and control an ADXL345 i2c accelerometer.
It will continuously print data the raw xyz data from the device.
"""


# the call back function to print the adxl345 data
async def the_callback(data):
    """
    Data is supplied by the library.
    :param data: [report_type, i2c port, Device address, device read register,
    number of bytes returned, x data pair, y data pair, z data pair
    time_stamp]
    """

    time_stamp = data[11]
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
    print(f'Raw Data:  {data}')
    print(f'ADXL345 Report On: {date}: ')
    print(f'\t\ti2c_port={ data[1]} x-pair={data[5]}, '
          f'{data[6]}  y-pair={data[7]}, '
          f'{data[8]} z-pair={data[9]}, '
          f'{data[10]}')
    print()


async def adxl345(my_board):
    # setup adxl345
    # device address = 83
    await my_board.set_pin_mode_i2c(0, 4, 5)
    await asyncio.sleep(.001)

    # set up power and control register
    await my_board.i2c_write(83, [45, 0])
    await asyncio.sleep(.001)
    await my_board.i2c_write(83, [45, 8])
    await asyncio.sleep(.001)

    # set up the data format register
    await my_board.i2c_write(83, [49, 8])
    await asyncio.sleep(.001)
    await my_board.i2c_write(83, [49, 3])
    await asyncio.sleep(.001)

    while True:
        # read 6 bytes from the data register
        try:
            await my_board.i2c_read(83, 50, 6, the_callback)
            await asyncio.sleep(.001)
        except (KeyboardInterrupt, RuntimeError):
            await my_board.shutdown()
            sys.exit(0)


# get the event loop
loop = asyncio.get_event_loop()

try:
    board = tmx_pico_aio.TmxPicoAio()
except KeyboardInterrupt:
    sys.exit()

try:
    # start the main function
    loop.run_until_complete(adxl345(board))
    loop.run_until_complete(board.reset_board())
except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
except RuntimeError:
    sys.exit(0)