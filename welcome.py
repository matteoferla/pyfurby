"""Boot greeting; wait at most two minutes for an IPv4 connection."""
import argparse
import ipaddress
import subprocess
import time

from pyfurby import Furby


def ipv4_addresses():
    result = subprocess.run(["hostname", "-I"], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True, check=False)
    addresses = []
    for value in result.stdout.split():
        try:
            address = ipaddress.ip_address(value)
        except ValueError:
            continue
        if address.version == 4 and not address.is_loopback and not address.is_link_local:
            addresses.append(str(address))
    return addresses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--move', action='store_true', help='Enable greeting motor movement after wiring checks')
    args = parser.parse_args()
    furby = Furby()
    try:
        furby.say("Hello World", move=args.move)
        if args.move:
            furby.flutter()
        deadline = time.monotonic() + 120
        while not ipv4_addresses():
            if time.monotonic() >= deadline:
                furby.say("Network connection unavailable", move=False)
                print("No IPv4 connection after 120 seconds", flush=True)
                return
            furby.say("Awaiting network connection", move=False)
            time.sleep(5)
        for address in ipv4_addresses():
            furby.say("My local IP address is " + address.replace('.', ' dot '), move=args.move)
    finally:
        furby.halt()


if __name__ == "__main__":
    main()
