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

# 上游基准 URL
REPCZ_BASE="https://raw.githubusercontent.com/Repcz/Tool/X"
BLACKMATRIX_BASE="https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule"
MIN_RULE_LINES=2

# 规则字典定义（每个元素结构："本地相对路径|上游URL|来源名"）
# 实际同步源由 resolve_remote_rule 统一解析，保留 URL/来源字段用于兼容旧格式。
RULES=()

# ----------------- Surge Rules -----------------
RULES+=( "Surge/Rules/Direct.list|${REPCZ_BASE}/Surge/Rules/Direct.list|Repcz" )
RULES+=( "Surge/Rules/Ads_SukkaW.list|${REPCZ_BASE}/Surge/Rules/Ads_SukkaW.list|Repcz" )
RULES+=( "Surge/Rules/Reject.list|${REPCZ_BASE}/Surge/Rules/Reject.list|Repcz" )
RULES+=( "Surge/Rules/AI.list|${REPCZ_BASE}/Surge/Rules/AI.list|Repcz" )
RULES+=( "Surge/Rules/PayPal.list|${BLACKMATRIX_BASE}/Surge/PayPal/PayPal.list|blackmatrix7" )
RULES+=( "Surge/Rules/Netflix.list|${REPCZ_BASE}/Surge/Rules/Netflix.list|Repcz" )
RULES+=( "Surge/Rules/Telegram.list|${REPCZ_BASE}/Surge/Rules/Telegram.list|Repcz" )
RULES+=( "Surge/Rules/Twitter.list|${REPCZ_BASE}/Surge/Rules/Twitter.list|Repcz" )
RULES+=( "Surge/Rules/Instagram.list|${REPCZ_BASE}/Surge/Rules/Instagram.list|Repcz" )
RULES+=( "Surge/Rules/TikTok.list|${REPCZ_BASE}/Surge/Rules/TikTok.list|Repcz" )
RULES+=( "Surge/Rules/Steam.list|${REPCZ_BASE}/Surge/Rules/Steam.list|Repcz" )
RULES+=( "Surge/Rules/Epic.list|${REPCZ_BASE}/Surge/Rules/Epic.list|Repcz" )
RULES+=( "Surge/Rules/YouTube.list|${REPCZ_BASE}/Surge/Rules/YouTube.list|Repcz" )
RULES+=( "Surge/Rules/Google.list|${REPCZ_BASE}/Surge/Rules/Google.list|Repcz" )
RULES+=( "Surge/Rules/Github.list|${REPCZ_BASE}/Surge/Rules/Github.list|Repcz" )
RULES+=( "Surge/Rules/OneDrive.list|${REPCZ_BASE}/Surge/Rules/OneDrive.list|Repcz" )
RULES+=( "Surge/Rules/Microsoft.list|${REPCZ_BASE}/Surge/Rules/Microsoft.list|Repcz" )
RULES+=( "Surge/Rules/Emby.list|${REPCZ_BASE}/Surge/Rules/Emby.list|Repcz" )
RULES+=( "Surge/Rules/Spotify.list|${REPCZ_BASE}/Surge/Rules/Spotify.list|Repcz" )
RULES+=( "Surge/Rules/Bahamut.list|${REPCZ_BASE}/Surge/Rules/Bahamut.list|Repcz" )
RULES+=( "Surge/Rules/Disney.list|${REPCZ_BASE}/Surge/Rules/Disney.list|Repcz" )
RULES+=( "Surge/Rules/PrimeVideo.list|${REPCZ_BASE}/Surge/Rules/PrimeVideo.list|Repcz" )
RULES+=( "Surge/Rules/HBO.list|${REPCZ_BASE}/Surge/Rules/HBO.list|Repcz" )
RULES+=( "Surge/Rules/Proxy.list|${REPCZ_BASE}/Surge/Rules/Proxy.list|Repcz" )
RULES+=( "Surge/Rules/AppleCN.list|${REPCZ_BASE}/Surge/Rules/AppleCN.list|Repcz" )
RULES+=( "Surge/Rules/AppleServers.list|${REPCZ_BASE}/Surge/Rules/AppleServers.list|Repcz" )

