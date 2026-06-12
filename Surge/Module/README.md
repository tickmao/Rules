# Surge Module

此目录用于存放需要自托管或固定版本的 Surge 模块。

## 使用建议

- 优先在 Surge 中直接安装上游远程模块，便于及时获得维护者更新。
- 只有在需要固定版本、修改内容或离线引用时，才将 `.sgmodule` 文件放入本目录。
- 新增第三方模块前，确认来源、授权和更新频率；不建议把可随时重新拉取且未修改的模块长期提交到仓库。
- 私有模块、含个人订阅或账号信息的模块不要提交到 GitHub。

## 当前模块

- `BoxJs.sgmodule`: BoxJs 重写模块
- `SubStore.sgmodule`: Sub-Store 订阅管理模块

## 推荐远程引用

```text
https://raw.githubusercontent.com/chavyleung/scripts/master/box/rewrite/boxjs.rewrite.surge.sgmodule
https://raw.githubusercontent.com/sub-store-org/Sub-Store/master/config/Surge.sgmodule
https://raw.githubusercontent.com/Script-Hub-Org/Script-Hub/main/Script-Hub.sgmodule
```

## 更新方式

如需刷新本目录中的固定模块，可运行：

```bash
python3 scripts/fetch_surge_modules.py
```

该脚本会访问上游网络资源，运行前请确认网络环境和下载列表。
