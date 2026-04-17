# -*- coding: utf-8 -*-
"""
Zotero PDF 导出工具 - 配置文件

请根据你的实际情况修改以下配置
"""

# ==================== Zotero 数据目录 ====================
# 这里填写你的 Zotero 数据存放目录
# Windows 示例: r'C:\Users\你的用户名\Zotero' 或 r'D:\Zotero Data'
# macOS 示例: r'/Users/你的用户名/Zotero'
# Linux 示例: r'/home/你的用户名/Zotero'

# Windows 用户 - 根据你的实际路径修改
ZOTERO_DATA_PATH = r'D:\Zotero Data'

# ==================== 输出目录 ====================
# 导出后的 PDF 存放位置
OUTPUT_DIR = r'E:\1 博士进程\1 进程推进（初步理解中）\0 临时\my_exported_pdfs'

# ==================== 导出模式 ====================
# 'title' - 使用文献标题命名文件
# 'key'   - 使用 Zotero key + 标题命名（更可靠，避免重名）
EXPORT_MODE = 'title'

# ==================== 说明 ====================
# 1. Windows 用户: 确保 Zotero 已关闭后再运行
# 2. 首次使用请先修改 ZOTERO_DATA_PATH 为你的 Zotero 数据目录
# 3. 运行命令: python export_zotero_pdfs.py
# 4. 需要 Python 3.6+ 环境