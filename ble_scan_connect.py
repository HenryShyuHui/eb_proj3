# ble_scan_connect.py:
from bluepy.btle import Peripheral, UUID, Characteristic
from bluepy.btle import Scanner, DefaultDelegate
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)
            
# different module
class MyDelegate(DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print ("Notification received: handle =", cHandle, "; Raw data =", binascii.b2a_hex(data))


scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
n=0
addr = []
for dev in devices:
    print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr,
dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print (" %s = %s" % (desc, value))
number = input('Enter your device number: ')
print ('Device', number)
num = int(number)
print (addr[num])
#
print ("Connecting...")
dev = Peripheral(addr[num], 'random')
#
print ("Services...")
for svc in dev.services:
    print (str(svc))
#
try:
    testService = dev.getServiceByUUID(UUID(0xfff0))
    for ch in testService.getCharacteristics():
        print (str(ch))
#
    ch = dev.getCharacteristics(uuid=UUID(0xfff1))[0]
    print(ch.propertiesToString())
    cccd_uuid = 0x2902
    cccd_handle = ch.getHandle() + 1  # CCCD handle is the characteristic handle + 1
    dev.writeCharacteristic(cccd_handle, b"\x01\x00")
    print(ch.propertiesToString())
    if (ch.supportsRead()):
        print (ch.read())
        

    ch = dev.getCharacteristics(uuid=UUID(0xfff2))[0]
    if (ch.supportsRead()):
        print (ch.read())
        ch.write("fuck u BLE 0xfff2".encode("utf-8"))
        

    ch = dev.getCharacteristics(uuid=UUID(0xfff3))[0]
    
    
    print(ch.propertiesToString())
    if (ch.supportsRead()):
        print (ch.read())
        ch.write("fuck u BLE 0xfff3".encode("utf-8"))

    ch = dev.getCharacteristics(uuid=UUID(0xfff4))[0]
    print(ch.propertiesToString())
    print(ch.getHandle())
    print(hex(ch.getHandle()))
    # cccd = ch.getHandle() + 1
    # dev.writeCharacteristic(cccd, bytes([0x01, 0x00]))
    if (ch.supportsRead()):
        print (ch.read())
        ch.write("fuck u BLE".encode("utf-8"))
        # ch.setWriteType(WRITE_TYPE_DEFAULT)
        # setValue = ch.setValue(new byte[]{/*..BYTES.*/})
        # writeCharacteristic=dev.writeCharacteristic(ch)
        # print (setValue)
        # print (writeCharacteristic)
    cccd_handle = ch.getHandle() + 1 
    print (hex(cccd_handle))
    k = dev.writeCharacteristic(cccd_handle, b"\x01\x00")
    print(ch.propertiesToString())
    print(k)


    while True:
        ch = dev.getCharacteristics(uuid=UUID(0xfff4))[0]
        if (ch.supportsRead()):        
            if dev.waitForNotifications(1.0):
                # handleNotification() was called
                print ("notify, value is :", ch.read())
                continue
        print("Waiting...")
        

#
finally:
    dev.disconnect()
