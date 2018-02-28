__author__ = "Thea Llanes/Oboark"
import sys
import socket
import struct



def split_ip(n):
    #Splits the parts of an IP Address
    ip, prelen = n.split("/")
    split_ip = ip.split(".")
    return split_ip, prelen 


def get_submask(prelen):
    #Gets the submask from the prefix-length
    host_bits = 32 - int(prelen)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return netmask


def get_wildcard(submask):
    #Gets wildcard address by inverting the submask
    wildcard = []
    for i in submask:
        wildcard.append(~i & 0xFF)
    return wildcard


def get_network_address(ip, sub):
    #Calculates the network address
    address = []
    #ANDING the IP address and the submask
    for a, b in zip(ip, sub):
        address.append(a & b)
    return address


def get_broadcast_address(ip, sub):
    #Calculates the broadcast address
    broadcast = []
    for a, b in zip(ip, sub):
        broadcast.append(a | b)
    return broadcast


def get_host_range(net, broad):
    #Calculates the host range
    host_min = net[:]
    host_min[-1] += 1
    
    host_max = broad[:]
    host_max[-1] -= 1
    
    return host_min, host_max


def get_max_hosts(min, max):
    #Get max number of hosts
    min_to_dec = 0
    max_to_dec = 0

    #Convert min and max to decimal
    for c, i in enumerate(reversed(min)):
        min_to_dec += i*256**c

    for c, i in enumerate(reversed(max)):
        max_to_dec += i*256**c

    return (max_to_dec + 1) - min_to_dec



if __name__ == '__main__':
    ip = sys.argv[1] if len(sys.argv) > 1 else sys.exit(0)
    
    #Split main address into 4 parts, including the prefix-length
    ip, prelen = split_ip(ip)

    #Get proper IP address and submask for calculation
    ip = list(map(int, ip)) #We convert the ip into a list of ints, it was actually a string before
    submask = list(map(int,get_submask(prelen).split("."))) #Get submask from prefix length
    wildcard = get_wildcard(submask)

    #Get addresses
    network_address = get_network_address(ip, submask)
    broadcast_address = get_broadcast_address(ip, wildcard)
    host_min, host_max = get_host_range(network_address, broadcast_address)
    max_hosts = get_max_hosts(host_min, host_max)
    

    print("Network Address: ", ".".join(map(str, network_address)))
    print("Broadcast Address: ", ".".join(map(str, broadcast_address)))
    print("Host range: ", ".".join(map(str, host_min)), " - ", ".".join(map(str, host_max)))
    print("Max number of hosts: ", max_hosts)
    print("Submask: ", ".".join(map(str, submask)))
    print("Wildcard: ", ".".join(map(str, wildcard)))
