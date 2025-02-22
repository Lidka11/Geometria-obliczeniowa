import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser


def skaluj(points, canvas_width, canvas_height):
    canvas_margin = 50
    canvas_width = canvas_frame.winfo_width()
    canvas_height = canvas_frame.winfo_height()
    x_min = min(x for x, y in points)
    y_min = min(y for x, y in points)
    x_max = max(x for x, y in points)
    y_max = max(y for x, y in points)
    x_range = x_max - x_min
    y_range = y_max - y_min
    s_x = x_max / (y_max - y_min) 
    s_y = y_max / (x_max - x_min)
    if s_x < s_y:
        s_x = s_y
    else:
        s_y = s_x
    scaled_points = [(s_x * (y - y_min), y_max - s_y * (x - x_min)) for x, y in points]
    x_scale = (canvas_width - 2 * canvas_margin) / (x_range * s_x)
    y_scale = (canvas_height - 2 * canvas_margin) / (y_range * s_y)
    scale = min(x_scale, y_scale)
    if x_scale < y_scale:
        x_offset = (canvas_width - x_range * s_x * scale) / 2
        y_offset = canvas_margin
    else:
        x_offset = canvas_margin
        y_offset = (canvas_height - y_range * s_y * scale) / 2
    scaled_points = [(s_x * (y - y_min), y_max - s_y * (x - x_min)) for x, y in points]
    scaled_points = [(x * scale + x_offset, y * scale + y_offset) for x, y in scaled_points]
    return x_min, y_min, x_max, y_max, s_x, s_y, scale, x_offset, y_offset

def rysuj_wielokat(canvas, punkty, kolor='black'):
    lines = []
    for i in range(len(punkty)):
        x1, y1 = punkty[i]
        x2, y2 = punkty[(i + 1) % len(punkty)]
        line = canvas.create_line(x1, y1, x2, y2, fill=kolor, width=2)
        lines.append(line)
    return lines

def wczytaj_i_rysuj_przeskalowany_wielokat():
    global x_min_scaled, y_min_scaled, x_max_scaled, y_max_scaled, s_x_wielokata, s_y_wielokata, x_offset_wielokata, y_offset_wielokata, scale_wielokata, scaled_points_w, punkty_wielokata, linia1, x_min_w, y_min_w, x_max_w, y_max_w
    punkty_wielokata = wczytaj_wielokat()
    if punkty_wielokata:
        x_min_w, y_min_w, x_max_w, y_max_w, s_x_wielokata, s_y_wielokata, scale_wielokata, x_offset_wielokata, y_offset_wielokata = skaluj(punkty_wielokata, canvas_frame.winfo_width(), canvas_frame.winfo_height())
        scaled_points = [(s_x_wielokata * (y - y_min_w), y_max_w - s_y_wielokata * (x - x_min_w)) for x, y in punkty_wielokata]
        scaled_points_w = [(x * scale_wielokata + x_offset_wielokata, y * scale_wielokata + y_offset_wielokata) for x, y in scaled_points]
        x_min_scaled = min(x for x, y in scaled_points_w)
        y_min_scaled = min(y for x, y in scaled_points_w)
        x_max_scaled = max(x for x, y in scaled_points_w)
        y_max_scaled = max(y for x, y in scaled_points_w)
        linia1 = rysuj_wielokat(canvas, scaled_points_w, color_line1)


def rysuj_punkty(canvas, punkty, kolor='red'):
    for punkt in punkty:
        x, y = punkt
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=kolor, outline=kolor)


