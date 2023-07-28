#!/usr/bin/env python

import subprocess
import optparse
import re


def get_options():

    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()

    if (not options.interface):
        parser.error("\n[-] Please specify an interface, use --help for more info")

    if (not options.new_mac):
        parser.error("\n[-] Please specify a MAC address, use --help for more info")

    return options

def change_mac(interface, new_mac):
    print("\n[+] Changing MAC address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface,  "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def check_output(interface):
    ifconfig_result = str(subprocess.check_output(["ifconfig", interface]))
    output = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if output:
        return output.group(0)

    print("[-] Could not read MAC address.")

if __name__ == "__main__":

    options = get_options()
    current_mac = check_output(options.interface)
    print(f"\nCurrent MAC: {current_mac}")
    change_mac(options.interface, options.new_mac)
    current_mac = check_output(options.interface)
    if (current_mac==options.new_mac):
        print("\n-----------------------------------------\n[+] Successfully changed the MAC address to " + current_mac)
    else:
        print("\n-----------------------------------------\n[-] Failed to change the MAC address")

