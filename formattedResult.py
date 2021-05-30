import IPv4 as ip

def getIPv4Properties(address):
    properties = f'-- IPv4 Address Properties --\nCurrent IPv4 Address: {address}\n\n'
    properties += f'\tClass:\t\t\t\t{ip.getClass(address)}\n'
    properties += f'\tScope:\t\t\t\t{ip.getScope(address)}\n'
    properties += f'\tSubnetmask:\t\t\t{ip.getSubnetmask(address)}\n'
    properties += f'\tNetwork:\t\t\t{ip.getNetworkInfo(address)}\n'
    properties += f'\tFirst Host:\t\t\t{ip.getNetworkInfo(address, "firstHost")}\n'
    properties += f'\tLast Host:\t\t\t{ip.getNetworkInfo(address, "lastHost")}\n'
    properties += f'\tBroadcast:\t\t\t{ip.getNetworkInfo(address, "broadcast")}\n'
    properties += f'\tNext Subnet:\t\t{ip.getNetworkInfo(address, "nextSubnet")}\n\n'
    properties += f'\tIP in binary:\t\t{ip.getBinaryIP(address)}\n'
    properties += f'\tSubnet in binary:\t{ip.getSubnetmask(address, "binary")}\n'
    return properties

def getIPv4Subnets(address, networks):
    properties = f'-- IPv4 Subnets --\nCurrent IPv4 Address: {address}\nDesired Networks: {networks}\n\n'
    properties += f'\tActual Networks to create:\t{ip.getActualNetworks(networks)}\n'
    properties += f'\tSubnet bits to borrow:\t{ip.getSubnetsBitsToBorrow(networks)}\n'
    return properties

