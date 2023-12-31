def extract_text_from_pdf(pdf_file: str) -> [str]:
    import PyPDF2
    import json
    import http.client
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader (pdf, strict=False)
        pdf_text = []
        
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append (content)
        return pdf_text

def convert_CV(lien):
    import re
    
    extracted_text = extract_text_from_pdf(lien)
    CV_List = []

    for text in extracted_text:
        CV_List.append(text)

    CV_List_s = CV_List[0].splitlines()

    #Cette partie de l'algorithme est présente pour spliter les informations directement
    texte_seul = ' '.join(CV_List_s)  # Convertir la liste en une seule chaîne de texte
    texte_seul = re.sub(r'[^a-zA-ZÀ-ÖØ-öø-ÿ\s]', '', texte_seul)
    texte_seul = texte_seul.split()
    return texte_seul