import random
import string
import numpy as np

def normalize_word(word):
    """Normaliza una palabra quitando acentos y convirtiendo a mayúsculas."""
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ü': 'u', 'ñ': 'n', 'Á': 'A', 'É': 'E', 'Í': 'I',
        'Ó': 'O', 'Ú': 'U', 'Ü': 'U', 'Ñ': 'N'
    }
    result = word.upper()
    for original, replacement in replacements.items():
        result = result.replace(original, replacement)
    return result

def generate_word_search(size, words):
    """Genera una sopa de letras con las palabras dadas."""
    # Normalizar palabras
    normalized_words = [normalize_word(word) for word in words]
    
    # Filtrar palabras demasiado largas
    valid_words = [word for word in normalized_words if len(word) <= size]
    
    # Crear matriz vacía
    grid = np.full((size, size), '')
    
    # Direcciones posibles (horizontal, vertical, diagonal)
    directions = [
        (0, 1),   # derecha
        (1, 0),   # abajo
        (1, 1),   # diagonal abajo-derecha
        (1, -1),  # diagonal abajo-izquierda
        (0, -1),  # izquierda
        (-1, 0),  # arriba
        (-1, 1),  # diagonal arriba-derecha
        (-1, -1)  # diagonal arriba-izquierda
    ]
    
    placed_words = []
    
    # Intentar colocar cada palabra
    random.shuffle(valid_words)
    for word in valid_words:
        word_placed = False
        attempts = 0
        max_attempts = 100
        
        while not word_placed and attempts < max_attempts:
            # Seleccionar dirección aleatoria
            dx, dy = random.choice(directions)
            
            # Determinar longitud de palabra
            word_length = len(word)
            
            # Calcular límites para posición inicial
            if dx < 0:
                x_range = range(size - 1, word_length - 2, -1)
            elif dx > 0:
                x_range = range(size - word_length)
            else:
                x_range = range(size)
                
            if dy < 0:
                y_range = range(size - 1, word_length - 2, -1)
            elif dy > 0:
                y_range = range(size - word_length)
            else:
                y_range = range(size)
            
            if not x_range or not y_range:
                attempts += 1
                continue
            
            # Seleccionar posición inicial aleatoria
            x = random.choice(list(x_range))
            y = random.choice(list(y_range))
            
            # Verificar si la palabra cabe en la ubicación elegida
            fits = True
            positions = []
            
            for i in range(word_length):
                nx, ny = x + i * dx, y + i * dy
                if nx < 0 or nx >= size or ny < 0 or ny >= size:
                    fits = False
                    break
                
                if grid[nx, ny] != '' and grid[nx, ny] != word[i]:
                    fits = False
                    break
                
                positions.append((nx, ny))
            
            # Si la palabra cabe, colocarla en la matriz
            if fits:
                for i, (nx, ny) in enumerate(positions):
                    grid[nx, ny] = word[i]
                word_placed = True
                placed_words.append(word)
            else:
                attempts += 1
    
    # Rellenar espacios vacíos con letras aleatorias
    spanish_letters = string.ascii_uppercase + "Ñ"
    for i in range(size):
        for j in range(size):
            if grid[i, j] == '':
                grid[i, j] = random.choice(spanish_letters)
    
    return grid, placed_words

def save_word_search_to_file(grid, placed_words, filename="sopa_de_letras.txt"):
    """Guarda la sopa de letras en un archivo de texto."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("SOPA DE LETRAS\n")
        file.write("=" * (len(grid) * 2) + "\n")
        
        # Escribir la sopa de letras con espaciado monoespaciado
        for i in range(len(grid)):
            file.write(" ".join(grid[i]) + "\n")
        
        # Escribir las palabras a encontrar
        file.write("\nPalabras a encontrar:\n")
        file.write(", ".join(placed_words) + "\n")
    
    print(f"Sopa de letras guardada en '{filename}'")

# Configuración
grid_size = 25
words_to_find = ["HARDWARE", "MONITOR", "PIXEL", "RESOLUCION", "RGB",
                 "PROCESADOR", "MEMORIA", "GRAFICO", "PANTALLA", "USB",
                 "TECLADO", "IMAGEN", "BRILLO", "CONTRASTE", "SATURACION"]

# Generar sopa de letras
word_search, placed_words = generate_word_search(grid_size, words_to_find)

# Mostrar en pantalla
print("SOPA DE LETRAS")
print("=" * (grid_size * 2))
for i in range(len(word_search)):
    print(" ".join(word_search[i]))
print("\nPalabras a encontrar:")
print(", ".join(placed_words))

# Guardar en archivo de texto
save_word_search_to_file(word_search, placed_words)