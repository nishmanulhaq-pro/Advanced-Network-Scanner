import socket
import csv
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

open_ports = []

def banner():
    print(Fore.CYAN + """
================================================
         ADVANCED NETWORK SCANNER
================================================
    Multi-threaded Port Scanner
    Service Detection | CSV | JSON
================================================
""")

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))

        if result == 0:

            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            print(Fore.GREEN + f"[OPEN] Port {port} ({service})")

            open_ports.append({
                "port": port,
                "service": service
            })

        sock.close()

    except:
        pass

# Main Program
banner()

target = input("Enter Target IP: ")
start_port = int(input("Enter Start Port: "))
end_port = int(input("Enter End Port: "))

start_time = datetime.now()

print(Fore.YELLOW + f"\nScanning {target}...\n")

with ThreadPoolExecutor(max_workers=100) as executor:
    for port in range(start_port, end_port + 1):
        executor.submit(scan_port, target, port)

end_time = datetime.now()

# CSV Export
with open("scan_report.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Port", "Service"])

    for item in open_ports:
        writer.writerow([item["port"], item["service"]])

# JSON Export
with open("scan_report.json", "w") as file:
    json.dump(open_ports, file, indent=4)

# Scan Summary
print(Fore.CYAN + "\n===================================")
print("           SCAN SUMMARY")
print("===================================")

print(f"Target: {target}")
print(f"Scan Started : {start_time}")
print(f"Scan Finished: {end_time}")
print(f"Open Ports Found: {len(open_ports)}")

print("\nCSV Report Saved : scan_report.csv")
print("JSON Report Saved: scan_report.json")

print(Fore.GREEN + "\nScan Completed.")

# Keep Window Open
input("\nPress Enter to Exit...")