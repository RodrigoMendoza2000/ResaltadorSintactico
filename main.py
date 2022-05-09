import re


# Separa en diferentes valores en una lista los diferentes tokens que tenemos
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


# En una lista de listas, agrega el token con su apropiada definición
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


# Lee los archivos para obtener una lista de listas de los tokens con su definicion
def lexer_aritmetico(archivo):
    tokens_definidos = []

    # Leer el archivo y utilizar la funcion asignar tokens y obtener_valores_regex para hacer la lista de listas
    # de los valores con sus respectivos tokens
    with open(archivo, 'r') as archivo:
        for line in archivo:
            tokens_definidos.append(asignar_tokens(obtener_valores_regex(line)))

    print(tokens_definidos)
    return tokens_definidos


def lex(line):
    tokens_definidos = []
    tokens_definidos.append(asignar_tokens(obtener_valores_regex(line)))

    return tokens_definidos


def start(line):
    preGramatica(lex(line))


def preGramatica(line):
    # Variable, asignacion, exprecion,
    for tokens in line:
        iter = 0
        gramaticalist = []
        for token in tokens:
            print(f"elemento: {token[0]} , tipo: {token[1]}")
            token = token[1]
            gramaticalist.append(gramatica(token, iter, tokens))
            iter += 1


def gramatica(token, iter, tokens):
    if (iter == 0):
        if token == "Variable":
            return (True)
        elif token == "Comentario":
            return (True)
        elif token == "Comentario":
            return (True)

    elif (iter == 1):
        if token == "Asignacion":
            return (True)
    elif (iter == 2):
        if token == "Real" or token == "Entero" or token == "Parentesis_que_abre":
            # llamar a los tokens
            # movernos hasta el token del if
            # contar a partir de ahi
            # contar hasta el final o //  o valor no valido

            tok = []

            for token in tokens:
                if (token[1] == "Real" or token[1] == "Entero" or token[1] == "Cometario"):
                    tok.append(token[1])
                elif (token[1] == "no_valido"):
                    return (False)
                else:
                    continue

            global exp
            exp = []
            e(tok)

    elif (iter == 3):
        if token == "Comentario":
            return (True)
    else:
        return (False)


def e(tok):
    expresion = ["Suma", "Resta", "Multiplicacion", "Division", "Potencia"]
    if len(tok) > 1:

        if tok[0] in expresion:
            if (exp[-1] == "Real" or exp[-1] == "Entero" or exp[-1] == "Parentesis_que_cierra"):
                exp.append(tok[0])
                tok.pop(0)
                e(tok)
            elif (exp[-1] == "Parentesis_que_abre"):
                return (False)
            else:
                return (False)

        elif ((tok[0] == "Entero" or tok[0] == "Real") and (tok[1] != "Entero" or tok[1] != "Real")):
            exp.append(tok[0])
            tok.pop(0)
            e(tok)

        elif tok[0] in expresion and tok[1] in expresion:
            return (False)

        elif tok[0] in expresion and tok[1] not in expresion:
            exp.append(tok[0])
            tok.pop(0)
            e(tok)

        elif tok[0] == "Parentesis_que_abre":
            if (tok[1] == "Entero" or tok[1] == "Real"):
                exp.append(tok[0])
                tok.pop(0)
                e(tok)
            elif (tok[1] in expresion):
                return (False)
            elif (tok[1] == "Parentesis_que_cierra"):
                return (False)

        elif tok[0] == "Parentesis_que_cierra":
            if "Parentesis_que_abre" in exp:
                exp.append(tok[0])
                tok.pop(0)
                e(tok)
            else:
                return (False)

        elif tok[0] == "Comentario":
            if (exp[-1] == "parentesis_que_abre" or exp[-1] in expresion):
                return (False)
            else:
                return (True)
        else:
            return (True)
    else:
        if tok[0] in expresion:
            return ("L_Error")
        elif tok[0] == "Entero" or tok[0] == "Real":
            return (True)
        elif tok[0] == "Parentesis_que_abre":
            return (False)
        elif tok[0] == "Parentesis_que_cierra":
            if "Parentesis_que_abre" in exp:
                return (True)
        if tok[0] == "Comentario":
            return (False)


# De nuestra lista de listas con nuestros tokens y definiciones, se crean archivos html y css
# Aplicando diferentes estilos de css
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
        css.write(".no_valido{background-color: red;}")


html_css('archivo.txt')
