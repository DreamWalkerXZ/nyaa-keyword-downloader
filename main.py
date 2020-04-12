import requests
import json
import aria2p
from bs4 import BeautifulSoup

global aria2
global current_url


def routine():
    global aria2
    global current_url

    resp = requests.get(current_url, headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})
    if resp.status_code == 200:
        soup = BeautifulSoup(markup=resp.text, features="html.parser")
        magnet_links = [element["href"] for element in soup.select(
            "body > div > div.table-responsive > table > tbody > tr.success > td:nth-child(3) > a:nth-child(2)")]
        for magnet_link in magnet_links:
            download = aria2.add_magnet(magnet_link)
            print(download.name)
        if '<li class="next">' in resp.text:
            current_url = "https://sukebei.nyaa.si" + \
                soup.select("body > div > div.center > ul > li.next > a")[0]["href"]
            routine()

    else:
        print("%s[status_code] = %d" % (current_url, resp.status_code))


def main():
    global aria2
    global current_url

    host = input("rpc host[http(s)://example.com]: ")
    port = input("rpc port: ")
    secret = input("rpc secret: ")
    aria2 = aria2p.API(
        aria2p.Client(
            host=host,
            port=port,
            secret=secret
        )
    )
    current_url = "https://sukebei.nyaa.si/?q=" + input("keyword: ")
    routine()


if __name__ == "__main__":
    main()
