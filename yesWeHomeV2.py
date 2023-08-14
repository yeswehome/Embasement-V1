import os
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk
import pandas as pd
import csv
from PIL import Image, ImageTk

from constants import csv_header, header_labels, COLONNE_MAPPING, ECOPART_MAPPING

def validate_number(value):
    return value == "" or value.isdigit() or value.replace(".", "", 1).isdigit()

def check_existing_catalog(fabricant):
    filename = f"{fabricant}.csv"
    return filename if os.path.exists(filename) else None

def save_to_csv(entries, filename):
    data = []
    for entry in entries:
        if isinstance(entry, tk.StringVar):
            data.append(entry.get())
        else:
            data.append(entry.get())
            entry.delete(0, tk.END)

    eco_part = data[6].strip()
    eco_code = ""
    if eco_part:
        eco_part = float(eco_part)
        eco_code = ECOPART_MAPPING.get(eco_part, "Code non trouvé")
    data.insert(6, eco_code)

    with open(filename, 'a') as file:
        file.write(";".join(data) + "\n")

def show_success_message():
    success_window = tk.Toplevel()
    success_window.title("Succès")
    success_label = tk.Label(success_window, text="Produit ajouté dans la base")
    success_label.pack()
    success_window.after(2000, success_window.destroy)

def create_new_catalog():

    def save_new_catalog():
        fabricant = entry_fabricant.get().strip()
        if not fabricant:
            return

        existing_file = check_existing_catalog(fabricant)
        if existing_file:
            tk.messagebox.showerror("Erreur", f"Le catalogue pour '{fabricant}' existe déjà.\nVeuillez utiliser un autre nom.")
            return

        filename = f"{fabricant}.csv"
        with open(filename, 'w') as file:
            file.write(csv_header)

        top.destroy()
        create_data_entry(filename)

    top = tk.Toplevel()
    top.title("Nouveau catalogue")

    label_fabricant = tk.Label(top, text="Nom du fabricant:", height=10, width=100,font=22)
    label_fabricant.pack()
    entry_fabricant = tk.Entry(top)
    entry_fabricant.pack()

    button_save = tk.Button(top, text="Valider", command=save_new_catalog)
    button_save.pack()

def add_to_existing_catalog():
    def choose_csv_file():
        filename = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        if filename:
            top.destroy()
            create_data_entry(filename)

    top = tk.Toplevel()
    top.title("Ajouter au catalogue existant")

    label_choose_csv = tk.Label(top, text="Choisir le fichier CSV à modifier:", height=10, width=100,font=22)
    label_choose_csv.pack()

    button_choose_csv = tk.Button(top, text="Choisir fichier", command=choose_csv_file)
    button_choose_csv.pack()

def update_csv_header(filename, new_column_name):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Ajouter la nouvelle colonne à l'entête
    header = lines[0].strip() + ";" + new_column_name + "\n"
    lines[0] = header

    # Réécrire le fichier avec la nouvelle entête
    with open(filename, 'w') as file:
        file.writelines(lines)

def get_additional_columns(filename):
    additional_columns = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            # Supposer que les noms de colonne sont dans la première ligne
            additional_columns = [col for col in row if col not in header_labels]
            break
    return additional_columns



