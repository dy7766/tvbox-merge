# TVBox 多源自动合并与缓存降级仓

本项目自动抓取并物理合并 **饭太硬** 与 **摸鱼儿** 的 TVBox 订阅源，并内置 **范明明超清 IPv6 央视卫视直播**，具备**网络失效自动缓存兜底**与**多源爬虫隔离**特性。

---

## 📺 方案一：主打单仓（推荐！饭太硬+摸鱼儿 物理合并）

在 TVBox 中填入以下任一高速地址（国内直接秒开）：

### 🚀 推荐高速地址 1（国内专用高可用镜像，推荐首选）
```text
https://jsd.cdn.zzko.cn/gh/dy7766/tvbox-merge@main/merged.json
```

### 🚀 推荐高速地址 2（GitHub Pages 官方直接托管）
```text
https://dy7766.github.io/tvbox-merge/merged.json
```

### 备用高速地址 3（Cloudflare 全球边缘节点）
```text
https://testingcf.jsdelivr.net/gh/dy7766/tvbox-merge@main/merged.json
```

### 备用高速地址 4（Fastly 节点）
```text
https://fastly.jsdelivr.net/gh/dy7766/tvbox-merge@main/merged.json
```

---

## 📺 方案二：多仓模式（可一键切换 高天流云）

在 TVBox 中填入此地址，可以在电视设置的线路切换列表里自由切换：
- 🚀 **饭太硬+摸鱼儿（合并线）**
- ☁️ **高天流云（原版独立线）**

```text
https://jsd.cdn.zzko.cn/gh/dy7766/tvbox-merge@main/index.json
```
*(备用：`https://dy7766.github.io/tvbox-merge/index.json`)*

---

## ⚡ 特性说明

1. **饭太硬 + 摸鱼儿 物理合并**：共 **145 个核心站点** + **8 组直播线路**。
2. **爬虫包专属隔离**：为每个站点绑定专属 `spider.jar`，彻底杜绝不同源之间的爬虫互相冲突。
3. **失效缓存兜底**：GitHub Actions 每天自动抓取一次（仍支持在网页上手动立即更新）。若任何上游宕机或报 502，自动回退使用最近一次成功的配置，电视端永不断流。
