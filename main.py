import requests
import os

CF_API_TOKEN = os.getenv("CF_API_TOKEN")
CF_ZONE_ID = os.getenv("CF_ZONE_ID")
CF_DNS_NAME = os.getenv("CF_DNS_NAME")

def get_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=10).text.strip()
    except:
        return None

def get_dns_record():
    url = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records?name={CF_DNS_NAME}&type=A"
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    res = requests.get(url, headers=headers).json()
    if res["success"] and res["result"]:
        return res["result"][0]["id"]
    return None

def update_dns(rid, ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records/{rid}"
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": CF_DNS_NAME,
        "content": ip,
        "ttl": 60,
        "proxied": False
    }
    return requests.put(url, json=data, headers=headers).json()

if __name__ == "__main__":
    ip = get_ip()
    if not ip:
        print("获取IP失败")
        exit(1)

    rid = get_dns_record()
    if not rid:
        print("未找到DNS记录")
        exit(1)

    res = update_dns(rid, ip)
    if res["success"]:
        print(f"DNS更新成功: {ip}")
    else:
        print(f"更新失败: {res}")
