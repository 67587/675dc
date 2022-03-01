#右邊切換到shell 輸入 python checkBAN.py 查看被BAN多久
import requests

r = requests.head(url="https://discord.com/api/v1")
try:
    print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
    print("No rate limit")