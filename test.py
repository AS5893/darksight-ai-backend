import requests

url = "http://localhost:8001/analyze-pcap"
file_path = r"C:\Users\aarthshah\Documents\ctf\hack\Noobs Keylogger.pcap"

data = {
    "context": "Initial Dark Web threat correlation test - Noobs Keylogger"
}

files = {
    "file": ("Noobs Keylogger.pcap", open(file_path, "rb"), "application/vnd.tcpdump.pcap")
}

print(f"Sending PCAP to DarkSight Node at {url}...")

try:
    response = requests.post(url, data=data, files=files)
    print(f"Status Code: {response.status_code}")
    print("Analysis Result:")
    print(response.json())
except Exception as e:
    print(f"Connection failed: {e}")


# to test, first run the server and run this additional file in another cmd