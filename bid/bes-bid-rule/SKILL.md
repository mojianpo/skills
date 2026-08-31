---
name: bes-bid-rule
description: 根据用户上传或指定的标书审核规则，提取规则字段并返回结构化 JSON；未指定规则时使用 data/rules.xlsx。
---

# 标书规则技能

## 规则来源

按以下优先级选择规则：用户明确指定的规则内容；用户上传或指定的 Excel 规则文件；本技能目录下的 `data/rules.xlsx`。用户指定的规则只覆盖规则来源，不改变输出字段。若同时给出多份规则且无法确定，应说明冲突，不要静默合并。

## 处理流程

1. 确定规则来源，并记录来源类型和文件路径（如适用）。
2. 读取 Excel 中的每个工作表，默认第一行为表头。
3. 提取 `审核模块`、`审核项`、`审核要点`、`规则名称`、`风险等级`、`规则类型`、`关联模版`、`规则描述`。
4. Excel 中连续规则行的空白单元格继承最近一条非空值；完全没有 `规则名称` 和 `规则描述` 的空行不输出。
5. 保留原始文字、换行和风险等级，不根据常识补写或改写规则描述。
6. 规则提取本身不判定合格/不合格；需要执行审核时，再将提取出的规则与标书证据交给审核流程。

## 输出格式

只能返回可被标准 JSON 解析器直接解析的对象，不要添加 Markdown 或解释性前后缀：

```json
{
  "rule_source": {"type": "user_file", "path": "rules.xlsx"},
  "rules": [{
    "sheet_name": "rules", "row_number": 2,
    "audit_module": "模块一：投标人资格合规审核", "audit_item": "营业执照",
    "audit_point": "扫描件清晰，有效期内", "rule_name": "企业名称一致性",
    "risk_level": "P0", "rule_type": "业务检查",
    "related_template": "商务投标文件", "rule_description": "检查投标文件中每处的企业名称均一致。"
  }]
}
```

Excel 表头与 JSON 字段映射为：`审核模块`→`audit_module`、`审核项`→`audit_item`、`审核要点`→`audit_point`、`规则名称`→`rule_name`、`风险等级`→`risk_level`、`规则类型`→`rule_type`、`关联模版`→`related_template`、`规则描述`→`rule_description`。

`rule_source.type` 取 `user_text`、`user_file` 或 `default_file`。用户只提供文本规则时，按同一字段契约提取；无法确定的字段使用空字符串，不得臆造。

## 本地解析入口

```powershell
python scripts/parse_rules.py
python scripts/parse_rules.py --rules C:\path\to\rules.xlsx
```

脚本默认输出 JSON 到标准输出；输入文件不存在、无法读取、缺少必要表头或没有有效规则时必须报错并以非零状态退出。
