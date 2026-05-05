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


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_markers(text: str, section: str, start_marker: str, end_marker: str) -> str:
    section_re = re.compile(rf"(?ms)^\[{re.escape(section)}\]\n(.*?)(?=^\[|\Z)")
    m = section_re.search(text)
    if not m:
        return text
    body = m.group(1)
    if start_marker in body and end_marker in body:
        return text
    core = f"{start_marker}\n{end_marker}\n"
    if body.startswith("\n"):
        new_body = core + body
    else:
        new_body = core + "\n" + body
    return text[: m.start(1)] + new_body + text[m.end(1) :]


def replace_between_markers(text: str, start_marker: str, end_marker: str, payload: str) -> str:
    pattern = re.compile(
        rf"(?ms)({re.escape(start_marker)}\n)(.*?)(\n{re.escape(end_marker)})"
    )
    if not pattern.search(text):
        return text
    return pattern.sub(rf"\1{payload}\3", text, count=1)


def extract_surge_rules() -> list[str]:
    surge = MAIN_FILES["surge"].read_text(encoding="utf-8")
    m = re.search(r"(?ms)^\[Rule\]\n(.*?)(?=^\[|\Z)", surge)
    if not m:
        return []
    lines = []
    for raw in m.group(1).splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Surge/Rules/"):
            lines.append(line)
    return lines


def build_order(map_cfg: dict, surge_rules: list[str]) -> list[dict]:
    by_file = {entry["file"]: entry for entry in map_cfg["rules"]}
    order = []
    for line in surge_rules:
        m = re.match(
            r"RULE-SET,https://raw\.githubusercontent\.com/tickmao/Rules/master/Surge/Rules/([^,]+),",
            line,
        )
        if not m:
            continue
        file_name = m.group(1)
        if file_name in by_file:
            order.append(by_file[file_name])
    # include unmapped tail entries if any
    known = {e["file"] for e in order}
    for entry in map_cfg["rules"]:
        if entry["file"] not in known:
            order.append(entry)
    return order


def build_loon_block(order: list[dict], interval_default: int) -> str:
    lines = []
    for e in order:
        target = e["targets"]["loon"]
        tag = e["tag"]
        file_name = e["file"]
        interval = e.get("qx_interval", interval_default)
        _ = interval  # for consistent field availability
        lines.append(
            f"https://raw.githubusercontent.com/tickmao/Rules/master/Loon/Rules/{file_name}, policy={target}, tag={tag}, enabled=true"
        )
    return "\n".join(lines)


def build_qx_block(order: list[dict], interval_default: int, qx_tail: list[str]) -> str:
    lines = []
    for e in order:
        target = e["targets"]["qx"]
        tag = e["tag"]
        file_name = e["file"]
        interval = e.get("qx_interval", interval_default)
        lines.append(
            f"https://raw.githubusercontent.com/tickmao/Rules/master/QuantumultX/Rules/{file_name}, tag={tag}, force-policy={target}, update-interval={interval}, opt-parser=false, enabled=true"
        )
    lines.extend(qx_tail)
    return "\n".join(lines)


def build_shadowrocket_block(order: list[dict], tail: list[str]) -> str:
    lines = []
    for e in order:
        target = e["targets"]["shadowrocket"]
        file_name = e["file"]
        lines.append(
            f"RULE-SET,https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Rules/{file_name},{target}"
        )
    lines.extend(tail)
    return "\n".join(lines)


def build_clash_rule_providers(order: list[dict]) -> str:
    lines = []
    for e in order:
        key = e["key"]
        file_name = e["file"]
        lines.append(
            f"  {key}: {{<<: *c, path: ./rule-providers/{file_name},  url: https://raw.githubusercontent.com/tickmao/Rules/master/Clash/Meta/Rules/{file_name}}}"
        )
    return "\n".join(lines)


def build_clash_rules(order: list[dict], tail: list[str]) -> str:
    lines = []
    for e in order:
        key = e["key"]
        target = e["targets"]["clash"]
        lines.append(f"  - RULE-SET,{key},{target}")
    lines.extend([f"{line}" if line.startswith("  - ") else (f"  {line}" if line.startswith("-") else f"  - {line}") for line in tail])
    return "\n".join(lines)


