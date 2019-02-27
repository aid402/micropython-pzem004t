# Micropython communication library for Peacefair PZEM-004T Energy monitor
# Author --> Suttipong Wongkheaw
# Github --> https://github.com/aid402/micropython-pzem004t
# Credit --> https://github.com/rafaelferreirapt/pzem004t-to-emoncms

from machine import UART
from struct import unpack

class PZEM004T:
    setAddrBytes = bytearray([0xB4, 0xC0, 0xA8, 0x01, 0x01, 0x00, 0x1E])
    readVoltageBytes = bytearray([0xB0, 0xC0, 0xA8, 0x01, 0x01, 0x00, 0x1A])
    readCurrentBytes = bytearray([0XB1, 0xC0, 0xA8, 0x01, 0x01, 0x00, 0x1B])
    readPowerBytes = bytearray([0XB2, 0xC0, 0xA8, 0x01, 0x01, 0x00, 0x1C])
    readEnergyBytes = bytearray([0XB3, 0xC0, 0xA8, 0x01, 0x01, 0x00, 0x1D])
    setPowerAlarmCmd = [0XB3, 0xC0, 0xA8, 0x01, 0x01, 0x00, 0x1D]

    def __init__(self,id=0):
        self.uart = UART(id)
        self.init()

    def init(self):
        self.uart.init(9600, bits=8, parity=None, stop=1)

    def checkChecksum(self, _tuple):
        _list = list(_tuple)
        _checksum = _list[-1]
        _list.pop()
        _sum = sum(_list)

        if _checksum == _sum % 256:
            return True
        else:
            return False

    def isReady(self):
        data = self.send(self.setAddrBytes)
        if data[0]:
            return True
        return False

    def readVoltage(self):
        data = self.send(self.readVoltageBytes)
        if data[0]:
            return data[2] + data[3] / 10.0
        return None

    def readCurrent(self):
        data = self.send(self.readCurrentBytes)
        if data[0]:
            return data[2] + data[3] / 100.0
        return None

    def readPower(self):
        data = self.send(self.readPowerBytes)
        if data[0]:
            return data[1] * 256 + data[2]
        return None

    def readEnergy(self):
        data = self.send(self.readEnergyBytes)
        if data[0]:
            return data[1] * 256 * 256 + data[2] * 256 + data[3]
        return None

    def readAll(self):
        return self.readVoltage(), self.readCurrent(), self.readPower(), self.readEnergy()

    def send(self, cmd):
        self.uart.read()
        self.uart.write(cmd)
        while not self.uart.any():
            pass
        data = self.uart.read(7)
        unpacked = unpack("!7B", data)
        if self.checkChecksum(unpacked):
            return unpacked
        return None
