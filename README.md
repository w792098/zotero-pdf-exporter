# Zotero PDF 一键导出工具

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue?logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
</p>

从 Zotero 文献库中一键提取所有 PDF 附件，**按集合自动分类**，以文献标题自动重命名。

---

## 两种版本

| 版本 | 说明 | 适用用户 |
|------|------|----------|
| **EXE 版** | 双击即用，无需安装 Python | 大多数用户（推荐） |
| **Python 版** | 需要 Python 3.6+ 环境 | 开发者/需要自定义 |

---

## 快速开始（EXE 版）

### 1. 下载

访问 [Releases](https://github.com/w792098/zotero-pdf-exporter/releases) 下载 `ZoteroPDF导出工具.exe`

### 2. 配置

首次运行会自动查找数据库，如果找不到，需要：

1. 在同目录下创建 `config.py` 文件
2. 内容如下（根据你的实际情况修改路径）：

```python
# config.py
ZOTERO_DATA_PATH = r'D:\Zotero Data'
OUTPUT_DIR = r'E:\导出文件夹'
EXPORT_STRATEGY = 'by_collection'
```

### 3. 运行

**双击 `ZoteroPDF导出工具.exe`**

> ⚠️ **重要**：运行前请先**关闭 Zotero**！

---

## 功能特性

| 特性 | 说明 |
|------|------|
| 按集合分类 | 自动读取 Zotero 集合，导出为分类文件夹 |
| 智能重命名 | 根据文献标题自动命名文件 |
| 跨平台 | 兼容 Windows、macOS、Linux 系统 |
| 零依赖 | EXE 版无需安装任何环境 |

---

## 导出策略

### 方式一：按集合分类（推荐）

```
导出结果/
├── 1 博士文献/
│   ├── 论文1.pdf
│   └── 论文2.pdf
├── 2 书籍/
│   └── 书籍1.pdf
├── 3 思维类/
│   └── 思维相关.pdf
└── 未分类/
    └── 其他.pdf
```

### 方式二：全部平铺

在 `config.py` 中修改：

```python
EXPORT_STRATEGY = 'all_flat'
```

---

## 配置说明

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `ZOTERO_DATA_PATH` | Zotero 数据目录 | `D:\Zotero Data` |
| `OUTPUT_DIR` | 导出输出目录 | `E:\my_pdfs` |
| `EXPORT_STRATEGY` | `by_collection` 或 `all_flat` | 按集合分类 |
| `EXPORT_MODE` | `title` 或 `key` | 标题命名 |

### 如何找到 Zotero 数据目录？

- **Windows**: `C:\Users\你的用户名\Zotero` 或自定义目录
- **macOS**: `/Users/你的用户名/Zotero`
- **Linux**: `/home/你的用户名/Zotero`

---

## 常见问题

### Q1: 提示"数据库被锁定"

**A**: Zotero 正在运行。请完全退出 Zotero 后再运行。

### Q2: 找不到数据库

**A**: 请创建 `config.py` 文件，填写正确的 `ZOTERO_DATA_PATH`。

### Q3: 导出数量为 0

**A**: 检查 Zotero 中是否有 PDF 附件，以及路径是否正确。

---

## Python 版（开发者）

如果你需要自定义或二次开发：

```bash
# 克隆仓库
git clone https://github.com/w792098/zotero-pdf-exporter.git

# 安装依赖（可选，仅标准库）
# 无需安装任何包

# 运行
python export_zotero_pdfs_standalone.py

# 打包为 EXE
pip install pyinstaller
pyinstaller --onefile --windowed --name "ZoteroPDF导出工具" export_zotero_pdfs_standalone.py
```

---

## 项目结构

```
zotero-pdf-exporter/
├── ZoteroPDF导出工具.exe    # EXE 版本（双击即用）
├── export_zotero_pdfs_standalone.py  # Python 源码
├── config.py               # 配置文件（如需自定义）
├── run.bat                 # 快速启动（Python 版）
└── README.md               # 说明文档
```

---

## 许可证

MIT License - 允许自由使用、修改和分发。

---

<p align="center">
  <sub>如果这个工具对你有帮助，欢迎 ⭐ Star 支持！</sub>
</p>