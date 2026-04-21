# Zotero PDF 导出工具

从 Zotero 按集合分类导出 PDF 文件的工具。

## 版本升级历史

### v2.1 (2024-当前) - 自动检测增强版
- 支持从 Windows 注册表自动检测 Zotero 路径
- 智能搜索多版本 Zotero (Zotero 6+ Profiles 结构)
- 优先使用配置文件，如无则自动检测
- 修复变量作用域问题
- 默认导出到桌面 `Zotero_PDF_Export` 文件夹

### v2.0 (2024) - 一键 Exe 版
- 打包成 EXE 可执行文件，双击即可运行
- 无需安装 Python 环境
- 支持 Windows/macOS/Linux

### v1.5 (2024) - 分类导出版
- 按集合分类导出，保留 Zotero 原有的分类逻辑
- 支持未分类文献单独导出

### v1.0 (2024) - 基础版
- 从 Zotero 提取 PDF 并用标题重命名
- 平铺导出到单一目录

---

## 版本说明

### 🎯 EXE 版本（推荐）
- 位置: `dist/ZoteroPDF导出工具/`
- 使用: 双击 `ZoteroPDF导出工具.exe` 即可运行
- 无需安装 Python 环境

### 🐍 Python 版本
- 位置: 根目录
- 文件:
  - `export_zotero_pdfs.py` - 主程序
  - `export_zotero_pdfs_standalone.py` - 独立版（推荐）
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
- ✅ 自动检测 Zotero 数据目录

## 注意事项
- 运行前请先关闭 Zotero（数据库锁定）
- 如遇问题，检查 config.py 中的路径配置