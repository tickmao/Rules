from pathlib import Path
import yaml # using PyYAML might not preserve comments!

ROOT = Path(__file__).resolve().parent.parent
CLASH_PATH = ROOT / "Clash" / "Meta" / "Clash.yml"

with CLASH_PATH.open("r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("Clash/ClashPro/tickmao-pro.yml", "Clash/Meta/Clash.yml")
text = text.replace("策略选择", "Proxy")
text = text.replace("国外网站", "Outside")
text = text.replace("国际媒体", "Gmedia")
text = text.replace("苹果服务", "Apple")
text = text.replace("微软服务", "Microsoft")
text = text.replace("谷歌服务", "Google")
text = text.replace("电报消息", "Telegram")
text = text.replace("推特消息", "Social")
text = text.replace("游戏平台", "Game")
text = text.replace("广告拦截", "Reject")
text = text.replace("兜底分流", "Final")

text = text.replace("⏱香港延迟优选", "HK Auto")
text = text.replace("⏱美国延迟优选", "US Auto")
text = text.replace("⏱日本延迟优选", "JP Auto")
text = text.replace("⏱欧洲延迟优选", "EU Auto")
text = text.replace("🚥故障转移", "Fallback")
text = text.replace("🚥香港故障转移", "HK Fallback")
text = text.replace("🚥美国故障转移", "US Fallback")
text = text.replace("🚥日本故障转移", "JP Fallback")
text = text.replace("🚥欧洲故障转移", "EU Fallback")
text = text.replace("⚖️负载均衡", "Balance")
text = text.replace("⚖️香港负载均衡", "HK Balance")
text = text.replace("⚖️美国负载均衡", "US Balance")
text = text.replace("⚖️日本负载均衡", "JP Balance")
text = text.replace("⚖️欧洲负载均衡", "EU Balance")

import re
text = re.sub(r'https://github\.com/Repcz/Tool/raw/X/Clash/Rules/([a-zA-Z0-9_\-]+)\.list', r'https://raw.githubusercontent.com/tickmao/Rules/master/Clash/Meta/Rules/\1.list', text)
text = re.sub(r'https://github\.com/Repcz/Tool/raw/X/Surge/Rules/([a-zA-Z0-9_\-]+)\.list', r'https://raw.githubusercontent.com/tickmao/Rules/master/Clash/Meta/Rules/\1.list', text)

with CLASH_PATH.open("w", encoding="utf-8") as f:
    f.write(text)
