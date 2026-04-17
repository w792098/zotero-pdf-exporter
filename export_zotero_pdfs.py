#!/usr/bin/env python3
"""
Zotero PDF 导出工具
从 Zotero 数据库提取 PDF 文献并按标题重命名

使用方法:
    python export_zotero_pdfs.py

配置说明:
    编辑同目录下的 config.py 文件修改设置
"""

import os
import sqlite3
import shutil
import re
from pathlib import Path

# 导入配置
from config import ZOTERO_DATA_PATH, OUTPUT_DIR, EXPORT_MODE


def find_zotero_db():
    """自动查找 Zotero 数据库"""
    possible_paths = [
        os.path.join(ZOTERO_DATA_PATH, 'zotero.sqlite'),
        os.path.join(ZOTERO_DATA_PATH, 'storage', 'zotero.sqlite'),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # 尝试在 Zotero Data 目录下搜索
    if os.path.isdir(ZOTERO_DATA_PATH):
        for root, dirs, files in os.walk(ZOTERO_DATA_PATH):
            if 'zotero.sqlite' in files:
                return os.path.join(root, 'zotero.sqlite')

    return None


def find_storage_dir():
    """自动查找 Zotero storage 目录"""
    storage_path = os.path.join(ZOTERO_DATA_PATH, 'storage')
    if os.path.isdir(storage_path):
        return storage_path
    return None


def get_pdf_items(cursor):
    """获取所有 PDF 附件信息"""
    query = """
        SELECT
            a.itemID,
            v.value as title,
            a.path,
            i.key as item_key
        FROM itemAttachments a
        JOIN items i ON a.itemID = i.itemID
        LEFT JOIN itemData d ON i.itemID = d.itemID AND d.fieldID = 1
        LEFT JOIN itemDataValues v ON d.valueID = v.valueID
        WHERE a.contentType = 'application/pdf'
    """
    cursor.execute(query)
    return cursor.fetchall()


def find_pdf_file(storage_dir, path):
    """在 storage 目录中查找 PDF 文件"""
    if not path or not path.startswith('storage:'):
        return None

    filename = path.replace('storage:', '')

    # 遍历 storage 下的所有文件夹
    for folder in os.listdir(storage_dir):
        folder_path = os.path.join(storage_dir, folder)
        if os.path.isdir(folder_path):
            # 直接匹配
            if filename in os.listdir(folder_path):
                return os.path.join(folder_path, filename)
            # 模糊匹配（处理编码问题）
            for f in os.listdir(folder_path):
                if f.endswith('.pdf'):
                    # 尝试匹配文件名核心部分
                    if filename.replace('.pdf', '').replace('-', '').replace('_', '') in f.replace('.pdf', '').replace('-', '').replace('_', ''):
                        return os.path.join(folder_path, f)

    return None


def clean_filename(title, item_id):
    """清理文件名，生成安全的文件名前"""
    if not title or title.strip() == '':
        title = f'untitled_{item_id}'

    # 移除 Windows/macOS/Linux 不兼容的字符
    safe = re.sub(r'[<>:"|?*\\/\x00-\x1f]', '', title)
    safe = safe.strip()
    safe = re.sub(r'\s+', ' ', safe)  # 多个空格合并为一个

    # 限制长度
    if len(safe) > 180:
        safe = safe[:180]

    return safe


def export_pdfs():
    """执行 PDF 导出"""
    print("=" * 50)
    print("Zotero PDF 导出工具")
    print("=" * 50)

    # 查找数据库
    print(f"\n[1] 查找 Zotero 数据库: {ZOTERO_DATA_PATH}")
    db_path = find_zotero_db()

    if not db_path:
        print("错误: 无法找到 zotero.sqlite 数据库")
        print("请检查 config.py 中的 ZOTERO_DATA_PATH 设置")
        return False

    print(f"    找到数据库: {db_path}")

    # 查找 storage 目录
    storage_dir = find_storage_dir()
    if not storage_dir:
        print("错误: 无法找到 storage 目录")
        return False

    print(f"    找到存储目录: {storage_dir}")

    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\n[2] 输出目录: {OUTPUT_DIR}")

    # 连接数据库
    try:
        conn = sqlite3.connect(db_path, timeout=30)
        cursor = conn.cursor()
    except sqlite3.OperationalError as e:
        print(f"错误: 数据库被锁定 - {e}")
        print("请先关闭 Zotero 后再运行此脚本")
        return False

    # 获取 PDF 列表
    print("\n[3] 读取文献数据...")
    items = get_pdf_items(cursor)
    print(f"    找到 {len(items)} 个 PDF 附件")

    if EXPORT_MODE == 'title':
        # 模式1: 使用标题命名
        success_count = 0
        for item_id, title, path, item_key in items:
            if not path:
                continue

            pdf_path = find_pdf_file(storage_dir, path)
            if pdf_path and os.path.exists(pdf_path):
                safe_title = clean_filename(title, item_id)
                dest_path = os.path.join(OUTPUT_DIR, f'{safe_title}.pdf')

                # 处理重名
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(OUTPUT_DIR, f'{safe_title}_{counter}.pdf')
                    counter += 1

                try:
                    shutil.copy2(pdf_path, dest_path)
                    success_count += 1
                    print(f"    [OK] {safe_title}.pdf")
                except Exception as e:
                    print(f"    [X] 复制失败: {e}")

        conn.close()
        print(f"\n[完成] 成功导出 {success_count} 个 PDF 文件")

    elif EXPORT_MODE == 'key':
        # 模式2: 使用 Zotero key 命名（更可靠）
        success_count = 0
        for item_id, title, path, item_key in items:
            if not path:
                continue

            pdf_path = find_pdf_file(storage_dir, path)
            if pdf_path and os.path.exists(pdf_path):
                # 使用 key + 标题
                display_name = title if title and title.strip() else f'item_{item_id}'
                safe_title = clean_filename(display_name, item_id)
                dest_path = os.path.join(OUTPUT_DIR, f'{item_key}_{safe_title}.pdf')

                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(OUTPUT_DIR, f'{item_key}_{safe_title}_{counter}.pdf')
                    counter += 1

                try:
                    shutil.copy2(pdf_path, dest_path)
                    success_count += 1
                    print(f"    [OK] {item_key}_{safe_title[:30]}...")
                except Exception as e:
                    print(f"    [X] 复制失败: {e}")

        conn.close()
        print(f"\n[完成] 成功导出 {success_count} 个 PDF 文件")

    return True


if __name__ == '__main__':
    export_pdfs()