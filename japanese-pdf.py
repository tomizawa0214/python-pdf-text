from PIL import Image
import sys

import pyocr
import pyocr.builders

from pdf2image import convert_from_path
import re

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))

lang_num=1
lang = langs[lang_num]
print("Will use lang '%s'" % (lang))

input_file = input('ファイルのパスを入力してください。')

texts = []
if '.pdf' in input_file:
    pages = convert_from_path(input_file)
    for page in pages:
        txt = tool.image_to_string(
            page,
            lang=lang,
            builder=pyocr.builders.TextBuilder(tesseract_layout=3)
        )
        texts.append(txt)
else:
    txt = tool.image_to_string(
        Image.open(input_file),
        lang=lang,
        builder=pyocr.builders.TextBuilder(tesseract_layout=3)
        )
    texts.append(txt)

for txt in texts:
    txt = re.sub('([あ-んア-ン一-龥ー])\s+((?=[あ-んア-ン一-龥ー]))',
    r'\1\2', txt)
    print(''*40)
    print( txt )
    print('-'*40)