import requests
import discord, re
import json

webhookurl = 'webhookhere'

url_pattern = r'https?://(?:www\.)?\S+'
catalog_id_pattern = r'/catalog/(\d+)'

itemreleasechannelid = 1307760060981579809

pekoraCOOKIE = 'cookiehere'

client = discord.Client()

def purchase(id, price):
    purchaseurl = f'https://www.pekora.zip/apisite/economy/v1/purchases/products/{str(id)}'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': f'.ROBLOSECURITY={pekoraCOOKIE}; rbxcsrf4=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJjc3JmIjoiWlNQQTZ6NlpSaWc9IiwiY3JlYXRlZEF0IjoiMjAyNS0wMi0xMFQyMTo1NToyNy42NDU2MjIxWiJ9.69jgT72PsA-hfFvKbFDJn0MUXcP1-sgmkdonarSBWv5qyzff0nqvO1k44-MxaKYdGiYb83_whM8zT_p8ELTWoA',
        'dnt': '1',
        'origin': 'https://www.pekora.zip',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'x-csrf-token': 'ZSPA6z6ZRig='
    }
    data = {
        "assetId": id,
        "expectedPrice": price,
        "expectedSellerId": 1,
        "userAssetId": None,
        "expectedCurrency": 1
    }
    response = requests.post(purchaseurl, headers=headers, json=data)
    print(response.json())
    return response.status_code

def getinfo(id):
    url = f'https://www.pekora.zip/marketplace/productinfo?assetId={str(id)}'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': f'.ROBLOSECURITY={pekoraCOOKIE}',
        'dnt': '1',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()

@client.event
async def on_ready():
    print(f'using {client.user}')

@client.event
async def on_message(message):
    if message.channel.id == itemreleasechannelid:
        links = re.findall(url_pattern, message.content)
        filtered_links = [link for link in links if 'catalog' in link]
        
        if filtered_links:
            for link in filtered_links:
                match = re.search(catalog_id_pattern, link)
                if match:
                    catalog_id = match.group(1)
                    print(f'catalog id found {catalog_id}')
                    info = getinfo(catalog_id)
                    price = info.get('PriceInRobux')
                    statuscodepurchase = purchase(catalog_id, price)
                    if statuscodepurchase == 200:
                        data = {
                            "content": f"@everyone sniped dat hoe {link} {price} robux"
                        }
                        requests.post(webhookurl, data=json.dumps(data), headers={"Content-Type": "application/json"})
                    elif statuscodepurchase == 403:
                        data = {
                            "content": f"@everyone lol ts unauthorized"
                        }
                        requests.post(webhookurl, data=json.dumps(data), headers={"Content-Type": "application/json"})
                    else:
                        data = {
                            "content": f"@everyone idk WTF happened g!"
                        }
                        requests.post(webhookurl, data=json.dumps(data), headers={"Content-Type": "application/json"})
                else:
                    print('nigga my regex failed on id')
        else:
            print('nigga yappin in da channel')

client.run('tokenhere')
