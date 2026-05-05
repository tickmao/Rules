#!/usr/bin/env python3
import sys

import yaml


try:
    with open("Clash/Meta/Clash.yml", "r", encoding="utf-8") as f:
        yaml.safe_load(f)
    print("YAML Parse OK")
    sys.exit(0)
except Exception as e:
    print("YAML Parse Error:", e)
    sys.exit(1)
