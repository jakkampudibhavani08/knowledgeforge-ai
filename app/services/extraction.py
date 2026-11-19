import pymupdf
from pathlib import Path 
def extract_txt(file_path):
    with open(file_path,"r",encoding="UTF-8") as file:
        text= file.read()
        if not text.strip():
            raise ValueError("No extractable text found in TXT")
        return [{
            "Page_number":None,
            "text":text
        }
        ]

def extract_pdf(file_path):
    with pymupdf.open(file_path) as doc:
        text=[{"Page_number":page_num,"text":page_data.get_text()} for page_num,page_data in enumerate(doc,start=1)]
        if all(not page["text"].strip() for page in text):
            raise ValueError("No extractable text found in PDF")
        return text
    
def text_extraction(file_path):
    extension=Path(file_path).suffix.lower() 
    if extension==".txt":
        return extract_txt(file_path)
    elif extension==".pdf":
        return extract_pdf(file_path)
    else:
        raise ValueError("Unsupported file type")

