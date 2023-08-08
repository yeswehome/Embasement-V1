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
    1.25: "009",
    1.67: "010",
    2.08: "011",
    2.5: "012",
    2.92: "013",
    3.33: "014",
    3.75: "015",
    4.17: "016",
    5.42: "017",
    5.83: "018",
    6.67: "019",
    7.5: "020",
    8.33: "021",
    10.83: "022",
    15: "023",
    19.17: "024",
    27.5: "026",
    31.67: "027",
    40: "029",
    52.5: "032",
    69.17: "036",
    5: "042",
    0.68: "044",
    0.02: "047",
    0.05: "048",
    0.09: "049",
    0.15: "050",
    0.21: "051",
    0.5: "053",
    0.92: "054",
    0.96: "055",
    1: "056",
    1.42: "057",
    1.46: "058",
    1.5: "059",
    1.92: "060",
    2: "061",
    2.33: "062",
    4.58: "065",
    7.08: "067",
    7.92: "068",
    8.75: "069",
    9.17: "070",
    12.5: "072",
    17.5: "073",
    21.67: "074",
    26.67: "075",
    51.67: "079",
    61.67: "080",
    76.67: "083",
    86.67: "084",
    106.67: "088",
    0.1: "094",
    0.03: "095",
    0.06: "096",
    0.12: "097",
    0.14: "098",
    0.16: "099",
    0.18: "100",
    0.2: "101",
    0.25: "102",
    0.27: "103",
    0.31: "104",
    0.4: "105",
    0.46: "106",
    0.47: "107",
    0.49: "108",
    0.51: "109",
    0.67: "110",
    0.69: "111",
    0.81: "112",
    1.08: "113",
    1.21: "114",
    1.33: "115",
    1.71: "116",
    1.83: "117",
    2.25: "118",
    2.67: "119",
    2.75: "120",
    3.08: "121",
    3.25: "122",
    3.58: "123",
    3.67: "124",
    3.92: "125",
    4.42: "126",
    4.5: "127",
    4.67: "128",
    4.75: "129",
    4.83: "130",
    5.17: "131",
    5.33: "132",
    5.58: "133",
    6.08: "134",
    6.25: "135",
    6.92: "136",
    8.83: "137",
    10: "138",
    10.42: "139",
    11.25: "140",
    11.67: "141",
    13.33: "142",
    14.17: "143",
    15.42: "144",
    16.25: "145",
    17.08: "146",
    18.33: "147",
    20: "148",
    20.83: "149",
    22.5: "150",
    25: "151",
    26.92: "152",
    30: "153",
    30.83: "154",
    31.25: "155",
    32.17: "156",
    32.5: "157",
    34.17: "158",
    35: "159",
    35.42: "160",
    37.42: "161",
    37.5: "162",
    39.17: "163",
    42.5: "164",
    42.67: "165",
    42.92: "166",
    43.33: "167",
    43.75: "168",
    45: "169",
    45.42: "170",
    47.5: "171",
    47.92: "172",
    50: "173",
    50.42: "174",
    53.17: "175",
    55.42: "176",
    55.83: "177",
    56.25: "178",
    58.42: "179",
    60: "180",
    60.42: "181",
    62.5: "182",
    63.67: "183",
    64.17: "184",
    65.42: "185",
    68.33: "186",
    68.75: "187",
    68.92: "188",
    72.5: "189",
    72.92: "190",
    74.17: "191",
    75: "192",
    75.42: "193",
    77.92: "194",
    79.42: "195",
    80.83: "196",
    81.25: "197",
    84.17: "198",
    84.67: "199",
    85: "200",
    85.42: "201",
    87.5: "202",
    89.92: "203",
    93.75: "204",
    95.17: "205",
    95.42: "206",
    100: "207",
    100.42: "208",
    104.17: "209",
    105.42: "210",
    105.67: "211",
    106.25: "212",
    110.92: "213",
    112.5: "214",
    112.92: "215",
    115.42: "216",
    117.92: "217",
    118.75: "218",
    121.67: "219",
    125: "220",
    125.42: "221",
    129.17: "222",
    130.42: "223",
    131.25: "224",
    135.42: "225",
    139.17: "226",
    140.42: "227",
    145.42: "228",
    147.92: "229",
    151.67: "230",
    155.42: "231",
    156.67: "232",
    162.92: "233",
    165.42: "234",
    # Notez que la valeur "165.42" est répétée, et elle sera écrasée dans un dictionnaire.
    174.17: "236",
    175.42: "237",
    182.92: "238",
    185.42: "239",
    # Notez que la valeur "185.42" est répétée, et elle sera écrasée dans un dictionnaire.
    195.42: "241",
    196.67: "242",
    205.42: "243",
    207.92: "244",
    219.17: "245",
    230.42: "246",
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