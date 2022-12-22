import os
import re  # Para expresiones regulares
import sys  # Para interactuar con el sistema operativo

# Método para convertir el árbol a una forma más legible
def parse_syntax_tree(tree):
    parsed_tree = ""
    for node in tree:
        if isinstance(node, list):
            parsed_tree += parse_syntax_tree(node)
        else:
            parsed_tree += node + " "
    return parsed_tree

# Implementación del analizador léxico
def lexical_analyzer(code):
    # Expresiones regulares para tokenizar el código de entrada
    tokens_regex = [
        (r'^(\s+)',              None), # Esoacio en blanco
        (r'^(#.*)',              None), # Comentarios
        (r"\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|inline|int|long|register|restrict|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|main)\b", 'KEYWORD'),
        (r'^(int|float|char)',   'TYPE'), # Tipos de datos
        (r'^("[^"]*")',          'STRING'), # Strings
        (r"[(){}\[\],;:=<>+-/*&|^~%!]", 'PUNCTUATION'), # Puntuación
        (r'^([0-9]+(\.[0-9]+)?)', 'NUMBER'), # Números
        (r'^([A-Za-z_][A-Za-z0-9_]*)', 'IDENTIFIER'), # Identifiers
        (r'^(\+|-|\*|/)',        'OPERATOR') # Operadores
    ]
    
    tokens = []
    code = code.strip()
    
    while code:
        for regex, token_type in tokens_regex:
            match = re.match(regex, code)
            if match:
                token_value = match.group(0)
                tokens.append((token_type, token_value))
                code = code[len(token_value):].strip()
                break
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = open(dir_path + "\lexic_output.txt", "w")
    file.write(str(tokens))
    lista = []
    for par in tokens:
        lista.append(par[1])
    return lista

def syntax_analyzer(tokens):
  syntax_tree = []
  errors = []

  # Inicializa al automata en el estado 
  state = 0

  for token in tokens:
    # Checkear estado actual y avanzar al siguiente basado en el token
    if state == 0:
      if token == "int":
        state = 1
      else:
        errors.append("Expected int, got {}".format(token))
    elif state == 1:
      if token == "main":
        state = 2
      else:
        errors.append("Expected main, got {}".format(token))
    elif state == 2:
      if token == "(":
        state = 3
      else:
        errors.append("Expected '(', got {}".format(token))
    elif state == 3:
      if token == ")":
        state = 4
      else:
        errors.append("Expected ')', got {}".format(token))
    elif state == 4:
      if token == "{":
        state = 5
      else:
        errors.append("Expected '{', got {}".format(token))
    elif state == 5:
      if token == "}":
        # Fin de la función principal, se agrega al árbol y se vuelve al estado inicial
        syntax_tree.append(["main", []])
        state = 0
      else:
        syntax_tree.append([token, []])

  return syntax_tree, errors

	# Programa principal
if __name__ == "__main__":
    # Lee el código de entrada C desde un archivo
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    with open(dir_path + "\Input6.c", "r") as file:
        input_string = file.read()

    # Se ejecutan los analizadores léxicos y sintácticos
    tokens = lexical_analyzer(input_string)

    syntax_tree, error_message = syntax_analyzer(tokens)

    # Se reescribe el árbol sintáctico de forma más legible
    parsed = parse_syntax_tree(syntax_tree)
    file = open(dir_path + "\parsed_tree.txt", "w")
    file.write(parsed)

    # Se escribe la salida a un archivo .txt
    with open(dir_path + "\syntax_output.txt", "w") as file:
        if syntax_tree:
            file.write("Árbol Sintáctico:\n")
            file.write(str(syntax_tree))
        else:
            file.write("Error:\n")
            file.write(str(error_message))