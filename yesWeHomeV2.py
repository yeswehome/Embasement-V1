import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# En-tête du fichier CSV pour les colonnes
csv_header = "Caract_Collection;Produits_ReferenceFabriquant;Produits_Libelle;Caract_FamilleProduit;Produits_Description;Produits_Points;ProduitEcotaxe_Code_EcoMob3;ProduitEcotaxe_MontantHT_EcoMob3;Caract_Longueur;Caract_Hauteur;Caract_Largeur;Caract_PoidsNet\n"
ECOPART_MAPPING = {
    0.04: "002",
    0.08: "003",
    0.13: "004",
    0.17: "005",
    0.33: "006",
    0.83: "008",
    1.27: "009",
    9.17: "070",
}

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

    label_fabricant = tk.Label(top, text="Nom du fabricant:")
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

    label_choose_csv = tk.Label(top, text="Choisir le fichier CSV à modifier:")
    label_choose_csv.pack()

    button_choose_csv = tk.Button(top, text="Choisir fichier", command=choose_csv_file)
    button_choose_csv.pack()

def create_data_entry(filename):
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

    button_save = tk.Button(root, text="Sauvegarder", command=save_and_clear)
    button_save.grid(row=len(labels), column=0)

    root.mainloop()

def main():
    root = tk.Tk()
    root.title("Gestionnaire de catalogues de meubles")
    root.geometry("400x200")

    button_new_catalog = tk.Button(root, text="Nouveau catalogue", command=create_new_catalog)
    button_new_catalog.pack()

    button_add_to_existing = tk.Button(root, text="Ajouter au catalogue existant", command=add_to_existing_catalog)
    button_add_to_existing.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