def update_file(path: Path, new_text: str, dry_run: bool) -> bool:
    old_text = path.read_text(encoding="utf-8")
    if old_text == new_text:
        return False
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def generate_report(report_path: Path, changed: list[str], dry_run: bool) -> None:
    if not changed:
        return
    lines = [
        "# Sync Report",
        "",
        f"- Mode: {'dry-run' if dry_run else 'apply'}",
        f"- Changed files: {len(changed)}",
        "",
    ]
    lines.append("## Updated")
    lines.extend([f"- {p}" for p in changed])
    if not dry_run:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild cross-platform core rules from Surge semantic order")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = parser.parse_args()

    cfg = load_json(MAP_PATH)
    start_marker = cfg["marker_start"]
    end_marker = cfg["marker_end"]
    interval_default = int(cfg.get("qx_default_interval", 172800))
    report_path = ROOT / cfg.get("report_path", "reports/sync_report.md")

    surge_rules = extract_surge_rules()
    if not surge_rules:
        print("ERROR: failed to extract Surge RULE-SET baseline")
        return 1
    order = build_order(cfg, surge_rules)

    changed = []

    # Loon [Remote Rule]
    loon_path = MAIN_FILES["loon"]
    loon_text = loon_path.read_text(encoding="utf-8")
    loon_text = ensure_markers(loon_text, "Remote Rule", start_marker, end_marker)
    loon_payload = build_loon_block(order, interval_default)
    loon_new = replace_between_markers(loon_text, start_marker, end_marker, loon_payload)
    if update_file(loon_path, loon_new, args.dry_run):
        changed.append("Loon/Loon.conf")

    # QX [filter_remote]
    qx_path = MAIN_FILES["qx"]
    qx_text = qx_path.read_text(encoding="utf-8")
    qx_text = ensure_markers(qx_text, "filter_remote", start_marker, end_marker)
    qx_payload = build_qx_block(order, interval_default, cfg.get("qx_tail", []))
    qx_new = replace_between_markers(qx_text, start_marker, end_marker, qx_payload)
    if update_file(qx_path, qx_new, args.dry_run):
        changed.append("QuantumultX/QuantumultX.conf")

    # Shadowrocket [Rule]
    sr_path = MAIN_FILES["shadowrocket"]
    sr_text = sr_path.read_text(encoding="utf-8")
    sr_text = ensure_markers(sr_text, "Rule", start_marker, end_marker)
    sr_payload = build_shadowrocket_block(order, cfg.get("shadowrocket_tail", []))
    sr_new = replace_between_markers(sr_text, start_marker, end_marker, sr_payload)
    if update_file(sr_path, sr_new, args.dry_run):
        changed.append("Shadowrocket/Shadowrocket.conf")

    # Clash rule-providers
    clash_path = MAIN_FILES["clash"]
    clash_text = clash_path.read_text(encoding="utf-8")
    rp_marker_start = f"{start_marker} rule-providers"
    rp_marker_end = f"{end_marker} rule-providers"
    rl_marker_start = f"{start_marker} rules"
    rl_marker_end = f"{end_marker} rules"

    if rp_marker_start not in clash_text or rp_marker_end not in clash_text:
        m = re.search(r"(?ms)^rule-providers:\n", clash_text)
        if m:
            insert = f"{rp_marker_start}\n{rp_marker_end}\n"
            clash_text = clash_text[: m.end()] + insert + clash_text[m.end() :]
    if rl_marker_start not in clash_text or rl_marker_end not in clash_text:
        m = re.search(r"(?ms)^rules:\n", clash_text)
        if m:
            insert = f"{rl_marker_start}\n{rl_marker_end}\n"
            clash_text = clash_text[: m.end()] + insert + clash_text[m.end() :]

    rp_payload = build_clash_rule_providers(order)
    rl_payload = build_clash_rules(order, cfg.get("clash_tail", []))
    clash_text = replace_between_markers(clash_text, rp_marker_start, rp_marker_end, rp_payload)
    clash_new = replace_between_markers(clash_text, rl_marker_start, rl_marker_end, rl_payload)
    if update_file(clash_path, clash_new, args.dry_run):
        changed.append("Clash/Meta/Clash.yml")

    generate_report(report_path, changed, args.dry_run)

    mode = "dry-run" if args.dry_run else "apply"
    print(f"rebuild_core: {mode} completed, changed={len(changed)}")
    for item in changed:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
