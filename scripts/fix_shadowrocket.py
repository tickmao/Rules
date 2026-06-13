import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SR_PATH = ROOT / "Shadowrocket" / "Shadowrocket.conf"

with SR_PATH.open("r", encoding="utf-8") as f:
    text = f.read()

# Replace Group Configs
replacements = {
    "手动切换 = select,PROXY": "Proxy = select,PROXY,US Manual,JP Manual,EU Manual,All,DIRECT\nAll = select,policy-regex-filter=.*",
    "国外网站 = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Outside = select,Proxy,US Manual,JP Manual,EU Manual,All",
    "国内网站 = select,DIRECT,手动切换,美国节点,日本节点,香港节点,台湾节点": "Mainland = select,DIRECT,Proxy,US Manual,JP Manual,EU Manual,All",
    "YouTube = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Google = select,Proxy,US Manual,JP Manual,EU Manual,All",
    "NETFLIX = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Gmedia = select,Proxy,US Manual,JP Manual,EU Manual,All",
    "Disney+ = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Microsoft = select,Proxy,US Manual,JP Manual,EU Manual,All",
    "Twitter = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Social = select,Proxy,US Manual,JP Manual,EU Manual,All",
    "Telegram = select,手动切换,美国节点,日本节点,香港节点,台湾节点": "Telegram = select,Proxy,US Manual,JP Manual,EU Manual,All,DIRECT",
    "PayPal = select,DIRECT,手动切换,美国节点,日本节点,香港节点,台湾节点": "PayPal = select,Proxy,US Manual,JP Manual,EU Manual,All",
    "网易音乐 = select,DIRECT": "AI = select,Proxy,US Manual,JP Manual,EU Manual,All",
    "苹果服务 = select,DIRECT,手动切换,美国节点,日本节点,香港节点,台湾节点": "Apple = select,DIRECT,Proxy,US Manual,JP Manual,EU Manual,All",
    "微软服务 = select,DIRECT,手动切换,美国节点,日本节点,香港节点,台湾节点": "Game = select,Proxy,US Manual,JP Manual,EU Manual,All",
    "哔哩哔哩 = select,DIRECT,手动切换,美国节点,日本节点,香港节点,台湾节点": "Emby = select,Proxy,US Manual,JP Manual,EU Manual,All",
    "游戏平台 = select,手动切换,美国节点,日本节点,香港节点,台湾节点,DIRECT": "Spotify = select,Proxy,US Manual,JP Manual,EU Manual,All",
    "AdBlock = select,REJECT": "AdBlock = select,REJECT",
    "漏网之鱼 = select,手动切换,美国节点,日本节点,香港节点,台湾节点,DIRECT": "Final = select,Proxy,US Manual,JP Manual,EU Manual,All,DIRECT",
    "美国节点 = select,policy-regex-filter=(?=.*(美|洛杉矶|🇺🇸|US|(?i)States|American))^((?!(港|台|日|韩|新)).)*$": "US Manual = select,US Auto,US Fallback,US Balance\nUS Auto = url-test,policy-regex-filter=(?=.*(美|洛杉矶|🇺🇸|US|(?i)States|American))^((?!(港|台|日|韩|新)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300,tolerance=0\nUS Fallback = fallback,policy-regex-filter=(?=.*(美|洛杉矶|🇺🇸|US|(?i)States|American))^((?!(港|台|日|韩|新)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300\nUS Balance = load-balance,policy-regex-filter=(?=.*(美|洛杉矶|🇺🇸|US|(?i)States|American))^((?!(港|台|日|韩|新)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300",
    "日本节点 = select,policy-regex-filter=(?=.*(日|🇯🇵|东京|JP|(?i)Japan))^((?!(港|台|韩|新|美)).)*$": "JP Manual = select,JP Auto,JP Fallback,JP Balance\nJP Auto = url-test,policy-regex-filter=(?=.*(日|🇯🇵|东京|JP|(?i)Japan))^((?!(港|台|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300,tolerance=0\nJP Fallback = fallback,policy-regex-filter=(?=.*(日|🇯🇵|东京|JP|(?i)Japan))^((?!(港|台|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300\nJP Balance = load-balance,policy-regex-filter=(?=.*(日|🇯🇵|东京|JP|(?i)Japan))^((?!(港|台|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300",
    "香港节点 = select,policy-regex-filter=(?=.*(港|HK|(?i)Hong))^((?!(台|日|韩|新|美)).)*$": "# HK Manual = select,HK Auto,HK Fallback,HK Balance\n# HK Auto = url-test,policy-regex-filter=(?=.*(港|HK|(?i)Hong))^((?!(台|日|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300,tolerance=0\n# HK Fallback = fallback,policy-regex-filter=(?=.*(港|HK|(?i)Hong))^((?!(台|日|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300\n# HK Balance = load-balance,policy-regex-filter=(?=.*(港|HK|(?i)Hong))^((?!(台|日|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300",
    "台湾节点 = select,policy-regex-filter=(?=.*(台|TW|(?i)Taiwan))^((?!(港|日|韩|新|美)).)*$": "# TW Manual = select,TW Auto,TW Fallback,TW Balance\n# TW Auto = url-test,policy-regex-filter=(?=.*(台|台湾|台北|新北|🇹🇼|TW|(?i)Taiwan))^((?!(港|日|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300,tolerance=0\n# TW Fallback = fallback,policy-regex-filter=(?=.*(台|台湾|台北|新北|🇹🇼|TW|(?i)Taiwan))^((?!(港|日|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300\n# TW Balance = load-balance,policy-regex-filter=(?=.*(台|台湾|台北|新北|🇹🇼|TW|(?i)Taiwan))^((?!(港|日|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300",
    "欧洲节点 = select,policy-regex-filter=(?=.*(英|法|德|欧|🇬🇧|🇫🇷|🇩🇪|🇪🇺))^((?!(港|台|日|韩|新|美)).)*$": "EU Manual = select,EU Auto,EU Fallback,EU Balance\nEU Auto = url-test,policy-regex-filter=(?=.*(英|法|德|欧|🇬🇧|🇫🇷|🇩🇪|🇪🇺|(?i)Europe|EU|UK))^((?!(港|台|日|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300,tolerance=0\nEU Fallback = fallback,policy-regex-filter=(?=.*(英|法|德|欧|🇬🇧|🇫🇷|🇩🇪|🇪🇺|(?i)Europe|EU|UK))^((?!(港|台|日|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300\nEU Balance = load-balance,policy-regex-filter=(?=.*(英|法|德|欧|🇬🇧|🇫🇷|🇩🇪|🇪🇺|(?i)Europe|EU|UK))^((?!(港|台|日|韩|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300",
    "新加坡节点 = select,policy-regex-filter=(?=.*(新加坡|狮城|狮|🇸🇬|SG|(?i)Singapore))^((?!(港|台|日|韩|美)).)*$": "# SG Manual = select,SG Auto,SG Fallback,SG Balance\n# SG Auto = url-test,policy-regex-filter=(?=.*(新加坡|狮城|狮|🇸🇬|SG|(?i)Singapore))^((?!(港|台|日|韩|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300,tolerance=0\n# SG Fallback = fallback,policy-regex-filter=(?=.*(新加坡|狮城|狮|🇸🇬|SG|(?i)Singapore))^((?!(港|台|日|韩|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300\n# SG Balance = load-balance,policy-regex-filter=(?=.*(新加坡|狮城|狮|🇸🇬|SG|(?i)Singapore))^((?!(港|台|日|韩|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300",
    "韩国节点 = select,policy-regex-filter=(?=.*(韩|韩国|首尔|🇰🇷|KR|(?i)Korea))^((?!(港|台|日|新|美)).)*$": "# KR Manual = select,KR Auto,KR Fallback,KR Balance\n# KR Auto = url-test,policy-regex-filter=(?=.*(韩|韩国|首尔|🇰🇷|KR|(?i)Korea))^((?!(港|台|日|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300,tolerance=0\n# KR Fallback = fallback,policy-regex-filter=(?=.*(韩|韩国|首尔|🇰🇷|KR|(?i)Korea))^((?!(港|台|日|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300\n# KR Balance = load-balance,policy-regex-filter=(?=.*(韩|韩国|首尔|🇰🇷|KR|(?i)Korea))^((?!(港|台|日|新|美)).)*$,url=http://latency-test.skk.moe/endpoint,interval=300"
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
FINAL,Final
"""

text = re.sub(r'\[Rule\](.*?)\[URL Rewrite\]', rules_section + '\n[URL Rewrite]', text, flags=re.DOTALL)

with SR_PATH.open("w", encoding="utf-8") as f:
    f.write(text)
