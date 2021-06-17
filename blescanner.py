import asyncio
from bleak import discover

class BleScanner():
    loop = None

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def scan(self, keyword=None):
        return self.loop.run_until_complete(self.__scan(keyword))

    async def __scan(self, keyword):
        ret = []
        devices = await discover()
        for d in devices:
            if keyword:
                if keyword in d.name:
                    ret.append(d)
            else:
                ret.append(d)
        return ret