# ----------------- Loon Rules -----------------
RULES+=( "Loon/Rules/Direct.list|${REPCZ_BASE}/Loon/Rules/Direct.list|Repcz" )
RULES+=( "Loon/Rules/Ads_SukkaW.list|${REPCZ_BASE}/Loon/Rules/Ads_SukkaW.list|Repcz" )
RULES+=( "Loon/Rules/Reject.list|${REPCZ_BASE}/Loon/Rules/Reject.list|Repcz" )
RULES+=( "Loon/Rules/AI.list|${REPCZ_BASE}/Loon/Rules/AI.list|Repcz" )
RULES+=( "Loon/Rules/PayPal.list|${BLACKMATRIX_BASE}/Loon/PayPal/PayPal.list|blackmatrix7" )
RULES+=( "Loon/Rules/Netflix.list|${REPCZ_BASE}/Loon/Rules/Netflix.list|Repcz" )
RULES+=( "Loon/Rules/Telegram.list|${REPCZ_BASE}/Loon/Rules/Telegram.list|Repcz" )
RULES+=( "Loon/Rules/Twitter.list|${REPCZ_BASE}/Loon/Rules/Twitter.list|Repcz" )
RULES+=( "Loon/Rules/Instagram.list|${REPCZ_BASE}/Loon/Rules/Instagram.list|Repcz" )
RULES+=( "Loon/Rules/TikTok.list|${REPCZ_BASE}/Loon/Rules/TikTok.list|Repcz" )
RULES+=( "Loon/Rules/Steam.list|${REPCZ_BASE}/Loon/Rules/Steam.list|Repcz" )
RULES+=( "Loon/Rules/Epic.list|${REPCZ_BASE}/Loon/Rules/Epic.list|Repcz" )
RULES+=( "Loon/Rules/YouTube.list|${REPCZ_BASE}/Loon/Rules/YouTube.list|Repcz" )
RULES+=( "Loon/Rules/Google.list|${REPCZ_BASE}/Loon/Rules/Google.list|Repcz" )
RULES+=( "Loon/Rules/Github.list|${REPCZ_BASE}/Loon/Rules/Github.list|Repcz" )
RULES+=( "Loon/Rules/OneDrive.list|${REPCZ_BASE}/Loon/Rules/OneDrive.list|Repcz" )
RULES+=( "Loon/Rules/Microsoft.list|${REPCZ_BASE}/Loon/Rules/Microsoft.list|Repcz" )
RULES+=( "Loon/Rules/Emby.list|${REPCZ_BASE}/Loon/Rules/Emby.list|Repcz" )
RULES+=( "Loon/Rules/Spotify.list|${REPCZ_BASE}/Loon/Rules/Spotify.list|Repcz" )
RULES+=( "Loon/Rules/Bahamut.list|${REPCZ_BASE}/Loon/Rules/Bahamut.list|Repcz" )
RULES+=( "Loon/Rules/Disney.list|${REPCZ_BASE}/Loon/Rules/Disney.list|Repcz" )
RULES+=( "Loon/Rules/PrimeVideo.list|${REPCZ_BASE}/Loon/Rules/PrimeVideo.list|Repcz" )
RULES+=( "Loon/Rules/HBO.list|${REPCZ_BASE}/Loon/Rules/HBO.list|Repcz" )
RULES+=( "Loon/Rules/Proxy.list|${REPCZ_BASE}/Loon/Rules/Proxy.list|Repcz" )
RULES+=( "Loon/Rules/AppleCN.list|${REPCZ_BASE}/Loon/Rules/AppleCN.list|Repcz" )
RULES+=( "Loon/Rules/AppleServers.list|${REPCZ_BASE}/Loon/Rules/AppleServers.list|Repcz" )

