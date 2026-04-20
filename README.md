# Zotero PDF 一键导出工具

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue?logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
</p>

从 Zotero 文献库中一键提取所有 PDF 附件，**按集合自动分类**，以文献标题自动重命名。

---

## 工具起源

> 这是一个从实际需求中诞生的工具。

在学术研究过程中，我们通常会在 Zotero 中积累大量的 PDF 文献。随着文献数量增多，如何高效管理和导出这些文献成了一个实际问题：

- 直接从 Zotero 导出文件时，文件名通常是原始的（如 `PDF.pdf`、`bing-compare.pdf`）
- 虽然 Zotero 内部按集合（Collection）分类管理文献，但导出后会丢失分类信息
- 他人无法直接使用你的 Zotero 数据

因此，我开发了这个工具——帮助自己（也帮助他人）更方便地管理和导出 Zotero 文献。

---

## 版本演进

### v1.0 - 基础版本
最初的想法很简单：从 Zotero 提取所有 PDF 并用文献标题重命名。

```
输入: Zotero 数据库 + storage 目录
输出: 一堆以标题命名的 PDF 文件
```

**问题**: 所有文件都平铺在一起，无法体现原有的分类逻辑。

---

### v1.5 - 分类导出
改进了思路：从 Zotero 数据库中读取**集合（Collection）**信息，按集合分类导出。

```
输入: Zotero 数据库
  ↓
读取 collections 表 → 获取所有集合
读取 itemAttachments 表 → 获取 PDF 附件
读取 collectionItems 表 → 建立 PDF 与集合的映射
  ↓
输出: 按集合分类的文件夹
```

**效果**:
```
导出结果/
├── 1 博士文献/     ← 来自 Zotero 集合
├── 2 书籍/         ← 来自 Zotero 集合
├── 3 思维类/       ← 来自 Zotero 集合
└── 未分类/         ← 未在任何集合中的文献
```

---

### v2.0 - 一键Exe

为了让更多用户无门槛使用，将 Python 脚本打包成 **EXE 可执行文件**。

```
Python 脚本 + PyInstaller → 单文件 EXE
```

用户无需安装 Python，无需配置环境，**双击即可运行**。

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

程序会自动检测 Zotero 数据目录，**大多数情况下无需手动配置**。

如果自动检测失败，在同目录下创建 `config.py` 文件：

```python
# config.py
ZOTERO_DATA_PATH = r'C:\Users\你的用户名\AppData\Roaming\Zotero\Profiles\xxx.default\zotero'
OUTPUT_DIR = r'C:\Users\你的用户名\Desktop\My Exported PDFs'
EXPORT_STRATEGY = 'by_collection'
```

> 💡 可参考 `config.example.py` 文件中的说明

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

程序会自动检测以下 Zotero 常见位置：

- `%APPDATA%\Zotero\Profiles\*.default\zotero`
- `%LOCALAPPDATA%\Zotero\Zotero\Profiles\*.default\zotero`

如需自定义，可创建 `config.py`：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `ZOTERO_DATA_PATH` | Zotero 数据目录（可选，自动检测） | 留空自动检测 |
| `OUTPUT_DIR` | 导出输出目录（默认桌面） | `C:\Users\You\Desktop\My PDFs` |
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

# 运行
python export_zotero_pdfs_standalone.py

# 打包为 EXE
pip install pyinstaller
pyinstaller --onefile --windowed --name "ZoteroPDF导出工具" export_zotero_pdfs_standalone.py
```

### 技术原理

```
1. 连接 Zotero SQLite 数据库
2. 读取 collections 表获取所有集合
3. 读取 itemAttachments 表获取 PDF 附件
4. 读取 collectionItems 表建立 item-collection 映射
5. 遍历 storage 目录查找对应 PDF 文件
6. 复制并按标题重命名到目标目录
```

---

## 项目结构

```
zotero-pdf-exporter/
├── ZoteroPDF导出工具.exe    # EXE 版本（双击即用）
├── export_zotero_pdfs_standalone.py  # Python 源码
├── config.py               # 配置文件
├── README.md               # 说明文档
└── run.bat                 # 快速启动（Python 版）
```

---

## 许可证

MIT License - 允许自由使用、修改和分发。

---

<p align="center">
  <sub>如果这个工具对你有帮助，欢迎 ⭐ Star 支持！</sub>
</p>