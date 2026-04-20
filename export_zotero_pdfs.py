#!/usr/bin/env python3
"""
Zotero PDF 导出工具 - 按集合分类导出
支持按 Zotero 集合（Collection）自动归类文件

使用方法:
    python export_zotero_pdfs.py
"""

import os
import sqlite3
import shutil
import re
from pathlib import Path

# 导入配置
from config import ZOTERO_DATA_PATH, OUTPUT_DIR, EXPORT_MODE, EXPORT_STRATEGY


def find_zotero_db():
    """自动查找 Zotero 数据库"""
    possible_paths = [
        os.path.join(ZOTERO_DATA_PATH, 'zotero.sqlite'),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # 递归搜索
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


def get_collections(cursor):
    """获取所有集合及其层级关系"""
    cursor.execute("""
        SELECT collectionID, collectionName, parentCollectionID
        FROM collections
        WHERE collectionName IS NOT NULL
        ORDER BY parentCollectionID NULLS FIRST, collectionName
    """)
    return cursor.fetchall()


def get_items_by_collection(cursor):
    """获取每个集合中的 PDF 附件"""
    # 获取有 PDF 附件的 items 及其所在的集合
    query = """
        SELECT
            ci.collectionID,
            a.itemID,
            v.value as title,
            a.path
        FROM itemAttachments a
        JOIN items i ON a.itemID = i.itemID
        LEFT JOIN itemData d ON i.itemID = d.itemID AND d.fieldID = 1
        LEFT JOIN itemDataValues v ON d.valueID = v.valueID
        JOIN collectionItems ci ON i.itemID = ci.itemID
        WHERE a.contentType = 'application/pdf'
    """
    cursor.execute(query)

    # 按集合分组
    result = {}
    for collection_id, item_id, title, path in cursor.fetchall():
        if collection_id not in result:
            result[collection_id] = []
        result[collection_id].append({
            'item_id': item_id,
            'title': title,
            'path': path
        })

    return result


def get_items_without_collection(cursor):
    """获取不在任何集合中的 PDF 附件"""
    query = """
        SELECT
            a.itemID,
            v.value as title,
            a.path
        FROM itemAttachments a
        JOIN items i ON a.itemID = i.itemID
        LEFT JOIN itemData d ON i.itemID = d.itemID AND d.fieldID = 1
        LEFT JOIN itemDataValues v ON d.valueID = v.valueID
        WHERE a.contentType = 'application/pdf'
        AND a.itemID NOT IN (SELECT itemID FROM collectionItems)
    """
    cursor.execute(query)
    return [{'item_id': r[0], 'title': r[1], 'path': r[2]} for r in cursor.fetchall()]


def find_pdf_file(storage_dir, path):
    """在 storage 目录中查找 PDF 文件"""
    if not path or not path.startswith('storage:'):
        return None

    filename = path.replace('storage:', '')

    for folder in os.listdir(storage_dir):
        folder_path = os.path.join(storage_dir, folder)
        if os.path.isdir(folder_path):
            if filename in os.listdir(folder_path):
                return os.path.join(folder_path, filename)
            # 模糊匹配
            for f in os.listdir(folder_path):
                if f.endswith('.pdf'):
                    if filename.replace('.pdf', '').replace('-', '').replace('_', '') in f.replace('.pdf', '').replace('-', '').replace('_', ''):
                        return os.path.join(folder_path, f)

    return None


def clean_filename(title, item_id):
    """清理文件名"""
    if not title or title.strip() == '':
        title = f'untitled_{item_id}'

    safe = re.sub(r'[<>:"|?*\\/\x00-\x1f]', '', title)
    safe = safe.strip()
    safe = re.sub(r'\s+', ' ', safe)

    if len(safe) > 180:
        safe = safe[:180]

    return safe


def export_pdfs():
    """执行 PDF 导出"""
    print("=" * 50)
    print("Zotero PDF 导出工具 - 按集合分类")
    print("=" * 50)

    # 查找数据库
    print(f"\n[1] 查找 Zotero 数据库: {ZOTERO_DATA_PATH}")
    db_path = find_zotero_db()

    if not db_path:
        print("错误: 无法找到 zotero.sqlite 数据库")
        print("请检查 config.py 中的 ZOTERO_DATA_PATH 设置")
        return False

    print(f"    找到数据库: {db_path}")

    storage_dir = find_storage_dir()
    if not storage_dir:
        print("错误: 无法找到 storage 目录")
        return False

    print(f"    找到存储目录: {storage_dir}")

    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\n[2] 输出目录: {OUTPUT_DIR}")
    print(f"    导出策略: {EXPORT_STRATEGY}")

    try:
        conn = sqlite3.connect(db_path, timeout=30)
        conn.text_factory = str
        cursor = conn.cursor()
    except sqlite3.OperationalError as e:
        print(f"错误: 数据库被锁定 - {e}")
        print("请先关闭 Zotero 后再运行此脚本")
        return False

    # 获取集合信息
    print("\n[3] 读取数据...")
    collections = {c[0]: {'name': c[1], 'parent': c[2]} for c in get_collections(cursor)}
    print(f"    找到 {len(collections)} 个集合")

    items_by_collection = get_items_by_collection(cursor)
    items_without_collection = get_items_without_collection(cursor)

    total_pdfs = sum(len(v) for v in items_by_collection.values()) + len(items_without_collection)
    print(f"    找到 {total_pdfs} 个 PDF 附件")

    # 显示集合列表供选择
    print("\n[4] 集合列表:")
    for cid, info in collections.items():
        count = len(items_by_collection.get(cid, []))
        prefix = "  " if info['parent'] else ""
        print(f"    {prefix}[{cid}] {info['name']} ({count} 个PDF)")

    no_collection_count = len(items_without_collection)
    if no_collection_count > 0:
        print(f"    [0] 未分类 ({no_collection_count} 个PDF)")

    # 执行导出
    print("\n[5] 开始导出...")

    if EXPORT_STRATEGY == 'by_collection':
        # 策略1: 按集合分类导出
        success_count = 0
        collection_stats = {}

        for cid, info in collections.items():
            items = items_by_collection.get(cid, [])
            if not items:
                continue

            # 创建集合文件夹
            folder_name = clean_filename(info['name'], cid)
            collection_dir = os.path.join(OUTPUT_DIR, folder_name)
            os.makedirs(collection_dir, exist_ok=True)

            collection_stats[info['name']] = 0

            for item in items:
                pdf_path = find_pdf_file(storage_dir, item['path'])
                if pdf_path and os.path.exists(pdf_path):
                    safe_title = clean_filename(item['title'], item['item_id'])
                    dest_path = os.path.join(collection_dir, f'{safe_title}.pdf')

                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(collection_dir, f'{safe_title}_{counter}.pdf')
                        counter += 1

                    try:
                        shutil.copy2(pdf_path, dest_path)
                        success_count += 1
                        collection_stats[info['name']] += 1
                    except Exception as e:
                        print(f"        复制失败: {e}")

            if collection_stats[info['name']] > 0:
                print(f"    [OK] {info['name']}: {collection_stats[info['name']]} 个")

        # 处理未分类
        if items_without_collection:
            uncat_dir = os.path.join(OUTPUT_DIR, '未分类')
            os.makedirs(uncat_dir, exist_ok=True)
            for item in items_without_collection:
                pdf_path = find_pdf_file(storage_dir, item['path'])
                if pdf_path and os.path.exists(pdf_path):
                    safe_title = clean_filename(item['title'], item['item_id'])
                    dest_path = os.path.join(uncat_dir, f'{safe_title}.pdf')
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(uncat_dir, f'{safe_title}_{counter}.pdf')
                        counter += 1
                    try:
                        shutil.copy2(pdf_path, dest_path)
                        success_count += 1
                    except:
                        pass
            print(f"    [OK] 未分类: {len(items_without_collection)} 个")

        conn.close()
        print(f"\n[完成] 成功导出 {success_count} 个 PDF 文件")
        print(f"       已按集合分类保存到 {OUTPUT_DIR}")

    elif EXPORT_STRATEGY == 'all_flat':
        # 策略2: 全部平铺导出
        success_count = 0
        all_items = []

        for items in items_by_collection.values():
            all_items.extend(items)
        all_items.extend(items_without_collection)

        for item in all_items:
            pdf_path = find_pdf_file(storage_dir, item['path'])
            if pdf_path and os.path.exists(pdf_path):
                safe_title = clean_filename(item['title'], item['item_id'])
                dest_path = os.path.join(OUTPUT_DIR, f'{safe_title}.pdf')

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

    return True


if __name__ == '__main__':
    export_pdfs()