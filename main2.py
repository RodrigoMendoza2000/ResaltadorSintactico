import re


# Rodrigo Alfredo Mendoza España
# Sergio Manuel Gonzalez Vargas

# Agrega una cadena de texto para separarla por regex y agregarla a una lista para la separación de tokens
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


# Asigna a la lista generada con obtener_valores_regex los tokens definidos de asignación, suma etc... A una lista doble
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


# Lee el archivo para generar la lista de listas con todas las lineas leidas
def lexer_aritmetico(archivo):
    tokens_definidos = []

    # Leer el archivo y utilizar la funcion asignar tokens y obtener_valores_regex para hacer la lista de listas
    # de los valores con sus respectivos tokens
    with open(archivo, 'r') as archivo:
        for line in archivo:
            tokens_definidos.append(asignar_tokens(obtener_valores_regex(line)))

    return tokens_definidos


# nuestra gramatica consiste de dos aspectos
# El primero es la asignación de variables mientras que el segundo es puro comentario
def gramatica():
    if tokens[t][1] == "Variable" and tokens[t + 1][1] == "Asignacion":
        match("Variable")
        match("Asignacion")
        E()
    elif tokens[t][1] == "Comentario":
        match("Comentario")
    else:
        raise Exception


## Aplica recursión para que se sigan matcheando los tokens con las definiciones validas
def E():
    if t >= len(tokens):
        pass
    else:
        if tokens[t][1] == "Suma":  # Para las sumas +
            match("Suma")
            E()
        elif tokens[t][1] == "Resta":  # Para las restas -
            match("Resta")
            E()
        elif tokens[t][1] == "Multiplicacion":  # Para las multiplicaciones *
            match("Multiplicacion")
            E()
        elif tokens[t][1] == "Division":  # para las divisiones /
            match("Division")
            E()
        elif tokens[t][1] == "Potencia":  # Para las potencias ^
            match("Potencia")
            E()
        elif tokens[t][1] == "Parentesis_que_abre":
            # Matchea primero un parentesis que abre y aplica recursión hasta encontrar un parentesis que cierra y
            # vuelve a aplicar recursión. Así haciendo que un parentesis siempre se cierre
            match("Parentesis_que_abre")
            E()
            match("Parentesis_que_cierra")
            E()
        elif tokens[t][1] == "Real":  # Para numeros reales (ex. 1.1)
            match("Real")
            E()
        elif tokens[t][1] == "Entero":  # Para numeros enteros (ex. 5)
            match("Entero")
            E()
        elif tokens[t][1] == "Variable":  # Para variables (ex. a_2)
            match("Variable")
            E()
        elif tokens[t][1] == "no_valido":  # Para todos los otros caracteres no validos (ex. ?)
            raise Exception
        elif tokens[t][1] == "Comentario":  # Para todos los comentarios //
            match("Comentario")
        else:
            pass


# Si existe una verificación valida, aumenta el valor de t para que siga aplicando E()
def match(c):
    global t
    if tokens[t][1] == c:
        t += 1
    else:
        raise Exception


# Lee todo el archivo para utilizar el lexer_aritmetico y aplicar toda la gramatica
# Igualmente, si detecta un error en la gramatica, convierte todos los tokens en Error para el color en CSS
def start(archivo):
    lectura_lexer = lexer_aritmetico(archivo)
    tokens_corregidos = []
    # Por cada linea en el archivo txt, aplica la gramatica
    for linea in lectura_lexer:
        global tokens
        global t

        t = 0
        tokens = []

        try:
            tokens = linea
            gramatica()
            if t < len(tokens):
                raise Exception
        except Exception:
            for token in linea:
                token[1] = "ERROR"
        tokens_corregidos.append(tokens)
    return tokens_corregidos


# Lee los tokens con sus definiciones y los escribe en archivos html y css
def html_css(archivo):
    listado_tokens = start(archivo)
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
                # print(f"{tok[0]}, {tok[1]}")
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
        css.write(".ERROR{background-color:red}")


def main(archivo):
    html_css(archivo)


main('archivo.txt')