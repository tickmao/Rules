# Tickmao Rules

本项目是经过重构的代理工具统一样板规则库，支持 **Surge, Loon, QuantumultX, Clash Meta, Shadowrocket** 等主流代理客户端。

所有配置文件均以 `Tickmao` 为核心维护，内置了一套结构化、统一命名的策略组，并且拥有统一的上游规则聚合与同步机制。

## 🗂 目录结构

```text
.
├── Surge/            # Surge 配置及模块
├── Loon/             # Loon 配置及插件引用
├── QuantumultX/      # QX 配置及规则
├── Clash/Meta/       # Clash Meta 专属配置
├── Shadowrocket/     # Shadowrocket 配置
├── scripts/          # 用于自动化同步上游规则的脚本
└── .github/          # GitHub Actions 自动化工作流
```

## 🚀 一键导入链接

如果您想直接使用默认的配置框架，可以长按复制以下链接，进入对应客户端下载（配置中已映射好最新的自托管规则）。

> **⚠️ 注意：** 导入后请修改配置内的 `[Proxy]` / `[Proxy Group]` 组为您自己的实际节点。建议 Fork 本仓库后，将以下链接中的 `tickmao` 替换为您的 GitHub 用户名，以实现完全自托管。

- **Surge**:
  `https://raw.githubusercontent.com/tickmao/Rules/master/Surge/Surge.conf`

- **Loon**:
  `https://raw.githubusercontent.com/tickmao/Rules/master/Loon/Loon.conf`

- **Quantumult X**:
  `https://raw.githubusercontent.com/tickmao/Rules/master/QuantumultX/QuantumultX.conf`

- **Clash Verge Rev / Meta**:
  `https://raw.githubusercontent.com/tickmao/Rules/master/Clash/Meta/Clash.yml`

- **Shadowrocket**:
  `https://raw.githubusercontent.com/tickmao/Rules/master/Shadowrocket/Shadowrocket.conf`

## 🧩 策略组命名规范

为了保证您在客户端之间随意切换也能拥有相同的体验与肌肉记忆，本项目采用标准统一的英文策略组命名体系：

| 策略组名称         | 推荐底层策略    | 说明                                                           |
| :----------------- | :-------------- | :------------------------------------------------------------- |
| **Proxy**          | Select          | 手动指定节点（推荐默认此项），管理所有需要走代理的基础流量。   |
| **Outside**        | Select / Proxy  | 匹配未被明确规则命中，但被判定为国外服务的流量（防漏网之鱼）。 |
| **Mainland**       | Select / DIRECT | 发往中国大陆被直连匹配的流量。                                 |
| **Apple**          | Select / DIRECT | Apple 服务相关流量（视是否代理可指定 DIRECT 或 Proxy）。       |
| **Microsoft**      | Select / Proxy  | 微软相关服务（OneDrive / GitHub 等）。                         |
| **Google**         | Select / Proxy  | 谷歌相关服务（YouTube / 搜索等）。                             |
| **Gmedia**         | Select / Proxy  | 国际流媒体（Netflix / Disney+ / HBO 等）。                     |
| **Telegram**       | Select / Proxy  | 电报相关服务，可分配专用高连通性节点。                         |
| **Social**         | Select / Proxy  | 其他国际社交媒体（Twitter / Instagram 等）。                   |
| **AI**             | Select / Proxy  | ChatGPT / Claude 等新锐 AI 大语言模型专用组。                  |
| **Game**           | Select / Proxy  | 游戏特化组（Steam / Epic 等）。                                |
| **Emby / Spotify** | Select / Proxy  | 私人影音与音乐专属组。                                         |
| **PayPal**         | Select / Proxy  | PayPal 等需要锁定 IP 或固定节点的高风控金融支付类服务。        |
| **NoAuto**         | Select / DIRECT | 最终的 Final 兜底规则，视您的全局倾向而定。                    |

## 🤖 自动化规则同步

本项目搭载了 `sync_rules.sh` 脚本与 GitHub Actions，可以在每天的北京时间 `12:00` 自动从以下优质防广告与分流项目同步最新的 `.list` 碎片：

- [Repcz/Tool](https://github.com/Repcz/Tool)
- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)

所有碎片将以原生格式生成在各个客户端的目录中，并带有 `SyncFrom` 表头供查验。

## ✅ 同步后校验（推荐）

建议每次同步后执行以下命令，先做语法与一致性检查再发布：

```bash
python3 scripts/rebuild_core.py
python3 scripts/validate_yaml.py
python3 scripts/check_consistency.py --strict-order
```

也可以直接运行同步脚本，脚本末尾会自动执行一致性检查：

```bash
bash scripts/sync_rules.sh
```

### 一致性检查覆盖项

- 配置中引用的远程规则文件是否在仓库中存在对应本地文件
- 各客户端 `RULE-SET` / `policy` / `force-policy` 是否引用了已定义策略组
- Shadowrocket `update-url` 是否指向仓库内真实存在文件
- Clash `rule-providers` 的本地路径与远程规则名是否一致（警告级）
- 核心分流段（受 marker 保护）的规则顺序是否和 Surge 语义顺序一致

## 📖 免责声明

在此项目中涉及的任何脚本、配置或规则，仅用于测试和学习研究。本项目不保证其合法性、准确性、完整性和有效性，请根据本地法律法规自行判断。项目中所有的内容绝不应用于任何商业或非法目的；否则后果自负。
