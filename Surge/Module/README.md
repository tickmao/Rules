# Surge Modules 模块仓库

此文件夹用于存放您可以自托管或引用的 Surge 模块 (`.sgmodule`)。

您由于大部分优秀的去广告、重写插件本身维护频率极高（例如去开屏广告），建议不要将全部代码复制到本地，而是通过 Surge UI 直接安装远程模块。针对需要固定版本的模块，可以存放在本目录下。

## 推荐模块引用链接 (请在 Surge 中复制安装)

### 工具类
- **BoxJS** (用于配合本地 Script 管理重写存储):
  `https://raw.githubusercontent.com/chavyleung/scripts/master/box/rewrite/boxjs.rewrite.surge.sgmodule`

- **Sub-Store** (高级订阅管理):
  `https://raw.githubusercontent.com/sub-store-org/Sub-Store/master/config/Surge.sgmodule`

- **Script-Hub** (脚本转换器):
  `https://raw.githubusercontent.com/Script-Hub-Org/Script-Hub/main/Script-Hub.sgmodule`

### 去广告 & 增强
可以参考常用插件维护者的上游：
- app2smile (Spotify解锁等)
- Maasea (YouTube去广告)
- BiliUniverse (B站增强)
- lodepuly / NobyDa 等等

若您需要对模块进行自托管修改，只需将他们的 `.sgmodule` 下载后放入本文件夹，并在 Surge 中使用 `Surge/Module/您的模块名.sgmodule` 的形式进行离线导入。
