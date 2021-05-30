import re
import math

def getClass(address):
    firstBlock = format(int(address.split('.')[0]), '08b')
    if re.match(r'^0.*', firstBlock):
        return 'A'
    elif re.match(r'^10.*', firstBlock):
        return 'B'
    elif re.match(r'^110.*', firstBlock):
        return 'C'
    elif re.match(r'^1110.*', firstBlock):
        return 'D'
    elif re.match(r'^1111.*', firstBlock):
        return 'E'
    else:
        return 'Invalid'

def getScope(address):
    firstBlock = int(address.split('.')[0])
    secondBlock = int(address.split('.')[1])
    thirdBlock = int(address.split('.')[2])
    fourthBlock = int(address.split('.')[3].split('/')[0])
    if firstBlock == 0:
        return 'Software'
    elif firstBlock == 10:
        return 'Private'
    elif firstBlock == 100 and 64 <= secondBlock <= 127:
        return 'NAT Shared Address Space'
    elif firstBlock == 127:
        return 'Loopback'
    elif firstBlock == 169 and secondBlock == 254:
        return 'DHCP AutoConfig'
    elif firstBlock == 172 and 16 <= secondBlock <= 31:
        return 'Private'
    elif firstBlock == 192 and secondBlock == 0 and thirdBlock == 0:
        return 'IETF Protocol Assignments'
    elif firstBlock == 192 and secondBlock == 0 and thirdBlock == 2:
            return 'TEST-NET-1 Documentation'
    elif firstBlock == 192 and secondBlock == 88 and thirdBlock == 99:
        return 'Reserved. Formerly used for IPv6 to IPv4 relay'
    elif firstBlock == 192 and secondBlock == 168:
        return 'Private'
    elif firstBlock == 198 and 18 <= secondBlock <= 19:
        return 'Benchmark'
    elif firstBlock == 198 and secondBlock == 51 and thirdBlock == 100:
            return 'TEST-NET-2 Documentation'
    elif firstBlock == 203 and secondBlock == 0 and thirdBlock == 113:
        return 'TEST-NET-3 Documentation'
    elif firstBlock == 233 and secondBlock == 252 and thirdBlock == 0:
        return 'MCAST-TEST-NET Documentation'
    elif 224 <= firstBlock <= 239:
        return 'Multicast'
    elif 240 <= firstBlock <= 255 and 0 <= fourthBlock <= 254:
        return 'Reserved for Future Use'    
    elif firstBlock == 255 and secondBlock == 255 and thirdBlock == 255 and fourthBlock == 255:
        return 'Broadcast'
    else:
        return 'Public'

def getSubnetmask(address, mode ='decimal', complement = False):
    subnetmaskBit = ''
    subnetmask = ''
    networkBits = int(address.split('/')[1])
    for i in range(0, 32):
        if networkBits > 0:
            if complement:
                subnetmaskBit += '0'
            else:
                subnetmaskBit += '1'
            networkBits -= 1
        else:
            if complement:
                subnetmaskBit += '1'
            else:
                subnetmaskBit += '0'
    if mode == 'decimal':
        for index in range(0, 32, 8):
            binary = subnetmaskBit[index:index+8]
            decimal = 0
            for digit in binary:
                decimal = decimal*2 + int(digit)
            subnetmask += str(decimal) + '.' 
        subnetmask = subnetmask[:-1]
        return subnetmask
    elif mode == 'binary':
        subnetmask = '.'.join(subnetmaskBit[i:i+8] for i in range(0, len(subnetmaskBit), 8))
        return subnetmask

def getBinaryIP(address):
    ip = address.split('/')[0]
    firstBlock = format(int(ip.split('.')[0]), '08b')
    secondBlock = format(int(ip.split('.')[1]), '08b')
    thirdBlock = format(int(ip.split('.')[2]), '08b')
    fourthBlock = format(int(ip.split('.')[3]), '08b')
    binaryIp = f'{firstBlock}.{secondBlock}.{thirdBlock}.{fourthBlock}'
    return binaryIp

