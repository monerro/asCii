import requests
import os
from base64 import b64encode


logo = r"""

██      ▄▄▄▄▄   ▄█▄    ▄█ ▄█ 
█ █    █     ▀▄ █▀ ▀▄  ██ ██ 
█▄▄█ ▄  ▀▀▀▀▄   █   ▀  ██ ██ 
█  █  ▀▄▄▄▄▀    █▄  ▄▀ ▐█ ▐█ 
   █            ▀███▀   ▐  ▐ 
  █                          
 ▀   discord webhook manager by @compilings
"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def test_webhook(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print(f"[✓] Webhook is valid: {url}")
            return True
        elif r.status_code == 404:
            print(f"[!] Webhook not found: {url}")
        else:
            print(f"[!] Unknown status: {r.status_code}")
    except Exception as e:
        print(f"[!] Error testing webhook: {e}")
    return False

def delete_webhook(url):
    try:
        r = requests.delete(url)
        if r.status_code == 204:
            print(f"[✓] Deleted: {url}")
        else:
            print(f"[!] Failed to delete ({r.status_code})")
    except Exception as e:
        print(f"[!] Error deleting: {e}")

def change_name(url):
    new_name = input("[>] New webhook name: ").strip()
    json = {"name": new_name}
    try:
        r = requests.patch(url, json=json)
        if r.status_code == 200:
            print(f"[✓] Webhook name changed to {new_name}")
        else:
            print(f"[!] Failed to change name ({r.status_code})")
    except Exception as e:
        print(f"[!] Error: {e}")

def change_avatar(url):
    path = input("[>] Enter path to image (jpg/png): ").strip()
    if not os.path.exists(path):
        print("[!] File not found.")
        return

    try:
        with open(path, "rb") as f:
            img_data = f.read()
        b64_img = b64encode(img_data).decode()
        ext = "png" if path.endswith(".png") else "jpeg"
        avatar_data = f"data:image/{ext};base64,{b64_img}"
        json = {"avatar": avatar_data}

        r = requests.patch(url, json=json)
        if r.status_code == 200:
            print("[✓] Avatar changed successfully.")
        else:
            print(f"[!] Failed to change avatar ({r.status_code})")
    except Exception as e:
        print(f"[!] Error: {e}")

def send_message(url):
    content = input("[>] Enter message content: ").strip()
    username = input("[>] (Optional) Override username (leave blank for default): ").strip()
    json = {"content": content}
    if username:
        json["username"] = username

    try:
        r = requests.post(url, json=json)
        if r.status_code == 204 or r.status_code == 200:
            print("[✓] Message sent.")
        else:
            print(f"[!] Failed to send message ({r.status_code})")
    except Exception as e:
        print(f"[!] Error: {e}")


def menu():
    while True:
        clear()
        print(logo)
        print("""
[1] Test webhook
[2] Delete webhook
[3] Change webhook name
[4] Change webhook avatar
[5] Send message as webhook
[6] Exit
""")
        choice = input("[>] Select an option: ").strip()
        if choice not in {'1','2','3','4','5','6'}:
            print("[!] Invalid option.")
            input("[Enter] to return...")
            continue

        if choice == '6':
            break

        url = input("[>] Enter webhook URL: ").strip()

        if choice == '1':
            test_webhook(url)
        elif choice == '2':
            delete_webhook(url)
        elif choice == '3':
            change_name(url)
        elif choice == '4':
            change_avatar(url)
        elif choice == '5':
            send_message(url)

        input("\n[Enter] to return to menu...")


if __name__ == "__main__":
    menu()
