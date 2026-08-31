#!/usr/bin/env python3
"""Deterministic PDF/Office/image -> Markdown converter with optional OCR HTTP adapter."""
from __future__ import annotations
import argparse, base64, json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

EXTS = {'.pdf','.doc','.docx','.xls','.xlsx','.ppt','.pptx','.png','.jpg','.jpeg','.tif','.tiff','.bmp'}
_BAIDU_TOKEN = None
_ENV_FILE = Path(__file__).resolve().parent.parent / 'config' / '.env'
_ENV_FILE_VALUES = {}
_ENV_FILE_ERROR = None

def load_env_file():
    global _ENV_FILE_VALUES, _ENV_FILE_ERROR
    if not _ENV_FILE.exists():
        return
    try:
        for raw in _ENV_FILE.read_text(encoding='utf-8-sig').splitlines():
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('export '):
                line = line[7:].lstrip()
            if '=' not in line:
                continue
            name, value = line.split('=', 1)
            name, value = name.strip(), value.strip()
            if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', name):
                continue
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            _ENV_FILE_VALUES[name] = value
    except (OSError, UnicodeError) as e:
        _ENV_FILE_ERROR = str(e)

load_env_file()

def config(name, default=None):
    value = _ENV_FILE_VALUES.get(name)
    if value:
        return value
    try:
        return os.getenv(name, default)
    except OSError as e:
        raise RuntimeError(f'Cannot access system environment variable {name}: {e}') from e

def config_source(name):
    if _ENV_FILE_VALUES.get(name):
        return 'config/.env'
    try:
        return 'system environment' if os.getenv(name) else 'not configured'
    except OSError:
        return 'system environment (access denied)'

def optional(name):
    try: return __import__(name)
    except ImportError: return None

def esc(v): return str(v if v is not None else '').replace('|','\\|').replace('\n','<br>')
def table(rows):
    rows = [[esc(x) for x in r] for r in rows if any(str(x or '').strip() for x in r)]
    if not rows: return ''
    n = max(len(r) for r in rows); rows = [r + ['']*(n-len(r)) for r in rows]
    return '| ' + ' | '.join(rows[0]) + ' |\n| ' + ' | '.join(['---']*n) + ' |\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in rows[1:])

def baidu_access_token(requests):
    global _BAIDU_TOKEN
    configured = config('BAIDU_ACCESS_TOKEN')
    if configured:
        return configured
    if _BAIDU_TOKEN and time.time() < _BAIDU_TOKEN[1]:
        return _BAIDU_TOKEN[0]
    api_key = config('BAIDU_API_KEY')
    secret_key = config('BAIDU_SECRET_KEY')
    if not api_key or not secret_key:
        raise RuntimeError('BAIDU_API_KEY and BAIDU_SECRET_KEY are required')
    response = requests.post(
        config('BAIDU_TOKEN_URL', 'https://aip.baidubce.com/oauth/2.0/token'),
        params={'grant_type': 'client_credentials', 'client_id': api_key, 'client_secret': secret_key},
        headers={'Accept': 'application/json'},
        timeout=float(config('OCR_SERVICE_TIMEOUT', '60')),
    )
    response.raise_for_status()
    data = response.json()
    if data.get('error') or not data.get('access_token'):
        raise RuntimeError('Baidu access_token response did not contain a token')
    expires_in = int(data.get('expires_in', 2592000))
    _BAIDU_TOKEN = (data['access_token'], time.time() + max(0, expires_in - 300))
    return _BAIDU_TOKEN[0]

