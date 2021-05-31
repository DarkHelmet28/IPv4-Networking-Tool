import IPv4 as ip
from termcolor import colored

def getIPv4Properties(address):
    properties = f'-- {colored("IPv4 Address Properties", "yellow", attrs=["bold"])} --\nCurrent IPv4 Address: {address}\n\n'
    properties += f'\t{colored("Class", "yellow")}:\t\t\t\t{ip.getClass(address)}\n'
    properties += f'\t{colored("Scope", "yellow")}:\t\t\t\t{ip.getScope(address)}\n'
    properties += f'\t{colored("Subnetmask", "yellow")}:\t\t\t{ip.getSubnetmask(address)}\n'
    properties += f'\t{colored("Network", "yellow", attrs=["bold"])}:\t\t\t{ip.getNetworkInfo(address)}\n'
    properties += f'\t{colored("First Host", "yellow")}:\t\t\t{ip.getNetworkInfo(address, "firstHost")}\n'
    properties += f'\t{colored("Last Host", "yellow")}:\t\t\t{ip.getNetworkInfo(address, "lastHost")}\n'
    properties += f'\t{colored("Broadcast", "yellow")}:\t\t\t{ip.getNetworkInfo(address, "broadcast")}\n'
    properties += f'\t{colored("Next Subnet", "yellow")}:\t\t{ip.getNetworkInfo(address, "nextSubnet")}\n\n'
    properties += f'\t{colored("IP in binary", "yellow")}:\t\t{ip.getBinaryIP(address)}\n'
    properties += f'\t{colored("Subnet in binary", "yellow")}:\t{ip.getSubnetmask(address, "binary")}\n'
    return properties

def getIPv4Subnets(address, networks):
    subnetBits = ip.getSubnetsBitsToBorrow(networks)
    newCidr = str(int(address.split("/")[1]) + subnetBits)

    properties = f'-- {colored("IPv4 Subnets", "yellow", attrs=["bold"])} --\nCurrent IPv4 Address:\t{address}\nDesired Networks:\t\t{networks}\n\n'
    properties += f'\t{colored("Actual Networks to create", "yellow")}:\t{ip.getActualNetworks(networks)}\n'
    properties += f'\t{colored("Subnet bits to borrow", "yellow")}:\t\t{subnetBits}\n'
    properties += f'\t{colored("Old Subnetmask", "yellow")}:\t\t\t\t{ip.getSubnetmask(address)}\n'
    properties += f'\t{colored("New Subnetmask", "yellow")}:\t\t\t\t{ip.getSubnetmask(address, subnetBits = subnetBits)}\n'
    properties += f'\t{colored("New CIDR", "yellow")}:\t\t\t\t\t/{newCidr}\n'
    properties += f'\t{colored("# Host per Subnet", "yellow")}:\t\t\t{ip.getNumberHostNetwork(address, subnetBits)}\n\n'

    # Analyze every Single Subnets
    newAddr = f'{address.split("/")[0]}/{newCidr}' 
    prevAddr = newAddr
    subAddr = prevAddr
    for i in range(0, int(ip.getActualNetworks(networks))):
        properties += f'\t{colored("SUBNET", "yellow")} #{i+1}\n'
        properties += f'\t\tNetwork:\t{ip.getNetworkInfo(subAddr)}\n'
        properties += f'\t\tFirst Host:\t{ip.getNetworkInfo(subAddr, "firstHost")}\n'
        properties += f'\t\tLast Host:\t{ip.getNetworkInfo(subAddr, "lastHost")}\n'
        properties += f'\t\tBroadcast:\t{ip.getNetworkInfo(subAddr, "broadcast")}\n'
        prevAddr = subAddr
        subAddr = f'{ip.getNetworkInfo(prevAddr, "nextSubnet")}/{newCidr}'
    return properties

