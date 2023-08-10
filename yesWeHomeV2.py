import os
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk
import pandas as pd
import csv
from PIL import Image, ImageTk

# En-tête du fichier CSV pour les colonnes
csv_header = "Caract_Collection;Produits_ReferenceFabriquant;Produits_Libelle;Caract_FamilleProduit;Produits_Description;Produits_Points;ProduitEcotaxe_Code_EcoMob3;ProduitEcotaxe_MontantHT_EcoMob3;Caract_Longueur;Caract_Hauteur;Caract_Largeur;Caract_PoidsNet\n"
header_labels = csv_header.strip().split(";")
COLONNE_MAPPING = {
    'Nomenclature_FAB': 'Nomenclature_FAB',
    'Produits_IdentifiantExterne': 'Produits_IdentifiantExterne',
    'ProduitsRelations_TypeRelation': 'ProduitsRelations_TypeRelation',
    'ProduitsRelations_IDParent': 'ProduitsRelations_IDParent',
    'Produits_ReferenceFabriquant': 'Produits_ReferenceFabriquant',
    'Produits_ReferenceCommande': 'Produits_ReferenceCommande',
    'Produits_Libelle': 'Produits_Libelle',
    'Produits_Description': 'Produits_Description',
    'Produits_CodeEAN': 'Produits_CodeEAN',
    'ProduitEcotaxe_Code_EcoMob11': 'ProduitEcotaxe_Code_EcoMob11',
    'ProduitEcotaxe_Code_EcoMob3': 'ProduitEcotaxe_Code_EcoMob3',
    'ProduitEcotaxe_MontantHT_EcoMob3': 'ProduitEcotaxe_MontantHT_EcoMob3',
    'ProduitEcotaxe_Code_DEEE': 'ProduitEcotaxe_Code_DEEE',
    'ProduitEcotaxe_MontantHT_DEEE': 'ProduitEcotaxe_MontantHT_DEEE',
    'Produits_TVAReduite': 'Produits_TVAReduite',
    'Produits_TVAReduiteTaux': 'Produits_TVAReduiteTaux',
    'Produits_Points': 'Produits_Points',
    'Produits_PrixVenteConseille': 'Produits_PrixVenteConseille',
    'Produits_Hashtags': 'Produits_Hashtags',
    'RegroupementProduits': 'RegroupementProduits',
    'Caract_Collection': 'Caract_Collection',
    'Caract_CollectionDesc': 'Caract_CollectionDesc',
    'Caract_DateNouveaute': 'Caract_DateNouveaute',
    'Caract_DateSortieCollection': 'Caract_DateSortieCollection',
    'Caract_FamilleProduit': 'Caract_FamilleProduit',
    'Caract_FonctionConvertible_Fixe': 'Caract_FonctionConvertible_Fixe',
    'Caract_GroupeProduit': 'Caract_GroupeProduit',
    'Caract_GroupeProduitDesc': 'Caract_GroupeProduitDesc',
    'Caract_Modele': 'Caract_Modele',
    'Caract_NbrAssise': 'Caract_NbrAssise',
    'Caract_NbrPlace': 'Caract_NbrPlace',
    'Caract_PositionAccoudoir': 'Caract_PositionAccoudoir',
    'Caract_SousFamilleProduit': 'Caract_SousFamilleProduit',
    'Caract_Style': 'Caract_Style',
    'Caract_TypeAccessoiresChaisesCanapes': 'Caract_TypeAccessoiresChaisesCanapes',
    'Caract_TypeCanape': 'Caract_TypeCanape',
    'Caract_TypeCommode': 'Caract_TypeCommode',
    'Caract_TypeFauteuil': 'Caract_TypeFauteuil',
    'Caract_TypeFinitionSofa': 'Caract_TypeFinitionSofa',
    'Caract_TypeLit': 'Caract_TypeLit',
    'Caract_TypeMatelas': 'Caract_TypeMatelas',
    'Caract_TypeMatelasDesc': 'Caract_TypeMatelasDesc',
    'Caract_TypePouf': 'Caract_TypePouf',
    'Caract_TypeSommier': 'Caract_TypeSommier',
    'Caract_TypeSommierDesc': 'Caract_TypeSommierDesc',
    'Caract_Usage': 'Caract_Usage',
    'Caract_Dimension': 'Caract_Dimension',
    'Caract_AccoudoirCouleur': 'Caract_AccoudoirCouleur',
    'Caract_AccoudoirHauteur': 'Caract_AccoudoirHauteur',
    'Caract_AccoudoirLargeur': 'Caract_AccoudoirLargeur',
    'Caract_AccoudoirProfondeur': 'Caract_AccoudoirProfondeur',
    'Caract_AssiseHauteur': 'Caract_AssiseHauteur',
    'Caract_AssiseLargeur': 'Caract_AssiseLargeur',
    'Caract_AssiseProfondeur': 'Caract_AssiseProfondeur',
    'Caract_Diametre': 'Caract_Diametre',
    'Caract_DiametreMax': 'Caract_DiametreMax',
    'Caract_DiametreTechnique': 'Caract_DiametreTechnique',
    'Caract_DimensionTissu': 'Caract_DimensionTissu',
    'Caract_DossierHauteur': 'Caract_DossierHauteur',
    'Caract_DossierLargeur': 'Caract_DossierLargeur',
    'Caract_EpaisseurMatelas': 'Caract_EpaisseurMatelas',
    'Caract_Hauteur': 'Caract_Hauteur',
    'Caract_HauteurMax': 'Caract_HauteurMax',
    'Caract_HauteurTechnique': 'Caract_HauteurTechnique',
    'Caract_Largeur': 'Caract_Largeur',
    'Caract_LargeurAllonge': 'Caract_LargeurAllonge',
    'Caract_LargeurMatelas': 'Caract_LargeurMatelas',
    'Caract_LargeurMax': 'Caract_LargeurMax',
    'Caract_LargeurTechnique': 'Caract_LargeurTechnique',
    'Caract_Longueur': 'Caract_Longueur',
    'Caract_LongueurAllonge': 'Caract_LongueurAllonge',
    'Caract_LongueurMatelas': 'Caract_LongueurMatelas',
    'Caract_LongueurMax': 'Caract_LongueurMax',
    'Caract_LongueurTechnique': 'Caract_LongueurTechnique',
    'Caract_PiedHauteur': 'Caract_PiedHauteur',
    'Caract_PoidsNet': 'Caract_PoidsNet',
    'Caract_Profondeur': 'Caract_Profondeur',
    'Caract_ProfondeurMax': 'Caract_ProfondeurMax',
    'Caract_ProfondeurTechnique': 'Caract_ProfondeurTechnique',
    'Caract_Taille': 'Caract_Taille',
    'Caract_TailleLit': 'Caract_TailleLit',
    'Caract_Volume': 'Caract_Volume',
    'Caract_CategorieTissusCoutil': 'Caract_CategorieTissusCoutil',
    'Caract_CodeCouleurAllonge1': 'Caract_CodeCouleurAllonge1',
    'Caract_CodeCouleurCorps1': 'Caract_CodeCouleurCorps1',
    'Caract_CodeCouleurDessusTable1': 'Caract_CodeCouleurDessusTable1',
    'Caract_CodeCouleurFacade1': 'Caract_CodeCouleurFacade1',
    'Caract_CodeTissusCoutil': 'Caract_CodeTissusCoutil',
    'Caract_CompositionMateriau1': 'Caract_CompositionMateriau1',
    'Caract_Couleur': 'Caract_Couleur',
    'Caract_CouleurAllonge1': 'Caract_CouleurAllonge1',
    'Caract_CouleurAllongeTableDesc': 'Caract_CouleurAllongeTableDesc',
    'Caract_CouleurAutre1': 'Caract_CouleurAutre1',
    'Caract_CouleurCorps1': 'Caract_CouleurCorps1',
    'Caract_CouleurCorps1Desc': 'Caract_CouleurCorps1Desc',
    'Caract_CouleurDessusTable1': 'Caract_CouleurDessusTable1',
    'Caract_CouleurDessusTableDesc': 'Caract_CouleurDessusTableDesc',
    'Caract_CouleurFacade1': 'Caract_CouleurFacade1',
    'Caract_CouleurFacade1Desc': 'Caract_CouleurFacade1Desc',
    'Caract_FaceMatelas': 'Caract_FaceMatelas',
    'Caract_FinitionAutre1': 'Caract_FinitionAutre1',
    'Caract_FinitionProduit': 'Caract_FinitionProduit',
    'Caract_GammeTissusCoutil': 'Caract_GammeTissusCoutil',
    'Caract_MateriauAllonge': 'Caract_MateriauAllonge',
    'Caract_MateriauAllongeDesc': 'Caract_MateriauAllongeDesc',
    'Caract_MateriauCorps1': 'Caract_MateriauCorps1',
    'Caract_MateriauCorpsDesc': 'Caract_MateriauCorpsDesc',
    'Caract_MateriauFacade1': 'Caract_MateriauFacade1',
    'Caract_MateriauFacade1Desc': 'Caract_MateriauFacade1Desc',
    'Caract_MateriauInterieurMatelas1': 'Caract_MateriauInterieurMatelas1',
    'Caract_MateriauInterieurMatelas1Desc': 'Caract_MateriauInterieurMatelas1Desc',
    'Caract_MateriauTissusCoutil1': 'Caract_MateriauTissusCoutil1',
    'Caract_MateriauTissusCoutilDesc': 'Caract_MateriauTissusCoutilDesc',
    'Caract_Matiere': 'Caract_Matiere',
    'Caract_NbrAllonge': 'Caract_NbrAllonge',
    'Caract_NbrPoignee': 'Caract_NbrPoignee',
    'Caract_ReferenceTissusCoutil': 'Caract_ReferenceTissusCoutil',
    'Caract_TissusCoutilDesc': 'Caract_TissusCoutilDesc',
    'Caract_TraitementCoutil': 'Caract_TraitementCoutil',
    'Caract_TraitementCoutilDesc': 'Caract_TraitementCoutilDesc',
    'Caract_TypeAllonge': 'Caract_TypeAllonge',
    'Caract_TypeBois': 'Caract_TypeBois',
    'Caract_TypeBoisFacade1': 'Caract_TypeBoisFacade1',
    'Caract_TypeChantTable': 'Caract_TypeChantTable',
    'Caract_TypeChantTableDesc': 'Caract_TypeChantTableDesc',
    'Caract_TypeMetal': 'Caract_TypeMetal',
    'Caract_TypeTissus': 'Caract_TypeTissus',
    'Caract_ExtensionGarantie': 'Caract_ExtensionGarantie',
    'Caract_GarantieDesc': 'Caract_GarantieDesc',
    'Caract_NbrAnneeGarantie': 'Caract_NbrAnneeGarantie',
    'Caract_CaracteristiqueCle1': 'Caract_CaracteristiqueCle1',
    'Caract_ColisDimension': 'Caract_ColisDimension',
    'Caract_ColisHauteur': 'Caract_ColisHauteur',
    'Caract_ColisLongueur': 'Caract_ColisLongueur',
    'Caract_ColisProfondeur': 'Caract_ColisProfondeur',
    'Caract_DateFinCommande': 'Caract_DateFinCommande',
    'Caract_DehoussableMatelasDesc': 'Caract_DehoussableMatelasDesc',
    'Caract_DescrCoussin': 'Caract_DescrCoussin',
    'Caract_DossierTypeReglage': 'Caract_DossierTypeReglage',
    'Caract_Eclairage': 'Caract_Eclairage',
    'Caract_EstAntiAcariens': 'Caract_EstAntiAcariens',
    'Caract_EstAssemble': 'Caract_EstAssemble',
    'Caract_EstAvecAccoudoir': 'Caract_EstAvecAccoudoir',
    'Caract_EstAvecAppuiTete': 'Caract_EstAvecAppuiTete',
    'Caract_EstAvecCranSurete': 'Caract_EstAvecCranSurete',
    'Caract_EstAvecEclairage': 'Caract_EstAvecEclairage',
    'Caract_EstAvecRangement': 'Caract_EstAvecRangement',
    'Caract_EstAvecReposePieds': 'Caract_EstAvecReposePieds',
    'Caract_EstAvecRoulette': 'Caract_EstAvecRoulette',
    'Caract_EstAvecTiroir': 'Caract_EstAvecTiroir',
    'Caract_EstContremarquable': 'Caract_EstContremarquable',
    'Caract_EstDemontable': 'Caract_EstDemontable',
    'Caract_EstDoubleCorps': 'Caract_EstDoubleCorps',
    'Caract_EstEcoResponsable': 'Caract_EstEcoResponsable',
    'Caract_EstElectrique': 'Caract_EstElectrique',
    'Caract_EstEmpilable': 'Caract_EstEmpilable',
    'Caract_EstErgonomique': 'Caract_EstErgonomique',
    'Caract_EstExclusif': 'Caract_EstExclusif',
    'Caract_EstFinSerie': 'Caract_EstFinSerie',
    'Caract_EstLitDouble': 'Caract_EstLitDouble',
    'Caract_EstMassant': 'Caract_EstMassant',
    'Caract_QuantiteStock': 'Caract_QuantiteStock',
    'Caract_DelaiLivraison': 'Caract_DelaiLivraison',
    'Caract_EstMatelasinclus': 'Caract_EstMatelasinclus',
    'Caract_EstMeubleAngle': 'Caract_EstMeubleAngle',
    'Caract_EstModulable': 'Caract_EstModulable',
    'Caract_EstPivotant': 'Caract_EstPivotant',
    'Caract_EstPliante': 'Caract_EstPliante',
    'Caract_EstReglableHauteur': 'Caract_EstReglableHauteur',
    'Caract_EstRelaxation': 'Caract_EstRelaxation',
    'Caract_EstReleveur': 'Caract_EstReleveur',
    'Caract_EstRetourautomatique': 'Caract_EstRetourautomatique',
    'Caract_EstReversible': 'Caract_EstReversible',
    'Caract_EstSommierinclus': 'Caract_EstSommierinclus',
    'Caract_Extensible_Allonge': 'Caract_Extensible_Allonge',
    'Caract_FerragePorte': 'Caract_FerragePorte',
    'Caract_Forme': 'Caract_Forme',
    'Caract_MethodeAssemblage1': 'Caract_MethodeAssemblage1',
    'Caract_ModeAjustement': 'Caract_ModeAjustement',
    'Caract_NbrAccoudoir': 'Caract_NbrAccoudoir',
    'Caract_NbrColis': 'Caract_NbrColis',
    'Caract_NbrCoussin': 'Caract_NbrCoussin',
    'Caract_NbrElementsDansSet': 'Caract_NbrElementsDansSet',
    'Caract_NbrEtageres': 'Caract_NbrEtageres',
    'Caract_NbrPlaceRelaxation': 'Caract_NbrPlaceRelaxation',
    'Caract_PositionPlaceRelaxation': 'Caract_PositionPlaceRelaxation',
    'Caract_NbrPorte': 'Caract_NbrPorte',
    'Caract_NbrTiroir': 'Caract_NbrTiroir',
    'Caract_TypeAjustementAppuiTete': 'Caract_TypeAjustementAppuiTete',
    'Caract_TypeMotorisation': 'Caract_TypeMotorisation',
    'Caract_TypeOuverturePlateau': 'Caract_TypeOuverturePlateau',
    'Caract_CouleurPlateau': 'Caract_CouleurPlateau',
    'Caract_MateriauPlateau': 'Caract_MateriauPlateau',
    'Caract_TypeOuverturePorte': 'Caract_TypeOuverturePorte',
    'Caract_TypePose': 'Caract_TypePose',
    'Caract_UtilisationCouchage': 'Caract_UtilisationCouchage',
    'Caract_VolumeColis': 'Caract_VolumeColis',
    'CaractEstCouchage': 'CaractEstCouchage',
    'Caract_CaracteristiqueRevetement': 'Caract_CaracteristiqueRevetement',
    'Caract_CategorieTissu': 'Caract_CategorieTissu',
    'Caract_CategorieTissuElement1': 'Caract_CategorieTissuElement1',
    'Caract_CategorieTissuElement2': 'Caract_CategorieTissuElement2',
    'Caract_CodeTissuElement1': 'Caract_CodeTissuElement1',
    'Caract_CodeTissuElement2': 'Caract_CodeTissuElement2',
    'Caract_GammeTissuElement1': 'Caract_GammeTissuElement1',
    'Caract_GammeTissuElement2': 'Caract_GammeTissuElement2',
    'Caract_MateriauTissuDescElement1': 'Caract_MateriauTissuDescElement1',
    'Caract_MateriauTissuDescElement2': 'Caract_MateriauTissuDescElement2',
    'Caract_MateriauTissuElement1': 'Caract_MateriauTissuElement1',
    'Caract_MateriauTissuElement2': 'Caract_MateriauTissuElement2',
    'Caract_ReferenceTissuElement1': 'Caract_ReferenceTissuElement1',
    'Caract_ReferenceTissuElement2': 'Caract_ReferenceTissuElement2',
    'Caract_TonCouture': 'Caract_TonCouture',
    'Caract_TypeCouture': 'Caract_TypeCouture',
    'Caract_TypeCoutureDesc': 'Caract_TypeCoutureDesc',
    'Caract_AccoudoirDensiteMousse': 'Caract_AccoudoirDensiteMousse',
    'Caract_AccoudoirSuspensionDesc': 'Caract_AccoudoirSuspensionDesc',
    'Caract_AccueilMatelas': 'Caract_AccueilMatelas',
    'Caract_AssiseFermete': 'Caract_AssiseFermete',
    'Caract_AssiseDensiteMousse': 'Caract_AssiseDensiteMousse',
    'Caract_AssiseSuspensionDesc': 'Caract_AssiseSuspensionDesc',
    'Caract_CodeCouleurPied1': 'Caract_CodeCouleurPied1',
    'Caract_ConfortMatelas': 'Caract_ConfortMatelas',
    'Caract_ConfortMatelasDesc': 'Caract_ConfortMatelasDesc',
    'Caract_ConfortSommier': 'Caract_ConfortSommier',
    'Caract_ConfortSommierDesc': 'Caract_ConfortSommierDesc',
    'Caract_CouleurPied1': 'Caract_CouleurPied1',
    'Caract_CouleurPiedDesc': 'Caract_CouleurPiedDesc',
    'Caract_DescAccoudoir': 'Caract_DescAccoudoir',
    'Caract_DossierDensiteMousse': 'Caract_DossierDensiteMousse',
    'Caract_DossierMateriau': 'Caract_DossierMateriau',
    'Caract_DossierSuspensionDesc': 'Caract_DossierSuspensionDesc',
    'Caract_MateriauDescPied1': 'Caract_MateriauDescPied1',
    'Caract_MateriauDessusTable1': 'Caract_MateriauDessusTable1',
    'Caract_MateriauDessusTableDesc': 'Caract_MateriauDessusTableDesc',
    'Caract_MateriauPied1': 'Caract_MateriauPied1',
    'Caract_MateriauStructureBati1': 'Caract_MateriauStructureBati1',
    'Caract_MateriauStructureDescBati1': 'Caract_MateriauStructureDescBati1',
    'Caract_ModelePied': 'Caract_ModelePied',
    'Caract_ModelePiedDesc': 'Caract_ModelePiedDesc',
    'Caract_NbrRessort': 'Caract_NbrRessort',
    'Caract_NbrZoneConfort': 'Caract_NbrZoneConfort',
    'Caract_NoyauMatelas': 'Caract_NoyauMatelas',
    'Caract_SoutienMatelas': 'Caract_SoutienMatelas',
    'Caract_SuspensionMatelas': 'Caract_SuspensionMatelas',
    'Caract_SuspensionMatelasDesc': 'Caract_SuspensionMatelasDesc',
    'Caract_SuspensionSommier': 'Caract_SuspensionSommier',
    'Caract_SuspensionSommierDesc': 'Caract_SuspensionSommierDesc',
    'Caract_TypeAccoudoir': 'Caract_TypeAccoudoir',
    'Caract_RaisonTypeRelation': 'Caract_RaisonTypeRelation',


}

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
    root.geometry("400x200")
    root.configure(bg='white')  # Fond blanc pour l'application

    # Définir l'icône de la fenêtre
    root.iconbitmap('logoYesWeHome.ico')

    # Charger le logo, le redimensionner et le placer au centre
    image = Image.open('logoYesWeHome.png')
    image = image.resize((100, 100))  # Redimensionner l'image à 100x100
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