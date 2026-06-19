#!/bin/bash
# ============================================================
# 规则同步脚本 - 从上游仓库拉取最新规则到本仓库
# ============================================================

set -e

# ================= Configuration =================
WORK_DIR=$(cd "$(dirname "$0")/.." && pwd)
DRY_RUN=false
SKIP_REBUILD=false
SYNC_PLATFORMS=()

ALL_PLATFORMS=("Surge" "Loon" "QuantumultX" "Clash" "Shadowrocket")

# 上游基准 URL 和本地规则头
BLACKMATRIX_BASE="https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule"
MIN_RULE_LINES=2
LOCAL_HEADER_LINES=6

# 规则字典只保留本地相对路径；上游文件映射由 resolve_remote_rule 统一处理。
RULES=()

# ----------------- Surge Rules -----------------
RULES+=( "Surge/Rules/Direct.list" )
RULES+=( "Surge/Rules/Ads_SukkaW.list" )
RULES+=( "Surge/Rules/Reject.list" )
RULES+=( "Surge/Rules/AI.list" )
RULES+=( "Surge/Rules/PayPal.list" )
RULES+=( "Surge/Rules/Netflix.list" )
RULES+=( "Surge/Rules/Telegram.list" )
RULES+=( "Surge/Rules/Twitter.list" )
RULES+=( "Surge/Rules/Instagram.list" )
RULES+=( "Surge/Rules/TikTok.list" )
RULES+=( "Surge/Rules/Steam.list" )
RULES+=( "Surge/Rules/Epic.list" )
RULES+=( "Surge/Rules/YouTube.list" )
RULES+=( "Surge/Rules/Google.list" )
RULES+=( "Surge/Rules/Github.list" )
RULES+=( "Surge/Rules/OneDrive.list" )
RULES+=( "Surge/Rules/Microsoft.list" )
RULES+=( "Surge/Rules/Emby.list" )
RULES+=( "Surge/Rules/Spotify.list" )
RULES+=( "Surge/Rules/Bahamut.list" )
RULES+=( "Surge/Rules/Disney.list" )
RULES+=( "Surge/Rules/PrimeVideo.list" )
RULES+=( "Surge/Rules/HBO.list" )
RULES+=( "Surge/Rules/Proxy.list" )
RULES+=( "Surge/Rules/AppleCN.list" )
RULES+=( "Surge/Rules/AppleServers.list" )

# ----------------- Loon Rules -----------------
RULES+=( "Loon/Rules/Direct.list" )
RULES+=( "Loon/Rules/Ads_SukkaW.list" )
RULES+=( "Loon/Rules/Reject.list" )
RULES+=( "Loon/Rules/AI.list" )
RULES+=( "Loon/Rules/PayPal.list" )
RULES+=( "Loon/Rules/Netflix.list" )
RULES+=( "Loon/Rules/Telegram.list" )
RULES+=( "Loon/Rules/Twitter.list" )
RULES+=( "Loon/Rules/Instagram.list" )
RULES+=( "Loon/Rules/TikTok.list" )
RULES+=( "Loon/Rules/Steam.list" )
RULES+=( "Loon/Rules/Epic.list" )
RULES+=( "Loon/Rules/YouTube.list" )
RULES+=( "Loon/Rules/Google.list" )
RULES+=( "Loon/Rules/Github.list" )
RULES+=( "Loon/Rules/OneDrive.list" )
RULES+=( "Loon/Rules/Microsoft.list" )
RULES+=( "Loon/Rules/Emby.list" )
RULES+=( "Loon/Rules/Spotify.list" )
RULES+=( "Loon/Rules/Bahamut.list" )
RULES+=( "Loon/Rules/Disney.list" )
RULES+=( "Loon/Rules/PrimeVideo.list" )
RULES+=( "Loon/Rules/HBO.list" )
RULES+=( "Loon/Rules/Proxy.list" )
RULES+=( "Loon/Rules/AppleCN.list" )
RULES+=( "Loon/Rules/AppleServers.list" )

