# Zotero PDF 导出工具

从 Zotero 按集合分类导出 PDF 文件的工具。

## 版本说明

### 🎯 EXE 版本（推荐）
- 位置: `dist/ZoteroPDF导出工具/`
- 使用: 双击 `ZoteroPDF导出工具.exe` 即可运行
- 无需安装 Python 环境

### 🐍 Python 版本
- 位置: 根目录
- 文件:
  - `export_zotero_pdfs.py` - 主程序
  - `config.py` - 配置文件
  - `run.bat` - 快速启动脚本
- 需要 Python 3.x 环境

## 使用方法

### EXE 版本
1. 确保 Zotero 已关闭
2. 双击运行 `ZoteroPDF导出工具.exe`
3. 程序会自动检测 Zotero 数据目录

### 配置文件修改
如需自定义，编辑 `dist/ZoteroPDF导出工具/_internal/config.py`:

```python
ZOTERO_DATA_PATH = r'D:\Zotero Data'  # Zotero 数据目录
OUTPUT_DIR = r'E:\输出路径'             # 导出保存位置
EXPORT_STRATEGY = 'by_collection'      # 按集合分类
```

## 功能特性
- ✅ 按 Zotero 集合自动分类导出
- ✅ 智能文件名清理
- ✅ 支持 Windows/macOS/Linux
- ✅ 静默模式（双击即用）

## 注意事项
- 运行前请先关闭 Zotero（数据库锁定）
- 如遇问题，检查 config.py 中的路径配置