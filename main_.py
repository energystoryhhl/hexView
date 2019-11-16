##from fileAnalysis import *
from intelhex import IntelHex
from tqdm import tqdm, trange
import time
def merge_all_hex_segments(file_name,padding = 0xff):
    origin_hex_file = IntelHex()
    origin_hex_file.loadhex(file_name)

def loadHex(fielname):
    hex_file = IntelHex()
    hex_file.loadhex(fielname)
    print("block number is: " + str(len(hex_file.segments())))
    print("start addr is: " + str(hex(hex_file.segments()[0][0])))
    print("end addr is: " + str(hex(  hex_file.segments()[-1][1]-1     )))
    return hex_file,hex_file.segments()[0][0],hex_file.segments()[-1][1]-1


def mergeAllBlocks(hexfile, startAddr, length):
    newHexFile = IntelHex()
    for i in tqdm(range(length)):
        newHexFile[startAddr + i] = hexfile[startAddr + i]
    return newHexFile

def appendHex(originHex,additionalHex,originStartAddr,additionalAddr,length):
    newHexFile = originHex
    for i in tqdm(range(length)):
        newHexFile[originStartAddr + i] = additionalHex[additionalAddr + i]
    return newHexFile



if __name__ == '__main__':
    print("hexfile hhl 2019/11/12")

    originHexFile = "GAW3.1_TC387_A0.hex"
    additionalHexFile = "C229_G8R410A500_CanFlash.hex"

    hexfile, startAddr, endAddr = loadHex(originHexFile)
    addhexfile, addstartAddr, addendAddr = loadHex(additionalHexFile)

    newHexFileStartAddr = 0xa0000000
    newHexFileLength = 0x200000

    print("merge all locks:")
    newHexFile = mergeAllBlocks(hexfile, newHexFileStartAddr, newHexFileLength)
    time.sleep(1)
    print("append data")
    new2hex = appendHex(newHexFile, addhexfile, newHexFileStartAddr, newHexFileStartAddr, 0x20000)

    new2hex.write_hex_file("new2hex.hex")
    print("done")

    #hex_file.merge()


