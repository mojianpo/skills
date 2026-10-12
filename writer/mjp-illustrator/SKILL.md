---
name: mjp-illustrator
description: 分析文章结构，识别需要配图的位置，使用 类型 × 风格 × 色板 三维方法生成配图。当用户要求"为文章配图"、"添加图片"、"生成文章插图"时使用此技能。
---

# 文章配图助手

分析文章，识别配图位置，使用 类型 × 风格 × 色板 保持一致性地生成图片。

## 用户输入工具

当此技能需要提示用户时，请遵循以下工具选择规则（优先级顺序）：

1. **优先使用当前运行时暴露的内置用户输入工具** — 例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **备选方案**：如果不存在此类工具，发送带编号的纯文本消息，要求用户回复所选编号/答案。
3. **批量处理**：如果工具支持单次调用多个问题，将所有适用问题合并为一次调用；如果仅支持单问题，则按优先级逐一询问。

下面具体的 `AskUserQuestion` 引用仅为示例 — 在其他运行时中请替换为本地等效工具。

## 图片生成工具

当此技能需要渲染图片时，按以下顺序解析后端：

1. **当前请求覆盖** — 如果用户在当前消息中指定了特定后端，则使用该后端。
2. **`preferred_image_backend: ask`** — 如果 `EXTEND.md` 设置为 `ask`，强制询问一次后端（选项包含 `openai-api`），与其他初始问题批量处理。
3. **`config.json` 文生图 API（`openai-api`）⭐ 优先默认** — 读取本技能根目录的 `config.json`。若 `api_key`、`base_url`、`model` 三者齐全，**必须优先使用该 OpenAI 协议文生图服务**（当前配置为火山方舟 doubao-seedream），调用约定见 [references/openai-imagegen.md](references/openai-imagegen.md)。仅当配置缺失/不完整，或调用失败且重试一次后仍失败并经用户确认切换时，才继续向下解析。
4. **已保存的偏好设置** — 如果 `EXTEND.md` 将 `preferred_image_backend` 固定到某个当前可用的后端，则使用该后端。
5. **自动选择**（当偏好设置为 `auto`、未设置，或固定的后端不可用时）：
   - **Codex (`imagegen`)** — 首先，检查你的可用技能/工具清单。如果列出了名为 `imagegen` 的技能，说明你正在 Codex 运行时中，必须使用它：通过 `Skill` 工具调用，`skill: "imagegen"`，传递已保存的提示文件内容（加上 Codex `imagegen` 自身参数的输出路径和宽高比）。Codex `imagegen` 是该运行时中的官方光栅后端，优先级高于任何非原生技能（如 `mjp-image-gen`），除非用户明确指定了不同的 `preferred_image_backend`。
   - **通过 `codex exec` 使用 Codex (`codex-imagegen`)** — 如果当前运行时没有原生 `imagegen` 技能但 `codex` CLI 在 `PATH` 上且已激活 `codex login`，则通过 `image-gen --provider codex-cli` 路由（首选），或 — 如果 image-gen 不可用 — 调用内置包装器。详情、参数和运行时发现过程在 [references/codex-imagegen.md](references/codex-imagegen.md) 中 — 仅在此分支被选中时加载该文件。
   - **Cursor (`GenerateImage`)** — 如果运行时暴露原生 `GenerateImage` 工具，说明你正在 Cursor 中运行，它与 Codex `imagegen` 一样优先于任何非原生技能。两个硬性注意事项：(a) 它没有宽高比参数 — 在作为 `description` 传递的提示文本中明确说明目标宽高比/尺寸；(b) 它不接受输出目录 — 它保存到工具管理的位置，因此生成后需将文件复制/移动到技能期望的输出路径（如 `outputs/.../NN-xxx.png`）。参考图片放在 `reference_image_paths` 中。
   - **其他运行时原生工具** — 如果运行时暴露不同的原生图片工具（如 Hermes `image_generate`），以相同方式使用。
   - 否则，如果恰好安装了一个非原生后端（如 `image-gen`），使用它。
   - 否则（多个非原生后端且无运行时原生工具），询问用户一次 — 与其他初始问题批量处理。
6. **如果都不可用**，告知用户并询问如何继续。

**⛔ 绝不使用 SVG、HTML、canvas 或其他基于代码的渲染替代光栅图片生成。** Codex `imagegen` 自己的描述说应该在"输出应为位图资产而非仓库原生代码或矢量"时使用。如果你无法通过步骤 3 解析出光栅后端，进入步骤 4 询问用户 — **不要**静默输出 SVG、编写内联 `<svg>` 标记，或产生 HTML/CSS 艺术品作为替代品。即使文章/部分看起来"像图表"也适用此规则：调用此规则的消费者技能已经决定需要光栅图片。

