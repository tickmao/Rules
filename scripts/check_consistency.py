#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
MAP_PATH = SCRIPTS / "policy_map.json"
MAIN_FILES = {
    "surge": ROOT / "Surge" / "Surge.conf",
    "loon": ROOT / "Loon" / "Loon.conf",
    "qx": ROOT / "QuantumultX" / "QuantumultX.conf",
    "shadowrocket": ROOT / "Shadowrocket" / "Shadowrocket.conf",
    "clash": ROOT / "Clash" / "Meta" / "Clash.yml",
}

ISSUES_ERROR = []
ISSUES_WARN = []


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def add_error(msg: str) -> None:
    ISSUES_ERROR.append(msg)


def add_warn(msg: str) -> None:
    ISSUES_WARN.append(msg)


def check_file_exists(path: Path, reason: str) -> None:
    if not path.exists():
        add_error(f"[missing] {reason}: {path.relative_to(ROOT)}")


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        add_error(f"[read] {path.relative_to(ROOT)}: {exc}")
        return ""


def parse_surge_groups(text: str) -> set[str]:
    groups = set()
    in_group = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("["):
            in_group = line.lower() == "[proxy group]"
            continue
        if in_group and "=" in line:
            groups.add(line.split("=", 1)[0].strip().strip('"'))
    groups.update({"DIRECT", "REJECT", "REJECT-NO-DROP", "PROXY"})
    return groups


def parse_shadowrocket_groups(text: str) -> set[str]:
    groups = set()
    in_group = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("["):
            in_group = line.lower() == "[proxy group]"
            continue
        if in_group and "=" in line:
            groups.add(line.split("=", 1)[0].strip())
    groups.update({"DIRECT", "REJECT", "PROXY"})
    return groups


def parse_loon_groups(text: str) -> set[str]:
    groups = set()
    in_group = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("["):
            in_group = line.lower() == "[proxy group]"
            continue
        if in_group and "=" in line:
            groups.add(line.split("=", 1)[0].strip())
    groups.update({"DIRECT", "REJECT", "PROXY"})
    return groups


def parse_qx_policies(text: str) -> set[str]:
    reserved = {"direct", "reject", "proxy"}
    policies = set(reserved) | {name.upper() for name in reserved}
    in_policy = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("["):
            in_policy = line.lower() == "[policy]"
            continue
        if in_policy and "=" in line:
            after_eq = line.split("=", 1)[1]
            first = after_eq.split(",", 1)[0].strip()
            if first:
                if first.lower() in reserved:
                    add_error(f"[qx] policy group uses reserved name: {first}")
                policies.add(first)
    return policies


def parse_clash_proxy_groups(text: str) -> set[str]:
    groups = set()
    block_match = re.search(r"(?ms)^proxy-groups:\s*\n(.*?)(?=^[A-Za-z0-9_-]+:)", text)
    block = block_match.group(1) if block_match else text
    for m in re.finditer(r"\{name:\s*([^,}]+)", block):
        groups.add(m.group(1).strip().strip('"').strip("'"))
    for m in re.finditer(r"^\s*-\s*name:\s*([^#\n]+)", block, flags=re.M):
        groups.add(m.group(1).strip().strip('"').strip("'"))
    groups.update({"DIRECT", "REJECT", "Proxy", "PROXY"})
    return groups


def check_rule_urls_exist(text: str, platform_dir: str, filename: str) -> None:
    pattern = r"https://raw\.githubusercontent\.com/tickmao/Rules/master/([^,\s]+\.list)"
    for rel in re.findall(pattern, text):
        rel_path = ROOT / rel
        check_file_exists(rel_path, f"{filename} references")
        if not str(rel_path).startswith(str((ROOT / platform_dir).resolve())):
            # 允许跨目录引用，不作为错误；只记录信息性警告
            pass


def check_surge() -> None:
    path = MAIN_FILES["surge"]
    text = load_text(path)
    if not text:
        return
    groups = parse_surge_groups(text)
    check_rule_urls_exist(text, "Surge", "Surge/Surge.conf")
    for m in re.finditer(r"^RULE-SET,[^,]+,([^,\s#]+)", text, flags=re.M):
        target = m.group(1).strip().strip('"')
        if target not in groups:
            add_error(f"[surge] undefined policy in RULE-SET: {target}")


def check_shadowrocket() -> None:
    path = MAIN_FILES["shadowrocket"]
    text = load_text(path)
    if not text:
        return
    groups = parse_shadowrocket_groups(text)
    check_rule_urls_exist(text, "Shadowrocket", "Shadowrocket/Shadowrocket.conf")
    m = re.search(r"^update-url\s*=\s*(\S+)", text, flags=re.M)
    if m:
        update_url = m.group(1).strip()
        prefix = "https://raw.githubusercontent.com/tickmao/Rules/master/"
        if update_url.startswith(prefix):
            rel = update_url[len(prefix):]
            check_file_exists(ROOT / rel, "Shadowrocket update-url target")
    for rule in re.finditer(r"^RULE-SET,[^,]+,([^,\s#]+)", text, flags=re.M):
        target = rule.group(1).strip()
        if target not in groups:
            add_error(f"[shadowrocket] undefined policy in RULE-SET: {target}")


