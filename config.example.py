# -*- coding: utf-8 -*-
"""
Zotero PDF 导出工具 - 配置文件示例

将此文件复制为 config.py 并修改配置：
1. 运行程序后会自动检测 Zotero 目录
2. 如需自定义，请修改以下配置：
"""

# ==================== Zotero 数据目录 ====================
# 大多数情况下程序会自动检测，无需手动设置
ZOTERO_DATA_PATH = r'C:\Users\YourUser\AppData\Roaming\Zotero\Profiles\xxxx.default'

# ==================== 输出目录 ====================
 OUTPUT_DIR = r'C:\Users\YourUser\Desktop\My Exported PDFs'

# ==================== 导出策略 ====================
# 'by_collection' - 按集合分类导出
# 'all_flat'      - 全部平铺到同一目录
EXPORT_STRATEGY = 'by_collection'

# ==================== 命名模式 ====================
# 'title' - 使用文献标题
# 'key'   - 使用 Zotero key + 标题
EXPORT_MODE = 'title'