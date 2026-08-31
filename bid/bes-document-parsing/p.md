在当前工作目录下，创作文档解析技能，能够支持： pdf文档，word格式文档，excel格式文档，ppt格式文档 进行解析，文档解析、文档抽取、版面识别、OCR识别、非结构化数据处理、表格抽取等，最后输出md格式文档。
文档中含有图片，需要使用ocr配置的服务进行ocr内容识别提取。

文档中可能包含： 文本，图片，表格。

可参考网上已有的技能：
https://github.com/virgiliojr94/book-to-skill
https://github.com/firecrawl/anydoc

目标：生成可用、好用的文档解析技能，先梳理学习已有的方案，再定制化技能实现方案，最后再根据方案进行开发


## baidu ocr
$env:OCR_SERVICE_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
$env:OCR_PROVIDER = "baidu"
$env:BAIDU_API_KEY = ""
$env:BAIDU_SECRET_KEY = ""