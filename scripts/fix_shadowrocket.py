import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SR_PATH = ROOT / "Shadowrocket" / "Shadowrocket.conf"

with SR_PATH.open("r", encoding="utf-8") as f:
    text = f.read()

# Replace Group Configs
replacements = {
    "手动切换 = select,PROXY": "Proxy = select,PROXY",
    "国外网站 = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Outside = select,Proxy,United States,Japan,Hong Kong,Europe",
    "国内网站 = select,DIRECT,手动切换,美国节点,日本节点,香港节点,台湾节点": "Mainland = select,DIRECT,Proxy,United States,Japan,Hong Kong,Europe",
    "YouTube = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Google = select,Proxy,United States,Japan,Hong Kong,Europe",
    "NETFLIX = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Gmedia = select,Proxy,United States,Japan,Hong Kong,Europe",
    "Disney+ = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Microsoft = select,Proxy,United States,Japan,Hong Kong,Europe",
    "Twitter = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Social = select,Proxy,United States,Japan,Hong Kong,Europe",
    "Telegram = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Telegram = select,Proxy,United States,Japan,Hong Kong,Europe",
    "PayPal = select,DIRECT,手动切换,美国节点,日本节点,香港节点,台湾节点": "PayPal = select,Proxy,United States,Japan,Hong Kong,Europe",
    "网易音乐 = select,DIRECT": "AI = select,Proxy,United States,Japan,Hong Kong,Europe",
    "苹果服务 = select,DIRECT,手动切换,美国节点,日本节点,香港节点,台湾节点": "Apple = select,DIRECT,Proxy,United States,Japan,Hong Kong,Europe",
    "微软服务 = select,DIRECT,手动切换,美国节点,日本节点,香港节点,台湾节点": "Game = select,Proxy,United States,Japan,Hong Kong,Europe",
    "哔哩哔哩 = select,DIRECT,手动切换,美国节点,日本节点,香港节点,台湾节点": "Emby = select,Proxy,United States,Japan,Hong Kong,Europe",
    "游戏平台 = select,手动切换,美国节点,日本节点,香港节点,台湾节点,DIRECT": "Spotify = select,Proxy,United States,Japan,Hong Kong,Europe",
    "AdBlock = select,REJECT": "AdBlock = select,REJECT",
    "漏网之鱼 = select,手动切换,美国节点,日本节点,香港节点,台湾节点,DIRECT": "NoAuto = select,Proxy,United States,Japan,Hong Kong,Europe,DIRECT",
    "美国节点 = select,policy-regex-filter=(?=.*(美|洛杉矶|🇺🇸|US|(?i)States|American))^((?!(港|台|日|韩|新)).)*$": "United States = select,policy-regex-filter=(?=.*(美|洛杉矶|🇺🇸|US|(?i)States|American))^((?!(港|台|日|韩|新)).)*$",
    "日本节点 = select,policy-regex-filter=(?=.*(日|🇯🇵|东京|JP|(?i)Japan))^((?!(港|台|韩|新|美)).)*$": "Japan = select,policy-regex-filter=(?=.*(日|🇯🇵|东京|JP|(?i)Japan))^((?!(港|台|韩|新|美)).)*$",
    "香港节点 = select,policy-regex-filter=(?=.*(港|HK|(?i)Hong))^((?!(台|日|韩|新|美)).)*$": "Hong Kong = select,policy-regex-filter=(?=.*(港|HK|(?i)Hong))^((?!(台|日|韩|新|美)).)*$",
    "台湾节点 = select,policy-regex-filter=(?=.*(台|TW|(?i)Taiwan))^((?!(港|日|韩|新|美)).)*$": "Europe = select,policy-regex-filter=(?=.*(英|法|德|欧|🇬🇧|🇫🇷|🇩🇪|🇪🇺))^((?!(港|台|日|韩|新|美)).)*$"
}

for old, new in replacements.items():
    text = text.replace(old, new)


rules_section = """
[Rule]
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Direct.list,Mainland
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/AI.list,AI
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/PayPal.list,PayPal
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Netflix.list,Gmedia
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Disney.list,Gmedia
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/PrimeVideo.list,Gmedia
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/HBO.list,Gmedia
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Bahamut.list,Gmedia
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/TikTok.list,Gmedia
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/YouTube.list,Google
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Google.list,Google
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Microsoft.list,Microsoft
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/OneDrive.list,Microsoft
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Github.list,Microsoft
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Telegram.list,Telegram
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Twitter.list,Social
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Instagram.list,Social
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Steam.list,Game
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Epic.list,Game
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Emby.list,Emby
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Spotify.list,Spotify
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/AppleServers.list,Apple
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/AppleCN.list,Mainland
RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/Proxy.list,Outside
GEOIP,CN,Mainland
FINAL,NoAuto
"""

text = re.sub(r'\[Rule\](.*?)\[URL Rewrite\]', rules_section + '\n[URL Rewrite]', text, flags=re.DOTALL)

with SR_PATH.open("w", encoding="utf-8") as f:
    f.write(text)
