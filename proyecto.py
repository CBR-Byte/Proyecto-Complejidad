import tkinter as tk
import tkinter.messagebox as messagebox

def draw_grid():
    global canvas
    # Limpiar el canvas
    canvas.delete("all")

    #Limpair el codigo
    text_code.delete("1.0", tk.END)

    input_text = text_area.get("1.0", "end").strip().split("\n")

    # Obtener el tamaño de la matriz
    global size_input
    size_input = int(input_text[0])
    if size_input == "":
        # Mostrar mensaje de error si no se ingresó un número para el tamaño de la matriz
        error_label.config(text="Ingresa un número para el tamaño de la matriz")
        return

    try:
        size = int(size_input)
    except ValueError:
        # Mostrar mensaje de error si no se ingresó un número válido para el tamaño de la matriz
        error_label.config(text="Ingresa un número entero válido para el tamaño de la matriz")
        return
    
    #Número de ciudades
    num_points = int(input_text[1])

    #Nombre de las ciudades
    ciudades = []

    #Coordenadas de las ciudades
    points = []
    for line in input_text[2:]:
        parts = line.split()
        name = " ".join(parts[:-2]).strip()
        x = int(parts[-2])
        y = int(parts[-1])
        coordenada = str(x) + ',' + str(y)
        points.append(coordenada)
        ciudades.append((name,coordenada))

    # Calcular el desplazamiento para centrar la cuadrícula
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    cell_size = min(canvas_width, canvas_height) // size
    offset_x = (canvas_width - size * cell_size) // 2
    offset_y = (canvas_height - size * cell_size) // 2

    # Dibujar la cuadrícula
    for i in range(size):
        for j in range(size):
            x1 = offset_x + i * cell_size
            y1 = offset_y + j * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # Dibujar el recuadro
            canvas.create_rectangle(x1, canvas_height - y2, x2, canvas_height - y1, outline="black")

            # Colorear los recuadros de las parejas
            if f"{i},{j}" in points:

                global ciudad
                cor = str(i) + "," + str(j)
                for par in ciudades:
                    if par[1] == cor:
                        ciudad=par[0]


                centro_x = (x1 + x2) / 2
                centro_y = ((canvas_height-y1) + (canvas_height-y2)) / 2
                ancho_cuadrado = x2 - x1
                alto_cuadrado = y2 - y1
                tamaño_texto = min(ancho_cuadrado, alto_cuadrado) // 7
                canvas.create_rectangle(x1, canvas_height - y2, x2, canvas_height - y1, fill="turquoise")
                canvas.create_text(centro_x, centro_y, text=ciudad, fill="black", font=("Arial", tamaño_texto), anchor="center")

    # Borrar el mensaje de error
    error_label.config(text="")

    #Generar el codigo de minizinc
    
    texto ="var int: x1; %Coordenada en X \n"
    texto += "var int: x2; %Coordenada en Y \n"
    texto += "var int: z;\n"
    texto += "var int: centroidex;\n"
    texto += "var int: centroidey;\n"

    x = 0
    y = 0
    #Centroide
    for i in range(num_points):
        coor = points[i].split(",")
        x1 = coor[0]
        y1 = coor[1]
        x += int(x1)
        y += int(y1)

    division = round(x / num_points)
    texto += "constraint centroidex >= "+ str(division) +";\n"
    division = round (y / num_points)
    texto += "constraint centroidey >= "+ str(division) +";\n"

    texto += "constraint z = "

    #Distancias Manhaattan
    for i in range(num_points):
        coor = points[i].split(",")
        x = coor[0]
        y = coor[1]
        if i == num_points-1:
            texto += "abs(x1-"+ x +") + abs(x2-"+ y +");"
            break
        texto += "abs(x1-"+ x +") + abs(x2-"+ y +") + "

    texto += "\nconstraint x1 >= 0; \nconstraint x2 >= 0;\n"
    texto += "constraint x1 <= "+ str(size_input-1) + "; \nconstraint x2 <= "+ str(size_input-1) + ";\n"

    #Restriccion para no poner el concierto en una ciudad
    for i in range(num_points):
        coor = points[i].split(",")
        x = coor[0]
        y = coor[1]
        texto += "constraint x1 != "+ x +" \/ x2 != "+ y +";\n"

    texto += "constraint x1 >= centroidex;\n"
    texto += "constraint x2 >= centroidey;\n"
    texto += "solve minimize z; \n"
    texto += 'output["Coordenada en X: ", show(x1), " |Coordenada en Y: ", show(x2), " |Distancia: ", show(z)];'
    text_code.insert(tk.END,texto)

def copiar_texto():
    contenido = text_code.get("1.0", "end-1c")  # Obtener el contenido del TextArea
    window.clipboard_clear()  # Limpiar el portapapeles
    window.clipboard_append(contenido)  # Copiar el contenido al portapapeles
    messagebox.showinfo("Copiado", "Texto copiado al portapapeles")

# Crear la ventana
window = tk.Tk()
window.title("Concierto")

# Crear el Textarea
text_area = tk.Text(window, height=10, width=30)
text_area.pack()

# Crear el Canvas
canvas = tk.Canvas(window, width=900, height=400)
canvas.pack()

# Crear el botón
button = tk.Button(window, text="Solucionar", command=draw_grid)
button.pack()

# Crear el mensaje de error
error_label = tk.Label(window, fg="red")
error_label.pack()

#Crear el Textarea del código
global text_code
text_code = tk.Text(window, height=10, width=100)
text_code.pack()

#Boton para copiar el textarea
global copiar
copiar = tk.Button(window, text="Copiar", command=copiar_texto)
copiar.pack()

# Ejecutar la ventana
window.mainloop()