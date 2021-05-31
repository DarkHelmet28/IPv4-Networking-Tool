import IPv4 as ip
from utility import textYellow, textYellowBold

def getIPv4Properties(address):
    properties = f'-- {textYellowBold("IPv4 Address Properties")} --\nCurrent IPv4 Address: {address}\n\n'
    properties += f'\t{textYellow("Class")}:\t\t\t\t{ip.getClass(address)}\n'
    properties += f'\t{textYellow("Scope")}:\t\t\t\t{ip.getScope(address)}\n'
    properties += f'\t{textYellow("Subnetmask")}:\t\t\t{ip.getSubnetmask(address)}\n'
    properties += f'\t{textYellow("Network")}:\t\t\t{ip.getNetworkInfo(address)}\n'
    properties += f'\t{textYellow("First Host")}:\t\t\t{ip.getNetworkInfo(address, "firstHost")}\n'
    properties += f'\t{textYellow("Last Host")}:\t\t\t{ip.getNetworkInfo(address, "lastHost")}\n'
    properties += f'\t{textYellow("Broadcast")}:\t\t\t{ip.getNetworkInfo(address, "broadcast")}\n'
    properties += f'\t{textYellow("Next Subnet")}:\t\t{ip.getNetworkInfo(address, "nextSubnet")}\n\n'
    properties += f'\t{textYellow("IP in binary")}:\t\t{ip.getBinaryIP(address)}\n'
    properties += f'\t{textYellow("Subnet in binary")}:\t{ip.getSubnetmask(address, "binary")}\n'
    return properties

def getIPv4Subnets(address, networks):
    subnetBits = ip.getSubnetsBitsToBorrow(networks)
    newCidr = str(int(address.split("/")[1]) + subnetBits)

    properties = f'-- {textYellowBold("IPv4 Subnets")} --\nCurrent IPv4 Address:\t{address}\nDesired Networks:\t\t{networks}\n\n'
    properties += f'\t{textYellow("Actual Networks to create")}:\t{ip.getActualNetworks(networks)}\n'
    properties += f'\t{textYellow("Subnet bits to borrow")}:\t\t{subnetBits}\n'
    properties += f'\t{textYellow("Old Subnetmask")}:\t\t\t\t{ip.getSubnetmask(address)}\n'
    properties += f'\t{textYellow("New Subnetmask")}:\t\t\t\t{ip.getSubnetmask(address, subnetBits = subnetBits)}\n'
    properties += f'\t{textYellow("New CIDR")}:\t\t\t\t\t/{newCidr}\n'
    properties += f'\t{textYellow("# Host per Subnet")}:\t\t\t{ip.getNumberHostNetwork(address, subnetBits)}\n\n'

    # Analyze every Single Subnets
    newAddr = f'{address.split("/")[0]}/{newCidr}' 
    prevAddr = newAddr
    subAddr = prevAddr
    for i in range(0, int(ip.getActualNetworks(networks))):
        properties += f'\t{textYellow("SUBNET")} #{i+1}\n'
        properties += f'\t\tNetwork:\t{ip.getNetworkInfo(subAddr)}\n'
        properties += f'\t\tFirst Host:\t{ip.getNetworkInfo(subAddr, "firstHost")}\n'
        properties += f'\t\tLast Host:\t{ip.getNetworkInfo(subAddr, "lastHost")}\n'
        properties += f'\t\tBroadcast:\t{ip.getNetworkInfo(subAddr, "broadcast")}\n'
        prevAddr = subAddr
        subAddr = f'{ip.getNetworkInfo(prevAddr, "nextSubnet")}/{newCidr}'
    return properties

