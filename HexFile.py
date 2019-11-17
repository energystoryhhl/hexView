from intelhex import IntelHex
from tqdm import tqdm, trange



class HexFile:
    def __init__(self,fileName):
        self.blocks_ = list()
        self.hexFile_ = IntelHex()
        self.startAddr_ = 0
        self.endAddr_ = 0
        self.loadHex(fileName)

    def loadHex(self,fileName):
        self.hexFile_.loadhex(fileName)
        self.startAddr_ = self.hexFile_.segments()[0][0]
        self.endAddr_ = self.hexFile_.segments()[-1][1] - 1
        self.blocks()

    def mergeAllBlocks(self,startAddr, length, pad = 0xff):
        if startAddr < self.startAddr_ or startAddr > self.endAddr_:
            print("start addr not in hex addr")
            return
        if startAddr + length > self.endAddr_:
            print("length over hex length")
            return
        newHexFile = IntelHex()
        for byte in tqdm(range(length)):
            newHexFile[startAddr + byte] = self.hexFile_[startAddr + byte]
        self.hexFile_ = newHexFile

        self.startAddr_ = self.hexFile_.segments()[0][0]
        self.endAddr_ = self.hexFile_.segments()[-1][1] - 1
        self.blocks()

    def setPad(self, pad):
        self.hexFile_.padding(pad)

    def startEndAddr(self):
        return self.startAddr_, self.endAddr_

    def blocks(self):
        self.blocks_.clear()
        i = 0
        for block in self.hexFile_.segments():
            blockInfo = dict()
            blockInfo['startAddr'] = block[0]
            blockInfo['endAddr'] = block[1] - 1
            blockInfo['length'] = block[1] - block[0]
            self.blocks_.append(blockInfo)
            i = i+1

    def getBlocks(self):
        return self.blocks_

if __name__ == '__main__':
    originHexFile = "GAW3.1_TC387_A0_201901101_SPI.hex"
    additionalHexFile = "C229_G8R410A500_CanFlash.hex"

    hex1 = HexFile(originHexFile)

    print(hex(hex1.startEndAddr()[0]))
    print(hex(hex1.startEndAddr()[1]))

    blockInfos = hex1.getBlocks()

    for i in blockInfos:
        print(hex(i['startAddr']))
        print(hex(i['endAddr']))
        print(hex(i['length']))