# ----------------- QuantumultX Rules -----------------
RULES+=( "QuantumultX/Rules/Direct.list" )
RULES+=( "QuantumultX/Rules/Ads_SukkaW.list" )
RULES+=( "QuantumultX/Rules/Reject.list" )
RULES+=( "QuantumultX/Rules/AI.list" )
RULES+=( "QuantumultX/Rules/PayPal.list" )
RULES+=( "QuantumultX/Rules/Netflix.list" )
RULES+=( "QuantumultX/Rules/Telegram.list" )
RULES+=( "QuantumultX/Rules/Twitter.list" )
RULES+=( "QuantumultX/Rules/Instagram.list" )
RULES+=( "QuantumultX/Rules/TikTok.list" )
RULES+=( "QuantumultX/Rules/Steam.list" )
RULES+=( "QuantumultX/Rules/Epic.list" )
RULES+=( "QuantumultX/Rules/YouTube.list" )
RULES+=( "QuantumultX/Rules/Google.list" )
RULES+=( "QuantumultX/Rules/Github.list" )
RULES+=( "QuantumultX/Rules/OneDrive.list" )
RULES+=( "QuantumultX/Rules/Microsoft.list" )
RULES+=( "QuantumultX/Rules/Emby.list" )
RULES+=( "QuantumultX/Rules/Spotify.list" )
RULES+=( "QuantumultX/Rules/Bahamut.list" )
RULES+=( "QuantumultX/Rules/Disney.list" )
RULES+=( "QuantumultX/Rules/PrimeVideo.list" )
RULES+=( "QuantumultX/Rules/HBO.list" )
RULES+=( "QuantumultX/Rules/Proxy.list" )
RULES+=( "QuantumultX/Rules/AppleCN.list" )
RULES+=( "QuantumultX/Rules/AppleServers.list" )

# ----------------- Clash Rules -----------------
RULES+=( "Clash/Meta/Rules/Direct.list" )
RULES+=( "Clash/Meta/Rules/Ads_SukkaW.list" )
RULES+=( "Clash/Meta/Rules/Reject.list" )
RULES+=( "Clash/Meta/Rules/AI.list" )
RULES+=( "Clash/Meta/Rules/PayPal.list" )
RULES+=( "Clash/Meta/Rules/Netflix.list" )
RULES+=( "Clash/Meta/Rules/Telegram.list" )
RULES+=( "Clash/Meta/Rules/Twitter.list" )
RULES+=( "Clash/Meta/Rules/Instagram.list" )
RULES+=( "Clash/Meta/Rules/TikTok.list" )
RULES+=( "Clash/Meta/Rules/Steam.list" )
RULES+=( "Clash/Meta/Rules/Epic.list" )
RULES+=( "Clash/Meta/Rules/YouTube.list" )
RULES+=( "Clash/Meta/Rules/Google.list" )
RULES+=( "Clash/Meta/Rules/Github.list" )
RULES+=( "Clash/Meta/Rules/OneDrive.list" )
RULES+=( "Clash/Meta/Rules/Microsoft.list" )
RULES+=( "Clash/Meta/Rules/Emby.list" )
RULES+=( "Clash/Meta/Rules/Spotify.list" )
RULES+=( "Clash/Meta/Rules/Bahamut.list" )
RULES+=( "Clash/Meta/Rules/Disney.list" )
RULES+=( "Clash/Meta/Rules/PrimeVideo.list" )
RULES+=( "Clash/Meta/Rules/HBO.list" )
RULES+=( "Clash/Meta/Rules/Proxy.list" )
RULES+=( "Clash/Meta/Rules/AppleCN.list" )
RULES+=( "Clash/Meta/Rules/AppleServers.list" )

# ----------------- Shadowrocket Rules -----------------
RULES+=( "Shadowrocket/Rules/Direct.list" )
RULES+=( "Shadowrocket/Rules/Ads_SukkaW.list" )
RULES+=( "Shadowrocket/Rules/Reject.list" )
RULES+=( "Shadowrocket/Rules/AI.list" )
RULES+=( "Shadowrocket/Rules/PayPal.list" )
RULES+=( "Shadowrocket/Rules/Netflix.list" )
RULES+=( "Shadowrocket/Rules/Telegram.list" )
RULES+=( "Shadowrocket/Rules/Twitter.list" )
RULES+=( "Shadowrocket/Rules/Instagram.list" )
RULES+=( "Shadowrocket/Rules/TikTok.list" )
RULES+=( "Shadowrocket/Rules/Steam.list" )
RULES+=( "Shadowrocket/Rules/Epic.list" )
RULES+=( "Shadowrocket/Rules/YouTube.list" )
RULES+=( "Shadowrocket/Rules/Google.list" )
RULES+=( "Shadowrocket/Rules/Github.list" )
RULES+=( "Shadowrocket/Rules/OneDrive.list" )
RULES+=( "Shadowrocket/Rules/Microsoft.list" )
RULES+=( "Shadowrocket/Rules/Emby.list" )
RULES+=( "Shadowrocket/Rules/Spotify.list" )
RULES+=( "Shadowrocket/Rules/Bahamut.list" )
RULES+=( "Shadowrocket/Rules/Disney.list" )
RULES+=( "Shadowrocket/Rules/PrimeVideo.list" )
RULES+=( "Shadowrocket/Rules/HBO.list" )
RULES+=( "Shadowrocket/Rules/Proxy.list" )
RULES+=( "Shadowrocket/Rules/AppleCN.list" )
RULES+=( "Shadowrocket/Rules/AppleServers.list" )

