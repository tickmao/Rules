#!/usr/bin/env python3
import urllib.request
import os

MODULES = {
    "SubStore.sgmodule": "https://raw.githubusercontent.com/sub-store-org/Sub-Store/master/config/Surge.sgmodule",
    "BoxJs.sgmodule": "https://raw.githubusercontent.com/chavyleung/scripts/master/box/rewrite/boxjs.rewrite.surge.sgmodule",
    "YouTube.sgmodule": "https://raw.githubusercontent.com/Maasea/sgmodule/master/Youtube.sgmodule",
    "Weibo.sgmodule": "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/Surge/Weibo.sgmodule",
    "TestFlight.sgmodule": "https://raw.githubusercontent.com/NobyDa/Script/master/Surge/Module/TFDownload.sgmodule",
    "Bilibili.sgmodule": "https://raw.githubusercontent.com/BiliUniverse/Global/main/Surge/Bilibili.sgmodule",
    "Bilibili_Intl.sgmodule": "https://raw.githubusercontent.com/BiliUniverse/Global/main/Surge/Bilibili_Intl.sgmodule",
    "Advertising.sgmodule": "https://raw.githubusercontent.com/app2smile/rules/master/module/advertising.sgmodule",
    "Spotify.sgmodule": "https://raw.githubusercontent.com/app2smile/rules/master/module/spotify.sgmodule"
}

DIR = "Surge/Module"
os.makedirs(DIR, exist_ok=True)

for name, url in MODULES.items():
    path = os.path.join(DIR, name)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                with open(path, 'wb') as f:
                    f.write(response.read())
                print(f"✅ Downloaded {name}")
            else:
                print(f"❌ Failed to download {name} (Status: {response.status})")
    except Exception as e:
        print(f"❌ Error downloading {name}: {e}")
