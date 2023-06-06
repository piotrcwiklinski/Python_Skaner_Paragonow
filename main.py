import customtkinter
import tkinter as tk
import tkinter.messagebox as messagebox
from tkcalendar import DateEntry
from tkinter import filedialog
import json
import requests
import os
from datetime import datetime
from PIL import Image


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
    
def show_main_frame(this_frame):
    this_frame.pack_forget()
    frame.pack(pady=20, padx=60, fill="both", expand=True)
    
def scanner(file_path):
    url = "https://ocr.asprise.com/api/v1/receipt"

    image = file_path

    if image != "":
        res = requests.post(url,
                    data = {
                        'api_key': 'TEST',
                        'reckognizer': 'PL',
                        'ref_no': 'oct'
                    },
                    files = {
                        'file': open(image, 'rb')
                    })

    response_data = json.loads(res.text)
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_folder = "archiwum"

    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    else:
        archive_file_path = os.path.join(archive_folder, f"{current_datetime}.json")

        with open(archive_file_path, "w") as f:
            json.dump(response_data, f)
            
        print("Plik JSON został zapisany w folderze archiwum.")
        
def data_reader(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    return data
    
def add_Receipt():
    def select_file_from_explorer():
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg")])
        if file_path:
            try:
                print("Wybrano plik:", file_path)
                scanner(file_path)
                messagebox.showinfo("Sukces", "Plik został pomyślnie wczytany.")
                show_main_frame(new_frame)
            except OSError as e:
                messagebox.showerror("Błąd", "Wystąpił błąd podczas dodawania pliku.")
        else:
            print("Nie wybrano żadnego pliku.")
    def select_file_from_entry():
        file_path = entry.get()
        if file_path:
            try:
                print("Wybrano plik:", file_path)
                scanner(file_path)
                messagebox.showinfo("Sukces", "Plik został pomyślnie wczytany.")
                show_main_frame(new_frame)
            except OSError as e:
                messagebox.showerror("Błąd", "Wystąpił błąd podczas dodawania pliku.")
        else:
            print("Nie podano żadnej ścieżki.")

    frame.pack_forget()  # Ukrywanie bieżącej ramki
    new_frame = customtkinter.CTkFrame(root)
    
    label = customtkinter.CTkLabel(master=new_frame, text="Dodaj nowy paragon", font=("Roboto", 24))
    label.pack(pady=16, padx=10)
    
    spacer_label = customtkinter.CTkLabel(master=new_frame, text="")
    spacer_label.pack()
    
    label = customtkinter.CTkLabel(master=new_frame, text="Wskaż lokalizację pliku", font=("Roboto", 14))
    label.pack()
    
    browse_button = customtkinter.CTkButton(master=new_frame, text="Otwórz eksplorator", command=select_file_from_explorer, width=200)
    browse_button.pack()
    
    spacer_label = customtkinter.CTkLabel(master=new_frame, text="")
    spacer_label.pack()
    
    label = customtkinter.CTkLabel(master=new_frame, text="Wpisz ręcznie ścieżkę", font=("Roboto", 14))
    label.pack()
    
    entry = customtkinter.CTkEntry(master=new_frame, width=200)
    entry.pack()

    manual_button = customtkinter.CTkButton(master=new_frame, text="Dodaj plik", command=select_file_from_entry, width=200)
    manual_button.pack(pady=6)

    back_button = customtkinter.CTkButton(master=new_frame, text="Powrót", command=lambda: show_main_frame(new_frame), width=200)
    back_button.pack(pady=24, padx=10, side=tk.BOTTOM)

    new_frame.pack(pady=20, padx=60, fill="both", expand=True)  # Wyświetlanie nowej ramki
    
def view_Receipt():
    frame.pack_forget()  # Ukrywanie bieżącej ramki
    new_frame = customtkinter.CTkFrame(root)
    
    details_icon = customtkinter.CTkImage(Image.open("images/details.png") , size=(25, 25))
    thrash_icon = customtkinter.CTkImage(Image.open("images/thrash.png") , size=(25, 25))

    label = customtkinter.CTkLabel(master=new_frame, text="Wybierz Paragon", font=("Roboto", 24))
    label.grid(row=0, column=0, columnspan=6, pady=16, padx=10)
    
    nr_header = customtkinter.CTkLabel(master=new_frame, text="Nr", font=("Roboto", 12, "bold"))
    nr_header.grid(row=1, column=0, pady=5, padx=5)
    
    data_header = customtkinter.CTkLabel(master=new_frame, text="Data", font=("Roboto", 12, "bold"))
    data_header.grid(row=1, column=1, pady=5, padx=5)
    
    sklep_header = customtkinter.CTkLabel(master=new_frame, text="Nazwa Sprzedawcy", font=("Roboto", 12, "bold"))
    sklep_header.grid(row=1, column=2, pady=5, padx=5)
    
    wartosc_header = customtkinter.CTkLabel(master=new_frame, text="Kwota", font=("Roboto", 12, "bold"))
    wartosc_header.grid(row=1, column=3, pady=5, padx=5)
    
    akcja_header = customtkinter.CTkLabel(master=new_frame, text="Szczegóły", font=("Roboto", 12, "bold"))
    akcja_header.grid(row=1, column=4, pady=5, padx=5)
    
    usun_header = customtkinter.CTkLabel(master=new_frame, text="Usuń", font=("Roboto", 12, "bold"))
    usun_header.grid(row=1, column=5, pady=5, padx=5)

    # Odczytywanie plików .json z folderu "archiwum"
    folder_path = "archiwum"
    nr = 0
    file_paths = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)
            file_paths.append(file_path)
            data = data_reader(file_path)

            nr_label = customtkinter.CTkLabel(master=new_frame, text=nr+1)
            nr_label.grid(row=nr+2, column=0, padx=5, pady=5)

            data_label = customtkinter.CTkLabel(master=new_frame, text=data['receipts'][0]['date'])
            data_label.grid(row=nr+2, column=1, padx=5, pady=5)

            sklep_label = customtkinter.CTkLabel(master=new_frame, text=data['receipts'][0]['merchant_name'])
            sklep_label.grid(row=nr+2, column=2, padx=5, pady=5)

            wartosc_label = customtkinter.CTkLabel(master=new_frame, text=f"{data['receipts'][0]['total']}  PLN")
            wartosc_label.grid(row=nr+2, column=3, padx=5, pady=5)

            akcja_button = customtkinter.CTkButton(master=new_frame, width=25, corner_radius=30, text="", image=details_icon, command=lambda nr=nr: open_details_window(file_paths[nr]))
            akcja_button.grid(row=nr+2, column=4, padx=5, pady=5)
            
            usun_button = customtkinter.CTkButton(master=new_frame, width=25, corner_radius=30, text="", image=thrash_icon, command=lambda nr=nr: delete_receipt(file_paths[nr], new_frame))
            usun_button.grid(row=nr+2, column=5, padx=5, pady=5)

            nr += 1

    back_button = customtkinter.CTkButton(master=new_frame, text="Powrót", command=lambda: show_main_frame(new_frame), width=200)
    back_button.grid(row=nr+2, column=0, columnspan=6, pady=24, padx=10)

    new_frame.pack(pady=20, padx=60, fill="both", expand=True)  # Wyświetlanie nowej ramki
    
