import ast

def parser(sciezka_do_pliku):
    with open(sciezka_do_pliku, "r", encoding="utf-8") as f:
        kod_zrodlowy = f.read()

    drzewo = ast.parse(kod_zrodlowy)
    wyniki = []

    for wezel in ast.walk(drzewo):
        if isinstance(wezel, (ast.FunctionDef, ast.ClassDef)):
            fragment = ast.get_source_segment(kod_zrodlowy, wezel)
            
            if fragment:
                wyniki.append(fragment)

    return wyniki