def check_loon() -> None:
    path = MAIN_FILES["loon"]
    text = load_text(path)
    if not text:
        return
    groups = parse_loon_groups(text)
    check_rule_urls_exist(text, "Loon", "Loon/Loon.conf")
    for m in re.finditer(r"policy\s*=\s*([^,\n]+)", text):
        policy = m.group(1).strip()
        if policy not in groups:
            add_error(f"[loon] undefined policy reference: {policy}")
    if "策略选择" in text or "自动选择" in text:
        add_warn("[loon] found legacy policy aliases (策略选择/自动选择); recommend mapping to active groups")


def check_qx() -> None:
    path = MAIN_FILES["qx"]
    text = load_text(path)
    if not text:
        return
    policies = parse_qx_policies(text)
    check_rule_urls_exist(text, "QuantumultX", "QuantumultX/QuantumultX.conf")
    for m in re.finditer(r"force-policy\s*=\s*([^,\n]+)", text):
        p = m.group(1).strip()
        if p not in policies:
            add_error(f"[qx] undefined force-policy: {p}")


def check_clash() -> None:
    path = MAIN_FILES["clash"]
    text = load_text(path)
    if not text:
        return
    groups = parse_clash_proxy_groups(text)
    check_rule_urls_exist(text, "Clash/Meta", "Clash/Meta/Clash.yml")

    # rule-providers path/url basenames should match for maintainability
    for m in re.finditer(r"^\s*([A-Za-z0-9_-]+):\s*\{[^}]*path:\s*\.\/rule-providers\/([^,\s]+),[^}]*url:\s*(https://raw\.githubusercontent\.com/tickmao/Rules/master/[^,\s]+)\s*\}", text, flags=re.M):
        provider, path_name, url = m.groups()
        url_name = url.rsplit("/", 1)[-1]
        if path_name != url_name:
            add_warn(f"[clash] rule-provider {provider} path/url basename mismatch: {path_name} vs {url_name}")

    for m in re.finditer(r"^\s*-\s*RULE-SET,([^,\s]+),([^,\s]+)", text, flags=re.M):
        _, target = m.groups()
        if target not in groups:
            add_error(f"[clash] undefined target group in rules: {target}")


def check_markers() -> None:
    if not MAP_PATH.exists():
        add_warn("[marker] scripts/policy_map.json missing, skip marker checks")
        return
    cfg = load_json(MAP_PATH)
    start = cfg.get("marker_start", "")
    end = cfg.get("marker_end", "")
    if not start or not end:
        add_warn("[marker] marker config missing in policy_map.json")
        return

    marker_targets = [
        MAIN_FILES["loon"],
        MAIN_FILES["qx"],
        MAIN_FILES["shadowrocket"],
        MAIN_FILES["clash"],
    ]
    for path in marker_targets:
        text = load_text(path)
        if not text:
            continue
        if start not in text:
            add_error(f"[marker] missing start marker in {path.relative_to(ROOT)}")
        if end not in text:
            add_error(f"[marker] missing end marker in {path.relative_to(ROOT)}")


def strict_order_check() -> None:
    if not MAP_PATH.exists():
        add_warn("[strict-order] scripts/policy_map.json missing, skip strict order checks")
        return
    cfg = load_json(MAP_PATH)
    expected = [e["file"] for e in cfg.get("rules", [])]

    loom = MAIN_FILES["loon"]
    qx = MAIN_FILES["qx"]
    sr = MAIN_FILES["shadowrocket"]
    clash = MAIN_FILES["clash"]

    # Loon
    loom_text = load_text(loom)
    loom_files = re.findall(r"/Loon/Rules/([^,\s]+\.list),\s*policy=", loom_text)
    if loom_files:
        if loom_files[: len(expected)] != expected:
            add_error("[strict-order] Loon remote rule order differs from policy_map")

    # QX
    qx_text = load_text(qx)
    qx_files = re.findall(r"/QuantumultX/Rules/([^,\s]+\.list),\s*tag=", qx_text)
    if qx_files:
        if qx_files[: len(expected)] != expected:
            add_error("[strict-order] QuantumultX filter_remote order differs from policy_map")

    # Shadowrocket
    sr_text = load_text(sr)
    sr_files = re.findall(r"/Shadowrocket/Rules/([^,\s]+\.list),", sr_text)
    if sr_files:
        if sr_files[: len(expected)] != expected:
            add_error("[strict-order] Shadowrocket rule order differs from policy_map")

    # Clash
    clash_text = load_text(clash)
    clash_files = re.findall(r"path:\s*\.\/rule-providers\/([^,\s]+\.list),", clash_text)
    if clash_files:
        if clash_files[: len(expected)] != expected:
            add_error("[strict-order] Clash rule-provider order differs from policy_map")


def main() -> int:
    parser = argparse.ArgumentParser(description="Cross-platform consistency checks")
    parser.add_argument("--strict-order", action="store_true", help="enforce policy_map order checks")
    args = parser.parse_args()

    check_surge()
    check_loon()
    check_qx()
    check_clash()
    check_shadowrocket()
    check_markers()
    if args.strict_order:
        strict_order_check()

    for w in ISSUES_WARN:
        print(f"WARN: {w}")
    for e in ISSUES_ERROR:
        print(f"ERROR: {e}")

    if ISSUES_ERROR:
        print(f"\nConsistency check failed: {len(ISSUES_ERROR)} error(s), {len(ISSUES_WARN)} warning(s).")
        return 1
    if ISSUES_WARN:
        print(f"\nConsistency check passed with warnings: {len(ISSUES_WARN)}")
        return 2
    print("Consistency check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
