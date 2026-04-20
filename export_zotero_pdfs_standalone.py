#!/usr/bin/env python3
"""
Zotero PDF 导出工具 - 独立版（可打包为 EXE）
按集合分类导出 PDF

使用方法:
    双击运行或: python export_zotero_pdfs_standalone.py

首次运行会自动检测 Zotero 数据目录，也可创建 config.py 自定义路径。
"""

import os
import sys
import sqlite3
import shutil
import re

# ==================== 配置区域 ====================
# 优先使用配置文件 config.py 中的设置
# 如未创建配置文件，将自动检测 Zotero 目录

# 导出策略: 'by_collection' 按集合分类, 'all_flat' 平铺
EXPORT_STRATEGY = 'by_collection'

# 命名模式: 'title' 标题, 'key' Key+标题
EXPORT_MODE = 'title'
# ==================================================


# 检查是否为打包后的 exe
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_default_zotero_path():
    """自动检测 Zotero 数据目录"""
    # Zotero 6+ 使用 Profiles 目录结构
    appdata = os.getenv('APPDATA')
    localappdata = os.getenv('LOCALAPPDATA')

    search_paths = []

    # 1. 搜索 %APPDATA%\Zotero\Profiles\
    if appdata:
        profiles_base = os.path.join(appdata, 'Zotero', 'Profiles')
        if os.path.exists(profiles_base):
            for folder in os.listdir(profiles_base):
                profile_path = os.path.join(profiles_base, folder)
                if os.path.isdir(profile_path) and folder.endswith('.default'):
                    # 检查是否是新的 profile 目录结构
                    zotero_data = os.path.join(profile_path, 'zotero')
                    if os.path.isdir(zotero_data):
                        search_paths.append(zotero_data)

    # 2. 搜索 %LOCALAPPDATA%\Zotero\Zotero\Profiles\
    if localappdata:
        profiles_base = os.path.join(localappdata, 'Zotero', 'Zotero', 'Profiles')
        if os.path.exists(profiles_base):
            for folder in os.listdir(profiles_base):
                profile_path = os.path.join(profiles_base, folder)
                if os.path.isdir(profile_path) and folder.endswith('.default'):
                    zotero_data = os.path.join(profile_path, 'zotero')
                    if os.path.isdir(zotero_data):
                        search_paths.append(zotero_data)

    # 3. 传统位置：%APPDATA%\Zotero\
    if appdata:
        legacy_path = os.path.join(appdata, 'Zotero')
        if os.path.isdir(legacy_path):
            search_paths.append(legacy_path)

    # 4. 常见自定义位置
    common_paths = [
        r'D:\Zotero Data',
        r'E:\Zotero Data',
        os.path.join(appdata, '..', 'Local', 'Zotero') if appdata else None,
    ]
    for p in common_paths:
        if p and os.path.isdir(p):
            search_paths.append(p)

    # 遍历搜索路径，查找 zotero.sqlite
    for zotero_path in search_paths:
        db_path = os.path.join(zotero_path, 'zotero.sqlite')
        if os.path.exists(db_path):
            # 验证 storage 目录存在
            storage_path = os.path.join(zotero_path, 'storage')
            if os.path.isdir(storage_path):
                return zotero_path

    return None


def find_zotero_db(zotero_path):
    """查找 Zotero 数据库"""
    db_path = os.path.join(zotero_path, 'zotero.sqlite')
    if os.path.exists(db_path):
        return db_path
    # 递归搜索
    if os.path.isdir(zotero_path):
        for root, dirs, files in os.walk(zotero_path):
            if 'zotero.sqlite' in files:
                return os.path.join(root, 'zotero.sqlite')
    return None


def find_storage_dir(zotero_path):
    """查找 storage 目录"""
    storage_path = os.path.join(zotero_path, 'storage')
    if os.path.isdir(storage_path):
        return storage_path
    # 递归搜索
    if os.path.isdir(zotero_path):
        for root, dirs, files in os.walk(zotero_path):
            if 'storage' in dirs:
                return os.path.join(root, 'storage')
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
    safe = re.sub(r'[\u003c\u003e:""|?*\\/\x00-\x1f]', '', title)
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
    global EXPORT_STRATEGY

    print_info("=" * 50)
    print_info("Zotero PDF 导出工具")
    print_info("=" * 50)

    ZOTERO_DATA_PATH = None
    OUTPUT_DIR = None

    # 检查配置文件
    config_path = os.path.join(BASE_DIR, 'config.py')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_content = f.read()
                for line in config_content.split('\n'):
                    if line.startswith('ZOTERO_DATA_PATH'):
                        ZOTERO_DATA_PATH = line.split('=')[1].strip().strip('r"\'"""')
                    elif line.startswith('OUTPUT_DIR'):
                        OUTPUT_DIR = line.split('=')[1].strip().strip('r"\'"""')
                    elif line.startswith('EXPORT_STRATEGY'):
                        EXPORT_STRATEGY = line.split('=')[1].strip().strip('r"\'"""')
        except:
            pass

    # 自动检测 Zotero 目录（如果未配置）
    if not ZOTERO_DATA_PATH:
        print_info("\n[信息] 正在自动检测 Zotero 数据目录...")
        ZOTERO_DATA_PATH = get_default_zotero_path()
        if ZOTERO_DATA_PATH:
            print_info(f"    自动检测到: {ZOTERO_DATA_PATH}")
        else:
            print_info("\n[错误] 无法自动检测到 Zotero 数据目录")
            print_info("请创建 config.py 文件，设置 ZOTERO_DATA_PATH")
            print_info("\n按回车键退出...")
            input()
            return

    # 默认输出目录：桌面/My Exported PDFs
    if not OUTPUT_DIR:
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop', 'My Exported PDFs')
        OUTPUT_DIR = desktop

    print_info(f"\n[1] Zotero 目录: {ZOTERO_DATA_PATH}")
    print_info(f"    输出目录: {OUTPUT_DIR}")
    print_info(f"    导出策略: {EXPORT_STRATEGY}")

    db_path = find_zotero_db(ZOTERO_DATA_PATH)
    if not db_path:
        print_info("\n[错误] 找不到 zotero.sqlite")
        print_info("请检查 ZOTERO_DATA_PATH 是否正确！")
        print_info("\n按回车键退出...")
        input()
        return

    print_info(f"    找到数据库: {os.path.basename(db_path)}")

    storage_dir = find_storage_dir(ZOTERO_DATA_PATH)
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