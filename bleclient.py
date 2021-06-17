import asyncio
from bleak import BleakClient

class BleClient:
    address = ''
    write_characteristic_id = ''
    read_characteristic_id = ''
    loop = None

    def __init__(self, address, write_characteristic_id, read_characteristic_id):
        self.address = address
        self.write_characteristic_id = write_characteristic_id
        self.read_characteristic_id = read_characteristic_id
        self.loop = asyncio.get_event_loop()

    def read(self, commands):
        return self.loop.run_until_complete(self.__read(commands))

    def write(self, commands, values):
        return self.loop.run_until_complete(self.__write(commands, values))

    def __create_read_command(self, c):
        r_command = bytearray([c])
        r_command.append(0x00)  # 長さ0
        return r_command

    def __create_write_command(self, c, v):
        wc = c + 0x80  # write command
        w_command = bytearray([wc])
        w_command.extend(bytearray([len(v)]))
        w_command.extend(v)
        return w_command

    async def __read(self, commands):
        async with BleakClient(self.address) as client:
            if not client.is_connected:
                return None
            ret = []
            for c in commands:
                r_command = self.__create_read_command(c)
                await client.write_gatt_char(self.write_characteristic_id, r_command)
                value = await client.read_gatt_char(self.read_characteristic_id)
                ret.append(value[2:])
            return ret

    async def __write(self, commands, values):
        async with BleakClient(self.address) as client:
            if not client.is_connected:
                return None
            ret = []
            compare = []
            for i, c in enumerate(commands):
                # write
                v = values[i]
                w_command = self.__create_write_command(c, v)
                await client.write_gatt_char(self.write_characteristic_id, w_command)

                # read
                r_command = self.__create_read_command(c)
                await client.write_gatt_char(self.write_characteristic_id, r_command)
                value = await client.read_gatt_char(self.read_characteristic_id)
                v2 = value[2:]
                ret.append(v2)
                if v == v2:
                    compare.append(True)
                else:
                    compare.append(False)
            return ret, compare