def czy_punkt_wewnatrz(punkt, wielokat):
    x, y = punkt
    ilosc_przeciec = 0
    for i in range(len(wielokat) - 1):
        x1, y1 = wielokat[i]
        x2, y2 = wielokat[i + 1]

        if ((y1 <= y < y2) or (y2 <= y < y1)) and (x > (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            ilosc_przeciec += 1
        if x1 == x and y1 == y:
            return True
        if x2 == x and y2 == y:
            return True
    return ilosc_przeciec % 2 == 1

def rysuj_w_prostokacie():

    punkty = wczytaj_punkty_kontrolne()
    global punkty_wybrane, punkty_w_prostokacie
    punkty_wybrane =[]
    #punkty_wielokata = wczytaj_wielokat()
    punkty_w_prostokacie = []
    liczba_punktow = 0
    if len(punkty)>=3:
        x_min, y_min, x_max, y_max, s_x, s_y, scale, x_offset, y_offset = skaluj(punkty_wielokata, canvas_frame.winfo_width, canvas_frame.winfo_height)
        for punkt in punkty_wielokata:
            x, y = punkt
            scaled = [(s_x * (y - y_min), y_max - s_y * (x - x_min)) for x, y in punkty]
            scaled_points = [(x * scale + x_offset, y * scale + y_offset) for x, y in scaled]
            #scaled_points_w.append(scaled_points)
        for x, y in scaled_points:
            if x_min_scaled <= x <= x_max_scaled and y_min_scaled <= y <= y_max_scaled:
                punkty_w_prostokacie.append((x, y))
                liczba_punktow +=1
                rysuj_punkty(canvas, punkty_w_prostokacie)
        for x, y in punkty_w_prostokacie:        
            if czy_punkt_wewnatrz((x, y), scaled_points_w):
                punkty_wybrane.append((x, y))


def display_selected_points_count():
    global punkty_wybrane
    if punkty_wybrane:
        message = f"Liczba punktów w wielokącie: {len(punkty_wybrane)}"
        tk.messagebox.showinfo("Wybrane punkty", message)

def rysuj_wybrane():
    if punkty_wybrane:
        rysuj_punkty(canvas, punkty_wybrane, 'blue')

def rysuj_ramke(canvas, kolor='black'):
    global prostokat_ramka
    prostokat_ramka = canvas.create_rectangle(x_min_scaled, y_min_scaled, x_max_scaled, y_max_scaled, outline=kolor, width=2)


def obsluz_rysuj_prostokat():
    if scaled_points_w:
        rysuj_ramke(canvas)

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


def wczytaj_wielokat():
    sciezka_do_wielokata = filedialog.askopenfilename(title="Wybierz plik z wielokątem", filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
    if not sciezka_do_wielokata:
        print("Nie wybrano pliku z wielokątem.")
        return None
    return wczytaj_dane(sciezka_do_wielokata)

def wczytaj_punkty_kontrolne():
    sciezka_punkty_kontrolne = filedialog.askopenfilename(title="Wybierz plik z punktami kontrolnymi", filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
    if not sciezka_punkty_kontrolne:
        print("Nie wybrano pliku z punktami kontrolnymi.")
        return None
    return wczytaj_dane(sciezka_punkty_kontrolne)

#zmiana koloru linii
color_line1 = 'black'
def change_line1_color():
    global color_line1, linia1
    new_color = colorchooser.askcolor()[1]
    if new_color:
        color_line1 = new_color
        for line in linia1:
            canvas.itemconfig(line, fill=color_line1)



color_line2= 'black'
def change_prostokat_color():
    global color_line2, prostokat_ramka
    new_color = colorchooser.askcolor()[1]
    if new_color and prostokat_ramka:
        color_line2 = new_color
        canvas.itemconfig(prostokat_ramka, outline=color_line2)

#zmiana grubości linii wielokąta
MAX_THICKNESS = 5
MIN_THICKNESS = 1
def change_line1_thickness():
    global grubosc_linii1_var, linia1

    current_thickness = grubosc_linii1_var.get()

    if current_thickness == MAX_THICKNESS:
        new_thickness = MIN_THICKNESS
    else:
        new_thickness = min(current_thickness + 1, MAX_THICKNESS)

    grubosc_linii1_var.set(new_thickness)

    for line in linia1:
        canvas.itemconfig(line, width=new_thickness)


def zmien_kolor_punktu():
    global punkty_wybrane
    if punkty_wybrane:
        nowy_kolor = tk.colorchooser.askcolor()[1]
        if nowy_kolor:
            rysuj_punkty(canvas, punkty_wybrane, nowy_kolor)

#zmiana grubności linii ramki
def change_line2_thickness():
    current_thickness = grubosc_linii2_var.get()
    if current_thickness == MAX_THICKNESS:
        new_thickness = MIN_THICKNESS
    else:
        new_thickness = min(current_thickness + 1, MAX_THICKNESS)
    grubosc_linii2_var.set(new_thickness)
    canvas.itemconfig(prostokat_ramka, width=new_thickness)

#zmiana stylu linii wielokąta
def change_line1_style():
    global styl_linii1_var, linia1

    # Dostępne style linii
    available_styles = ["solid", "dashed", "dotted", "dashdot", "dashdotdot"]

    current_style = styl_linii1_var.get()

    # Znajdź indeks aktualnego stylu i uzyskaj indeks kolejnego stylu
    current_style_index = available_styles.index(current_style)
    next_style_index = (current_style_index + 1) % len(available_styles)

    new_style = available_styles[next_style_index]
    styl_linii1_var.set(new_style)

    for line in linia1:
        # Ustawienia dla różnych stylów
        if new_style == "solid":
            canvas.itemconfig(line, dash=())
        elif new_style == "dashed":
            canvas.itemconfig(line, dash=(4, 4))
        elif new_style == "dotted":
            canvas.itemconfig(line, dash=(1, 1))
        elif new_style == "dashdot":
            canvas.itemconfig(line, dash=(4, 1, 1, 1))
        elif new_style == "dashdotdot":
            canvas.itemconfig(line, dash=(4, 1, 1, 1, 1, 1))
        # Dodaj kolejne warunki dla innych stylów, jeśli są potrzebne

def obsluz_sprawdz():
    x_str = e_x.get()
    y_str = e_y.get()

    if x_str and y_str:
        x = float(x_str)
        y = float(y_str)

        punkt = (x, y)
        
        # Sprawdź, czy punkt jest wewnątrz wielokąta
        if czy_punkt_wewnatrz(punkt, punkty_wielokata):
            wynik = "Punkt jest wewnątrz wielokąta."
            tk.messagebox.showinfo("Wynik", wynik)

            #dorobic skalowanie i rysowanie
            

        else:
            wynik = "Punkt nie jest wewnątrz wielokąta."
            tk.messagebox.showinfo("Wynik", wynik)
       
    else:
        tk.messagebox.showwarning("Błąd", "Wprowadź wartości x i y.")

def sprawdz():
    global punkty_wybrane
    x_str = e_x.get()
    y_str = e_y.get()

    if x_str and y_str:
        x = float(x_str)
        y = float(y_str)
        
        # Przeskaluj punkt zgodnie z zastosowanym skalowaniem
        x_scaled = s_x_wielokata * (y - y_min_w)
        y_scaled = y_max_w - s_y_wielokata * (x - x_min_w)

        punkt = (x_scaled * scale_wielokata + x_offset_wielokata, y_scaled * scale_wielokata + y_offset_wielokata)

        # Sprawdź, czy przeskalowany punkt jest wewnątrz wielokąta
        if czy_punkt_wewnatrz(punkt, scaled_points_w):
            wynik = "Punkt jest wewnątrz wielokąta."
            tk.messagebox.showinfo("Wynik", wynik)

            # Rysuj przeskalowany punkt
            rysuj_punkty(canvas, [punkt], 'green')

            # Dodaj punkt do listy punktów wybranych
            punkty_wybrane.append(punkt)

        else:
            wynik = "Punkt nie jest wewnątrz wielokąta."
            tk.messagebox.showinfo("Wynik", wynik)
    else:
        tk.messagebox.showwarning("Błąd", "Wprowadź wartości x i y.")




def zapisz_punkty_do_pliku(nazwa_pliku, punkty):
    with open(nazwa_pliku, 'w') as plik:
        for x, y in punkty:
            plik.write(f"{x} {y}\n")

def on_zapisz_button_click():
    global punkty_wybrane
    nazwa_pliku = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if nazwa_pliku:
        zapisz_punkty_do_pliku(nazwa_pliku, punkty_wybrane)
        print(f"Punkty zostały zapisane do pliku: {nazwa_pliku}")

if __name__ == '__main__':
    root = tk.Tk()
    root.title('cw 3')
    root.geometry('920x650')

    grubosc_linii1 = 2  # domyślna grubość linii wielokąta
    grubosc_linii1_var = tk.IntVar()
    grubosc_linii1_var.set(grubosc_linii1)
    grubosc_linii2 = 2  # domyślna grubość linii wielokąta
    grubosc_linii2_var = tk.IntVar()
    grubosc_linii2_var.set(grubosc_linii2)
    styl_linii1_var = tk.StringVar()
    styl_linii1_var.set("solid")

    canvas_frame = tk.Frame(root, width =500, height = 500, bg='white')
    #canvas_width = canvas_frame.winfo_width()
    #canvas_height = canvas_frame.winfo_height()
    canvas_frame.grid(row=0, column= 10, rowspan=10, columnspan=10, padx=10, pady=10)
    canvas = tk.Canvas(canvas_frame, width = 500, height = 500, bg='white')
    canvas.grid(row=0, column= 10, rowspan=10, columnspan=10, padx=10, pady=10)
    napis = tk.Label(root, text='Wprowadź wspołrzędne punktu')
    napis.config(font=('Arial', 12))
    napis.grid(row=5, columnspan=6, padx=10, pady=10)
    l_x = tk.Label(root, text='X: ')
    l_x.grid(row=6, column=0, padx=10, pady=10)
    l_x.config(font=('Arial', 11))
    e_x = tk.Entry(root)
    e_x.grid(row=6, column=1)
    l_y = tk.Label(root, text='Y: ')
    l_y.config(font=('Arial', 11))
    l_y.grid(row=6, column=3, padx=10, pady=10)
    e_y = tk.Entry(root)
    e_y.grid(row=6, column=4)
    przycisk1 = tk.Button(root, text='Sprawdź',command=sprawdz, width=40, height=1, borderwidth=1, bg='white')
    przycisk1.grid(row=7, columnspan=6, ipadx=10, ipady=10)
    przycisk2 = tk.Button(root, text='Wybierz plik z punktami wielokąta i rysuj wielokąt', command=wczytaj_i_rysuj_przeskalowany_wielokat,
                           width=40, height=1, borderwidth=1, bg='light grey')
    przycisk2.grid(row=0, columnspan=6, ipadx=10, ipady=10)
    przycisk4 = tk.Button(root, text='Narysuj prostokąt ograniczający', command=obsluz_rysuj_prostokat,
                          width=40, height=1, borderwidth=1, bg='light grey')
    przycisk4.grid(row=1, columnspan=6, ipadx=10, ipady=10)
    przycisk3= tk.Button(root, text='Wybierz plik z punktami kontrolnymi i rysuj',command=rysuj_w_prostokacie,
                          width=40, height=1, borderwidth=1, bg='light grey')
    przycisk3.grid(row=2, columnspan=6, ipadx=10, ipady=10)
    przycisk5 = tk.Button(root, text='Pokaż punkty wewnątrz',  width=30, height=2, borderwidth=2, command=rysuj_wybrane, bg= 'light grey')
    przycisk5.grid(row=3, columnspan=6, ipadx=5, ipady=5)
    przycisk_pokaz_okienko= tk.Button(root, text="Pokaż liczbe punktów w wielokącie",command=display_selected_points_count, width=30, height=2,bg='light grey', borderwidth=2)
    przycisk_pokaz_okienko.grid(row=4, columnspan=6, ipadx=5, ipady=5)
    napis1 = tk.Label(root, text='Reprezentacja graficzna')
    napis1.config(font=('Arial', 12))
    napis1.grid(row=8, columnspan=6, padx=1, pady=1)


    przycisk_zmien_linie1_color = tk.Button(root, text="Zmień kolor wielokata",command=change_line1_color, width=20,bg='light grey', height=2, borderwidth=2)
    przycisk_zmien_linie1_color.grid(row=9, column=0,columnspan=2, ipadx=10, ipady=5)
    przycisk_zmien_linie1 = tk.Button(root, text="Zmień grubość wieloąta",command=change_line1_thickness, width=20, height=2,bg='light grey', borderwidth=2)
    przycisk_zmien_linie1.grid(row=9, column=3,columnspan=2, ipadx=10, ipady=5)


    przycisk_zmien_linie2_color = tk.Button(root, text="Zmień kolor ramki",command=change_prostokat_color, width=20,bg='light grey', height=2, borderwidth=2)
    przycisk_zmien_linie2_color.grid(row=10, column=0,columnspan=2, ipadx=10, ipady=5)

    przycisk_zmien_linie2 = tk.Button(root, text="Zmień grubość ramki", command=change_line2_thickness,width=20, height=2,bg='light grey', borderwidth=2)
    przycisk_zmien_linie2.grid(row=10,column=3,columnspan=2, ipadx=10, ipady=5)

    przycisk5 = tk.Button(root, text='Zamknij program',  width=20,bg='grey', height=3, borderwidth=2, command=root.destroy)
    przycisk5.grid(row=10, column=15,columnspan=4, ipadx=5, ipady=5, rowspan=2)
    przycisk5 = tk.Button(root, text='Zapisz do pliku tekstowego',  width=40,bg='white', height=3, borderwidth=2, command=on_zapisz_button_click)
    przycisk5.grid(row=10, column=11,columnspan=4, ipadx=5, ipady=5, rowspan=2)
    przycisk5 = tk.Button(root, text='Zmień styl linii wielokąta',  width=20,bg='light grey', height=2, borderwidth=2, command=change_line1_style)
    przycisk5.grid(row=11, column=0,columnspan=2, ipadx=10, ipady=5)
    przycisk5 = tk.Button(root, text='Zmień kolor wyb. punktów',  width=20,bg='light grey', height=2, borderwidth=2, command=zmien_kolor_punktu)
    przycisk5.grid(row=11,column=3,columnspan=2, ipadx=10, ipady=5)

    root.mainloop()
