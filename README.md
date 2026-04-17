# Zotero PDF 一键导出工具

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue?logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
</p>

从 Zotero 文献库中一键提取所有 PDF 附件，**按集合自动分类**，以文献标题自动重命名，方便整理和备份。

---

## 功能特性

| 特性 | 说明 |
|------|------|
| 按集合分类 | 自动读取 Zotero 集合，导出为分类文件夹 |
| 智能重命名 | 根据文献标题自动命名文件，易于识别和管理 |
| 跨平台 | 兼容 Windows、macOS、Linux 系统 |
| 零依赖 | 仅使用 Python 标准库，无需安装第三方包 |
| 灵活配置 | 支持自定义 Zotero 数据目录和输出路径 |

---

## 环境要求

- **Python 3.6** 或更高版本
- **Zotero** 客户端

### 验证 Python 安装

```bash
python --version
```

---

## 快速开始

### 1. 下载项目

```bash
# 方式一：Clone 仓库
git clone https://github.com/w792098/zotero-pdf-exporter.git

# 方式二：下载 ZIP
# 访问 https://github.com/w792098/zotero-pdf-exporter/releases
```

### 2. 配置路径

用文本编辑器打开 `config.py`，修改以下两项：

```python
# Zotero 数据目录（必填）
ZOTERO_DATA_PATH = r'D:\Zotero Data'

# 导出后 PDF 存放位置（必填）
OUTPUT_DIR = r'E:\my_exported_pdfs'
```

### 3. 运行程序

```bash
# 方式一：Windows 双击 run.bat

# 方式二：命令行运行
python export_zotero_pdfs.py
```

> ⚠️ **重要**：运行前请先**关闭 Zotero** 客户端！

---

## 导出策略

在 `config.py` 中选择导出方式：

```python
# 方式一：按集合分类导出（推荐）
EXPORT_STRATEGY = 'by_collection'

# 方式二：全部平铺到一个文件夹
EXPORT_STRATEGY = 'all_flat'
```

### 策略一：按集合分类（推荐）

自动读取 Zotero 中的集合（如"博士文献"、"书籍"、"思维类"等），每个集合导出为一个文件夹。

```
导出结果/
├── 1 博士文献/
│   ├── 论文1.pdf
│   └── 论文2.pdf
├── 2 书籍/
│   ├── 书籍1.pdf
│   └── 书籍.pdf
├── 3 思维类/
│   └── 思维相关.pdf
└── 未分类/
    └── 其他.pdf
```

### 策略二：全部平铺

所有 PDF 导出到同一个文件夹，按标题命名。

```
导出结果/
├── 文献标题1.pdf
├── 文献标题2.pdf
└── 文献标题3.pdf
```

---

## 集合列表

运行脚本时会自动显示你的 Zotero 集合列表：

```
[4] 集合列表:
    [10] 1 博士文献 (15 个PDF)
    [12] 2 书籍 (9 个PDF)
    [11] 3 思维类 (8 个PDF)
    [14] 5 情绪调节 (2 个PDF)
    [0] 未分类 (262 个PDF)
```

---

## 完整配置说明

| 配置项 | 必填 | 说明 | 默认值 |
|--------|:----:|------|--------|
| `ZOTERO_DATA_PATH` | ✅ | Zotero 数据目录 | - |
| `OUTPUT_DIR` | ✅ | 导出文件存放目录 | - |
| `EXPORT_STRATEGY` | - | 导出策略 | `by_collection` |
| `EXPORT_MODE` | - | 命名模式 | `title` |

### 命名模式

```python
# 模式一：使用文献标题（推荐）
EXPORT_MODE = 'title'
# 输出：文献标题.pdf

# 模式二：使用 Zotero Key（避免重名）
EXPORT_MODE = 'key'
# 输出：ABC123DEF_文献标题.pdf
```

---

## 如何找到 Zotero 数据目录？

**Windows:**
```
C:\Users\你的用户名\Zotero
# 或自定义目录（如 D:\Zotero Data）
```

**macOS:**
```
/Users/你的用户名/Zotero
```

**Linux:**
```
/home/你的用户名/Zotero
```

---

## 常见问题

### Q1: 提示"数据库被锁定"

**A**: Zotero 正在运行。请完全退出 Zotero（包括系统托盘图标），然后重新运行脚本。

---

### Q2: 找不到 `zotero.sqlite` 数据库

**A**: 请检查 `config.py` 中 `ZOTERO_DATA_PATH` 是否正确。确认该目录下存在 `zotero.sqlite` 文件。

---

### Q3: 导出数量为 0

**A**: 可能原因：
1. 你的 Zotero 文献库中没有 PDF 附件
2. `ZOTERO_DATA_PATH` 路径不正确
3. PDF 存储在云端而非本地

---

### Q4: 文件名出现乱码

**A**: 部分文献标题含有特殊字符，脚本会自动过滤非法字符。建议在 Zotero 中完善文献元数据。

---

### Q5: 部分 PDF 没有被分类

**A**: 如果文献没有添加到任何集合中，会自动归入"未分类"文件夹。

---

### Q6: 支持 Zotero 6 吗？

**A**: 支持。脚本通过读取 SQLite 数据库工作，与 Zotero 版本无关。

---

## 项目结构

```
zotero-pdf-exporter/
├── export_zotero_pdfs.py   # 主程序
├── config.py               # 配置文件
├── run.bat                 # Windows 快速启动
└── README.md               # 使用说明
```

---

## 技术原理

```
1. 连接 Zotero SQLite 数据库
2. 读取 collections 表获取所有集合
3. 读取 itemAttachments 表获取 PDF 附件
4. 读取 collectionItems 表建立 item-collection 映射
5. 根据 EXPORT_STRATEGY 导出：
   - by_collection: 按集合创建子文件夹
   - all_flat: 全部导出到根目录
6. 读取 items 表获取文献标题并重命名文件
```

---

## 许可证

MIT License - 允许自由使用、修改和分发。

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

---

<p align="center">
  <sub>如果这个工具对你有帮助，欢迎 ⭐ Star 支持！</sub>
</p>