def open_details_window(file_path):
    details_window = customtkinter.CTkToplevel(root)
    details_window.title("Szczegóły")
    details_window.geometry("+2250+600")

    label = customtkinter.CTkLabel(master=details_window, text="Szczegóły Paragonu", font=("Roboto", 24))
    label.pack(pady=10)
    
    data = data_reader(file_path)
    items = data['receipts'][0]['items']
    
    content_label = customtkinter.CTkLabel(master=details_window, text=
    "Twoje zakupy zrobione w sklepie " + data['receipts'][0]['merchant_name'])
    content_label.pack(pady=12 , padx=10)
    
    date_label = customtkinter.CTkLabel(master=details_window, text=
    "DATA ZAKUPU:  " + data['receipts'][0]['date'])
    date_label.pack(pady=12 , padx=10)
    
    items_list = "Przedmioty na rachunku:\n"
    for item in items:
        items_list += "\n" + item['description'] + " - " + f"{item['amount']}" + "PLN"
    
    items_label = customtkinter.CTkLabel(master=details_window, text=items_list, justify="left", anchor="w")
    items_label.pack(pady=12 , padx=10)
    
    summary_label = customtkinter.CTkLabel(master=details_window, text= 
    ("-" * len(content_label._text)) +
    "\nŁĄCZNIE: " + f"{data['receipts'][0]['total']}" + " PLN")
    summary_label.pack()
    
    close_button = customtkinter.CTkButton(master=details_window, text="Zamknij", command=details_window.destroy, width=200)
    close_button.pack(pady=12 , padx=10)
    
