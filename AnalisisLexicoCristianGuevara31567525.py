#CRISTIAN GUEVARA 31.567.525 SECCION: 307C2
# Importamos el módulo 're' de Python que nos permite trabajar con expresiones regulares
import re

# Definición de los tokens en una lista de tuplas. Cada tupla tiene dos elementos:
# 1. El nombre del token (como 'NUMBER', 'ID', 'PLUS', etc.)
# 2. La expresión regular que coincide con ese tipo de token en el código fuente

token_specification = [
    ('NUMBER',   r'\d+'),           # Coincide con uno o más dígitos (números enteros)
    ('ASSIGN',   r'='),             # Coincide con el operador de asignación (=)
    ('END',      r';'),             # Coincide con el punto y coma (fin de una instrucción)
    ('ID',       r'[A-Za-z]+'),     # Coincide con identificadores que consisten en letras (por ejemplo, 'x', 'y', 'variable')
    ('PLUS',     r'\+'),            # Coincide con el operador de suma (+)
    ('MINUS',    r'-'),             # Coincide con el operador de resta (-)
    ('TIMES',    r'\*'),            # Coincide con el operador de multiplicación (*)
    ('DIVIDE',   r'/'),             # Coincide con el operador de división (/)
    ('LPAREN',   r'\('),            # Coincide con el paréntesis izquierdo '('
    ('RPAREN',   r'\)'),            # Coincide con el paréntesis derecho ')'
    ('SKIP',     r'[ \t\n]+'),      # Coincide con espacios en blanco, tabulaciones y saltos de línea (se ignoran)
    ('MISMATCH', r'.'),             # Coincide con cualquier otro carácter que no sea reconocido (errores léxicos)
]

# Creamos una expresión regular combinada que une todas las expresiones regulares definidas
# Usamos la notación (?P<nombre>) para nombrar cada grupo y que luego podamos referirnos a él
# de forma legible por su nombre (como 'NUMBER', 'ID', etc.)

tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

# Función principal del lexer (analizador léxico). Recibe el código fuente como entrada.
# La función usará el patrón de expresiones regulares para encontrar tokens en el código.

def lexer(code):
    line_num = 1              # Número de la línea (inicialmente 1)
    line_start = 0            # Posición de inicio de la línea (inicialmente 0)
    
    # Usamos 're.finditer' para buscar todas las coincidencias del patrón en el código
    # Esta función devuelve un objeto que contiene información sobre cada coincidencia encontrada
    
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup   # El nombre del grupo que coincide con la expresión regular (por ejemplo, 'NUMBER', 'ID')
        value = mo.group()     # El valor que coincide con esa expresión regular (el texto encontrado)
        column = mo.start() - line_start + 1  # Calculamos la columna donde comienza el token (para mostrar mejor los errores)
        
        # Si el tipo de token es 'SKIP' (espacios, tabulaciones o saltos de línea), lo ignoramos y continuamos con el siguiente token
        if kind == 'SKIP':
            continue
        # Si el token no coincide con ninguno de los definidos, lanzamos un error de sintaxis
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} inesperado en la línea {line_num}')
        
        # Si es un token válido, generamos el tipo de token y su valor para que lo podamos procesar
        yield kind, value

# Código de ejemplo para probar el lexer. Es un fragmento simple de código fuente.
# Este código se procesará para identificar los tokens como 'x', '=', '10', ';', etc.
code = """
x = 10;
y = x + 5;
"""

# Llamamos al lexer con el código de ejemplo y mostramos los tokens encontrados
# 'lexer(code)' devolverá una secuencia de tuplas con el tipo de token y su valor
for token in lexer(code):
    print(token)


 