# ----------------- QuantumultX Rules -----------------
RULES+=( "QuantumultX/Rules/Direct.list|${REPCZ_BASE}/QuantumultX/Rules/Direct.list|Repcz" )
RULES+=( "QuantumultX/Rules/Ads_SukkaW.list|${REPCZ_BASE}/QuantumultX/Rules/Ads_SukkaW.list|Repcz" )
RULES+=( "QuantumultX/Rules/Reject.list|${REPCZ_BASE}/QuantumultX/Rules/Reject.list|Repcz" )
RULES+=( "QuantumultX/Rules/AI.list|${REPCZ_BASE}/QuantumultX/Rules/AI.list|Repcz" )
RULES+=( "QuantumultX/Rules/PayPal.list|${BLACKMATRIX_BASE}/QuantumultX/PayPal/PayPal.list|blackmatrix7" )
RULES+=( "QuantumultX/Rules/Netflix.list|${REPCZ_BASE}/QuantumultX/Rules/Netflix.list|Repcz" )
RULES+=( "QuantumultX/Rules/Telegram.list|${REPCZ_BASE}/QuantumultX/Rules/Telegram.list|Repcz" )
RULES+=( "QuantumultX/Rules/Twitter.list|${REPCZ_BASE}/QuantumultX/Rules/Twitter.list|Repcz" )
RULES+=( "QuantumultX/Rules/Instagram.list|${REPCZ_BASE}/QuantumultX/Rules/Instagram.list|Repcz" )
RULES+=( "QuantumultX/Rules/TikTok.list|${REPCZ_BASE}/QuantumultX/Rules/TikTok.list|Repcz" )
RULES+=( "QuantumultX/Rules/Steam.list|${REPCZ_BASE}/QuantumultX/Rules/Steam.list|Repcz" )
RULES+=( "QuantumultX/Rules/Epic.list|${REPCZ_BASE}/QuantumultX/Rules/Epic.list|Repcz" )
RULES+=( "QuantumultX/Rules/YouTube.list|${REPCZ_BASE}/QuantumultX/Rules/YouTube.list|Repcz" )
RULES+=( "QuantumultX/Rules/Google.list|${REPCZ_BASE}/QuantumultX/Rules/Google.list|Repcz" )
RULES+=( "QuantumultX/Rules/Github.list|${REPCZ_BASE}/QuantumultX/Rules/Github.list|Repcz" )
RULES+=( "QuantumultX/Rules/OneDrive.list|${REPCZ_BASE}/QuantumultX/Rules/OneDrive.list|Repcz" )
RULES+=( "QuantumultX/Rules/Microsoft.list|${REPCZ_BASE}/QuantumultX/Rules/Microsoft.list|Repcz" )
RULES+=( "QuantumultX/Rules/Emby.list|${REPCZ_BASE}/QuantumultX/Rules/Emby.list|Repcz" )
RULES+=( "QuantumultX/Rules/Spotify.list|${REPCZ_BASE}/QuantumultX/Rules/Spotify.list|Repcz" )
RULES+=( "QuantumultX/Rules/Bahamut.list|${REPCZ_BASE}/QuantumultX/Rules/Bahamut.list|Repcz" )
RULES+=( "QuantumultX/Rules/Disney.list|${REPCZ_BASE}/QuantumultX/Rules/Disney.list|Repcz" )
RULES+=( "QuantumultX/Rules/PrimeVideo.list|${REPCZ_BASE}/QuantumultX/Rules/PrimeVideo.list|Repcz" )
RULES+=( "QuantumultX/Rules/HBO.list|${REPCZ_BASE}/QuantumultX/Rules/HBO.list|Repcz" )
RULES+=( "QuantumultX/Rules/Proxy.list|${REPCZ_BASE}/QuantumultX/Rules/Proxy.list|Repcz" )
RULES+=( "QuantumultX/Rules/AppleCN.list|${REPCZ_BASE}/QuantumultX/Rules/AppleCN.list|Repcz" )
RULES+=( "QuantumultX/Rules/AppleServers.list|${REPCZ_BASE}/QuantumultX/Rules/AppleServers.list|Repcz" )

