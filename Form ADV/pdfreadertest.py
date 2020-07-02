import os
import sys
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import time


def clear_text():
   open("../PDFs-TextExtract/output/Output.txt", "w").close()
   
#writelines function
def writelines(self, lines):
    self._checkClosed()
    for line in lines:
       self.write(line)

#PDF to text Function. 
def pdf_to_text(path):
    manager = PDFResourceManager()
    retstr = BytesIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(manager, retstr, laparams=layout)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(manager, device)

    for page in PDFPage.get_pages(filepath, caching=False, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    filepath.close()
    device.close()
    retstr.close()
    return text

start_time = time.time()

crd = '161709'
text_output = pdf_to_text(crd + '.pdf') #Extract text with PDF_to_text Function call

print((time.time() - start_time) / 60, ' minutes')
start_time = time.time()

text1_output = text_output.decode("utf-8")     #Decode result from bytes to text

print((time.time() - start_time) / 60, ' minutes')
start_time = time.time()

#Save extracted text to TEXT_FILE    
with open("Output.txt", "a", encoding="utf-8") as text_file:
	text_file.writelines(text1_output)

print((time.time() - start_time) / 60, ' minutes')

