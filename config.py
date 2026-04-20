# -*- coding: utf-8 -*-
"""
Zotero PDF 导出工具 - 配置文件

直接双击 EXE 运行通常会自动查找数据库，
如需自定义，请修改以下配置：
"""

# ==================== Zotero 数据目录 ====================
ZOTERO_DATA_PATH = r'D:\Zotero Data'

# ==================== 输出目录 ====================
OUTPUT_DIR = r'E:\1 博士进程\1 进程推进（初步理解中）\0 临时\my_exported_pdfs'

# ==================== 导出策略 ====================
# 'by_collection' - 按集合分类导出
# 'all_flat'      - 全部平铺
EXPORT_STRATEGY = 'by_collection'

# ==================== 命名模式 ====================
# 'title' - 使用文献标题
# 'key'   - 使用 Zotero key + 标题
EXPORT_MODE = 'title'

# ==================== 说明 ====================
# 1. 修改配置后保存
# 2. 双击运行 ZoteroPDF导出工具.exe
# 3. 运行前请先关闭 Zotero