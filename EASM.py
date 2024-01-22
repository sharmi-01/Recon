import os
domain=input("Give the Domain:")
url = f"https://{domain}"
#runs recon1.py
os.system(f"python3 recon1.py --headers --sslinfo --whois --crawl --dns --sub --wayback --ps -r -s {url}")
#runs recon2.py
os.system(f"python3 recon2.py -d {domain} -o -s -jl -t -w -r --email")
