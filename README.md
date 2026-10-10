# TVBox 多源自动合并与缓存降级仓

本项目自动抓取并合并 **饭太硬** 与 **摸鱼儿** 的 TVBox 订阅源，具备**网络失效自动缓存兜底**与**多源爬虫隔离**特性。

## 📺 TVBox 订阅地址

在 TVBox 或影视仓中直接填入以下任一加速链接：

### 推荐高速地址（国内首选）
```text
https://ghproxy.net/https://raw.githubusercontent.com/dy7766/tvbox-merge/main/merged.json
```

### 备用加速地址
```text
https://ghp.ci/https://raw.githubusercontent.com/dy7766/tvbox-merge/main/merged.json
```

---

## ⚡ 特性说明

1. **自动合并去重**：物理合并各个源的站点（`sites`）、电视直播（`lives`）与解析规则（`parses`）。
2. **专属标识**：站点名称自动带有 `[饭]`、`[摸]` 前缀，方便在搜索时快速区分线路。
3. **爬虫隔离**：为每个站点绑定其源专属的 `spider.jar`，彻底防止不同作者的爬虫包冲突导致“未找到爬虫”。
4. **失效缓存兜底**：GitHub Actions 每 3 小时自动抓取一次。若上游宕机或报 502，自动回退使用最近一次成功的配置，电视端永不断流。