def delete_receipt(file_path, current_frame_name):
    try:
        os.remove(file_path)
        messagebox.showinfo("Sukces", "Plik został pomyślnie usunięty.")
        show_main_frame(current_frame_name)
    except OSError as e:
        messagebox.showerror("Błąd", "Wystąpił błąd podczas usuwania pliku.")
        
def receipt_Summary():
    frame.pack_forget()  # Ukrywanie bieżącej ramki
    new_frame = customtkinter.CTkFrame(root)
    new_frame.grid_columnconfigure((0, 1), weight=1)
    
    def calculate_summary():
        start_date = start_calendar.get_date()
        end_date = end_calendar.get_date()
        
        total_amount = 0
        receipts_count = 0
        detailed_receipt_list = "\nLISTA RACHUNKÓW: \n\nDATA \t\t| KWOTA \t\t| SPRZEDAWCA \n"
        
        for file_name in os.listdir("archiwum"):
            if file_name.endswith(".json"):
                file_path = os.path.join("archiwum", file_name)
                data = data_reader(file_path)
                receipt_date = data['receipts'][0]['date']
                receipt_date = datetime.strptime(receipt_date, "%Y-%m-%d").date()
                
                if start_date <= receipt_date <= end_date:
                    total_amount += data['receipts'][0]['total']
                    receipts_count += 1
                    detailed_receipt_list += f"\n{data['receipts'][0]['date']} \t| {data['receipts'][0]['total']} \t\t|  {data['receipts'][0]['merchant_name']} "
                            
        result_label.configure(text=f"PODSUMOWANIE ZA OKRES: {start_date} - {end_date}\n\nSuma kwot: {total_amount} PLN\nLiczba rachunków: {receipts_count}", font=('Roboto', 12, "bold"), justify="left")
        detailed_list.configure(text=detailed_receipt_list, justify="left")
    

    
    label = customtkinter.CTkLabel(master=new_frame, text="Wybierz okres do podsumowania:", font=("Roboto", 24))
    label.grid(row=0, column=0, columnspan=2, pady=16, padx=10)
    
    # Tworzenie etykiet i przycisków
    start_label = customtkinter.CTkLabel(new_frame, text="Data początkowa:")
    start_label.grid(row=1, column=0, sticky="e", padx=10)

    start_calendar = DateEntry(new_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    start_calendar.grid(row=2, column=0, sticky="e", padx=10)

    end_label = customtkinter.CTkLabel(new_frame, text="Data końcowa:")
    end_label.grid(row=1, column=1, sticky="w", padx=10)
    
    end_calendar = DateEntry(new_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    end_calendar.grid(row=2, column=1, sticky="w", padx=10)

    calculate_button = customtkinter.CTkButton(new_frame, text="Wyświetl Podsumowanie", command=calculate_summary, width=200)
    calculate_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    result_label = customtkinter.CTkLabel(new_frame, text="")
    result_label.grid(row=4, column=0, columnspan=2, pady=10)
    
    detailed_list = customtkinter.CTkLabel(new_frame, text="")
    detailed_list.grid(row=5, column=0, columnspan=2)
    
    back_button = customtkinter.CTkButton(new_frame, text="Powrót", command=lambda: show_main_frame(new_frame), width=200)
    back_button.grid(row=6, column=0, columnspan=2, pady=20)
    
    new_frame.pack(pady=20, padx=60, fill="both", expand=True)  

root = customtkinter.CTk()
root.geometry("650x600")
root.title("Skaner Paragonów")
root.eval("tk::PlaceWindow . center")    
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

ctk_logo = customtkinter.CTkImage(Image.open("images/logo.png") , size=(200, 200))

logo = customtkinter.CTkLabel(master=frame, image=ctk_logo, text="")
logo.pack()

label = customtkinter.CTkLabel(master=frame, text="Skaner Paragonów", font=('Roboto',24))
label.pack(pady=12 , padx=10)

button = customtkinter.CTkButton(master=frame, text="Dodaj Nowy Paragon", command=add_Receipt, width=200)
button.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Wyświetl Paragon", command=view_Receipt, width=200)
button.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Podsumowanie Okresowe", command=receipt_Summary, width=200)
button.pack(pady=12, padx=10)

label = customtkinter.CTkLabel(master=frame, text="Piotr Ćwikliński 2023", font=('Roboto',12, 'italic'))
label.pack(pady=12 , padx=10, side=tk.BOTTOM)

root.mainloop()