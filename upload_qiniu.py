# -*- coding: utf-8 -*-
"""
七牛云 Kodo 自动上传脚本
- 读取环境变量 QINIU_AK, QINIU_SK, QINIU_BUCKET
- 自动将 merged.json 与 index.json 同步到七牛云存储桶根目录
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
        from qiniu import Auth, put_file
    except ImportError:
        print("[Qiniu] 缺少 qiniu 模块，请先运行: pip install qiniu")
        sys.exit(1)

    q = Auth(ak, sk)
    files_to_upload = ["merged.json", "index.json"]

    for file_name in files_to_upload:
        if not os.path.exists(file_name):
            print(f"[Qiniu] 文件未找到: {file_name}，跳过")
            continue

        key = file_name
        # 允许覆盖上传（覆盖已有的同名配置）
        token = q.upload_token(bucket_name, key, 3600)
        
        print(f"[Qiniu] 正在上传 {file_name} 到存储桶 [{bucket_name}] ...")
        ret, info = put_file(token, key, file_name)

        if info.status_code == 200:
            print(f"[Qiniu] ✓ {file_name} 上传成功！hash: {ret.get('hash')}")
        else:
            print(f"[Qiniu] ✗ {file_name} 上传失败: {info}")

if __name__ == "__main__":
    upload_to_qiniu()
