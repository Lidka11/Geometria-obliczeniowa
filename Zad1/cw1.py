
from tkinter import scrolledtext
import tkinter as tk
from tkinter import ttk
import functools
from tkinter.colorchooser import askcolor


def inicjalizacjaOkienka():
    root =tk.Tk()
    #root.configure(bg= 'gray80')
    root.geometry('780x560')
    root.title('325708 cw 2')
    canvas_szare = szare_tlo(root)
    przycisk_na_szarym_tle(canvas_szare) 
    return root

def inicjalizacjaPolaDane(root,ekran):
    pass



def inicjalizacjaNapisow(root):
    labels = {}
    entries = {}

    coordinates = ['Xa', 'Ya', 'Xb', 'Yb', 'Xc', 'Yc', 'Xd', 'Yd']
    for i, coord in enumerate(coordinates):
        label= tk.Label(root, text=f'{coord}:')
        label.grid(row=i // 2, column=i % 2 * 2, padx=2, pady=2)
        label.config(font=('Arial', 11))
        entries[coord] = tk.Entry(root)
        entries[coord].grid(row=i // 2, column=i % 2 * 2 + 1)

    return coordinates, entries


colors= ['black', 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
color_line1 = 'blue'
color_line2 = 'blue'
colors_index = 0



def change_line1_color():
    global color_line1, colors_index
    color_line1 = colors[colors_index]
    colors_index = (colors_index + 1) % len(colors)
    white_canvas.itemconfig(linia1, fill=color_line1)

def change_line2_color():
    global color_line2, colors_index
    color_line2 = colors[colors_index]
    colors_index = (colors_index + 1) % len(colors)
    white_canvas.itemconfig(linia2, fill=color_line2)



def rysuj_linie(coordinates, entries, grubosc_linii1_var, grubosc_linii2_var):
    global x_a_scaled, y_a_scaled, x_b_scaled, y_b_scaled, x_c_scaled, y_c_scaled, x_d_scaled, y_d_scaled, xp_scaled, yp_scaled
    x_a = float(entries['Xa'].get())
    y_a = float(entries['Ya'].get())
    x_b = float(entries['Xb'].get())
    y_b = float(entries['Yb'].get())
    x_c = float(entries['Xc'].get())
    y_c = float(entries['Yc'].get())
    x_d = float(entries['Xd'].get())
    y_d = float(entries['Yd'].get())
    


    margin = 50
    # Przeskaluj współrzędne do obszaru canvas z uwzględnieniem marginesu
    canvas_width = white_canvas.winfo_width() - 2 * margin
    canvas_height = white_canvas.winfo_height() - 2 * margin
    x_max = max(x_a, x_b, x_c, x_d)
    x_min = min(x_a, x_b, x_c, x_d)
    y_max = max(y_a, y_b, y_c, y_d)
    y_min = min(y_a, y_b, y_c, y_d)
    x_range= x_max - x_min
    y_range= y_max - y_min

    x_scale = canvas_width / x_range
    y_scale = canvas_height / y_range
    
    global linia1,linia2
    # Rysuj linie 1
    x_a_scaled = (x_a - x_min) * x_scale + margin
    y_a_scaled = (y_a - y_min) * y_scale + margin
    x_b_scaled = (x_b - x_min) * x_scale + margin
    y_b_scaled = (y_b - y_min) * y_scale + margin
    linia1= white_canvas.create_line(x_a_scaled, y_a_scaled, x_b_scaled, y_b_scaled, fill= color_line1, width=grubosc_linii1_var.get())

    # Rysuj linie 2
    x_c_scaled = (x_c - x_min) * x_scale + margin
    y_c_scaled = (y_c - y_min) * y_scale + margin
    x_d_scaled = (x_d - x_min) * x_scale + margin
    y_d_scaled = (y_d - y_min) * y_scale + margin
    linia2=white_canvas.create_line(x_c_scaled, y_c_scaled, x_d_scaled, y_d_scaled, fill= color_line2, width=grubosc_linii2_var.get())

    delxac = x_c_scaled - x_a_scaled
    delycd = y_d_scaled - y_c_scaled
    delyac = y_c_scaled - y_a_scaled
    delxcd = x_d_scaled - x_c_scaled
    delxab = x_b_scaled - x_a_scaled
    delyab = y_b_scaled - y_a_scaled

    if (delxac * delycd - delyac * delxcd) != 0 and (delxab * delycd - delyab * delxcd) != 0:
        t = (delxac * delycd - delyac * delxcd) / (delxab * delycd - delyab * delxcd)
        xp_scaled = x_a_scaled + t * delxab
        yp_scaled = y_a_scaled + t * delyab




    # Dodaj etykiety dla punktów A, B, C, D
    white_canvas.create_text(x_a_scaled, y_a_scaled, text='A', fill='black', anchor='sw', font=('Arial', 12))
    white_canvas.create_text(x_b_scaled, y_b_scaled, text='B', fill='black', anchor='sw', font=('Arial', 12))
    white_canvas.create_text(x_c_scaled, y_c_scaled, text='C', fill='black', anchor='sw', font=('Arial', 12))
    white_canvas.create_text(x_d_scaled, y_d_scaled, text='D', fill='black', anchor='sw', font=('Arial', 12))
    white_canvas.create_text(xp_scaled, yp_scaled, text='P', fill='black', anchor='sw', font=('Arial', 12))

    create_point_objects()
    return x_a_scaled, y_a_scaled, x_b_scaled, y_b_scaled, x_c_scaled, y_c_scaled, x_d_scaled, y_d_scaled, xp_scaled, yp_scaled

def create_point_objects():
    global point_objects
    point_objects = {}  # Wyczyść słownik
    # Utwórz obiekty punktów w odpowiednich kształtach
    for point_name, (x, y) in [("A", (x_a_scaled, y_a_scaled)),
                                ("B", (x_b_scaled, y_b_scaled)),
                                ("C", (x_c_scaled, y_c_scaled)),
                                ("D", (x_d_scaled, y_d_scaled)),
                                ("P", (xp_scaled, yp_scaled))]:
        if point_shape == "oval":
            point_objects[point_name] = white_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red', tags="point")
        elif point_shape == "triangle":
            # Narysuj trójkąty (możesz dostosować współrzędne w celu uzyskania odpowiedniego kształtu)
            point_objects[point_name] = white_canvas.create_polygon(x, y - 7, x - 7, y + 7, x + 7, y + 7, fill='red', tags="point")
        elif point_shape == "square":
            # Narysuj kwadraty (możesz dostosować współrzędne w celu uzyskania odpowiedniego kształtu)
            point_objects[point_name] = white_canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill='red', tags="point")

def zmien_kolor_punktow():
    global point_objects
    # Poproś użytkownika o wybór koloru
    color = askcolor()[1]
    if color:
        for point_name in point_objects:
            white_canvas.itemconfig(point_objects[point_name], fill=color)

def change_all_point_shapes():
    global point_shape
    # Zmień kształt punktu na "triangle", "square" lub "oval"
    if point_shape == "oval":
        point_shape = "triangle"
    elif point_shape == "triangle":
        point_shape = "square"
    else:
        point_shape = "oval"
    # Aktualizuj kształty punktów
    for point_name, (x, y) in [("A", (x_a_scaled, y_a_scaled)),
                                ("B", (x_b_scaled, y_b_scaled)),
                                ("C", (x_c_scaled, y_c_scaled)),
                                ("D", (x_d_scaled, y_d_scaled)),
                                ("P", (xp_scaled, yp_scaled))]:
        if point_name in point_objects:
            white_canvas.delete(point_objects[point_name])  # Usuń istniejący kształt
        if point_shape == "oval":
            point_objects[point_name] = white_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red', tags="point")
        elif point_shape == "triangle":
            point_objects[point_name] = white_canvas.create_polygon(x, y - 7, x - 7, y + 7, x + 7, y + 7, fill='red', tags="point")
        elif point_shape == "square":
            point_objects[point_name] = white_canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill='red', tags="point")


MAX_THICKNESS = 5
MIN_THICKNESS = 1
def change_line1_thickness():
    current_thickness = grubosc_linii1_var.get()
    if current_thickness == MAX_THICKNESS:
        new_thickness = MIN_THICKNESS
    else:
        new_thickness = min(current_thickness + 1, MAX_THICKNESS)
    grubosc_linii1_var.set(new_thickness)
    white_canvas.itemconfig(linia1, width=new_thickness)

def change_line2_thickness():
    current_thickness = grubosc_linii2_var.get()
    if current_thickness == MAX_THICKNESS:
        new_thickness = MIN_THICKNESS
    else:
        new_thickness = min(current_thickness + 1, MAX_THICKNESS)
    grubosc_linii2_var.set(new_thickness)
    white_canvas.itemconfig(linia2, width=new_thickness)



def odswiez(coordinates, entries):
    try:

        x_a = float(entries['Xa'].get())
        y_a = float(entries['Ya'].get())
        x_b = float(entries['Xb'].get())
        y_b = float(entries['Yb'].get())
        x_c = float(entries['Xc'].get())
        y_c = float(entries['Yc'].get())
        x_d = float(entries['Xd'].get())
        y_d = float(entries['Yd'].get())

        margin = 50

        canvas_width = white_canvas.winfo_width() - 2 * margin
        canvas_height = white_canvas.winfo_height() - 2 * margin
        x_max = max(x_a, x_b, x_c, x_d)
        x_min = min(x_a, x_b, x_c, x_d)
        y_max = max(y_a, y_b, y_c, y_d)
        y_min = min(y_a, y_b, y_c, y_d)
        x_range= x_max - x_min
        y_range= y_max - y_min

        x_scale = canvas_width / x_range
        y_scale = canvas_height / y_range

        x_a_scaled = (x_a - x_min) * x_scale + margin
        y_a_scaled = (y_a - y_min) * y_scale + margin
        x_b_scaled = (x_b - x_min) * x_scale + margin
        y_b_scaled = (y_b - y_min) * y_scale + margin
        x_c_scaled = (x_c - x_min) * x_scale + margin
        y_c_scaled = (y_c - y_min) * y_scale + margin
        x_d_scaled = (x_d - x_min) * x_scale + margin
        y_d_scaled = (y_d - y_min) * y_scale + margin

        white_canvas.delete('all')

 

    except ValueError as e:
        print("Błąd konwersji:", e)

def wczytaj(coordinates, entries):
    path = "dane.txt"
    if path:
        try:
            with open(path, "r") as plik:
                lines = plik.readlines()
                if len(lines) >= len(coordinates):
                    for i, coord in enumerate(coordinates):
                        if i < len(lines):
                            entry_value = lines[i].strip()
                            entries[coord].delete(0, tk.END)
                            entries[coord].insert(0, entry_value)
                          
        except Exception as e:
            print("Error while loading file:", str(e))




def calculate_intersection(entries, e_xp, e_yp, pasek_polecen):
    try:
        xa = float(entries['Xa'].get())
        xb = float(entries['Xb'].get())
        xc = float(entries['Xc'].get())
        xd = float(entries['Xd'].get())
        ya = float(entries['Ya'].get())
        yb = float(entries['Yb'].get())
        yc = float(entries['Yc'].get())
        yd = float(entries['Yd'].get())
    except ValueError:
        e_xp.delete(0, 'end')
        e_xp.insert(0, "Błąd danych")
        e_yp.delete(0, 'end')
        e_yp.insert(0, "Błąd danych")
        return

    delxac = xc - xa
    delycd = yd - yc
    delyac = yc - ya
    delxcd = xd - xc
    delxab = xb - xa
    delyab = yb - ya

    if (delxac * delycd - delyac * delxcd) != 0 and (delxab * delycd - delyab * delxcd) != 0:
        t = (delxac * delycd - delyac * delxcd) / (delxab * delycd - delyab * delxcd)
        xp = xa + t * delxab
        yp = ya + t * delyab
        formatted_xp = "{:.3f}".format(xp)
        formatted_yp = "{:.3f}".format(yp)
        e_xp.delete(0, 'end')
        e_xp.insert(0, formatted_xp)
        e_yp.delete(0, 'end')
        e_yp.insert(0, formatted_yp)
        #narysuj_linie(canvas, xa, xb, xc, xd, ya, yb, yc, yd)
        #pasek_polecen.insert(0, "Linia została narysowana.")
    else:
        e_xp.delete(0, 'end')
        e_xp.insert(0, "Brak przecięcia")
        e_yp.delete(0, 'end')
        e_yp.insert(0, "Brak przecięcia")

   

def szare_tlo(root):
    canvas = tk.Canvas(root, width=430, height=150, bg='light grey')
    canvas.grid(row=10, column=0, padx=10, pady=10, columnspan=10)
    return canvas


def przycisk_na_szarym_tle(canvas):
    pass






def InicjalizacjaPrzyciskow(root):
    pass
    #przycisk3= tk.Button(root, text='Zapisz raport\n do pliku tekstowego', borderwidth=1, bg='light grey')
    #przycisk3.grid(row=6, column=3, ipadx = 5, ipady=5)
    
    #return  przycisk3

def calculate_and_draw(entries, e_xp, e_yp, canvas, grubosc_linii1_var, grubosc_linii2_var):
    calculate_intersection(entries, e_xp, e_yp, canvas)
    rysuj_linie(coordinates, entries, grubosc_linii1_var, grubosc_linii2_var)
    


colors_index=0




if __name__ == '__main__':

    
    point_shape = "oval"
    point_objects = {}
    point_size = 1
    point_sizes = {"A": 1, "B": 1, "C": 1, "D": 1, "P": 1}

    root= inicjalizacjaOkienka()
    coordinates, entries = inicjalizacjaNapisow(root)

    l_xp = tk.Label(root, text='Xp: ')
    l_xp.grid(row=5, column = 0, padx =2, pady=2)
    l_xp.config(font=('Arial', 11))
    e_xp = tk.Entry(root)
    e_xp.grid(row=5,column=1)
    l_yp = tk.Label(root, text='Yp: ')
    l_yp.config(font=('Arial', 11))
    l_yp.grid(row=5, column = 2, padx =2, pady=2)
    e_yp = tk.Entry(root)
    e_yp.grid(row=5,column=3)
    canvas = szare_tlo(root) 
    
    white_canvas = tk.Canvas(root, width=430, height=300, bg='white')
    white_canvas.grid(row=0, column =4, padx= 10, pady=10, rowspan=10)
    przyciski = InicjalizacjaPrzyciskow(root)
    przyciski1 = przycisk_na_szarym_tle(canvas)
    przyciski2 = przycisk_na_szarym_tle(canvas)
    grubosc_linii1_var = tk.IntVar()
    grubosc_linii1_var.set(4)  # Początkowa grubość linii nr 1

    grubosc_linii2_var = tk.IntVar()
    grubosc_linii2_var.set(4)  # Początkowa grubość linii nr 2


    przycisk2 = tk.Button(root, text='Wczytaj dane z pliku', command=lambda: wczytaj(coordinates, entries), borderwidth=1, width=20, height=1, bg='light grey')
    przycisk2.grid(row=6, column=1, ipadx=5, ipady=5, columnspan=3)
    przycisk1 = tk.Button(root, text='Oblicz',  width=20, height=1, borderwidth=1, command=lambda: calculate_and_draw(entries, e_xp, e_yp, canvas, grubosc_linii1_var, grubosc_linii2_var), bg='light grey')
    przycisk1.grid(row=4, columnspan=4, ipadx = 5, ipady=5)


    button3= tk.Button(canvas, text = 'Odswiez',command=lambda: odswiez(coordinates, entries), width=20, height=2, borderwidth=2)
    button3.grid(row=3, column=0, padx=15, pady=15, rowspan=2)
    
    przycisk_zmien_linie1 = tk.Button(canvas, text="Zmień grubość linii 1", width=20, height=2,bg='light grey', borderwidth=2, command=change_line1_thickness)
    przycisk_zmien_linie1.grid(row=0, column=0, padx=10, pady=10)
    
    przycisk_zmien_linie2 = tk.Button(canvas, text="Zmień grubość linii 2", width=20, height=2,bg='light grey', borderwidth=2, command=change_line2_thickness)
    przycisk_zmien_linie2.grid(row=1, column=0, padx=10, pady=10)



    przycisk_zmien_linie1_color = tk.Button(canvas, text="Zmień kolor linii 1", width=20,bg='light grey', height=2, borderwidth=2, command=change_line1_color)
    przycisk_zmien_linie1_color.grid(row=0, column=4, padx=10, pady=10)
    
    przycisk_zmien_linie2_color = tk.Button(canvas, text="Zmień kolor linii 2", width=20,bg='light grey', height=2, borderwidth=2, command=change_line2_color)
    przycisk_zmien_linie2_color.grid(row=1, column=4, padx=10, pady=10)


    button6 = tk.Button(canvas, text='Zamknij program',  width=40, height=2, borderwidth=2, command=root.destroy)
    button6.grid(row=2, column=3, padx=10, pady=10, rowspan=2, columnspan=2)


    button7= tk.Button(canvas, text='Zmień kształt punktów', width=20, height=2,bg='light grey', borderwidth=2, command=change_all_point_shapes)
    button7.grid(row=0, column=3, padx=10, pady=10)
    button8= tk.Button(canvas, text='Zmień kolor punktów', width=20,bg='light grey', height=2, borderwidth=2, command=zmien_kolor_punktow)
    button8.grid(row=1, column=3, padx=10, pady=10)

    aktualny_rodzaj_znaku = "kolo"  # Domyślnie jest to kółko

    #lista_punktow = []
    #lista_punktow= rysuj_linie(coordinates, entries, grubosc_linii1_var, grubosc_linii2_var)



    root.mainloop()
    
    
