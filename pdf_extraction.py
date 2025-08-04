import pymupdf

def extract_pdf_txt(filepath):
    try:
        result = pymupdf.get_text(path=filepath, method='mp')
        
        # Handle different return types
        if isinstance(result, list):
            # Filter out None values and convert to strings
            text_parts = [str(item) for item in result if item is not None]
            return '\n\n'.join(text_parts)
        elif isinstance(result, str):
            return result
        else:
            print(f"Unexpected return type: {type(result)}")
            return str(result)
            
    except Exception as e:
        print(f"Error: {e}")
        return ""

path = "C:/Users/rocks/Developer/fin_chat/reports/consolidated.pdf"
text = extract_pdf_txt(path)
with open("reliance_raw_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

