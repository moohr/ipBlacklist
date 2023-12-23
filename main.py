import yaml
import re
import asyncio
import httpx

import upload

#ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:\d{1,5}\b'
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
iplist = []


async def get_ips(html):
    html = html.replace('\n', ' ')
    iplist.extend(re.findall(ip_pattern, html))
    return


async def fetch(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text


async def main():
    with open("config.yaml", "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    tasks = [fetch(url) for url in config["sources"]]
    results = await asyncio.gather(*tasks)
    for result in results:
        await get_ips(result)
    deduped = set(iplist)
    print("Total IPs:", len(deduped))
    with open("list.txt", "w") as file:
        file.write('\n'.join(deduped))
    if config["upload"]:
        upload.upload_list(deduped)


if __name__ == "__main__":
    asyncio.run(main())

