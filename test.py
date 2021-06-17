from bleclient import BleClient

address = 'C4:6B:9B:7E:7E:F9'
write_characteristic_id = 'ab107001-7698-badc-fede-bc9a78563412'
read_characteristic_id = 'ab107002-7698-badc-fede-bc9a78563412'

print("start")
ble = BleClient(address, write_characteristic_id, read_characteristic_id)
print("read start")

val = ble.read([0x2a, 0x2b])
print(val)

print("write")
values = []
values.append(bytearray([0x01]))
val, compare = ble.write([0x2a], values)

print(val)
print(compare)
