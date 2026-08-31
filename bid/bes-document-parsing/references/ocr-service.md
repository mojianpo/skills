# OCR service contract

OCR providers do not share one universal API. Select a provider first:

```powershell
$env:OCR_PROVIDER = "generic"
```

The parser first reads `config/.env` in the current skill directory. A variable
missing there is then read from the process/system environment. On Windows,
configure system variables in System Properties > Environment Variables, then
restart the terminal or host application before running the parser. Run
`python scripts/parse_documents.py --check` to see the source and to be told if
the file or system environment cannot be accessed.

Supported values in the current version:

- `generic`: multipart HTTP endpoint; implemented
- `custom`: same request contract as `generic`; implemented for compatible self-hosted services
- `pandleocr`: PandleOCR HTTP adapter using the Eoeshop file-recognition endpoint
- `local`: reserved for a future local PaddleOCR/Tesseract adapter
- `baidu`: Baidu OCR adapter; obtains and caches an access token, or uses one supplied directly
- `aliyun`, `tencent`, `volcengine`: reserved provider names; vendor-specific adapters are not included yet

Configure an authorized HTTP endpoint for `generic` or `custom`:

```powershell
$env:OCR_SERVICE_URL = "https://ocr.example/v1/recognize"
$env:OCR_SERVICE_API_KEY = "..."
$env:OCR_SERVICE_TIMEOUT = "60"
$env:OCR_LANGUAGE = "chi_sim"
```

The script sends `multipart/form-data` with `file`, `language`, and `source`. Accepted responses are `{ "text": "..." }`, `{ "data": { "text": "..." } }`, or `{ "result": "..." }`. `OCR_SERVICE_HEADERS` may contain a JSON object for vendor-specific headers. Errors become explicit warnings, never fabricated OCR.

## PandleOCR

Configure the provider:

```powershell
$env:OCR_PROVIDER = "pandleocr"
# Optional override for a compatible or self-hosted deployment:
$env:OCR_SERVICE_URL = "https://www.eoeshop.com/ocr/recognize"
```

The adapter sends exactly one multipart field, `file`, as in:

```bash
curl -X POST https://www.eoeshop.com/ocr/recognize \
  -F "file=@your_image.png"
```

The default endpoint is `https://www.eoeshop.com/ocr/recognize`. The adapter accepts the same JSON text fields as the generic adapter: `text`, `data.text`, or `result`.

## Baidu OCR

Configure the provider and Baidu application credentials:

```powershell
$env:OCR_PROVIDER = "baidu"
$env:BAIDU_API_KEY = "..."
$env:BAIDU_SECRET_KEY = "..."
```

The variable names must be spelled exactly as shown: `OCR_PROVIDER`,
`BAIDU_API_KEY`, and `BAIDU_SECRET_KEY`. `--check` validates these variables
when `OCR_PROVIDER=baidu`; for a generic provider it validates
`OCR_SERVICE_URL` instead.

The adapter calls Baidu's OAuth endpoint with `grant_type=client_credentials`, caches the returned token for its reported lifetime (defaulting to 30 days), and sends images as Base64 form data to the standard `general_basic` endpoint. If an access token is already available, it can be supplied with `BAIDU_ACCESS_TOKEN`; `BAIDU_TOKEN_URL` and `BAIDU_OCR_URL` can override the endpoints for testing or compatible deployments.
