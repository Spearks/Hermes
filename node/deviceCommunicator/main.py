# Parse devices Data.
from scapy.all import ARP, Ether, srp

def scan(ip):
    # Create an ARP request packet
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # Send the packet and receive a response
    result = srp(packet, timeout=3, verbose=0)[0]

    # Return a list of discovered devices
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

def check_new_device(ip, known_devices):
    devices = scan(ip)

    for device in devices:
        if device not in known_devices:
            print(f"New device connected: IP {device['ip']} with MAC {device['mac']}")

known_devices = []
network_ip = "192.168.1.1/24"  # Change this to match your network

while True:
    check_new_device(network_ip, known_devices)

