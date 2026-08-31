# Parser backend guide

`auto` is recommended.

| Content | Preferred | Fallback |
|---|---|---|
| PDF | Docling, if installed | PyMuPDF |
| DOCX | Docling, if installed | python-docx |
| XLSX | Docling, if installed | openpyxl |
| PPTX | Docling, if installed | python-pptx |
| Legacy Office | LibreOffice headless | — |

```powershell
pip install docling pymupdf python-docx openpyxl python-pptx requests
```

The script does not install packages automatically.
