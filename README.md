# Zotero PDF 一键导出工具

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue?logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
</p>

从 Zotero 文献库中一键提取所有 PDF 附件，并以文献标题自动重命名，方便整理和备份。

---

## 📋 功能特性

- **一键导出** - 自动扫描 Zotero 数据库中的所有 PDF 附件
- **智能重命名** - 根据文献标题自动命名文件，易于识别和管理
- **跨平台支持** - 兼容 Windows、macOS、Linux 系统
- **轻量简洁** - 仅依赖 Python 标准库，无需额外安装第三方包
- **灵活配置** - 支持自定义 Zotero 数据目录和输出路径

---

## 🚀 快速开始

### 准备工作

确保已安装 **Python 3.6** 或更高版本：

```bash
python --version
```

### 配置步骤

1. 解压项目文件
2. 用任意文本编辑器打开 `config.py`
3. 修改以下配置项：

```python
# Zotero 数据目录（必填）
# Windows 示例：r'D:\Zotero Data'
# macOS 示例：r'/Users/用户名/Zotero'
ZOTERO_DATA_PATH = r'D:\Zotero Data'

# 导出后 PDF 存放位置（必填）
OUTPUT_DIR = r'E:\输出文件夹\my_pdfs'
```

### 运行程序

**方式一：Windows 双击运行**

```
双击 run.bat
```

**方式二：命令行运行**

```bash
python export_zotero_pdfs.py
```

> ⚠️ **重要提示**：运行前请先**关闭 Zotero**，避免数据库被锁定！

---

## ⚙️ 配置说明

| 配置项 | 必填 | 说明 | 示例 |
|--------|:----:|------|------|
| `ZOTERO_DATA_PATH` | ✅ | Zotero 数据存放目录 | `D:\Zotero Data` |
| `OUTPUT_DIR` | ✅ | 导出文件的存放路径 | `E:\my_pdfs` |
| `EXPORT_MODE` | - | 命名模式：`title` 或 `key` | 默认 `title` |

### 命名模式说明

- **`title`** - 使用文献标题命名（兼容性更好）
  ```
  王五 - 2024 - 论文标题.pdf
  ```

- **`key`** - 使用 Zotero 唯一标识符 + 标题（避免重名）
  ```
  ABC123DEF_王五 - 2024 - 论文标题.pdf
  ```

---

## 📖 使用流程

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  1. 关闭 Zotero  │ ──► │  2. 修改 config  │ ──► │  3. 运行脚本    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  4. 查看导出结果 │
                                               └─────────────────┘
```

---

## ❓ 常见问题

### Q1: 提示"数据库被锁定"

**A**: Zotero 正在运行。请先完全退出 Zotero（包括系统托盘图标），然后重新运行脚本。

---

### Q2: 找不到 `zotero.sqlite` 数据库

**A**: 请检查 `config.py` 中的 `ZOTERO_DATA_PATH` 是否指向正确的 Zotero 数据目录。默认路径通常为：
- **Windows**: `C:\Users\你的用户名\Zotero` 或 `D:\Zotero Data`
- **macOS**: `/Users/你的用户名/Zotero`
- **Linux**: `/home/你的用户名/Zotero`

---

### Q3: 导出的文件数量为 0

**A**: 请检查以下几点：
1. 你的 Zotero 文献库中是否有 PDF 附件
2. `ZOTERO_DATA_PATH` 路径是否正确
3. `storage` 目录是否存在

---

### Q4: 文件名出现乱码

**A**: 部分文献的标题可能包含特殊字符，脚本会自动清理非法字符。如需更精确的命名，建议在 Zotero 中完善文献元数据。

---

### Q5: 如何只导出部分文献？

**A**: 当前版本为全量导出。如需筛选，可在 `export_zotero_pdfs.py` 中的 SQL 查询添加条件（如按年份、标签筛选）。

---

## 📂 项目结构

```
zotero-export-tool/
├── export_zotero_pdfs.py   # 主程序入口
├── config.py               # 配置文件（用户需修改）
├── run.bat                 # Windows 快速启动脚本
└── README.md               # 使用说明
```

---

## 🔧 依赖说明

本项目**无需安装任何第三方依赖**，仅使用 Python 标准库：

- `os`、`pathlib` - 文件路径处理
- `sqlite3` - 读取 Zotero 数据库
- `shutil` - 文件复制操作
- `re` - 正则表达式处理

---

## 📜 开源协议

MIT License - 允许自由使用、修改和分发。

---

## 👤 作者

如有问题或建议，欢迎提交 Issue 或 Pull Request。

---

<p align="center">
  <sub>如果这个工具对你有帮助，欢迎 ⭐ Star 支持！</sub>
</p>