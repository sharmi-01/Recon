#!/usr/bin/env python3

import os
import sys

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white

import settings as config

home = config.home
usr_data = config.usr_data
conf_path = config.conf_path
path_to_script = config.path_to_script
src_conf_path = config.src_conf_path
meta_file_path = config.meta_file_path

import argparse

version = '1.1.5'
gh_version = ''
twitter_url = ''
discord_url = ''

parser = argparse.ArgumentParser(description=f'FinalRecon - The Last Web Recon Tool You Will Need | v{version}')
parser.add_argument('url', help='Target URL')
parser.add_argument('--headers', help='Header Information', action='store_true')
parser.add_argument('--sslinfo', help='SSL Certificate Information', action='store_true')
parser.add_argument('--whois', help='Whois Lookup', action='store_true')
parser.add_argument('--crawl', help='Crawl Target', action='store_true')
parser.add_argument('--dns', help='DNS Enumeration', action='store_true')
parser.add_argument('--sub', help='Sub-Domain Enumeration', action='store_true')
parser.add_argument('--dir', help='Directory Search', action='store_true')
parser.add_argument('--wayback', help='Wayback URLs', action='store_true')
parser.add_argument('--ps', help='Fast Port Scan', action='store_true')
parser.add_argument('--full', help='Full Recon', action='store_true')

ext_help = parser.add_argument_group('Extra Options')
ext_help.add_argument('-dt', type=int, help='Number of threads for directory enum [ Default : 30 ]')
ext_help.add_argument('-pt', type=int, help='Number of threads for port scan [ Default : 50 ]')
ext_help.add_argument('-T', type=float, help='Request Timeout [ Default : 30.0 ]')
ext_help.add_argument('-w', help='Path to Wordlist [ Default : wordlists/dirb_common.txt ]')
ext_help.add_argument('-r', action='store_true', help='Allow Redirect [ Default : False ]')
ext_help.add_argument('-s', action='store_false', help='Toggle SSL Verification [ Default : True ]')
ext_help.add_argument('-sp', type=int, help='Specify SSL Port [ Default : 443 ]')
ext_help.add_argument('-d', help='Custom DNS Servers [ Default : 1.1.1.1 ]')
ext_help.add_argument('-e', help='File Extensions [ Example : txt, xml, php ]')
ext_help.add_argument('-o', help='Export Format [ Default : txt ]')
ext_help.set_defaults(
	dt=config.dir_enum_th,
	pt=config.port_scan_th,
	T=config.timeout,
	w=config.dir_enum_wlist,
	r=config.dir_enum_redirect,
	s=config.dir_enum_sslv,
	sp=config.ssl_port,
	d=config.dir_enum_dns,
	e=config.dir_enum_ext,
	o=config.export_fmt
)

try:
	args = parser.parse_args()
except SystemExit:
	sys.exit()

target = args.url
headinfo = args.headers
sslinfo = args.sslinfo
whois = args.whois
crawl = args.crawl
dns = args.dns
dirrec = args.dir
wback = args.wayback
pscan = args.ps
full = args.full
threads = args.dt
pscan_threads = args.pt
tout = args.T
wdlist = args.w
redir = args.r
sslv = args.s
sslp = args.sp
dserv = args.d
filext = args.e
subd = args.sub
output = args.o

import socket
import datetime
import ipaddress
import tldextract
from json import loads

type_ip = False
data = {}




def full_recon():
	from modules.sslinfo import cert
	from modules.crawler import crawler
	from modules.headers import headers
	from modules.dns import dnsrec
	from modules.whois import whois_lookup
	from modules.dirrec import hammer
	from modules.portscan import ps
	from modules.subdom import subdomains
	from modules.wayback import timetravel
	headers(target, output, data)
	cert(hostname, sslp, output, data)
	whois_lookup(ip, output, data)
	dnsrec(domain, output, data)
	if type_ip is False:
		subdomains(domain, tout, output, data, conf_path)
	else:
		pass
	ps(ip, output, data, pscan_threads)
	crawler(target, output, data)
	hammer(target, threads, tout, wdlist, redir, sslv, dserv, output, data, filext)
	timetravel(target, data, output)


try:


	if target.startswith(('http', 'https')) is False:
		print(f'{R}[-] {C}Protocol Missing, Include {W}http:// {C}or{W} https:// \n')
		sys.exit(1)
	else:
		pass

	if target.endswith('/') is True:
		target = target[:-1]
	else:
		pass

	print(f'{G}[+] {C}Target : {W}{target}')
	ext = tldextract.extract(target)
	domain = ext.registered_domain
	hostname = '.'.join(part for part in ext if part)

	try:
		ipaddress.ip_address(hostname)
		type_ip = True
		ip = hostname
	except Exception:
		try:
			ip = socket.gethostbyname(hostname)
			print(f'\n{G}[+] {C}IP Address : {W}{str(ip)}')
		except Exception as e:
			print(f'\n{R}[-] {C}Unable to Get IP : {W}{str(e)}')
			sys.exit(1)

	start_time = datetime.datetime.now()

	if output != 'None':
		fpath = usr_data
		dt_now = str(datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S'))
		fname = f'{fpath}fr_{hostname}_{dt_now}.{output}'
		respath = f'{fpath}fr_{hostname}_{dt_now}'
		if not os.path.exists(respath):
			os.makedirs(respath)
		output = {
			'format': output,
			'directory': respath,
			'file': fname
		}

	if full is True:
		full_recon()

	if headinfo is True:
		from modules.headers import headers
		headers(target, output, data)

	if sslinfo is True:
		from modules.sslinfo import cert
		cert(hostname, sslp, output, data)

	if whois is True:
		from modules.whois import whois_lookup
		whois_lookup(ip, output, data)

	if crawl is True:
		from modules.crawler import crawler
		crawler(target, output, data)

	if dns is True:
		from modules.dns import dnsrec
		dnsrec(domain, output, data)

	if subd is True and type_ip is False:
		from modules.subdom import subdomains
		subdomains(domain, tout, output, data, conf_path)
	elif subd is True and type_ip is True:
		print(f'{R}[-] {C}Sub-Domain Enumeration is Not Supported for IP Addresses{W}\n')
		sys.exit(1)
	else:
		pass

	if wback is True:
		from modules.wayback import timetravel
		timetravel(hostname, data, output)

	if pscan is True:
		from modules.portscan import ps
		ps(ip, output, data, threads)

	if dirrec is True:
		from modules.dirrec import hammer
		hammer(target, threads, tout, wdlist, redir, sslv, dserv, output, data, filext)

	if any([full, headinfo, sslinfo, whois, crawl, dns, subd, wback, pscan, dirrec]) is not True:
		print(f'\n{R}[-] Error : {C}At least One Argument is Required with URL{W}')
		output = 'None'
		sys.exit(1)

	end_time = datetime.datetime.now() - start_time
	print(f'\n{G}[+] {C}Completed in {W}{str(end_time)}\n')
	print(f'{G}[+] {C}Exported : {W}{respath}')
	sys.exit()
except KeyboardInterrupt:
	print(f'{R}[-] {C}Keyboard Interrupt.{W}\n')
	sys.exit(130)