def create_data_entry(filename):
    def add_new_column():
        def add_column():
            nonlocal row_count
            new_column_name = new_column_entry.get().strip()
            if new_column_name in COLONNE_MAPPING:
                lbl = tk.Label(root, text=new_column_name)
                lbl.grid(row=row_count, column=0)
                entry = tk.Entry(root)
                entry.grid(row=row_count, column=1)
                entries.append(entry)
                row_count += 1
                button_save.grid(row=row_count, column=0)

                update_csv_header(filename, new_column_name)
                new_column_window.destroy()


            else:
                tk.messagebox.showerror("Erreur", "La valeur saisie ne correspond pas.")

        new_column_window = tk.Toplevel(root)
        new_column_window.title("Ajouter une colonne")

        new_column_label = tk.Label(new_column_window, text="Nom de la colonne:")
        new_column_label.pack()

        new_column_entry = tk.Entry(new_column_window)
        new_column_entry.pack()

        button_add_column = tk.Button(new_column_window, text="Ajouter", command=add_column)
        button_add_column.pack()

    def save_and_clear():
        save_to_csv(entries, filename)
        for entry in entries:
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
        show_success_message()

    root = tk.Tk()
    root.title("Gestionnaire de catalogues de meubles")
    root.geometry("800x600")

    entries = []
    row_count = 0

    labels = ["Nom de la collection", "Référence du produit", "Libellé du produit", "Type de produit", "Description du produit", "Prix du produit", "Eco-part", "Longueur", "Largeur", "Hauteur", "Poids"]
    for i, label in enumerate(labels):
        lbl = tk.Label(root, text=label)
        lbl.grid(row=i, column=0)
        if label == "Type de produit":
            type_produit_var = tk.StringVar(root)
            type_produit_var.set("Enfilade")
            type_produit_options = sorted(["Enfilade", "Chaise", "Meuble TV", "Table", "Table ronde", "Bibliothèque", "Console", "Bibus", "Buffet", "Colonne", "Fauteuil", "Vitrine"])
            entry = tk.OptionMenu(root, type_produit_var, *type_produit_options)
        else:
            entry = tk.Entry(root)
            if label in ["Prix du produit", "Eco-part", "Longueur", "Largeur", "Hauteur", "Poids"]:
                entry['validate'] = 'key'
                entry['validatecommand'] = (entry.register(validate_number), '%P')
        entry.grid(row=i, column=1)
        entries.append(entry if label != "Type de produit" else type_produit_var)

    row_count = len(labels)

    # Ajout des colonnes supplémentaires depuis le fichier CSV
    additional_columns = get_additional_columns(filename)
    for col in additional_columns:
        lbl = tk.Label(root, text=col)
        lbl.grid(row=row_count, column=0)
        entry = tk.Entry(root)
        entry.grid(row=row_count, column=1)
        entries.append(entry)
        row_count += 1

    button_add_column = tk.Button(root, text="+", command=add_new_column)
    button_add_column.grid(row=row_count, column=2)

    button_save = tk.Button(root, text="Sauvegarder", command=save_and_clear)
    button_save.grid(row=row_count, column=0)

    root.mainloop()



def main():
    root = tk.Tk()
    root.title("Gestionnaire de catalogues de meubles")
    root.geometry("800x400")
    root.configure(bg='white')  # Fond blanc pour l'application

    # Définir l'icône de la fenêtre
    root.iconbitmap('logoYesWeHome.ico')

    # Charger le logo, le redimensionner et le placer au centre
    image = Image.open('logoYesWeHome.png')
    image = image.resize((281, 180))  # Redimensionner l'image à 100x100
    logo_image = ImageTk.PhotoImage(image)
    logo_label = tk.Label(root, image=logo_image, bg='white')  # Fond blanc pour le label
    logo_label.grid(row=0, column=0, columnspan=2)  # Centrer le logo

    # Style pour les boutons
    button_style = {'font': ('Helvetica', 14), 'bg': '#ffbf23', 'fg': 'white', 'borderwidth': 1, 'relief': 'solid'}

    button_new_catalog = tk.Button(root, text="Nouveau catalogue", command=create_new_catalog, **button_style)
    button_new_catalog.grid(row=1, column=0, columnspan=2, sticky=tk.EW)

    button_add_to_existing = tk.Button(root, text="Ajouter au catalogue existant", command=add_to_existing_catalog, **button_style)
    button_add_to_existing.grid(row=2, column=0, columnspan=2, sticky=tk.EW)

    # Configurer les lignes et les colonnes pour qu'elles s'étirent avec la fenêtre
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()