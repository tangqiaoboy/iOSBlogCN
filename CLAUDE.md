# CLAUDE.md

## 项目概述

**iOSBlogCN** 是一个由社区维护的中文 iOS/Mac 开发博客列表。项目以 GitHub 仓库形式管理，核心内容为 Markdown 格式的博客表格，并配有自动生成的 OPML 文件供 RSS 阅读器导入。

- **仓库地址**: `tangqiaoboy/iOSBlogCN`
- **开源协议**: GNU GPLv2
- **语言**: 内容为中文，文件名和代码为英文

## 仓库结构

```
iOSBlogCN/
├── README.md        # 核心内容：Markdown 表格形式的博客列表
├── Export.py        # Python 3 脚本，从 README.md 生成 OPML 文件
├── blogcn.opml     # 自动生成的 OPML 订阅文件（请勿手动编辑）
├── LICENSE          # GNU GPLv2 协议
├── CLAUDE.md        # 本文件
└── .gitignore       # 忽略 .idea/ 和 __pycache__/
```

## 核心文件说明

### README.md
项目的核心文件，包含：
- 项目说明和贡献方式（中文）
- Markdown 表格，列为：`博客地址 | RSS地址`
- 每行格式：`[博客名称](url) | <rss-feed-url>`
- 没有 RSS 的博客，RSS 列填写 `无`

### Export.py
Python 3 脚本，解析 README.md 并生成 `blogcn.opml`：
- 仅使用标准库（`os`、`re`），无外部依赖
- 通过正则表达式提取博客条目信息
- 输出符合 OPML 格式的 XML 文件，可导入 RSS 阅读器
- 运行命令：`python Export.py`
- **必须在仓库根目录下运行**（脚本使用 `os.getcwd()` 获取路径）

### blogcn.opml
自动生成的文件。**请勿手动编辑** — 修改 README.md 后运行 `Export.py` 重新生成即可。

## 常见操作

### 添加新博客
1. 编辑 `README.md`
2. 在表格中新增一行，格式：`[博客名称](https://example.com) | <https://example.com/feed.xml>`
3. 如果没有 RSS 源，RSS 列填写 `无`
4. 运行 `python Export.py` 重新生成 `blogcn.opml`
5. 将 `README.md` 和 `blogcn.opml` 一起提交

### 删除博客
1. 从 `README.md` 的表格中删除对应行
2. 运行 `python Export.py` 重新生成 `blogcn.opml`
3. 将两个文件一起提交

### 重新生成 OPML 文件
```bash
python Export.py
```

## 开发说明

- **无构建系统、CI/CD、测试或代码检查** — 这是一个内容策展仓库
- **无外部依赖** — Export.py 仅使用 Python 标准库
- **Python 版本**: Python 3（使用 `decode()`/`encode()` 处理 UTF-8 编码）
- **贡献方式**: 社区成员通过 [GitHub Issue #1](https://github.com/tangqiaoboy/iOSBlogCN/issues/1) 提交博客推荐

## 提交信息规范

根据仓库历史记录，提交信息采用以下格式：
- `ADD: 描述` — 新增博客条目或功能
- `DEL: 描述` — 删除条目
- `MOD: 描述` — 修改/调整
- `FIX: 描述` — 修复问题（通常引用 issue，如 `fix #36`）
- 也常用中文描述（如 `增加博客：博客名称`）

## 重要约定

- 始终保持 `README.md` 和 `blogcn.opml` 同步 — 修改博客表格后务必运行 `Export.py`
- `README.md` 中没有 RSS 的条目（标记为 `无`）会被 `Export.py` 自动跳过，因为不匹配 `<...>` 正则模式
- OPML 文件的条目分隔符使用 `\r\n` 换行
- 主分支为 `master`（非 `main`）