**⛔ 绝不通过在已生成的位图上绘画来修复渲染文本。** 不要使用 ImageMagick、Pillow、Canvas、SVG、HTML/CSS、OCR 脚本或任何其他程序化覆盖来覆盖、重写、擦除、描边或替换已生成插图中的标签、标题或任何其他文本。如果文本不正确或不清晰，从更正后的提示重新生成，用更少或没有图片上的文本重新绘制，或询问用户保留哪个不完美的候选图。

设置 `preferred_image_backend: ask` 会强制每次运行时都进行步骤 2 的后端询问，无论 `config.json` 是否可用。用户可通过下方的 `## 修改偏好设置` 部分更改固定的后端。不想使用 `config.json` API 时：在当前请求中指明后端，或临时改名/清空 `config.json` 的凭证字段。

**提示文件要求（硬性）**：在调用任何后端之前，将每张图片的完整最终提示写入 `prompts/` 下的独立文件（命名：`NN-{type}-[slug].md`）。后端接收提示文件（或其内容）；该文件是可复现性记录，让你无需重新生成提示即可切换后端。

上面的具体工具名称（`imagegen`、`GenerateImage`、`image_generate`）仅为示例 — 在相同规则下替换为本地等效工具。

## 批量生成策略

在该批次的每个提示文件都已保存并验证后，默认批量生成图片。

优先级顺序：

1. 如果所选后端有原生批量/多任务接口，使用它。每个任务必须保持自己的提示文件、输出路径、宽高比和直接参考图片。
2. 如果没有原生批量接口但运行时可以发出并行工具调用，一次分派最多 `generation_batch_size` 张图片。默认：`4`。当前消息中的明确用户请求，如 `--batch-size 4` 或"并行4张一起生成"，会覆盖 EXTEND.md。
3. 如果既没有原生批量也没有并行工具调用，则顺序生成。

规则：

- 在该批次的所有提示文件存在于磁盘上之前，绝不开始第一批。
- 失败的项目重试一次，不重新生成成功的项目。
- 不要仅为了并行化图片渲染而使用子代理。仅在需要单独的提示迭代或创意探索时使用子代理。

## 确认策略

默认行为：**生成前确认**。

- 将显式技能调用、文件路径、匹配的信号/预设和 `EXTEND.md` 默认值视为**仅推荐输入**。它们都不授权跳过确认。
- 在用户完成步骤 3 之前，**不要**开始步骤 4 或之后的步骤。
- 仅当当前请求明确表示要跳过确认时才跳过确认，例如："直接生成"、"不用确认"、"跳过确认"、"按默认出图"或等效措辞。
- 如果显式跳过确认，在生成前的下一个面向用户的更新中说明假定的类型/密度/风格/色板/语言/后端。

## 参考图片

用户可以通过 `--ref <files...>` 提供参考图片，或通过在对话中提供文件路径/粘贴图片。参考图片指导特定插图的风格、色板、构图或主题。

完整的检测、存储和处理规则在 [references/workflow.md](references/workflow.md) 中（步骤 1.0 保存到 `references/NN-ref-{slug}.{ext}`；步骤 5.3 按插图处理 `direct | style | palette` 用法）。当所选后端支持批量输入时，每个提示文件的 `references:` frontmatter 中的 `direct` 用法条目应传播到其批量负载中，以便后端可以传递它们（例如 `image-gen` 每个任务接受 `ref`）。

## 三个维度

| 维度 | 控制内容 | 示例 |
|------|----------|------|
| **类型** | 信息结构 | 信息图、场景图、流程图、对比图、框架图、时间线 |
| **风格** | 渲染方式 | notion、温暖、极简、蓝图、水彩、优雅 |
| **色板** | 配色方案（可选） | 马卡龙、温暖、霓虹 — 覆盖风格的默认颜色 |

自由组合：`--type infographic --style vector-illustration --palette macaron`

或使用预设：`--preset edu-visual` → 一个标志包含类型 + 风格 + 色板。参见 [风格预设](references/style-presets.md)。

## 类型

| 类型 | 最佳用途 |
|------|----------|
| `infographic`（信息图） | 数据、指标、技术内容 |
| `scene`（场景图） | 叙事、情感内容 |
| `flowchart`（流程图） | 流程、工作流 |
| `comparison`（对比图） | 并排对比、选项 |
| `framework`（框架图） | 模型、架构 |
| `timeline`（时间线） | 历史、演变 |

## 风格

参见 [references/styles.md](references/styles.md) 了解核心风格、完整画廊和类型 × 风格兼容性。

## 工作流程

