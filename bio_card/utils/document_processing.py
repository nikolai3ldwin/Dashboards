import PyPDF2
import docx
import io

def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_file: File-like object (opened with open() or uploaded through Streamlit)
    
    Returns:
        str: Extracted text content
    """
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(docx_file):
    """
    Extract text from a DOCX file.
    
    Args:
        docx_file: File-like object (opened with open() or uploaded through Streamlit)
    
    Returns:
        str: Extracted text content
    """
    doc = docx.Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(txt_file):
    """
    Extract text from a TXT file.
    
    Args:
        txt_file: File-like object (opened with open() or uploaded through Streamlit)
    
    Returns:
        str: Extracted text content
    """
    return txt_file.getvalue().decode("utf-8")

def extract_text(file):
    """
    Extract text from various file formats.
    
    Args:
        file: File object uploaded through Streamlit
    
    Returns:
        str: Extracted text content or None if format not supported
    """
    file_extension = file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(file)
    elif file_extension == 'docx':
        return extract_text_from_docx(file)
    elif file_extension == 'txt':
        return extract_text_from_txt(file)
    else:
        return None
