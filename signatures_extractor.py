import sys
from time import sleep

debug = True

class Signature:
    def __init__(self,name,offset):
        self.name = name
        self.offset = offset
        self.content = []
try:
    try:
        print(sys.argv)
        assert len(sys.argv) >= 3
    except AssertionError:
        if len(sys.argv) == 1:
            e = "No files specified..."
        else:
             e = "No filter was specified..."
        print(f"[ERROR] - {e}")
        sleep(10)
        exit()
    
    print("Reading file...")
    signatures = []
    file = open(sys.argv[1], 'r')
    lines = file.readlines()
    currentSignature = False
    listIsHex = "0123456789ABCDEFabcdef"
    for index, line in enumerate(lines):
        if line == "\n":
            continue
        line = line.split(" ")
        if len(line[0]) == 8: # we have an offset
            if currentSignature:
                signatures.append(currentSignature)
                currentSignature = Signature(line[1].rstrip(),line[0]) # rstrip because it has a \n in it
            else:
                currentSignature = Signature(line[1].rstrip(),line[0])
        if not currentSignature:
            continue
        for element in line[4:10]: # it's the hexes !
            try:
                if element[0] not in listIsHex: # make sure the first thing is hex
                    break
                currentSignature.content.append('\\x' + element.upper()) # that's how hex are formatted in sourcemod signatures
            except IndexError:
                break
    file.close()
    print("Done Reading...")
    for signature in signatures:
        if sys.argv[2].lower() in signature.name.lower():
            print(f"Signature name : {signature.name} (offset : {signature.offset})")
            print(f"Signature :\n {''.join(signature.content)}\n\n")

    input("Press Enter to exit...")

except Exception as e:
    print(f"[ERROR] : Exception {e.__class__.__name__} : {e}")
    sleep(10)


