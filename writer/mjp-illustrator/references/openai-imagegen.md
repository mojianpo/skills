# `openai-api` OpenAI 协议文生图调用

Load this reference only when the [图片生成工具](../SKILL.md#图片生成工具) rule has resolved to `openai-api` — i.e., the skill-root `config.json` is complete and the user has not overridden the backend.

## 配置发现

读取与 `SKILL.md` 同级的 `config.json`（本技能目录根）：

```json
{
  "api_key": "ark-xxxx",
  "base_url": "https://ark.cn-beijing.volces.com/api/plan/v3",
  "model": "doubao-seedream-5.0-pro"
}
```

| 字段 | 用途 |
|------|------|
| `api_key` | `Authorization: Bearer` 凭证 |
| `base_url` | OpenAI 兼容根地址（无尾部斜杠）；接口为 `{base_url}/images/generations` |
| `model` | 文生图模型 ID（当前配置为火山方舟 doubao-seedream） |

- 三个字段**齐全**才走此后端；缺失任一字段 → 落入解析顺序的下一级后端（仅当后续也没有可用后端时询问用户）。
- **绝不**把 `api_key` 打印给用户或写入提示文件、日志。

## 调用（每张图一次请求）

```bash
curl -sS -m 300 -X POST "{base_url}/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {api_key}" \
  -d '{
    "model": "{model}",
    "prompt": "{提示文件正文}",
    "size": "{WxH}",
    "response_format": "b64_json",
    "output_format": "png",
    "watermark": false
  }'
```

请求字段：

| 字段 | 取值 |
|------|------|
| `prompt` | 提示文件剥去 YAML frontmatter 后的正文（不要用临时内联提示） |
| `size` | 由提示中的 `ASPECT` 换算，见下表 |
| `response_format` | 固定 `"b64_json"`（避免外链下载与过期） |
| `output_format` | 固定 `"png"`。**已验证**：doubao-seedream-5.0-pro 不传此项时返回 JPEG 字节 |
| `watermark` | 固定 `false`；水印由本技能的提示词方案处理（EXTEND.md 启用时） |

`ASPECT` → `size` 默认表（长边 2048）：

| ASPECT | size |
|--------|------|
| `1:1` | `2048x2048` |
| `16:9` | `2048x1152` |
| `9:16` | `1152x2048` |
| `4:3` | `2048x1536` |
| `3:4` | `1536x2048` |
| `21:9` | `2560x1088` |
| 其他 | 长边 2048，两边各取 8 的倍数 |

## 响应与落盘

```json
{"model": "...", "created": 1791787371, "data": [{"b64_json": "<base64 PNG>"}]}
```

取 `data[0].b64_json`，base64 解码后写入该任务的输出路径（`{output-dir}/NN-{type}-{slug}.png`）。`data` 或 `data[0].b64_json` 缺失视为失败。

## 批量语义

- 该接口**无原生批量**：每张图一次 HTTP 请求。按 `## 批量生成策略` 使用运行时并行调用，每批最多 `generation_batch_size` 张。
- 失败任务从同一提示文件重试一次；成功任务不重发。

## 参考图片

此接口为纯文生图，不接受参考图输入。按 workflow 步骤 5.3 处理：`style` / `palette` 用法照常转成文字；`direct` 用法降级为文字描述并入 prompt，并在完成后向用户说明该降级。

## 错误处理

| 情况 | 操作 |
|------|------|
| HTTP 401 / 403 | 鉴权失败，直接报告用户（检查 `config.json` 的 `api_key`），不要重试 |
| HTTP 400（size/参数非法） | 按报错调整参数后重试一次 |
| HTTP 429 / 5xx / 超时 | 重试一次 |
| 重试后仍失败 | 询问用户：换下一级后端还是终止。不要静默切换 |

## 验证记录

以下行为已在本配置上实测通过（doubao-seedream-5.0-pro）：`{base_url}/images/generations` + `response_format: b64_json` + `output_format: png` 返回 PNG（magic `89504e47`）；`size: 2048x1152` 被接受。
