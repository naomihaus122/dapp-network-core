"""
Fork Finder — анализирует блоки Bitcoin, чтобы определить появление форков (временных разветвлений цепи).
"""

import requests
import time

def get_block_hash(height):
    url = f"https://blockstream.info/api/block-height/{height}"
    r = requests.get(url)
    r.raise_for_status()
    return r.text

def get_block_info(block_hash):
    url = f"https://blockstream.info/api/block/{block_hash}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def check_fork(height):
    main_hash = get_block_hash(height)
    main_info = get_block_info(main_hash)

    previous_hash = main_info["previousblockhash"]
    url = f"https://blockstream.info/api/block/{previous_hash}/children"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Ошибка получения дочерних блоков")

    children = r.json()
    if len(children) > 1:
        print(f"⚠️ Обнаружено {len(children)} дочерних блоков на высоте {height-1} — возможно, форк!")
        for blk in children:
            ts = blk.get("timestamp", "")
            print(f" - {blk['id']} @ {ts}")
    else:
        print(f"✅ Высота {height}: форк не обнаружен.")

def main():
    print("🌲 Fork Finder запущен. Проверка последних 10 блоков...")
    tip = int(requests.get("https://blockstream.info/api/blocks/tip/height").text)

    for h in range(tip - 10, tip + 1):
        try:
            check_fork(h)
        except Exception as e:
            print(f"Ошибка на высоте {h}: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()
