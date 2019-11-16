import  json

if __name__ == '__main__':
    script = dict()
    script["HexStartAddr"] = 0xa0000000
    script["HexLength"] = 0x200000

    print(json.dumps(script))

    scriptFile = open("script.json",'w+')
    scriptFile.write(json.dumps(script))
    scriptFile.close()

    content = json.load(open("script.json"))
    print(hex(content["HexStartAddr"]))


