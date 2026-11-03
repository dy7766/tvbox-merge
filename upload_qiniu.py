# -*- coding: utf-8 -*-
"""
七牛云 Kodo 自动上传与 CDN 刷新脚本
- 读取环境变量 QINIU_AK, QINIU_SK, QINIU_BUCKET
- 自动将 merged.json、index.json 以及 cache/ 下的 spider.jar 同步到七牛云
- 自动调用 CDN 刷新接口，确保电视端立刻获取最新文件
"""

import os
import sys

def upload_to_qiniu():
    ak = os.environ.get("QINIU_AK", "").strip()
    sk = os.environ.get("QINIU_SK", "").strip()
    bucket_name = os.environ.get("QINIU_BUCKET", "").strip()

    if not ak or not sk or not bucket_name:
        print("[Qiniu] 环境变量未完整配置 (QINIU_AK, QINIU_SK, QINIU_BUCKET)，跳过七牛云上传。")
        return

    try:
        from qiniu import Auth, put_file, CdnManager
    except ImportError:
        print("[Qiniu] 缺少 qiniu 模块，请先运行: pip install qiniu")
        sys.exit(1)

    q = Auth(ak, sk)

    # 待上传列表: (本地路径, 七牛存储 key)
    items_to_upload = [
        ("merged.json", "merged.json"),
        ("index.json", "index.json")
    ]

    # 添加专属 spider.jar 爬虫包
    for jar_name in ["fty_spider.jar", "my_spider.jar"]:
        local_path = os.path.join("cache", jar_name)
        if os.path.exists(local_path):
            items_to_upload.append((local_path, f"jar/{jar_name}"))

    uploaded_keys = []
    for local_path, key in items_to_upload:
        if not os.path.exists(local_path):
            print(f"[Qiniu] 文件未找到: {local_path}，跳过")
            continue

        token = q.upload_token(bucket_name, key, 3600)
        print(f"[Qiniu] 正在上传 {local_path} -> [{bucket_name}]:{key} ...")
        ret, info = put_file(token, key, local_path)

        if info.status_code == 200:
            print(f"[Qiniu] [OK] {key} 上传成功！hash: {ret.get('hash')}")
            uploaded_keys.append(key)
        else:
            print(f"[Qiniu] [ERR] {key} 上传失败: {info}")

    # 自动刷新 CDN 缓存，避免客户端拿到旧版
    if uploaded_keys:
        try:
            cdn = CdnManager(q)
            refresh_urls = [f"http://tvm.tenghen.com/{k}" for k in uploaded_keys]
            ret, info = cdn.refresh_urls(refresh_urls)
            print(f"[Qiniu] [OK] CDN 缓存刷新请求已提交 (Code: {ret.get('code')})")
        except Exception as e:
            print(f"[Qiniu] CDN 缓存刷新异常 (非致命): {e}")

if __name__ == "__main__":
    upload_to_qiniu()
