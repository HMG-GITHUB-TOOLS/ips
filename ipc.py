import subprocess
import ipaddress
import multiprocessing
import socket

def ping_ip(ip):
    try:
        # Use subprocess to ping
        output = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], stdout=subprocess.DEVNULL)
        if output.returncode == 0:
            return f"{ip} is up"
        else:
            return None
    except Exception as e:
        return None

def scan_network(network):
    try:
        ip_net = ipaddress.ip_network(network)
        ips = list(ip_net.hosts())

        # Using multiprocessing for faster execution
        with multiprocessing.Pool(processes=multiprocessing.cpu_count() * 2) as pool:
            results = pool.map(ping_ip, ips)

        # Filter out None responses
        active_ips = [res for res in results if res]
        for ip in active_ips:
            print(ip)
    except ValueError:
        print("Invalid network range!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage:
    network_range = input("Enter the network range (e.g., 192.168.1.0/24): ")
    scan_network(network_range)