```
- [ ] 步骤 1：预检查（EXTEND.md、参考文件、配置）
- [ ] 步骤 2：分析内容
- [ ] 步骤 3：确认设置（AskUserQuestion）
- [ ] 步骤 4：生成大纲
- [ ] 步骤 5：生成图片
- [ ] 步骤 6：完成
```

### 步骤 1：预检查

**1.5 加载偏好设置（EXTEND.md）⛔ 阻塞**

按优先级顺序检查 EXTEND.md — 找到的第一个生效：

| 优先级 | 路径 | 范围 |
|--------|------|------|
| 1 | `.mjp-skills/mjp-article-illustrator/EXTEND.md` | 项目级 |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/mjp-skills/mjp-article-illustrator/EXTEND.md` | XDG |
| 3 | `$HOME/.mjp-skills/mjp-article-illustrator/EXTEND.md` | 用户主目录 |

| 结果 | 操作 |
|------|------|
| 已找到 | 读取、解析、显示摘要 |
| 未找到 | ⛔ 运行 [首次设置](references/config/first-time-setup.md) |

完整流程：[references/workflow.md](references/workflow.md#step-1-pre-check)

### 步骤 2：分析

| 分析项 | 输出 |
|--------|------|
| 内容类型 | 技术 / 教程 / 方法论 / 叙事 |
| 目的 | 信息传递 / 可视化 / 想象力 |
| 核心论点 | 2-5 个要点 |
| 位置 | 插图增值的位置 |

**关键**：隐喻 → 可视化底层概念，而非字面图片。

完整流程：[references/workflow.md](references/workflow.md#step-2-setup--analyze)

### 步骤 3：确认设置 ⚠️

**硬性门槛**：此步骤是强制性的，参见[确认策略](#确认策略) — 在用户在此确认（或在当前请求中明确选择"直接生成"/等效措辞）之前，不能开始步骤 4 及之后的步骤。

**一次 AskUserQuestion，最多 4 个问题。Q1-Q2 必需。除非已选择预设，否则 Q3 必需。**

| 问题 | 选项 |
|------|------|
| **Q1：预设或类型** | [推荐预设]、[备选预设]，或手动选择：信息图、场景图、流程图、对比图、框架图、时间线、混合 |
| **Q2：密度** | 极简 (1-2)、均衡 (3-5)、逐节 (推荐)、丰富 (6+) |
| **Q3：风格** | [推荐]、minimal-flat、sci-fi、hand-drawn、editorial、scene、poster、其他 — **如果已选预设则跳过** |
| Q4：色板 | 默认（风格颜色）、马卡龙、温暖、霓虹 — **如果预设包含色板或已设置 preferred_palette 则跳过** |
| Q5：语言 | 当文章语言 ≠ EXTEND.md 设置时 |

完整流程：[references/workflow.md](references/workflow.md#step-3-confirm-settings-)

### 步骤 4：生成大纲

保存 `outline.md`，包含 frontmatter（类型、密度、风格、色板、图片数量）和条目：

```yaml
## 插图 1
**位置**: [章节/段落]
**目的**: [原因]
**视觉内容**: [内容]
**文件名**: 01-infographic-concept-name.png
```

完整模板：[references/workflow.md](references/workflow.md#step-4-generate-outline)

### 步骤 5：生成图片

⛔ **阻塞：提示文件必须在任何图片生成之前保存。** 这是硬性要求，无论选择哪个后端 — 提示文件是可复现性记录。

1. 为每个插图，按照 [references/prompt-construction.md](references/prompt-construction.md) 创建提示文件
2. 保存到 `prompts/NN-{type}-{slug}.md`，包含 YAML frontmatter
3. 提示**必须**使用特定类型的模板，包含结构化部分（ZONES / LABELS / COLORS / STYLE / ASPECT）
4. LABELS **必须**包含文章特定数据：实际数字、术语、指标、引用
5. **不要**在保存提示文件之前向 `--prompt` 传递临时内联提示
6. 通过顶部的 `## 图片生成工具` 规则选择后端：使用任何可用的；如果有多个，询问用户一次。每个会话在任何生成之前做一次。
   - **`openai-api` 调用**：当规则解析为 `openai-api`（`config.json` 配置齐全时的默认）时，参见 [references/openai-imagegen.md](references/openai-imagegen.md) 了解调用约定（请求字段、ASPECT→size 映射、b64 落盘、批量与错误处理）。
   - **`codex-imagegen` 调用**：当规则解析为 `codex-imagegen` 时，参见 [references/codex-imagegen.md](references/codex-imagegen.md) 了解调用约定（首选 `mjp-image-gen --provider codex-cli` 路径、运行时包装器发现、参数说明、stdout 模式、批量语义）。