# ================= Parse Arguments =================
for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            echo "⚠️  [DRY RUN MODE] No files will be modified."
            ;;
        --skip-rebuild)
            SKIP_REBUILD=true
            ;;
        sur|surge)
            SYNC_PLATFORMS+=("Surge")
            ;;
        loon)
            SYNC_PLATFORMS+=("Loon")
            ;;
        qx|quantumultx)
            SYNC_PLATFORMS+=("QuantumultX")
            ;;
        cla|clash)
            SYNC_PLATFORMS+=("Clash")
            ;;
        sr|shadowrocket)
            SYNC_PLATFORMS+=("Shadowrocket")
            ;;
        *)
            echo "Unknown argument: $arg"
            echo "Usage: $0 [surge|loon|qx|clash|sr] [--dry-run] [--skip-rebuild]"
            exit 1
            ;;
    esac
done

if [ ${#SYNC_PLATFORMS[@]} -eq 0 ]; then
    SYNC_PLATFORMS=("${ALL_PLATFORMS[@]}")
fi

echo "🔄 Syncing platforms: ${SYNC_PLATFORMS[*]}"

# ================= Helper Functions =================

# 检查当前平台是否在同步列表中
should_sync_platform() {
    local platform=$1
    for p in "${SYNC_PLATFORMS[@]}"; do
        if [[ "$platform" == "$p" ]]; then
            return 0
        fi
    done
    return 1
}

# 提取平台名称 (e.g., Surge/Rules/AI.list -> Surge)
get_platform() {
    local path=$1
    echo "$path" | cut -d'/' -f1
}

# 将本地规则名映射到更完整、常用的 blackmatrix7 上游规则名。
get_upstream_rule_name() {
    local name=$1
    case "$name" in
        Ads_SukkaW) echo "Advertising" ;;
        Reject) echo "AdvertisingLite" ;;
        AI) echo "OpenAI" ;;
        Github) echo "GitHub" ;;
        AppleCN) echo "Apple" ;;
        AppleServers) echo "AppleProxy" ;;
        *) echo "$name" ;;
    esac
}

get_remote_platform() {
    local platform=$1
    case "$platform" in
        Shadowrocket) echo "Surge" ;;
        *) echo "$platform" ;;
    esac
}

resolve_remote_rule() {
    local local_path=$1
    local platform rule_name upstream_name remote_platform

    platform=$(get_platform "$local_path")
    rule_name=$(basename "$local_path" .list)
    upstream_name=$(get_upstream_rule_name "$rule_name")
    remote_platform=$(get_remote_platform "$platform")

    REMOTE_URL="${BLACKMATRIX_BASE}/${remote_platform}/${upstream_name}/${upstream_name}.list"
}

count_rule_lines() {
    awk 'BEGIN{n=0} /^[[:space:]]*($|#|;|\/\/)/{next} {n++} END{print n}' "$1"
}

strip_upstream_metadata() {
    local file=$1
    awk 'BEGIN{seen_rule=0} !seen_rule && /^[[:space:]]*($|#|;|\/\/)/{next} {seen_rule=1; print}' "$file" > "${file}.rules"
    mv "${file}.rules" "$file"
}

# ================= Main Sync Loop =================

SYNC_TIME="$(date '+%Y-%m-%d %H:%M:%S %Z')"
COUNT_SUCCESS=0
COUNT_SKIP=0
COUNT_FAIL=0

