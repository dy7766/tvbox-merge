# TVBox 多源自动合并与缓存降级仓

本项目自动抓取并物理合并 **饭太硬**、**摸鱼儿** 与 **高天流云** 的 TVBox 订阅源，并内置 **范明明超清 IPv6 央视卫视直播**，具备**网络失效自动缓存兜底**与**多源爬虫隔离**特性。

## 📺 TVBox / 影视仓 订阅地址

在电视 TVBox 设置中直接填入以下地址（无需修改，开箱即用）：

### 🚀 推荐高速地址（全球 CDN 直连，稳定秒开）
```text
https://cdn.jsdelivr.net/gh/dy7766/tvbox-merge@main/merged.json
```

### 备用加速地址
```text
https://raw.gitmirror.com/dy7766/tvbox-merge/main/merged.json
```
```text
https://ghproxy.net/https://raw.githubusercontent.com/dy7766/tvbox-merge/main/merged.json
```

---

## ⚡ 特性与合并内容

1. **三源物理合并**：
   - 🍚 **[饭] 饭太硬**：经典老牌主线，全能影视与云盘。
   - 🐟 **[摸] 摸鱼儿**：B站精选、少儿专区、新片预告。
   - ☁️ **[高] 高天流云**：GitHub 顶级开源 JS/drpy 纯净线路，无广告秒播。
   - 📺 **范明明超清直播**：置顶央视 4K/8K、全国卫视 IPv6 高清直播。
2. **海量站点与直播**：当前全量合并已包含 **442 个点播站点** + **10 组直播线路**。
3. **爬虫包专属隔离**：为每个站点绑定其源专属的 `spider.jar`，彻底杜绝不同源之间的爬虫互相冲突。
4. **失效缓存兜底**：GitHub Actions 每 3 小时自动抓取一次。若任何上游宕机或报 502，自动回退使用最近一次成功的配置，电视端永不断流。