7. **执行策略**：按照 `## 批量生成策略` 批量生成：优先后端原生批量，其次运行时并行工具调用，仅作为备选顺序生成。默认批量大小为 4，除非 EXTEND.md 或当前请求覆盖。
8. 按提示 frontmatter 处理参考图片（`direct`/`style`/`palette`）
9. 如果 EXTEND.md 启用了水印则应用
10. 从已保存的提示文件生成；失败时重试一次

完整流程：[references/workflow.md](references/workflow.md#step-5-generate-images)

### 步骤 6：完成

在段落后插入 `![description]({relative-path}/NN-{type}-{slug}.png)`。路径相对于文章文件，基于输出目录设置计算。

```
文章配图完成！
文章：[路径] | 类型：[类型] | 密度：[级别] | 风格：[风格] | 色板：[色板或默认]
图片：X/N 已生成
```

## 输出目录

输出目录由 EXTEND.md 中的 `default_output_dir` 决定（在首次设置期间配置）：

| `default_output_dir` | 输出路径 | Markdown 插入路径 |
|----------------------|----------|-------------------|
| `imgs-subdir`（默认） | `{article-dir}/imgs/` | `imgs/NN-{type}-{slug}.png` |
| `same-dir` | `{article-dir}/` | `NN-{type}-{slug}.png` |
| `illustrations-subdir` | `{article-dir}/illustrations/` | `illustrations/NN-{type}-{slug}.png` |
| `independent` | `illustrations/{topic-slug}/` | `illustrations/{topic-slug}/NN-{type}-{slug}.png`（相对于 cwd） |

所有辅助文件（大纲、提示）保存在输出目录内：

```
{output-dir}/
├── outline.md
├── prompts/
│   └── NN-{type}-{slug}.md
└── NN-{type}-{slug}.png
```

当输入为**粘贴内容**（无文件路径）时，始终使用 `illustrations/{topic-slug}/`，并将 `source-{slug}.{ext}` 保存在旁边。

**Slug**：2-4 个单词，kebab-case。**冲突**：追加 `-YYYYMMDD-HHMMSS`。

## 修改

| 操作 | 步骤 |
|------|------|
| 编辑 | 更新提示 → 重新生成 → 更新引用 |
| 添加 | 定位 → 提示 → 生成 → 更新大纲 → 插入 |
| 删除 | 删除文件 → 移除引用 → 更新大纲 |

文本修正策略：

- 如果任何渲染文本（标签、标题等）拼写错误、乱码、难以阅读或视觉效果弱，不要用代码修补位图。
- 对于文本修正重新生成，写入新的提示文件和新的输出路径，以便保留有缺陷的候选图用于比较。
- 后处理仅限于不影响文本或主要构图的裁剪、调整大小、压缩或格式转换。

## 参考文件

| 文件 | 内容 |
|------|------|
| [references/workflow.md](references/workflow.md) | 详细流程 |
| [references/usage.md](references/usage.md) | 命令语法 |
| [references/styles.md](references/styles.md) | 风格画廊 + 色板画廊 |
| [references/style-presets.md](references/style-presets.md) | 预设快捷方式（类型 + 风格 + 色板） |
| [references/prompt-construction.md](references/prompt-construction.md) | 提示模板 |
| [references/openai-imagegen.md](references/openai-imagegen.md) | `config.json` OpenAI 协议文生图 API 调用约定 |
| [references/config/first-time-setup.md](references/config/first-time-setup.md) | 首次设置 |

## 修改偏好设置

EXTEND.md 位于步骤 1.5 中列出的第一个匹配路径。三种修改方式：

- **直接编辑** — 打开 EXTEND.md 并更改字段。完整架构：`references/config/preferences-schema.md`。
- **交互式重新配置** — 删除 EXTEND.md（或询问"重新配置 mjp-illustrator 偏好设置"/"重新配置"）。下次运行将重新触发首次设置。
- **常见单行编辑**：
  - `preferred_image_backend: auto` — 默认；`config.json` 齐全时优先 `openai-api`，否则运行时原生工具优先，回退到唯一安装的后端，仅在有多个非原生时询问。
  - `preferred_image_backend: openai-api` — 显式固定到 `config.json` 的 OpenAI 协议文生图 API（配置不完整时询问）。
  - `preferred_image_backend: codex-imagegen` — 固定到 Codex 内置（仅当用户在当前请求中指明或 `config.json` 不可用时生效，见 `## 图片生成工具` 优先级）。
  - `preferred_image_backend: image-gen` — 固定到 mjp-image-gen 技能。
  - `preferred_image_backend: ask` — 每次运行都确认后端。
  - `generation_batch_size: 4` — 运行时支持并行生成调用时默认并发渲染的图片数量。
  - `preferred_type: infographic`、`preferred_style: notion`、`preferred_palette: macaron`、`language: zh`。
  - `default_output_dir: imgs-subdir` — 相对于文章生成图片的位置。