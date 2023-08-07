import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# En-tête du fichier CSV pour les colonnes
csv_header = "Caract_Collection;Produits_ReferenceFabriquant;Produits_Libelle;Caract_FamilleProduit;Produits_Description;Produits_Points;ProduitEcotaxe_MontantHT_EcoMob3;Caract_Longueur;Caract_Hauteur;Caract_Largeur;Caract_PoidsNet;Resultat_Calcul\n"
ECOPART_MAPPING = {
    0.04: "002",
    0.08: "003",
    0.13: "004",
    0.17: "005",
    0.33: "006",
    0.83: "008",
    1.27: "009",
    9.17: "070",

    # Ajoutez d'autres montants et codes ici
}

def check_existing_catalog(fabricant):
    # Vérifie si le fichier CSV pour le nom de fabricant existe déjà
    filename = f"{fabricant}.csv"
    return filename if os.path.exists(filename) else None

def validate_number(value_if_allowed):
    # Vérifie si la valeur saisie est un nombre
    if value_if_allowed == "":
        return True
    try:
        float(value_if_allowed)
        return True
    except ValueError:
        return False

def save_to_csv(entries, filename):
    # Sauvegarde les données saisies dans les champs dans le fichier CSV
    data = []
    for entry in entries:
        if isinstance(entry, tk.StringVar):
            data.append(entry.get())
        else:
            data.append(entry.get())
            entry.delete(0, tk.END)
    
    # Récupération du montant de l'éco-participation (changer l'index si nécessaire)
    eco_part = float(data[6])  # index 6 correspond au champ "Eco-part"
    # Recherche du code correspondant dans le dictionnaire
    eco_code = ECOPART_MAPPING.get(eco_part, "Code non trouvé")
    data.append(eco_code)  # Ajout du code à la dernière colonne

    with open(filename, 'a') as file:
        file.write(";".join(data) + "\n")

def create_data_entry(filename):
    # Interface pour saisir les informations des produits dans le catalogue
    def save_and_clear():
        # Sauvegarde les données saisies pour le produit et réinitialise les champs pour un nouveau produit
        save_to_csv(entries, filename)
        for entry in entries:
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Gestionnaire de catalogues de meubles")
    root.geometry("800x600")

    entries = []

    # Création des widgets d'entrée pour chaque champ de données du produit
    labels = ["Nom de la collection", "Référence du produit", "Libellé du produit", "Type de produit", "Description du produit", "Prix du produit", "Eco-part", "Longueur", "Largeur", "Hauteur", "Poids"]
    for i, label in enumerate(labels):
        lbl = tk.Label(root, text=label)
        lbl.grid(row=i, column=0)
        if label == "Type de produit":
            type_produit_var = tk.StringVar(root)
            type_produit_var.set("Enfilade")  # valeur par défaut
            type_produit_options = sorted(["Enfilade", "Chaise", "Meuble TV", "Table", "Table ronde", "Bibliothèque", "Console", "Bibus", "Buffet", "Colonne", "Fauteuil", "Vitrine"])
            entry = tk.OptionMenu(root, type_produit_var, *type_produit_options)
        else:
            entry = tk.Entry(root)
            if label in ["Prix du produit", "Eco-part", "Longueur", "Largeur", "Hauteur", "Poids"]:
                entry['validate'] = 'key'
                entry['validatecommand'] = (entry.register(validate_number), '%P')
        entry.grid(row=i, column=1)
        entries.append(entry if label != "Type de produit" else type_produit_var)

    button_new_product = tk.Button(root, text="Nouveau produit", command=save_and_clear)
    button_new_product.grid(row=len(labels), column=0)

    button_save = tk.Button(root, text="Sauvegarder", command=lambda: save_to_csv(entries, filename))
    button_save.grid(row=len(labels), column=1)

    root.mainloop()

def add_to_existing_catalog():
    # Ouvre une boîte de dialogue pour choisir le fichier CSV à modifier
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

def create_new_catalog():
    # Crée un nouveau catalogue avec le nom de fabricant saisi
    def save_new_catalog():
        fabricant = entry_fabricant.get().strip()
        if not fabricant:
            return

        existing_file = check_existing_catalog(fabricant)
        if existing_file:
            messagebox.showerror("Erreur", f"Le catalogue pour '{fabricant}' existe déjà.\nVeuillez utiliser un autre nom.")
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

def main():
    # Fenêtre principale pour choisir de créer un nouveau catalogue ou ajouter au catalogue existant
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
