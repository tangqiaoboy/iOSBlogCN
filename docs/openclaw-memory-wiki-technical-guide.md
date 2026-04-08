# OpenClaw Memory Wiki 技术文档

> 基于 OpenClaw v2026.4.7 最新版本整理，更新日期：2026-04-08

## 目录

- [概述](#概述)
- [核心架构](#核心架构)
- [Memory Wiki 插件](#memory-wiki-插件)
  - [Vault 模式](#vault-模式)
  - [页面组织结构](#页面组织结构)
  - [结构化 Claim/Evidence 模型](#结构化-claimevidence-模型)
- [关键能力](#关键能力)
  - [矛盾检测与聚类](#矛盾检测与聚类)
  - [新鲜度加权搜索](#新鲜度加权搜索)
  - [编译摘要（Compiled Digests）](#编译摘要compiled-digests)
  - [过时性仪表盘](#过时性仪表盘)
- [Wiki 工具集](#wiki-工具集)
- [CLI 命令参考](#cli-命令参考)
- [Obsidian 集成](#obsidian-集成)
- [Dreaming 系统（实验性）](#dreaming-系统实验性)
- [搜索后端与混合检索](#搜索后端与混合检索)
- [配置参考](#配置参考)
- [v2026.4.7 更新要点](#v202647-更新要点)
- [参考资料](#参考资料)

---

## 概述

OpenClaw 是一个开源的个人 AI 代理框架，其记忆系统采用 **基于文件的记忆模型**——所有持久化信息以 Markdown 文件形式存储在代理工作空间中（默认路径：`~/.openclaw/workspace`）。系统不维护任何隐藏状态，只有显式写入磁盘的内容才计入记忆。

**Memory Wiki** 是 OpenClaw 记忆体系中的高级层，作为可选的伴生插件（`memory-wiki`），将持久化记忆编译为一个具有溯源能力的知识库（vault），支持确定性页面布局、结构化声明（claims）、矛盾追踪和机器可读摘要。

---

## 核心架构

OpenClaw 的记忆系统由三层文件构成：

| 文件 | 作用 | 加载时机 |
|------|------|----------|
| `MEMORY.md` | 长期持久存储：事实、偏好、决策 | 每次会话开始自动加载 |
| `memory/YYYY-MM-DD.md` | 每日笔记：运行中的上下文与观察 | 当日及前一日自动加载 |
| `DREAMS.md` | 实验性：梦境日记与巩固摘要 | 可选，供人工审阅 |

核心记忆工具：

- **`memory_search`**：语义搜索，匹配概念含义而非精确措辞
- **`memory_get`**：检索特定的记忆文件或指定行范围

Memory Wiki 作为补充层叠加在核心记忆之上，**不替换**核心记忆插件。

---

## Memory Wiki 插件

### Vault 模式

Memory Wiki 支持两种运行模式：

#### 1. Isolated（隔离）模式

```yaml
memory-wiki:
  vaultMode: "isolated"
  vault:
    path: "~/.openclaw/wiki/main"
    renderMode: "obsidian"
```

- Wiki 拥有独立的 vault 和数据源
- 不依赖 `memory-core`
- 适用于：希望 wiki 作为独立的、经过策展的知识库

#### 2. Bridge（桥接）模式

```yaml
memory-wiki:
  vaultMode: "bridge"
```

- 通过公共插件 SDK 接口读取活跃记忆插件的公开记忆 artifacts 和事件
- 不直接访问私有插件内部实现
- 适用于：希望 wiki 编译和组织核心记忆插件导出的 artifacts

> **建议**：除非明确需要桥接模式，否则优先选择 isolated 模式。

### 页面组织结构

Wiki vault 采用确定性目录布局：

```
~/.openclaw/wiki/main/
├── sources/          # 导入的原始材料、桥接页面
├── entities/         # 持久对象：人物、系统、项目
├── concepts/         # 观念、抽象、模式、策略
├── syntheses/        # 编译摘要、维护性汇总
├── reports/          # 生成的报告
├── _attachments/     # 附件资源
├── _views/           # 视图定义
└── .openclaw-wiki/   # 托管内容与缓存
    └── cache/
        └── claims.jsonl  # 编译后的声明摘要
```

**关键目录说明**：

| 目录 | 内容 | 示例 |
|------|------|------|
| `sources/` | 原始导入材料与桥接页面 | 论文摘录、会议纪要 |
| `entities/` | 持久对象——人、系统、项目 | `entity.kubernetes`、`entity.alice` |
| `concepts/` | 抽象概念与模式 | `concept.event-sourcing` |
| `syntheses/` | 编译摘要与汇总 | `synthesis.q1-review` |

### 结构化 Claim/Evidence 模型

Memory Wiki 的核心创新是将知识从自由文本升级为 **结构化声明**。每个页面可在 frontmatter 中携带结构化的 claims：

```markdown
---
id: entity.kubernetes
claims:
  - claim: "Kubernetes 默认调度器使用 bin-packing 策略"
    confidence: 0.85
    source: "sources/k8s-scheduler-doc"
    updated: 2026-03-15
    status: active
  - claim: "Helm v4 已移除 Tiller 依赖"
    confidence: 0.95
    source: "sources/helm-release-notes"
    updated: 2026-04-01
    status: active
---

# Kubernetes

正文内容...
```

**Claim 字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `claim` | string | 声明内容 |
| `confidence` | float | 置信度（0-1） |
| `source` | string | 溯源引用（指向 sources/ 下的页面） |
| `updated` | date | 最后更新日期 |
| `status` | enum | `active` / `contested` / `resolved` / `stale` |

Claims 可被追踪、评分、质疑和溯源，使 wiki 的行为更像一个 **信念层（belief layer）** 而非被动的笔记堆。

---

## 关键能力

### 矛盾检测与聚类

`wiki_lint` 工具能自动扫描 vault 中的结构性问题：

- **矛盾检测**：发现语义上互相冲突的 claims
- **矛盾聚类（Contradiction Clustering）**：将相关的矛盾声明分组，便于集中解决
- **溯源缺口**：标记缺少 source 引用的 claims
- **开放问题**：识别尚未解决的疑问

### 新鲜度加权搜索

`wiki_search` 的搜索排序综合考虑：

- **语义相关性**：基于向量相似度的概念匹配
- **关键词匹配**：精确标识符和代码符号的 BM25 匹配
- **新鲜度权重（Freshness Weighting）**：最近更新的 claims 获得更高排名
- **置信度得分**：高置信度的声明优先展示

### 编译摘要（Compiled Digests）

为避免代理和运行时代码在查询时解析 Markdown 页面，Memory Wiki 维护编译后的摘要：

```
.openclaw-wiki/cache/claims.jsonl
```

每行为一个 JSON 对象，包含 claim 的完整元数据。代理可直接读取此文件进行高效查询，无需遍历页面。

### 过时性仪表盘

Memory Wiki 内置 **Staleness Dashboard**，可视化展示：

- 各 claim 的最后更新时间
- 过时（stale）声明的数量与分布
- 需要审查的知识区域

---

## Wiki 工具集

Memory Wiki 插件注册以下工具供代理使用：

| 工具 | 功能 |
|------|------|
| `wiki_status` | 显示当前 vault 模式、健康状态、Obsidian CLI 可用性 |
| `wiki_search` | 搜索 wiki 页面，支持共享记忆语料库 |
| `wiki_get` | 按 id/path 读取 wiki 页面，可回退至共享记忆语料库 |
| `wiki_apply` | 执行窄范围的综合/元数据变更，无需全页编辑 |
| `wiki_lint` | 结构检查：溯源缺口、矛盾、开放问题 |

**使用建议**：

- 当溯源（provenance）重要时，使用 `wiki_search` / `wiki_get` 而非通用 `memory_search`
- 对元数据更新使用 `wiki_apply`，避免自由编辑页面
- 有意义的变更后运行 `wiki_lint`

---

## CLI 命令参考

```bash
# 状态与诊断
openclaw wiki status              # 查看 vault 状态
openclaw wiki doctor              # 诊断 vault 健康问题

# 初始化与数据导入
openclaw wiki init                # 初始化新 vault
openclaw wiki ingest ./notes/alpha.md   # 导入外部文档

# 编译与质量检查
openclaw wiki compile             # 重新编译 claims 摘要
openclaw wiki lint                # 结构检查与矛盾检测

# 搜索与检索
openclaw wiki search "kubernetes" # 搜索 wiki 内容
openclaw wiki get entity.alpha    # 获取指定页面

# 综合与应用
openclaw wiki apply synthesis     # 应用综合更新

# Obsidian 集成
openclaw wiki obsidian status     # 检查 Obsidian 集成状态
```

---

## Obsidian 集成

Memory Wiki 支持与 Obsidian 笔记软件深度集成：

```yaml
memory-wiki:
  obsidian:
    enabled: true
    useOfficialCli: true     # 使用 Obsidian 官方 CLI (v1.12+)
    vaultName: "openclaw-wiki"
    openAfterWrite: false
```

官方 Obsidian CLI（v1.12+）提供完整的 vault 自动化能力，包括：文件管理、每日笔记、搜索、任务、标签、属性、链接、书签、模板、主题、插件、同步与发布。

当 `renderMode` 设为 `"obsidian"` 时，Wiki 页面输出为 Obsidian 兼容格式，可直接在 Obsidian 中浏览和编辑。

---

## Dreaming 系统（实验性）

Dreaming 是一个可选的后台巩固流程，与 Memory Wiki 配合工作：

1. **收集（Collect）**：从每日笔记中提取短期信号
2. **评分（Score）**：基于阈值（得分、召回频率、查询多样性）筛选候选项
3. **晋升（Promote）**：将合格项目提升至长期记忆（`MEMORY.md`）
4. **记录（Document）**：在 `DREAMS.md` 中写入阶段性摘要

v2026.4.7 中 Dreaming 系统的改进：

- 支持将脱敏的会话转录导入 dreaming 语料库
- 按天生成 session-corpus 笔记
- 游标检查点与晋升/诊断支持
- 在每日笔记导入前剥离托管的 Light Sleep 和 REM 块

---

## 搜索后端与混合检索

Memory Wiki 的搜索依托 OpenClaw 的混合检索架构：

| 后端 | 特点 |
|------|------|
| **Builtin（默认）** | 基于 SQLite，支持关键词、向量和混合搜索 |
| **QMD** | 本地优先，支持 reranking 和外部目录索引 |
| **Honcho** | AI 原生跨会话记忆，支持用户建模 |

当配置了 embedding provider 时（支持 OpenAI、Gemini、Voyage、Mistral），`wiki_search` 采用 **混合搜索** 策略：

- **向量相似度**：语义理解层面的概念匹配
- **BM25 关键词匹配**：精确标识符与代码符号匹配
- **新鲜度加权**：近期更新的内容获得排名提升

v2026.4.7 新增了当 `sqlite-vec` 不可用或向量写入降级时的显式警告。

---

## 配置参考

完整的 Memory Wiki 插件配置示例：

```yaml
plugins:
  memory-wiki:
    enabled: true
    vaultMode: "isolated"          # "isolated" | "bridge"
    vault:
      path: "~/.openclaw/wiki/main"
      renderMode: "obsidian"       # "obsidian" | "plain"
    obsidian:
      enabled: true
      useOfficialCli: true
      vaultName: "openclaw-wiki"
      openAfterWrite: false
    ingest:
      autoIndex: true
    search:
      backend: "builtin"           # "builtin" | "qmd" | "honcho"
      freshnessWeight: 0.3         # 新鲜度权重系数
    lint:
      contradictionClustering: true
      stalenessThresholdDays: 30
    dashboard:
      enabled: true
```

---

## v2026.4.7 更新要点

OpenClaw v2026.4.7 是 Memory Wiki 的重要里程碑版本，恢复了完整的 `memory-wiki` 栈：

### Memory Wiki 核心恢复

- 插件 + CLI + sync/query/apply 工具链
- Memory-host 集成
- 结构化 claim/evidence 字段
- 编译摘要检索
- Claim 健康度 linting
- 矛盾聚类
- 过时性仪表盘
- 新鲜度加权搜索

### 其他相关更新

- **推理中心**：新增 `openclaw infer` hub，支持跨 model/media/web/embedding 的 provider 推理工作流
- **媒体生成**：工具/媒体生成支持跨 provider 自动降级，保留意图
- **Webhook 集成**：内置 webhook ingress 插件，支持外部自动化创建和驱动 TaskFlow
- **向量召回警告**：`sqlite-vec` 不可用时显式提醒
- **Dreams 配置感知**：Dreams 配置读写现在尊重选定的 memory slot 插件

---

## 参考资料

- [OpenClaw GitHub Releases](https://github.com/openclaw/openclaw/releases)
- [OpenClaw v2026.4.7 Release Notes](https://github.com/openclaw/openclaw/releases/tag/v2026.4.7)
- [OpenClaw Memory 概念文档](https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory.md)
- [OpenClaw CHANGELOG](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md)
- [Memory & Search - DeepWiki](https://deepwiki.com/openclaw/openclaw/3.4.3-memory-and-search)
- [OpenClaw Memory Wiki 官方文档](https://docs.openclaw.ai/plugins/memory-wiki)
- [Luke The Dev 关于 v2026.4.7 的推文](https://x.com/iamlukethedev/status/2041717991109169169)
