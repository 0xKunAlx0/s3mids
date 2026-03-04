#!/usr/bin/env python3

import argparse
import subprocess
import requests
import random
import string
import os
import socket
import signal
from urllib.parse import urlparse

# ===============================
# COLORS
# ===============================

RED="\033[91m"
GREEN="\033[92m"
YELLOW="\033[93m"
BLUE="\033[94m"
CYAN="\033[96m"
BOLD="\033[1m"
RESET="\033[0m"

stop_scan=False

def signal_handler(sig,frame):
    global stop_scan
    print(f"\n{YELLOW}[!] Scan interrupted by user. Exiting...{RESET}")
    stop_scan=True

signal.signal(signal.SIGINT,signal_handler)

# ===============================
# BANNER
# ===============================

def banner():
    print(f"""{CYAN}{BOLD}
   _____ ____  __  __ _     _
  / ____|___ \\|  \\/  (_)   | |
 | (___   __) | \\  / |_  __| |___
  \\___ \\ |__ <| |\\/| | |/ _` / __|
  ____) |___) | |  | | | (_| \\__ \\
 |_____/|____/|_|  |_|_|\\__,_|___|

      S3 Misconfiguration Scanner - by KunAl
{RESET}""")

# ===============================
# UTILS
# ===============================

def random_string(length=6):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def normalize_bucket(value):

    if value.startswith("http"):
        parsed=urlparse(value)
        value=parsed.netloc

    if ".s3." in value:
        return value.split(".s3.")[0]

    return value

# ===============================
# BUCKET EXISTENCE
# ===============================

def bucket_exists(bucket):

    try:
        url=f"https://s3.amazonaws.com/{bucket}"
        r=requests.head(url,timeout=6,allow_redirects=True)

        if r.status_code==404:
            return False,None

        region=r.headers.get("x-amz-bucket-region")

        if region:
            return True,region

        if r.status_code in [200,403]:
            return True,"us-east-1"

        return False,None

    except:
        return False,None

# ===============================
# SCAN BUCKET
# ===============================

def scan_bucket(bucket_input,file_path,index,total):

    bucket=normalize_bucket(bucket_input)

    print(f"\n{BOLD}{CYAN}[{index}/{total}] Target: {bucket}{RESET}\n")

    exists,region=bucket_exists(bucket)

    if not exists:

        print(f"{RED}[-] Bucket does NOT exist{RESET}\n")

        if "cloudfront.net" in bucket_input:
            print(f"{GREEN}[OK] CloudFront endpoint — takeover not possible{RESET}")
            return

        print(f"{CYAN}[*] Checking takeover possibility for: {bucket_input}{RESET}")

        try:
            socket.gethostbyname(bucket_input)

            r=requests.get(f"http://{bucket_input}",timeout=6)
            server=r.headers.get("Server","")

            if "AmazonS3" in server:
                print(f"{RED}[CRITICAL] Possible S3 Bucket Takeover!{RESET}")
            else:
                print(f"{GREEN}[OK] Not pointing to S3{RESET}")

        except:
            print(f"{GREEN}[OK] Domain does not resolve{RESET}")

        return

    print(f"{GREEN}[+] Bucket exists{RESET}")
    print(f"{BLUE}[+] Region: {region}{RESET}\n")

    print(f"{CYAN}[*] Checking public listing...{RESET}")

    try:
        url=f"https://s3.{region}.amazonaws.com/{bucket}"
        r=requests.get(url,timeout=6)

        if "<ListBucketResult" in r.text:
            print(f"{RED}[CRITICAL] Bucket is publicly listable!{RESET}")
            listing=True
        else:
            print(f"{GREEN}[OK] No public listing access{RESET}")
            listing=False

    except:
        print(f"{GREEN}[OK] Listing not accessible{RESET}")
        listing=False

    print("")
    print(f"{CYAN}[*] Testing anonymous upload...{RESET}")

    filename=f"poc-{random_string()}.txt"

    upload_cmd=[
        "aws","s3","cp",
        file_path,
        f"s3://{bucket}/{filename}",
        "--no-sign-request",
        "--region",region
    ]

    try:
        upload=subprocess.run(upload_cmd,capture_output=True,timeout=8)

        if upload.returncode==0:

            print(f"{RED}[CRITICAL] Anonymous upload SUCCESS: {filename}{RESET}")

            public_url=f"http://{bucket}.s3.amazonaws.com/{filename}"
            print(f"{YELLOW}[+] Uploaded to: {public_url}{RESET}")

            r=requests.get(public_url,timeout=6)

            if r.status_code==200:
                print(f"{RED}[CRITICAL] Uploaded object is PUBLICLY READABLE{RESET}")

            print(f"{CYAN}[*] Testing anonymous delete...{RESET}")

            delete_cmd=[
                "aws","s3","rm",
                f"s3://{bucket}/{filename}",
                "--no-sign-request",
                "--region",region
            ]

            delete=subprocess.run(delete_cmd,capture_output=True,timeout=8)

            if delete.returncode==0:
                print(f"{RED}[CRITICAL] Anonymous delete SUCCESS{RESET}")
            else:
                print(f"{YELLOW}[!] Upload works but delete blocked{RESET}")

            write=True

        else:
            print(f"{GREEN}[OK] No anonymous write access{RESET}")
            write=False

    except:
        print(f"{GREEN}[OK] Upload test failed{RESET}")
        write=False

    print("")
    print(f"{BOLD}========== FINAL SUMMARY =========={RESET}")

    if write:
        print(f"{RED}[CRITICAL] Bucket is PUBLICLY WRITABLE!{RESET}")
    elif listing:
        print(f"{RED}[HIGH] Bucket is PUBLICLY LISTABLE!{RESET}")
    else:
        print(f"{GREEN}[OK] No critical anonymous misconfig detected{RESET}")

# ===============================
# MAIN
# ===============================

def main():

    banner()

    parser=argparse.ArgumentParser()

    parser.add_argument("-b","--bucket")
    parser.add_argument("-l","--list")
    parser.add_argument("-f","--file",default="poc.txt")

    args=parser.parse_args()

    if args.bucket:
        scan_bucket(args.bucket,args.file,1,1)

    elif args.list:

        if not os.path.exists(args.list):
            print("Bucket list not found")
            return

        with open(args.list) as f:
            buckets=[line.strip() for line in f if line.strip()]

        total=len(buckets)

        for i,bucket in enumerate(buckets,1):

            if stop_scan:
                break

            scan_bucket(bucket,args.file,i,total)

    else:
        print("Provide -b or -l")

if __name__=="__main__":
    main()
