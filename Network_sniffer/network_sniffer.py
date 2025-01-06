import scapy.all as scapy
from scapy.layers import http
import argparse
from collections import Counter
import time
import os

# Define a function to sniff packets on a specified interface
def sniff_packets(interface):
    print(f"Sniffing started on interface: {interface}")
    scapy.sniff(iface=interface, store=False, prn=process_packet)

# Define a function to process and analyze packets
packet_count = Counter()

def process_packet(packet):
    global packet_count
    # Count packet by protocol
    if packet.haslayer(scapy.IP):
        ip_layer = packet[scapy.IP]
        protocol = ip_layer.proto
        packet_count[protocol] += 1

        # Display HTTP requests if present
        if packet.haslayer(http.HTTPRequest):
            print(f"[HTTP] {ip_layer.src} --> {ip_layer.dst}")
            print(f"Host: {packet[http.HTTPRequest].Host.decode()}")

        # Print general packet info
        print(f"Protocol: {protocol}, Src: {ip_layer.src}, Dst: {ip_layer.dst}")

# Define a function to save packets in PCAP format
def save_packets(interface, duration):
    file_name = f"captured_packets_{int(time.time())}.pcap"
    print(f"Capturing packets on {interface} for {duration} seconds...")
    packets = scapy.sniff(iface=interface, timeout=duration)
    scapy.wrpcap(file_name, packets)
    print(f"Packets saved to {file_name}")

# Display statistics
def display_statistics():
    print("\nPacket Statistics:")
    for proto, count in packet_count.items():
        print(f"Protocol {proto}: {count} packets")

# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Network Sniffer")
    parser.add_argument("-i", "--interface", help="Network interface to sniff on", required=True)
    parser.add_argument("-d", "--duration", help="Duration to capture packets in seconds", type=int, default=60)
    args = parser.parse_args()

    try:
        # Capture packets and analyze
        sniff_packets(args.interface)
        save_packets(args.interface, args.duration)
        display_statistics()
    except KeyboardInterrupt:
        print("\nSniffing stopped. Saving data...")
        display_statistics()
