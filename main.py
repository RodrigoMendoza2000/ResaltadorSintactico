import re


def obtener_valores_regex(texto):
    # Quitar espacios varios y saltos de linea
    texto = texto.replace("\n", "")
    # Encontrar los comentarios antes de quitar los espacios
    comentario = re.findall("\/{1}\/{1}.*", texto)
    texto = re.sub("\/{1}\/{1}.*", "", texto)
    texto = texto.replace(" ", "")
    # instrucciones regex con el siguiente orden:
    # 1. Comentarios 2. Reales 3. Variables 4. Enteros 5. Multiplicación 6. Suma 7. Resta 8. Parentesis que abre
    # 9. Parentesis que cierra 10. Division 11. Potencia 12. Asignacion
    lista_tokens = re.findall("\d*\.\d*|[A-Za-z]+[\d_]*|[0-9]+|\*|\+|\-|\(|\)|\/{1}|\^|\=|.", texto)
    lista_tokens += comentario

    return lista_tokens


def asignar_tokens(lista_valores):
    valores_tokenizados = []
    tokens_definicion = {
        "=": "Asignacion",
        "+": "Suma",
        "-": "Resta",
        "*": "Multiplicacion",
        "/": "Division",
        "^": "Potencia",
        "(": "Parentesis_que_abre",
        ")": "Parentesis_que_cierra",
    }

    for valor in lista_valores:
        # Si el valor se encuentra en el diccionario, conseguir el valor del diccionario
        if valor in tokens_definicion:
            valores_tokenizados.append([valor, tokens_definicion.get(valor)])
        # Si no se encuentra en el diccionario, hacer serie de ifs para asignarle token
        elif "//" in valor:
            valores_tokenizados.append([valor, "Comentario"])
        elif "." in valor and "//" not in valor:
            valores_tokenizados.append([valor, "Real"])
        elif valor.isdigit():
            valores_tokenizados.append([valor, "Entero"])
        elif valor[0].isalpha():
            valores_tokenizados.append([valor, "Variable"])
        else:
            valores_tokenizados.append([valor, "no_valido"])

    return valores_tokenizados


def lexer_aritmetico(archivo):
    tokens_definidos = []

    # Leer el archivo y utilizar la funcion asignar tokens y obtener_valores_regex para hacer la lista de listas
    # de los valores con sus respectivos tokens
    with open(archivo, 'r') as archivo:
        for line in archivo:
            tokens_definidos.append(asignar_tokens(obtener_valores_regex(line)))

    return tokens_definidos


def html_css(archivo):
    listado_tokens = lexer_aritmetico(archivo)
    with open('index.html', 'w') as html:
        html.write("""<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="index.css">
</head>
<body>

""")
        for token in listado_tokens:
            html.write("<p>")
            for tok in token:
                #print(f"{tok[0]}, {tok[1]}")
                html.write(f"""<span class="{tok[1]}">{tok[0]}</span>""")
            html.write("</p>\n")
        html.write("""
</body>
</html>""")

    lista_tokens = ['Variable', 'Entero', 'Real', 'Asignacion', 'Multiplicacion', 'Parentesis_que_abre', 'Resta',
                    'Parentesis_que_cierra', 'Comentario', 'Potencia', 'no_valido', 'Division']
    colores = ['DeepPink', 'Blue', 'Green', 'Orange', 'Yellow', 'Khaki', 'Gray', 'Purple', 'Pink', 'Black',
               'Red', 'Lavender']
    with open('index.css', 'w') as css:
        for i in range(len(lista_tokens)):
            css.write(f".{lista_tokens[i]}")
            css.write("{color:")
            css.write(f"{colores[i]}")
            css.write("}\n")


html_css('archivo.txt')