# ----------------- Clash Rules -----------------
RULES+=( "Clash/Meta/Rules/Direct.list|${REPCZ_BASE}/mihomo/Rules/Direct.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Ads_SukkaW.list|${REPCZ_BASE}/mihomo/Rules/Ads_SukkaW.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Reject.list|${REPCZ_BASE}/mihomo/Rules/Reject.list|Repcz" )
RULES+=( "Clash/Meta/Rules/AI.list|${REPCZ_BASE}/mihomo/Rules/AI.list|Repcz" )
RULES+=( "Clash/Meta/Rules/PayPal.list|${BLACKMATRIX_BASE}/Clash/PayPal/PayPal.list|blackmatrix7" )
RULES+=( "Clash/Meta/Rules/Netflix.list|${REPCZ_BASE}/mihomo/Rules/Netflix.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Telegram.list|${REPCZ_BASE}/mihomo/Rules/Telegram.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Twitter.list|${REPCZ_BASE}/mihomo/Rules/Twitter.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Instagram.list|${REPCZ_BASE}/mihomo/Rules/Instagram.list|Repcz" )
RULES+=( "Clash/Meta/Rules/TikTok.list|${REPCZ_BASE}/mihomo/Rules/TikTok.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Steam.list|${REPCZ_BASE}/mihomo/Rules/Steam.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Epic.list|${REPCZ_BASE}/mihomo/Rules/Epic.list|Repcz" )
RULES+=( "Clash/Meta/Rules/YouTube.list|${REPCZ_BASE}/mihomo/Rules/YouTube.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Google.list|${REPCZ_BASE}/mihomo/Rules/Google.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Github.list|${REPCZ_BASE}/mihomo/Rules/Github.list|Repcz" )
RULES+=( "Clash/Meta/Rules/OneDrive.list|${REPCZ_BASE}/mihomo/Rules/OneDrive.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Microsoft.list|${REPCZ_BASE}/mihomo/Rules/Microsoft.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Emby.list|${REPCZ_BASE}/mihomo/Rules/Emby.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Spotify.list|${REPCZ_BASE}/mihomo/Rules/Spotify.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Bahamut.list|${REPCZ_BASE}/mihomo/Rules/Bahamut.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Disney.list|${REPCZ_BASE}/mihomo/Rules/Disney.list|Repcz" )
RULES+=( "Clash/Meta/Rules/PrimeVideo.list|${REPCZ_BASE}/mihomo/Rules/PrimeVideo.list|Repcz" )
RULES+=( "Clash/Meta/Rules/HBO.list|${REPCZ_BASE}/mihomo/Rules/HBO.list|Repcz" )
RULES+=( "Clash/Meta/Rules/Proxy.list|${REPCZ_BASE}/mihomo/Rules/Proxy.list|Repcz" )
RULES+=( "Clash/Meta/Rules/AppleCN.list|${REPCZ_BASE}/mihomo/Rules/AppleCN.list|Repcz" )
RULES+=( "Clash/Meta/Rules/AppleServers.list|${REPCZ_BASE}/mihomo/Rules/AppleServers.list|Repcz" )

