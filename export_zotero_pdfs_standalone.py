#!/usr/bin/env python3
"""
Zotero PDF 导出工具 - 独立版（可打包为 EXE）
按集合分类导出 PDF

使用方法:
    双击运行或: python export_zotero_pdfs_standalone.py
"""

import os
import sys
import sqlite3
import shutil
import re

# ==================== 配置区域（修改这里） ====================
# Windows 用户
ZOTERO_DATA_PATH = r'D:\Zotero Data'
OUTPUT_DIR = r'E:\1 博士进程\1 进程推进（初步理解中）\0 临时\my_exported_pdfs'

# 导出策略: 'by_collection' 按集合分类, 'all_flat' 平铺
EXPORT_STRATEGY = 'by_collection'

# 命名模式: 'title' 标题, 'key' Key+标题
EXPORT_MODE = 'title'
# ============================================================


# 检查是否为打包后的 exe
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def find_zotero_db():
    """自动查找 Zotero 数据库"""
    possible_paths = [
        os.path.join(ZOTERO_DATA_PATH, 'zotero.sqlite'),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    if os.path.isdir(ZOTERO_DATA_PATH):
        for root, dirs, files in os.walk(ZOTERO_DATA_PATH):
            if 'zotero.sqlite' in files:
                return os.path.join(root, 'zotero.sqlite')
    return None


def find_storage_dir():
    """自动查找 storage 目录"""
    storage_path = os.path.join(ZOTERO_DATA_PATH, 'storage')
    if os.path.isdir(storage_path):
        return storage_path
    return None


def get_collections(cursor):
    """获取所有集合"""
    cursor.execute("""
        SELECT collectionID, collectionName, parentCollectionID
        FROM collections
        WHERE collectionName IS NOT NULL
        ORDER BY parentCollectionID NULLS FIRST, collectionName
    """)
    return {c[0]: {'name': c[1], 'parent': c[2]} for c in cursor.fetchall()}


def get_items_by_collection(cursor):
    """获取每个集合中的 PDF"""
    query = """
        SELECT ci.collectionID, a.itemID, v.value as title, a.path
        FROM itemAttachments a
        JOIN items i ON a.itemID = i.itemID
        LEFT JOIN itemData d ON i.itemID = d.itemID AND d.fieldID = 1
        LEFT JOIN itemDataValues v ON d.valueID = v.valueID
        JOIN collectionItems ci ON i.itemID = ci.itemID
        WHERE a.contentType = 'application/pdf'
    """
    cursor.execute(query)
    result = {}
    for cid, item_id, title, path in cursor.fetchall():
        if cid not in result:
            result[cid] = []
        result[cid].append({'item_id': item_id, 'title': title, 'path': path})
    return result


def get_items_without_collection(cursor):
    """获取未分类的 PDF"""
    query = """
        SELECT a.itemID, v.value as title, a.path
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
    """查找 PDF 文件"""
    if not path or not path.startswith('storage:'):
        return None
    filename = path.replace('storage:', '')
    for folder in os.listdir(storage_dir):
        folder_path = os.path.join(storage_dir, folder)
        if os.path.isdir(folder_path):
            if filename in os.listdir(folder_path):
                return os.path.join(folder_path, filename)
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


def print_info(msg):
    """打印信息（兼容 Windows 控制台）"""
    try:
        print(msg)
    except:
        print(msg.encode('utf-8', errors='ignore').decode('gbk', errors='ignore'))


def main():
    print_info("=" * 50)
    print_info("Zotero PDF 导出工具")
    print_info("=" * 50)

    # 检查配置文件
    config_path = os.path.join(BASE_DIR, 'config.py')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_content = f.read()
                # 尝试读取外部配置
                for line in config_content.split('\n'):
                    if line.startswith('ZOTERO_DATA_PATH'):
                        ZOTERO_DATA_PATH = line.split('=')[1].strip().strip('r"\'')
                    elif line.startswith('OUTPUT_DIR'):
                        OUTPUT_DIR = line.split('=')[1].strip().strip('r"\'')
                    elif line.startswith('EXPORT_STRATEGY'):
                        EXPORT_STRATEGY = line.split('=')[1].strip().strip("'\"")
        except:
            pass

    print_info(f"\n[1] Zotero 目录: {ZOTERO_DATA_PATH}")
    print_info(f"    输出目录: {OUTPUT_DIR}")
    print_info(f"    导出策略: {EXPORT_STRATEGY}")

    db_path = find_zotero_db()
    if not db_path:
        print_info("\n[错误] 找不到 zotero.sqlite")
        print_info("请检查 ZOTERO_DATA_PATH 是否正确！")
        print_info("\n按回车键退出...")
        input()
        return

    print_info(f"    找到数据库: {os.path.basename(db_path)}")

    storage_dir = find_storage_dir()
    if not storage_dir:
        print_info("\n[错误] 找不到 storage 目录")
        print_info("\n按回车键退出...")
        input()
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        conn = sqlite3.connect(db_path, timeout=30)
        conn.text_factory = str
        cursor = conn.cursor()
    except sqlite3.OperationalError as e:
        print_info(f"\n[错误] 数据库被锁定")
        print_info("请先关闭 Zotero 后再运行！")
        print_info("\n按回车键退出...")
        input()
        return

    print_info("\n[2] 读取数据...")
    collections = get_collections(cursor)
    items_by_collection = get_items_by_collection(cursor)
    items_without_collection = get_items_without_collection(cursor)

    print_info(f"    找到 {len(collections)} 个集合")
    total_pdfs = sum(len(v) for v in items_by_collection.values()) + len(items_without_collection)
    print_info(f"    共 {total_pdfs} 个 PDF")

    # 显示集合列表
    print_info("\n[3] 集合列表:")
    for cid, info in collections.items():
        count = len(items_by_collection.get(cid, []))
        prefix = "  " if info['parent'] else ""
        print_info(f"    {prefix}[{cid}] {info['name']} ({count} 个)")

    if items_without_collection:
        print_info(f"    [0] 未分类 ({len(items_without_collection)} 个)")

    print_info("\n[4] 开始导出...")

    if EXPORT_STRATEGY == 'by_collection':
        success_count = 0
        for cid, info in collections.items():
            items = items_by_collection.get(cid, [])
            if not items:
                continue
            folder_name = clean_filename(info['name'], cid)
            collection_dir = os.path.join(OUTPUT_DIR, folder_name)
            os.makedirs(collection_dir, exist_ok=True)

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
                    except:
                        pass

            if len(items) > 0:
                print_info(f"    [OK] {info['name']}: {len(items)} 个")

        # 未分类
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
            print_info(f"    [OK] 未分类: {len(items_without_collection)} 个")

        conn.close()
        print_info(f"\n[完成] 成功导出 {success_count} 个 PDF")
        print_info(f"       保存至: {OUTPUT_DIR}")

    else:
        # all_flat 模式
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
                except:
                    pass

        conn.close()
        print_info(f"\n[完成] 成功导出 {success_count} 个 PDF")

    print_info("\n按回车键退出...")
    try:
        input()
    except:
        pass


if __name__ == '__main__':
    main()