---
name: bes-bid-write
description: 依据用户提供的招标文件、评分办法、企业资质及项目资料，完成招标需求提取、合规响应矩阵、投标内容撰写、风险审查和 DOCX 文档交付。当用户要求撰写、续写、改写或审核标书/投标文件，解读招标文件，提取废标项、资格项或评分项，编制技术方案、商务方案、响应矩阵，或将投标内容排版导出为 DOCX 时触发此技能。
---

# bes-bid-write

基于用户提供的招标文件、评分办法和企业项目资料，编制可追溯、逐项响应、禁止虚构并经过合规审查的正式投标响应文件（paper），最终交付 DOCX。适用于标书撰写、投标文件编制、招标需求解读、响应矩阵、技术或商务方案撰写、标书审查以及 DOCX 排版导出。

## 不可违反的规则

1. 只把用户资料、招标文件和用户确认的信息写成事实。不得虚构资质、案例、人员、参数、报价、证书、日期、客户评价或服务承诺。
2. 原文要求与投标响应必须可追溯。关键结论记录来源文件、页码或章节；无法定位页码时记录文件名与标题。
3. 不得把推测写成已确认事实。非关键资料缺失时使用 `【待补充：具体内容｜责任人：用户｜影响：...】`；关键门槛资料缺失时停止定稿并输出缺口。
4. 不得擅自弱化“一票否决”“必须”“应当”“不得”“不接受偏离”等约束。
5. 不得承诺用户资料未支持的履约指标。建议性增强内容必须标记为“建议，待用户确认”。
6. DOCX 生成成功不等于内容合规。必须同时完成内容审查与文档校验。

## 按需加载参考文件

开始任务后按以下规则读取，不要一次加载无关文件：

- 所有标书任务先读取 [references/source-policy.md](references/source-policy.md)。
- 收到招标文件或评分办法时读取 [references/workflow.md](references/workflow.md)。
- 撰写正文时读取 [references/writing-style.md](references/writing-style.md)。
- 审查或定稿时读取 [references/compliance-review.md](references/compliance-review.md)。
- 生成 DOCX 时读取 [references/docx-spec.md](references/docx-spec.md)，并使用 `assets/default-style.json`。
- 招标文件未指定模板时，按需复制 `assets/default-paper-outline.md`、`assets/compliance-matrix-template.md` 和 `assets/review-report-template.md`。

## 输入识别与门禁

先盘点用户提供的文件和文字，建立“资料清单”。至少识别：

- 招标文件、澄清或补遗文件、评分办法；
- 投标人名称、项目名称、招标编号、标段；
- 资质证照、业绩案例、人员履历、技术参数；
- 商务条款、报价资料、交付计划、服务承诺；
- 用户提供的模板或格式要求。

若缺少招标文件，仍可生成通用草案，但必须在首页或交付说明中标注“未依据完整招标文件进行合规核验，不可直接投标”。

仅当以下任一情况成立时向用户提问并暂停定稿：

- 无法确定投标主体、项目或标段；
- 缺少一票否决项所需证明；
- 多份文件要求相互冲突，且无法按“补遗/澄清优先、日期较新优先、专用条款优先”解决；
- 用户要求写入资料没有支持的事实或承诺；
- 报价、签章、授权等必须由用户决策的内容尚未确认。

其他缺失项不得阻塞初稿，使用规范占位符并继续。

## 执行流水线

严格按顺序执行。小任务可以合并展示中间产物，但不得跳过核验。

### 阶段 1：资料解析

1. 提取文件名、版本、日期、页码或章节。
2. 区分“招标方要求”“投标方证据”“用户指示”“建议内容”。
3. 发现扫描件识别错误、过期证照或数据冲突时记录风险，不静默修正。
4. 输出资料清单和资料缺口表。

### 阶段 2：合规与评分矩阵

建立需求响应矩阵，字段至少包括：

| ID | 类型 | 招标原文摘要 | 来源定位 | 强制性 | 分值 | 响应策略 | 证据来源 | 状态 | 风险 |
|---|---|---|---|---|---:|---|---|---|---|

类型使用：废标项、资格项、符合性项、评分项、技术项、商务项、格式项。

先列废标项和资格项，再处理评分项。状态只能使用：`已满足`、`部分满足`、`待补充`、`不适用`、`存在偏离`。

### 阶段 3：大纲与内容计划

1. 招标文件有指定目录或模板时完全沿用。
2. 没有指定结构时使用：封面、投标函、资格与商务响应、技术方案、实施与服务方案、偏离表、附件。
3. 将每个高权重评分项映射到一个明确章节。
4. 长篇正文生成前向用户展示大纲；用户已明确要求直接完成时，可继续生成，但在交付说明中列出采用的大纲假设。

### 阶段 4：正文撰写

1. 使用招标文件原有术语逐项响应。
2. 每个关键章节采用“要求—响应—实施—证据—保障”的闭环。
3. 数据和案例后保留可追溯来源；不在正式正文中暴露内部推理。
4. 表格仅承载适合比较或逐项响应的信息。
5. 图示无法生成时提供带标题的图示占位符和图示内容说明，不声称已插图。

### 阶段 5：双重审查

按 [references/compliance-review.md](references/compliance-review.md) 完成：

1. 合规审查：废标项、资格项、实质性条款、签章与格式。
2. 内容审查：覆盖率、证据完整度、数字一致性、承诺一致性。
3. 写作审查：术语、逻辑、错别字、标题层级、交叉引用。
4. 将风险分为 `阻断`、`严重`、`一般`、`提示`；存在阻断风险时不得称为终稿。

### 阶段 6：DOCX 生成与验收

1. 将定稿内容保存为 UTF-8 Markdown；表格使用标准 Markdown 表格。
2. 将封面字段保存为 JSON，可参考 `assets/example-metadata.json`。
3. 检测依赖环境。优先执行 `python -c "import docx"`；缺少依赖时，有 `uv` 则在下述命令前加 `uv run --with-requirements requirements.txt`，否则执行 `python -m pip install -r requirements.txt`。
4. 执行（标准 Python 环境）：

```powershell
python scripts/save_paper.py `
  --input paper.md `
  --output deliverables/paper.docx `
  --metadata assets/example-metadata.json `
  --config assets/default-style.json `
  --report deliverables/paper-validation.json
```

使用 `uv` 时执行：

```powershell
uv run --with-requirements requirements.txt python scripts/save_paper.py `
  --input paper.md `
  --output deliverables/paper.docx `
  --metadata assets/example-metadata.json `
  --config assets/default-style.json `
  --report deliverables/paper-validation.json
```

5. 定稿时增加 `--strict`。严格模式发现待补占位符或文档结构错误时必须失败。
6. 执行 `python scripts/validate_docx.py deliverables/paper.docx --report deliverables/docx-check.json`。
7. 确认 DOCX 可打开、非空、包含正文段落、表格结构完整，并报告剩余占位符。

## 交付物

完整任务默认交付：

1. `paper.docx`：投标响应文件；
2. `compliance-matrix.md` 或等价表格：需求响应矩阵；
3. `review-report.md`：风险、缺口、覆盖情况与定稿状态；
4. `paper-validation.json`：DOCX 生成校验结果。

最终回复必须说明：

- DOCX 的文件路径；
- 当前版本是草案、内审稿还是终稿；
- 是否存在阻断或严重风险；
- 仍需用户补充或确认的事项；
- 已执行的验证命令及结果。

不得仅输出正文文本而声称 DOCX 已交付。