def baidu_ocr(path, requests):
    with open(path, 'rb') as f:
        image = base64.b64encode(f.read()).decode('ascii')
    response = requests.post(
        config('BAIDU_OCR_URL', 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'),
        params={'access_token': baidu_access_token(requests)},
        data={'image': image},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        timeout=float(config('OCR_SERVICE_TIMEOUT', '60')),
    )
    response.raise_for_status()
    data = response.json()
    if data.get('error_code'):
        raise RuntimeError(f"Baidu OCR error {data['error_code']}: {data.get('error_msg', 'unknown error')}")
    return '\n'.join(item.get('words', '') for item in data.get('words_result', []) if item.get('words'))

def pandleocr_ocr(path, requests):
    with open(path, 'rb') as f:
        response = requests.post(
            config('OCR_SERVICE_URL', 'https://www.eoeshop.com/ocr/recognize'),
            files={'file': (Path(path).name, f)},
            timeout=float(config('OCR_SERVICE_TIMEOUT', '60')),
        )
    response.raise_for_status()
    data = response.json()
    return data.get('text') or data.get('result') or (data.get('data') or {}).get('text', '')

def ocr(path, source):
    provider = config('OCR_PROVIDER', 'generic').lower()
    if provider == 'baidu':
        try:
            import requests
            text = baidu_ocr(path, requests).strip()
            return text, '' if text else 'Baidu OCR response contained no text'
        except Exception as e: return '', f'Baidu OCR failed: {e}'
    if provider == 'pandleocr':
        try:
            import requests
            text = pandleocr_ocr(path, requests).strip()
            return text, '' if text else 'PandleOCR response contained no text'
        except Exception as e: return '', f'PandleOCR failed: {e}'
    if provider in {'aliyun', 'tencent', 'volcengine', 'local'}:
        return '', f'OCR provider "{provider}" is declared but its adapter is not implemented'
    if provider not in {'generic', 'custom'}:
        return '', f'Unsupported OCR_PROVIDER: {provider}'
    url = config('OCR_SERVICE_URL')
    if not url: return '', 'OCR_SERVICE_URL is not configured'
    try:
        import requests
        headers = json.loads(config('OCR_SERVICE_HEADERS','{}'))
        if config('OCR_SERVICE_API_KEY'): headers.setdefault('Authorization','Bearer '+config('OCR_SERVICE_API_KEY'))
        with open(path, 'rb') as f:
            r = requests.post(url, files={'file': (Path(path).name, f)}, data={'source':source, 'language':config('OCR_LANGUAGE','')}, headers=headers, timeout=float(config('OCR_SERVICE_TIMEOUT','60')))
        r.raise_for_status(); data = r.json()
        text = data.get('text') or data.get('result') or (data.get('data') or {}).get('text','')
        return str(text).strip(), '' if text else 'OCR response contained no text'
    except Exception as e: return '', f'OCR failed: {e}'

def extract_images_zip(src, assets, prefix):
    import zipfile
    found=[]
    try:
        with zipfile.ZipFile(src) as z:
            names=[n for n in z.namelist() if re.search(r'\.(png|jpe?g|gif|bmp|tiff?)$',n,re.I)]
            for i,n in enumerate(names,1):
                out=assets/f'{prefix}-image-{i}{Path(n).suffix.lower()}'; out.write_bytes(z.read(n)); found.append(out)
    except zipfile.BadZipFile: pass
    return found

def pdf_parse(src, assets):
    fitz=optional('fitz'); parts=[]; imgs=[]; warnings=[]
    if not fitz: return '', [], ['Install pymupdf for PDF parsing']
    doc=fitz.open(src)
    for i,page in enumerate(doc,1):
        text=page.get_text('text').strip()
        blocks=[f'## Page {i}\n', text]
        for j,im in enumerate(page.get_images(full=True),1):
            raw=doc.extract_image(im[0]); out=assets/f'page-{i}-image-{j}.{raw["ext"]}'; out.write_bytes(raw['image']); imgs.append(out)
            t,w=ocr(out,f'page {i} image {j}')
            blocks += [f'\n### Image {j}\n![Page {i} image {j}]({assets.name}/{out.name})\n']
            if t: blocks += [f'\n#### OCR (page {i}, image {j})\n\n{t}\n']
            elif w: warnings.append(w)
        if not text:
            pix=page.get_pixmap(matrix=fitz.Matrix(2,2), alpha=False); out=assets/f'page-{i}-render.png'; pix.save(out); imgs.append(out)
            t,w=ocr(out,f'page {i} rendered page')
            if t: blocks += [f'\n### OCR (page {i})\n\n{t}\n']
            else: warnings.append(f'Page {i}: no text layer; {w}')
        parts.append('\n'.join(x for x in blocks if x))
    return '\n\n'.join(parts),imgs,warnings

def office_convert(src):
    if src.suffix.lower() in {'.doc','.xls','.ppt'}:
        lo=shutil.which('soffice') or shutil.which('libreoffice')
        if not lo: raise RuntimeError('Legacy Office format requires LibreOffice (soffice)')
        d=Path(tempfile.mkdtemp(prefix='docparse-')); subprocess.run([lo,'--headless','--convert-to',{'.doc':'docx','.xls':'xlsx','.ppt':'pptx'}[src.suffix.lower()], '--outdir',str(d),str(src)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return next(d.iterdir())
    return src

def docx_parse(src, assets):
    mod=optional('docx');
    if not mod: raise RuntimeError('Install python-docx for DOCX parsing')
    d=mod.Document(src); out=[f'# {src.stem}']; warnings=[]
    for p in d.paragraphs:
        if p.text.strip(): out.append(p.text)
    for i,t in enumerate(d.tables,1): out += [f'## Table {i}\n'+table([[c.text for c in row.cells] for row in t.rows])]
    for p in extract_images_zip(src,assets,src.stem):
        out.append(f'\n## Image\n![{p.name}]({assets.name}/{p.name})'); text,w=ocr(p,p.name)
        if text: out.append(f'\n### OCR ({p.name})\n{text}')
        elif w: warnings.append(f'{p.name}: {w}')
    return '\n\n'.join(out), warnings

def xlsx_parse(src, assets):
    mod=optional('openpyxl');
    if not mod: raise RuntimeError('Install openpyxl for XLSX parsing')
    wb=mod.load_workbook(src,data_only=False); out=[f'# {src.stem}']
    for ws in wb.worksheets:
        rows=[[c.value for c in r] for r in ws.iter_rows()]
        if any(any(x is not None for x in r) for r in rows): out.append(f'## Sheet: {ws.title}\n'+table(rows))
    return '\n\n'.join(out), []

def pptx_parse(src, assets):
    mod=optional('pptx');
    if not mod: raise RuntimeError('Install python-pptx for PPTX parsing')
    prs=mod.Presentation(src); out=[f'# {src.stem}']; warnings=[]
    for i,slide in enumerate(prs.slides,1):
        texts=[sh.text for sh in slide.shapes if hasattr(sh,'text') and sh.text.strip()]
        out.append(f'## Slide {i}\n'+'\n\n'.join(texts))
    for p in extract_images_zip(src,assets,src.stem):
        out.append(f'\n## Image\n![{p.name}]({assets.name}/{p.name})'); text,w=ocr(p,p.name)
        if text: out.append(f'\n### OCR ({p.name})\n{text}')
        elif w: warnings.append(f'{p.name}: {w}')
    return '\n\n'.join(out), warnings

def parse_one(src, outdir, backend):
    assets=outdir/(src.stem+'_assets'); assets.mkdir(parents=True,exist_ok=True); work=office_convert(src); ext=work.suffix.lower(); warnings=[]; images=[]
    if backend == 'docling':
        docling=optional('docling')
        if not docling: raise RuntimeError('Docling backend requested but docling is not installed')
        from docling.document_converter import DocumentConverter
        md=DocumentConverter().convert(str(work)).document.export_to_markdown()
        for p in extract_images_zip(work,assets,src.stem):
            images.append(p); t,w=ocr(p,p.name); md += f'\n\n## Image\n![{p.name}]({assets.name}/{p.name})'
            if t: md += f'\n\n### OCR ({p.name})\n{t}'
            elif w: warnings.append(f'{p.name}: {w}')
    elif ext=='.pdf': md,images,warnings=pdf_parse(work,assets)
    elif ext=='.docx': md,w=docx_parse(work,assets); warnings += w
    elif ext=='.xlsx': md,_=xlsx_parse(work,assets)
    elif ext=='.pptx': md,w=pptx_parse(work,assets); warnings += w
    elif ext in {'.png','.jpg','.jpeg','.tif','.tiff','.bmp'}:
        out=assets/src.name; shutil.copy2(src,out); t,w=ocr(out,src.name); md=f'# {src.stem}\n\n![{src.name}]({assets.name}/{out.name})\n\n## OCR\n\n{t or "[OCR unavailable]"}'; warnings += [w] if w else []
    else: raise RuntimeError(f'Unsupported format: {src.suffix}')
    status='partial' if warnings else 'complete'; md=f'---\nsource: {src.name}\nformat: {ext[1:]}\nstatus: {status}\n---\n\n'+md
    target=outdir/(src.stem+'.md'); target.write_text(md+'\n\n<!-- warnings: '+('; '.join(warnings) if warnings else 'none')+' -->\n',encoding='utf-8')
    return {'source':str(src),'output':str(target),'status':status,'warnings':warnings,'images':len(images)}

def main():
    ap=argparse.ArgumentParser(description='Parse PDF/Office/image files to Markdown')
    ap.add_argument('inputs',nargs='*'); ap.add_argument('-o','--output',default='parsed-markdown'); ap.add_argument('--manifest'); ap.add_argument('--backend',choices=['auto','native','docling'],default='auto'); ap.add_argument('--check',action='store_true')
    a=ap.parse_args()
    if a.check:
        for n in ['fitz','docx','openpyxl','pptx','requests']: print(f'{n}: {"installed" if optional(n) else "missing"}')
        provider = config('OCR_PROVIDER', 'generic').lower()
        if _ENV_FILE_ERROR:
            print('config/.env: unreadable -', _ENV_FILE_ERROR)
        print('config/.env:', 'loaded' if _ENV_FILE_VALUES else ('not found' if not _ENV_FILE.exists() else 'empty'))
        print('OCR_PROVIDER:', provider)
        if provider == 'baidu':
            for name in ['BAIDU_ACCESS_TOKEN', 'BAIDU_API_KEY', 'BAIDU_SECRET_KEY']:
                print(f'{name}: {"configured" if config(name) else "not configured"} ({config_source(name)})')
            ready = bool(config('BAIDU_ACCESS_TOKEN') or (config('BAIDU_API_KEY') and config('BAIDU_SECRET_KEY')))
        elif provider == 'pandleocr':
            print('OCR_SERVICE_URL:', config('OCR_SERVICE_URL', 'https://www.eoeshop.com/ocr/recognize'), f'({config_source("OCR_SERVICE_URL") if config("OCR_SERVICE_URL") else "default"})')
            ready = True
        elif provider in {'generic', 'custom'}:
            print('OCR_SERVICE_URL:', 'configured' if config('OCR_SERVICE_URL') else 'not configured', f'({config_source("OCR_SERVICE_URL")})')
            ready = bool(config('OCR_SERVICE_URL'))
        else:
            ready = False
        print('OCR configuration:', 'ready' if ready else 'incomplete')
        return 0 if ready else 1
    if not a.inputs: ap.error('provide files/directories, or use --check')
    files=[]
    for item in a.inputs:
        p=Path(item)
        files += [x for x in (p.rglob('*') if p.is_dir() else [p]) if x.is_file() and x.suffix.lower() in EXTS]
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True); results=[]
    for f in files:
        try: results.append(parse_one(f,out,a.backend))
        except Exception as e: results.append({'source':str(f),'status':'failed','error':str(e)})
    manifest=Path(a.manifest) if a.manifest else out/'manifest.json'; manifest.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(results,ensure_ascii=False,indent=2)); return 1 if any(x['status']=='failed' for x in results) else 0
if __name__=='__main__': sys.exit(main())
