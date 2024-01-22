import os
domain=input("Give the Domain:")
url = f"https://{domain}"
#runs final recon
os.system(f"python3 recon1.py --headers --sslinfo --whois --crawl --dns --sub --wayback --ps -r -s {url}")
#runs Sws-recon
os.system(f"python3 recon2.py -d {domain} -o -s -jl -t -w -r --email")