for rule in "${RULES[@]}"; do
    LOCAL_PATH="$rule"
    PLATFORM=$(get_platform "$LOCAL_PATH")
    
    if ! should_sync_platform "$PLATFORM"; then
        continue
    fi

    resolve_remote_rule "$LOCAL_PATH"
    
    FULL_LOCAL_PATH="$WORK_DIR/$LOCAL_PATH"
    
    if [ "$DRY_RUN" = true ]; then
        echo "🧐 [DRY-RUN] Will sync: $LOCAL_PATH"
        echo "    🔗 From: $REMOTE_URL"
        continue
    fi
    
    # 创建目标目录
    mkdir -p "$(dirname "$FULL_LOCAL_PATH")"
    
    # 临时文件
    TEMP_FILE=$(mktemp)
    
    echo -n "⬇️  Downloading $LOCAL_PATH ... "
    
    # 下载并检查 HTTP 状态码
    HTTP_CODE=$(curl -sL --retry 3 --connect-timeout 20 --write-out "%{http_code}" -o "$TEMP_FILE" "$REMOTE_URL")
    
    if [ "$HTTP_CODE" -eq 200 ] && [ -s "$TEMP_FILE" ]; then
        # 移除文件末尾多余的空行，同时保留完整规则内容。
        awk '{lines[NR]=$0} END{last=NR; while (last > 0 && lines[last] ~ /^[[:space:]]*$/) last--; for (i=1; i<=last; i++) print lines[i]}' "$TEMP_FILE" > "${TEMP_FILE}.clean"
        mv "${TEMP_FILE}.clean" "$TEMP_FILE"
        strip_upstream_metadata "$TEMP_FILE"

        RULE_LINE_COUNT=$(count_rule_lines "$TEMP_FILE")
        if [ "$RULE_LINE_COUNT" -lt "$MIN_RULE_LINES" ]; then
            echo "❌ FAILED (Only $RULE_LINE_COUNT rule line(s), below minimum $MIN_RULE_LINES)"
            COUNT_FAIL=$((COUNT_FAIL+1))
            rm -f "$TEMP_FILE"
            continue
        fi

        # 判断是否和本地内容一致（跳过 6 行自定义 header）
        if [ -f "$FULL_LOCAL_PATH" ]; then
            if tail -n +$((LOCAL_HEADER_LINES + 1)) "$FULL_LOCAL_PATH" | cmp -s - "$TEMP_FILE"; then
                echo "⏭️  SKIP (No changes)"
                COUNT_SKIP=$((COUNT_SKIP+1))
                rm "$TEMP_FILE"
                continue
            fi
        fi

        # 写入新文件（带 Header）
        {
            echo "# ============================================"
            echo "# @SyncTime    $SYNC_TIME"
            echo "# @LocalPath   $LOCAL_PATH"
            echo "# @GeneratedBy scripts/sync_rules.sh"
            echo "# @Maintainer  tickmao"
            echo "# ============================================"
            cat "$TEMP_FILE"
        } > "$FULL_LOCAL_PATH"
        
        echo "✅ OK"
        COUNT_SUCCESS=$((COUNT_SUCCESS+1))
    else
        echo "❌ FAILED (HTTP $HTTP_CODE)"
        COUNT_FAIL=$((COUNT_FAIL+1))
    fi
    
    rm -f "$TEMP_FILE"
done

echo "============================================"
echo "📊 Sync Summary:"
echo "✅ Success : $COUNT_SUCCESS"
echo "⏭️  Skipped : $COUNT_SKIP (No changes)"
echo "❌ Failed  : $COUNT_FAIL"
echo "============================================"

if [ "$COUNT_FAIL" -gt 0 ]; then
    exit 1
fi

if [ "$SKIP_REBUILD" = true ]; then
    echo "⏭️  Skipping core rebuild and validation."
    exit 0
fi

echo "🧱 Rebuilding cross-platform core blocks..."
if [ "$DRY_RUN" = true ]; then
    python3 "$WORK_DIR/scripts/rebuild_core.py" --dry-run
else
    python3 "$WORK_DIR/scripts/rebuild_core.py"
fi

echo "🧪 Running YAML validation..."
python3 "$WORK_DIR/scripts/validate_yaml.py"

echo "🔎 Running consistency checks..."
set +e
python3 "$WORK_DIR/scripts/check_consistency.py" --strict-order
CHECK_CODE=$?
set -e
if [ "$CHECK_CODE" -eq 1 ]; then
    echo "❌ Consistency check failed."
    exit 1
elif [ "$CHECK_CODE" -eq 2 ]; then
    echo "⚠️  Consistency check passed with warnings."
else
    echo "✅ Consistency check passed."
fi
