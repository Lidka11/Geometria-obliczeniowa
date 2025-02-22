import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import ttk

def wczytaj_dane(sciezka):
    dane = []

    with open(sciezka, "r") as plik:
        for linia in plik:
            kolumny = linia.split()

            # Dodaj sprawdzenie, czy linia zawiera przynajmniej dwie kolumny
            if len(kolumny) >= 2:
                dane.append((float(kolumny[0]), float(kolumny[1])))
            else:
                print(f"Ignorowanie niepoprawnej linii: {linia.strip()}")

    return dane

def wczytaj_punkty_kontrolne():
    sciezka_punkty_kontrolne = filedialog.askopenfilename(title="Wybierz plik z punktami kontrolnymi", filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
    if not sciezka_punkty_kontrolne:
        print("Nie wybrano pliku z punktami kontrolnymi.")
        return None
    return wczytaj_dane(sciezka_punkty_kontrolne)


def skaluj(points, canvas_width, canvas_height):
    canvas_margin = 50
    x_min = min(x for x, y in points)
    y_min = min(y for x, y in points)
    x_max = max(x for x, y in points)
    y_max = max(y for x, y in points)
    x_range = x_max - x_min
    y_range = y_max - y_min

    # Calculate the scaling factor based on the maximum range of points and canvas size
    x_scale = (canvas_width - 2 * canvas_margin) / x_range
    y_scale = (canvas_height - 2 * canvas_margin) / y_range
    scale = min(x_scale, y_scale)

    # Calculate the offset to center the scaled points within the canvas
    x_offset = (canvas_width - x_range * scale) / 2
    y_offset = (canvas_height - y_range * scale) / 2

    # Modify the global 'points' variable in place
    points = [(x * scale + x_offset, y * scale + y_offset) for x, y in points]

    return x_min, y_min, x_max, y_max, x_scale, y_scale, scale, x_offset, y_offset

def skaluj_punkty(punkty, szerokosc, wysokosc, margines):
    if not punkty:
        return []

    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    for x, y in punkty:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    skala_x = (szerokosc - 2 * margines) / (max_x - min_x) if max_x != min_x else 1
    skala_y = (wysokosc - 2 * margines) / (max_y - min_y) if max_y != min_y else 1

    przesuniecie_x = margines - min_x * skala_x
    przesuniecie_y = margines - min_y * skala_y

    skalowane_punkty = [(skala_x * p[0] + przesuniecie_x, skala_y * p[1] + przesuniecie_y) for p in punkty]

    return skalowane_punkty

def rysuj_punkty_na_canvas(canvas, punkty, kolor='red', rozmiar=3, ksztalt='koło'):
    for punkt in punkty:
        x, y = punkt
        if ksztalt == 'koło':
            canvas.create_oval(x - rozmiar, y - rozmiar, x + rozmiar, y + rozmiar, fill=kolor, outline=kolor)
        elif ksztalt == 'kwadrat':
            canvas.create_rectangle(x - rozmiar, y - rozmiar, x + rozmiar, y + rozmiar, fill=kolor, outline=kolor)
        elif ksztalt == 'trójkąt':
            canvas.create_polygon(x - rozmiar, y - rozmiar, x, y + rozmiar, x + rozmiar, y - rozmiar, fill=kolor, outline=kolor)



global points
"""
def wczytaj_i_rysuj():
    global points, x_min, y_min, x_max, y_max,scale, x_offset, y_offset
    points = wczytaj_punkty_kontrolne()
    if points is None:
        return
    #x_min, y_min, x_max, y_max, scale, x_offset, y_offset = skaluj(points, canvas_frame.winfo_width(), canvas_frame.winfo_height())
    rysuj_punkty_na_canvas(canvas, points)
    canvas_frame.update()
"""
global punkty
def wczytaj_i_rysuj():
    global points, x_min, y_min, x_max, y_max,scale, x_offset, y_offset, punkty
    punkty = wczytaj_punkty_kontrolne()
    if punkty is None:
        return
    points= skaluj_punkty(punkty, canvas_frame.winfo_width(), canvas_frame.winfo_height(), 50)
    #x_min, y_min, x_max, y_max, scale, x_offset, y_offset = skaluj(points, canvas_frame.winfo_width(), canvas_frame.winfo_height())
    rysuj_punkty_na_canvas(canvas, points)
    canvas_frame.update()

nowy_kolor='red'

def zmien_kolor_punktow():
    global points, nowy_kolor
    if points:
        nowy_kolor = tk.colorchooser.askcolor()[1]
        if nowy_kolor:
            rysuj_punkty_na_canvas(canvas, points, nowy_kolor)
        else:
            rysuj_punkty_na_canvas(canvas, points, 'red')

def zmien_wielkosc_punktow():
    global points, nowy_kolor, nowy_rozmiar
    if points:
        nowy_rozmiar = int(spinbox3.get())
        if nowy_kolor:
            canvas.delete("all")
            rysuj_punkty_na_canvas(canvas, points, nowy_kolor, nowy_rozmiar)
        else:
            canvas.delete("all")
            rysuj_punkty_na_canvas(canvas, points, 'red', nowy_rozmiar)

def zmien_rodzaj_punktu(event):
    global nowy_ksztalt
    nowy_ksztalt = combo_rodzaj_punktu.get()
    if nowy_ksztalt:
        if nowy_kolor:
            canvas.delete('all')
            rysuj_punkty_na_canvas(canvas, points, nowy_kolor, nowy_rozmiar, nowy_ksztalt)
        else:
            canvas.delete('all')
            rysuj_punkty_na_canvas(canvas, points, 'red', nowy_rozmiar, nowy_ksztalt)


global x_min, y_min, x_max, y_max, scale, x_offset, y_offset


def dodaj_punkt():
    global points, x_min, y_min, x_max, y_max, scale, x_offset, y_offset
    x_str = e_x.get()
    y_str = e_y.get()
    if x_str and y_str:
        x = float(x_str)
        y = float(y_str)
        # Dodaj punkt do listy punktów
        punkty.append((x, y))
        canvas.delete('all')  # Wyczyść zawartość canvasa
        pnowe= skaluj_punkty(punkty, canvas_frame.winfo_width(), canvas_frame.winfo_height(), 50)
        points= pnowe
        rysuj_punkty_na_canvas(canvas, points, nowy_kolor)
        canvas_frame.update()

def dodaj_numery_do_punktow():
    global numbers_ids
    numbers_ids = []
    for i, point in enumerate(points):
        x, y = point
        # Keep track of item IDs
        text_id = canvas.create_text(x, y, text=str(i+1), fill="black", font=("Helvetica", 8), anchor=tk.SW)
        numbers_ids.append(text_id)

def usun_numery():
    # Delete specific items using their IDs
    for text_id in numbers_ids:
        canvas.delete(text_id)
    numbers_ids.clear()
def toggle_numerki():
    global points
    
    if var_numer.get():
        dodaj_numery_do_punktow()
    else:
        usun_numery()



def orientation(p, q, r):
    # Funkcja pomocnicza do określania orientacji trójki punktów
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Punkty są współliniowe
    return 1 if val > 0 else 2  # Zgodnie z ruchem wskazówek zegara lub przeciwnie do ruchu wskazówek zegara

def algorytm_jarvisa(dane_punkty):
    # Znajdź punkt startowy (punkt o najmniejszej współrzędnej y, a w przypadku remisu, o najmniejszej współrzędnej x)
    start_point = min(dane_punkty, key=lambda point: (point[1], point[0]))

    hull = [start_point]
    current_point = start_point

    while True:
        next_point = None
        for candidate_point in dane_punkty:
            if candidate_point == current_point:
                continue

            # Znajdź kolejny punkt leżący na otoczce wypukłej
            if next_point is None or orientation(current_point, next_point, candidate_point) == 2:
                next_point = candidate_point

        # Jeśli następny punkt to punkt startowy, zakończ algorytm
        if next_point == start_point:
            break

        # Dodaj punkt do otoczki wypukłej
        hull.append(next_point)
        current_point = next_point

    return hull

def rysuj_otoczke():
    global punkty_otoczki
    hull = algorytm_jarvisa(points)
    #wyswietl punkty otoczki
    punkty_otoczki= hull
    lines = []
    if len(hull) > 1:
        for i in range(len(hull) - 1):
            x1, y1 = hull[i]
            x2, y2 = hull[i + 1]
            line = canvas.create_line(x1, y1, x2, y2, fill='blue', width=2, tags='otoczka')
            lines.append(line)

        # Połącz ostatni punkt otoczki z pierwszym punktem
        x1, y1 = hull[-1]
        x2, y2 = hull[0]
        line = canvas.create_line(x1, y1, x2, y2, fill='blue', width=2, tags='otoczka')
        lines.append(line)
    canvas_frame.update()
    return lines

def toggle_rysuj_otoczke():
    global linia1
    if rysuje_otoczke.get():
        linia1 = rysuj_otoczke()
    else:
        canvas.delete('otoczka')  # Usuń tylko elementy o tagu 'otoczka'
    canvas_frame.update()


color_line1 = 'black'
def change_line1_color():
    global color_line1, linia1
    new_color = colorchooser.askcolor()[1]
    if new_color:
        color_line1 = new_color
        for line in linia1:
            canvas.itemconfig(line, fill=color_line1)


#zmien grubosc otoczki
def change_line1_thickness():
    global spinbox, linia1
    try:
        new_thickness = int(spinbox.get())
    except ValueError:
        # Możesz dodać obsługę błędu, jeśli użytkownik wpisze coś, co nie jest liczbą
        print("Invalid input for thickness")
        return
    if linia1:
        for line in linia1:
            canvas.itemconfig(line, width=new_thickness)

def change_line1_style(event=None):
    global linia1, spinbox, combobox
    try:
        new_thickness = int(spinbox.get())
    except ValueError:
        print("Invalid input for thickness")
        return
    new_style = combobox.get()

    if linia1:
        if new_style == 'przerywana':
            for line in linia1:
                canvas.itemconfig(line, width=new_thickness, dash=(8, 4))
        else:
            for line in linia1:
                canvas.itemconfig(line, width=new_thickness, dash=())



prostokat_ramka=None
def rysuj_prostokat_ograniczajacy(canvas, kolor='black'):
    
    x_min = min(point[0] for point in points)
    y_min = min(point[1] for point in points)
    x_max = max(point[0] for point in points)
    y_max = max(point[1] for point in points)
    global prostokat_ramka
    prostokat_ramka = canvas.create_rectangle(x_min, y_min, x_max, y_max, outline=kolor, width=2)
    return prostokat_ramka

def toggle_rysuj_prostokat():
    if rysuje_prostokat.get():  # Use rysuje_prostokat.get() to check the checkbox state
        rysuj_prostokat_ograniczajacy(canvas)
    else:
        canvas.delete(prostokat_ramka)
    canvas_frame.update()

color_line2= 'black'
def change_prostokat_color():
    global color_line2, prostokat_ramka
    new_color = colorchooser.askcolor()[1]
    if new_color and prostokat_ramka:
        color_line2 = new_color
        canvas.itemconfig(prostokat_ramka, outline=color_line2)

def change_prostokat_thickness():
    global prostokat_ramka, spinbox2

    try:
        new_thickness = int(spinbox2.get())
    except ValueError:
        # Możesz dodać obsługę błędu, jeśli użytkownik wpisze coś, co nie jest liczbą
        print("Invalid input for thickness")
        return

    if prostokat_ramka:
        canvas.itemconfig(prostokat_ramka, width=new_thickness)

def change_prostokat_properties(event):
    global prostokat_ramka, spinbox2, combobox2

    try:
        new_thickness = int(spinbox2.get())
    except ValueError:
        # Możesz dodać obsługę błędu, jeśli użytkownik wpisze coś, co nie jest liczbą
        print("Invalid input for thickness")
        return

    new_style = combobox2.get()

    if prostokat_ramka:
        if new_style == 'przerywana':
            canvas.itemconfig(prostokat_ramka, width=new_thickness, dash=(8, 4))
        else:
            canvas.itemconfig(prostokat_ramka, width=new_thickness, dash=())


def zapisz_punkty_do_pliku(nazwa_pliku, punkty):
    with open(nazwa_pliku, 'w') as plik:
        for x, y in punkty:
            plik.write(f"{x} {y}\n")

def on_zapisz_button_click():
    global punkty_otoczki
    nazwa_pliku = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if nazwa_pliku:
        zapisz_punkty_do_pliku(nazwa_pliku, punkty_otoczki)
        print(f"Punkty zostały zapisane do pliku: {nazwa_pliku}")



if __name__ == '__main__':
    root = tk.Tk()
    root.title('cw 3')
    root.geometry('1000x700')
    grubosc_linii1 = 2  # domyślna grubość linii wielokąta
    grubosc_linii1_var = tk.IntVar()
    grubosc_linii1_var.set(grubosc_linii1)
    grubosc_linii2 = 2  # domyślna grubość linii wielokąta
    grubosc_linii2_var = tk.IntVar()
    grubosc_linii2_var.set(grubosc_linii2)
    styl_linii1_var = tk.StringVar()
    styl_linii1_var.set("solid")
    aktualny_kolor = tk.StringVar()
    aktualny_kolor.set('red')  # Set default color

    # Create a StringVar to store the current size
    aktualny_rozmiar = tk.StringVar()
    aktualny_rozmiar.set('3')  # Set default size

    rysuje_prostokat = tk.BooleanVar()
    rysuje_prostokat.set(False)
    rysuje_otoczke = tk.BooleanVar()
    rysuje_otoczke.set(False)

    canvas_frame = tk.Frame(root, width =500, height = 500, bg='white')
    canvas_frame.place(x=400, y=10)
    canvas = tk.Canvas(canvas_frame, width = 500, height = 500, bg='white')
    canvas.place(x=0, y=0)
    przycisk2 = tk.Button(root, text='Wczytaj wykaz punktow',
                        width=20, height=1, borderwidth=1, bg='light grey', command=wczytaj_i_rysuj)
    przycisk2.place(x=10, y=10)
    napis = tk.Label(root, text='Sprawdzenie pojedynczego punktu')
    canvas2 = tk.Canvas(root, width=340, height=40, bg='gray91')
    canvas2.place(x=10, y=60)
    napis.place(x=10, y=40)
    l_x = tk.Label(root, text='X: ', bg='gray91')
    l_x.place(x=10, y=70)
    e_x = tk.Entry(root, width=15)
    e_x.place(x=30, y=70)
    l_y = tk.Label(root, text='Y: ', bg='gray91')
    l_y.place(x=140, y=70)
    e_y = tk.Entry(root, width=15)
    e_y.place(x=160, y=70)
    przycisk3 = tk.Button(root, text='Dodaj punkt', width=10, bg='gray91', command=dodaj_punkt)
    przycisk3.place(x=267, y=70)
    #napis1 = tk.Label(root, text='Budowanie otoczki wypukłej')
    #napis1.place(x=15, y=100)
    #canvas1 = tk.Canvas(root, width=340, height=40, bg='gray91')
    #canvas1.place(x=10, y=120)
    #przycisk4 = tk.Button(root, text='Zbuduj otoczkę', width=15, height=1, borderwidth=1, bg= 'gray91')
    #przycisk4.place(x=40, y=130)
    
    canvas3 = tk.Canvas(root, width=340, height=270, bg='gray91')
    canvas3.place(x=10, y=130)
    napis2= tk.Label(root, text='Parametry rysunku')
    napis2.place(x=10, y=110)
    napis3 = tk.Label(root, text='Wykaz punktów', bg= 'gray91')
    napis3.place(x=15, y=140)
    przycisk6= tk.Button(root, text='Kolor', width=10, height=1, borderwidth=1, bg= 'gray91', command=zmien_kolor_punktow)
    przycisk6.place(x=20, y=170)
    napis4= tk.Label(root, text='Wielkosc', bg= 'gray91')
    napis4.place(x=100, y=170)
    spinbox3= tk.Spinbox(root, from_=1, to=10, width=5, command=zmien_wielkosc_punktow)
    spinbox3.place(x=180, y=170)
    combo_rodzaj_punktu = ttk.Combobox(root, values=['koło', 'kwadrat', 'trójkąt'], width=15)
    combo_rodzaj_punktu.place(x=230, y=170)
    combo_rodzaj_punktu.bind("<<ComboboxSelected>>", zmien_rodzaj_punktu)
    var_otoczka = tk.BooleanVar()
    checkbox_otoczka = tk.Checkbutton(root, text="Otoczka", bg= 'gray91', variable=rysuje_otoczke, command=toggle_rysuj_otoczke)
    checkbox_otoczka.place(x=15, y=200)
    przycisk7 = tk.Button(root, text='Kolor', width=10, height=1, borderwidth=1, bg= 'gray91', command=change_line1_color)
    przycisk7.place(x=20, y=230)
    napis5= tk.Label(root, text='Grubosc linii', bg= 'gray91')
    napis5.place(x=100, y=230)
    spinbox= tk.Spinbox(root, from_=1, to=10, width=5, command=change_line1_thickness)
    spinbox.place(x=180, y=230)
    combobox= ttk.Combobox(root, values=['ciągła', 'przerywana'], width=15)
    combobox.place(x=230, y=230)
    combobox.bind("<<ComboboxSelected>>", change_line1_style)
    var_numer= tk.BooleanVar()
    var_numer.set(False)
    przycisk5 = tk.Button(root, text='Zapisz otoczkę', width=15, height=1, borderwidth=1, bg= 'gray91', command=on_zapisz_button_click)
    przycisk5.place(x=100, y=270)
    checkbox_num= tk.Checkbutton(root, text="Widocznosc numerow punktow", variable=var_numer, bg= 'gray91', command=toggle_numerki)
    checkbox_num.place(x=15, y=310)
    
    checkbox_prost= tk.Checkbutton(root, text="Prostokat ograniczajacy",bg= 'gray91', variable=rysuje_prostokat, command=toggle_rysuj_prostokat)
    checkbox_prost.place(x=15, y=340)
    przycisk8 = tk.Button(root, text='Kolor', width=10, height=1, borderwidth=1, bg= 'gray91', command=change_prostokat_color)
    przycisk8.place(x=20, y=370)
    napis6= tk.Label(root, text='Grubosc linii', bg= 'gray91')
    napis6.place(x=100, y=370)
    spinbox2= tk.Spinbox(root, from_=1, to=10, width=5, command=change_prostokat_thickness)
    spinbox2.place(x=180, y=370)
    combobox2= ttk.Combobox(root, values=['ciągła', 'przerywana'], width=15)
    combobox2.place(x=230, y=370)
    combobox2.bind("<<ComboboxSelected>>", change_prostokat_properties)
    przycisk9 = tk.Button(root, text='Koniec', width=20, height=2, borderwidth=2, bg='light grey', command=root.destroy)
    przycisk9.place(x=100, y=420)

    root.mainloop()

