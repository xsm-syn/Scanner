import requests
import re
from concurrent.futures import ThreadPoolExecutor

# Fungsi untuk cek IP dan simpan hasil
def check_ip(line):
    ip, port = line.split(",")
    url = f"https://xsmnet.buzz/check?ip={ip}:{port}"
    
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
        
        if data.get("proxyip") is True:
            country_code = data.get("countryCode", "Unknown")
            org = data.get("org", "Unknown")
            delay = data.get("delay", "0ms")
            
            org_cleaned = re.sub(r"[^\w\s]", "", org)

            print(f"✅ Saved: {ip}:{port} -> {country_code}, {org_cleaned}, {delay}")
            
            with open("proxyList.txt", "a") as success_file:
                success_file.write(f"{ip},{port},{country_code},{org_cleaned},{delay}\n")
        else:
            print(f"❌ Tidak memenuhi kondisi proxyip true: {ip}:{port}")
            with open("deadIp.txt", "a") as failed_file:
                failed_file.write(f"{ip},{port}\n")
                
    except Exception as e:
        print(f"❌ Gagal: {ip}:{port} -> {e}")
        with open("deadIp.txt", "a") as failed_file:
            failed_file.write(f"{ip},{port}\n")

# Baca IP dari raw.txt
with open("raw.txt", "r") as f:
    lines = [line.strip() for line in f.readlines()]

open("proxyList.txt", "w").close()
open("deadIp.txt", "w").close()

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(check_ip, lines)

print("\n✅ Proses selesai! Hasil sukses di 'out.txt', gagal di 'dead.txt'.")