# ----------------- Shadowrocket Rules -----------------
RULES+=( "Shadowrocket/Rules/Direct.list|${REPCZ_BASE}/Surge/Rules/Direct.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Ads_SukkaW.list|${REPCZ_BASE}/Surge/Rules/Ads_SukkaW.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Reject.list|${REPCZ_BASE}/Surge/Rules/Reject.list|Repcz" )
RULES+=( "Shadowrocket/Rules/AI.list|${REPCZ_BASE}/Surge/Rules/AI.list|Repcz" )
RULES+=( "Shadowrocket/Rules/PayPal.list|${BLACKMATRIX_BASE}/Surge/PayPal/PayPal.list|blackmatrix7" )
RULES+=( "Shadowrocket/Rules/Netflix.list|${REPCZ_BASE}/Surge/Rules/Netflix.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Telegram.list|${REPCZ_BASE}/Surge/Rules/Telegram.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Twitter.list|${REPCZ_BASE}/Surge/Rules/Twitter.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Instagram.list|${REPCZ_BASE}/Surge/Rules/Instagram.list|Repcz" )
RULES+=( "Shadowrocket/Rules/TikTok.list|${REPCZ_BASE}/Surge/Rules/TikTok.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Steam.list|${REPCZ_BASE}/Surge/Rules/Steam.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Epic.list|${REPCZ_BASE}/Surge/Rules/Epic.list|Repcz" )
RULES+=( "Shadowrocket/Rules/YouTube.list|${REPCZ_BASE}/Surge/Rules/YouTube.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Google.list|${REPCZ_BASE}/Surge/Rules/Google.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Github.list|${REPCZ_BASE}/Surge/Rules/Github.list|Repcz" )
RULES+=( "Shadowrocket/Rules/OneDrive.list|${REPCZ_BASE}/Surge/Rules/OneDrive.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Microsoft.list|${REPCZ_BASE}/Surge/Rules/Microsoft.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Emby.list|${REPCZ_BASE}/Surge/Rules/Emby.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Spotify.list|${REPCZ_BASE}/Surge/Rules/Spotify.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Bahamut.list|${REPCZ_BASE}/Surge/Rules/Bahamut.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Disney.list|${REPCZ_BASE}/Surge/Rules/Disney.list|Repcz" )
RULES+=( "Shadowrocket/Rules/PrimeVideo.list|${REPCZ_BASE}/Surge/Rules/PrimeVideo.list|Repcz" )
RULES+=( "Shadowrocket/Rules/HBO.list|${REPCZ_BASE}/Surge/Rules/HBO.list|Repcz" )
RULES+=( "Shadowrocket/Rules/Proxy.list|${REPCZ_BASE}/Surge/Rules/Proxy.list|Repcz" )
RULES+=( "Shadowrocket/Rules/AppleCN.list|${REPCZ_BASE}/Surge/Rules/AppleCN.list|Repcz" )
RULES+=( "Shadowrocket/Rules/AppleServers.list|${REPCZ_BASE}/Surge/Rules/AppleServers.list|Repcz" )

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
    SOURCE="blackmatrix7/${upstream_name}"
}

count_rule_lines() {
    awk 'BEGIN{n=0} /^[[:space:]]*($|#|;|\/\/)/{next} {n++} END{print n}' "$1"
}

# ================= Main Sync Loop =================

SYNC_TIME="$(date '+%Y-%m-%d %H:%M:%S %Z')"
COUNT_SUCCESS=0
COUNT_SKIP=0
COUNT_FAIL=0

for rule in "${RULES[@]}"; do
    # 解析规则项
    IFS='|' read -r LOCAL_PATH REMOTE_URL SOURCE <<< "$rule"
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

        RULE_LINE_COUNT=$(count_rule_lines "$TEMP_FILE")
        if [ "$RULE_LINE_COUNT" -lt "$MIN_RULE_LINES" ]; then
            echo "❌ FAILED (Only $RULE_LINE_COUNT rule line(s), below minimum $MIN_RULE_LINES)"
            COUNT_FAIL=$((COUNT_FAIL+1))
            rm -f "$TEMP_FILE"
            continue
        fi

        # 判断是否和本地内容一致（跳过 6 行自定义 header）
        if [ -f "$FULL_LOCAL_PATH" ]; then
            # 如果本地文件存在，跳过本地前六行和下载内容的比较
            # (假设外部规则本身没有我们的特定 header，如果有可以用更精确的 diff)
            if tail -n +7 "$FULL_LOCAL_PATH" | cmp -s - "$TEMP_FILE"; then
                echo "⏭️  SKIP (No changes)"
                COUNT_SKIP=$((COUNT_SKIP+1))
                rm "$TEMP_FILE"
                continue
            fi
        fi

        # 写入新文件（带 Header）
        {
            echo "# ============================================"
            echo "# @SyncFrom    $SOURCE"
            echo "# @SyncTime    $SYNC_TIME"
            echo "# @LocalPath   $LOCAL_PATH"
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