def getActualNetworks(desiredNetworks):  
    return 1<<(desiredNetworks-1).bit_length() 

def getSubnetsBitsToBorrow(desiredNetworks):
    actualNetworks = getActualNetworks(desiredNetworks)
    return int(math.log2(actualNetworks))

def getNetworkInfo(address, mode = 'network'):
    ip = address.split('/')[0]
    firstBlockIP = int(ip.split('.')[0])
    secondBlockIP = int(ip.split('.')[1])
    thirdBlockIP = int(ip.split('.')[2])
    fourthBlockIP = int(ip.split('.')[3])

    if mode in('network', 'firstHost'):
        subnetMask = getSubnetmask(address)
        firstBlockMask = int(subnetMask.split('.')[0])
        secondBlockMask = int(subnetMask.split('.')[1])
        thirdBlockMask = int(subnetMask.split('.')[2])
        fourthBlockMask = int(subnetMask.split('.')[3])
    else:
        subnetMaskComplement = getSubnetmask(address, 'decimal', True)
        firstBlockMaskComplement = int(subnetMaskComplement.split('.')[0])
        secondBlockMaskComplement = int(subnetMaskComplement.split('.')[1])
        thirdBlockMaskComplement = int(subnetMaskComplement.split('.')[2])
        fourthBlockMaskComplement = int(subnetMaskComplement.split('.')[3])

    if mode == 'network':
        return f'{firstBlockIP & firstBlockMask}.{secondBlockIP & secondBlockMask}.{thirdBlockIP & thirdBlockMask}.{fourthBlockIP & fourthBlockMask}'
    elif mode == 'firstHost':
        return f'{firstBlockIP & firstBlockMask}.{secondBlockIP & secondBlockMask}.{thirdBlockIP & thirdBlockMask}.{(fourthBlockIP & fourthBlockMask) + 1}'
    elif mode == 'lastHost':
        return f'{firstBlockIP | firstBlockMaskComplement}.{secondBlockIP | secondBlockMaskComplement}.{thirdBlockIP | thirdBlockMaskComplement}.{(fourthBlockIP | fourthBlockMaskComplement) - 1}'
    elif mode == 'broadcast':
        return f'{firstBlockIP | firstBlockMaskComplement}.{secondBlockIP | secondBlockMaskComplement}.{thirdBlockIP | thirdBlockMaskComplement}.{(fourthBlockIP | fourthBlockMaskComplement)}'
    elif mode == 'nextSubnet':
        broadcast = f'{firstBlockIP | firstBlockMaskComplement}.{secondBlockIP | secondBlockMaskComplement}.{thirdBlockIP | thirdBlockMaskComplement}.{(fourthBlockIP | fourthBlockMaskComplement)}'
        firstBlockBroadcast = int(broadcast.split('.')[0])
        secondBlockBroadcast = int(broadcast.split('.')[1])
        thirdBlockBroadcast = int(broadcast.split('.')[2])
        fourthBlockBroadcast = int(broadcast.split('.')[3])

        nextSubnet = ''
        if fourthBlockBroadcast + 1 > 255:
            fourthBlockBroadcast = 0
            if thirdBlockBroadcast + 1 > 255:
                thirdBlockBroadcast = 0
                if secondBlockBroadcast + 1 > 255:
                    secondBlockBroadcast = 0
                    if firstBlockBroadcast + 1 > 255:
                        nextSubnet = 'Nothing'
                        return nextSubnet
                    else:
                        firstBlockBroadcast += 1
                else:
                    secondBlockBroadcast += 1
            else:
                thirdBlockBroadcast += 1
        else:
            fourthBlockBroadcast += 1
        nextSubnet = f'{firstBlockBroadcast}.{secondBlockBroadcast}.{thirdBlockBroadcast}.{fourthBlockBroadcast}'
        return nextSubnet