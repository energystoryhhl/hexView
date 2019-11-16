from intelhex import IntelHex
import main_

if __name__ == '__main__':

    originHexName = "GAW3.1_TC387_A0_201901101_SPI.hex"
    originHex ,startAddr,endAddr= main_.loadHex(originHexName)
    newhex = main_.mergeAllBlocks(originHex,startAddr,0x200000)
    print("writing file...")
    newhex.write_hex_file(originHexName.replace(".hex","_merged.hex"))




