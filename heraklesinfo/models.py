# -*- coding: windows-1252 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

#liste articles
class B50Composants(models.Model):
    t50_1_code_bibli = models.CharField(db_column='T50-1-Code bibli', primary_key=True, max_length=2)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_2_code_comp = models.CharField(db_column='T50-2-Code comp', max_length=25)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_3_code_fournisseur_principal = models.CharField(db_column='T50-3-Code fournisseur principal', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_4_référence = models.CharField(db_column='T50-4-Référence', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_5_tarif = models.DecimalField(db_column='T50-5-Tarif', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_6_remise = models.DecimalField(db_column='T50-6-Remise', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_7_pa = models.DecimalField(db_column='T50-7-PA', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_7_pa_tarif = models.DecimalField(db_column='T50-7-PA_tarif', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_7_unite_pa_tarif = models.CharField(db_column='T50-7-Unite_PA_tarif', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_8_unité_achat = models.CharField(db_column='T50-8-Unité achat', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_9_coef_technique = models.DecimalField(db_column='T50-9-Coef technique', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_10_frais_directs = models.DecimalField(db_column='T50-10-Frais directs', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_11_prix_de_revient_uach = models.DecimalField(db_column='T50-11-Prix de revient /UAch', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_12_conv_uvtes_uach = models.DecimalField(db_column='T50-12-Conv Uvtes/UAch', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_13_unité_de_vente = models.CharField(db_column='T50-13-Unité de vente', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_14_prix_de_revient_uvtes = models.DecimalField(db_column='T50-14-Prix de revient / Uvtes', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_15_coef_1 = models.DecimalField(db_column='T50-15-Coef 1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_16_tarif_1 = models.DecimalField(db_column='T50-16-Tarif 1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_17_coef_2 = models.DecimalField(db_column='T50-17-Coef 2', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_18_prix_de_vente_calculé = models.DecimalField(db_column='T50-18-Prix de vente calculé', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_19_prix_de_vente_catalogue = models.DecimalField(db_column='T50-19-Prix de vente catalogue', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_19_1_code_tva = models.SmallIntegerField(db_column='T50-19-1-Code TVA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_19_2_prix_de_vente_catalogue_bloqué = models.BooleanField(db_column='T50-19-2-Prix de vente catalogue bloqué')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_19_3_coefficients_indépendants = models.BooleanField(db_column='T50-19-3-coefficients indépendants')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_20_famille_de_critères_hiérarchiques = models.CharField(db_column='T50-20-Famille de critères hiérarchiques', max_length=3, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_21_1_identificateur_hiérarchique_1 = models.CharField(db_column='T50-21-1-Identificateur hiérarchique 1', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_21_2_identificateur_hiérarchique_2 = models.CharField(db_column='T50-21-2-Identificateur hiérarchique 2', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_21_3_identificateur_hiérarchique_3 = models.CharField(db_column='T50-21-3-Identificateur hiérarchique 3', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_21_4_identificateur_hiérarchique_4 = models.CharField(db_column='T50-21-4-Identificateur hiérarchique 4', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_22_famille_de_critères_libres = models.CharField(db_column='T50-22-Famille de critères libres', max_length=3, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_23_code_famille_de_gestion = models.CharField(db_column='T50-23-Code famille de gestion', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_23_1_code_famille_de_gestion_ouvrage = models.CharField(db_column='T50-23-1-Code famille de gestion ouvrage', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_24_code_d_appel_libre = models.CharField(db_column="T50-24-Code d'appel libre", max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_25_niveau_de_nomenclature = models.SmallIntegerField(db_column='T50-25-Niveau de nomenclature', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_26_date_maj_prix_achat = models.DateTimeField(db_column='T50-26-Date MAJ prix achat', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_27_date_maj_prix_de_vente = models.DateTimeField(db_column='T50-27-Date MAJ prix de vente', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_28_code_fonction = models.CharField(db_column='T50-28-Code fonction', max_length=3, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_29_code_édition = models.CharField(db_column='T50-29-Code édition', max_length=3, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_30_prix_de_revient_ouvrage_par_unité_de_vente = models.DecimalField(db_column='T50-30-Prix de revient ouvrage par unité de vente', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_30_1_prix_de_revient_du_sous_détail = models.DecimalField(db_column='T50-30-1-Prix de revient du sous détail', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_30_2_tarif_1_du_sous_détail = models.DecimalField(db_column='T50-30-2-Tarif 1 du sous détail', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_30_3_prix_de_vente_du_sous_détail = models.DecimalField(db_column='T50-30-3-Prix de vente du sous détail', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_31_coef_1_moyen = models.DecimalField(db_column='T50-31-Coef 1 moyen', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_32_tarif_1_ouvrage = models.DecimalField(db_column='T50-32-Tarif 1 ouvrage', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_33_coef_2_moyen = models.DecimalField(db_column='T50-33-Coef 2 moyen', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_34_prix_de_vente_ouvrage_calculé = models.DecimalField(db_column='T50-34-Prix de vente ouvrage calculé', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_35_prix_de_vente_ouvrage_catalogue = models.DecimalField(db_column='T50-35-Prix de vente ouvrage catalogue', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_36_nom_du_fichier_image = models.CharField(db_column='T50-36-Nom du fichier image', max_length=12, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_37_titre_du_composant = models.CharField(db_column='T50-37-Titre du composant', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_38_descriptif_court_du_composant = models.TextField(db_column='T50-38-Descriptif court du composant', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_39_descriptif_long_du_composant = models.TextField(db_column='T50-39-Descriptif long du composant', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_45_indicateur_sous_detail = models.BooleanField(db_column='T50-45-Indicateur-Sous-Detail')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_46_indicateur_métré = models.BooleanField(db_column='T50-46-Indicateur-Métré')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t50_47_indicateur_descriptif2 = models.BooleanField(db_column='T50-47-Indicateur-Descriptif2')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    qtéréelle = models.DecimalField(db_column='QtéRéelle', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtéréservée = models.DecimalField(db_column='QtéRéservée', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtéoption = models.DecimalField(db_column='QtéOption', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtédisponible = models.DecimalField(db_column='Qtédisponible', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtécommandée = models.DecimalField(db_column='QtéCommandée', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtécommandéeof = models.DecimalField(db_column='QtéCommandéeOF', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    dpa = models.DecimalField(db_column='DPA', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    montantstock = models.DecimalField(db_column='MontantStock', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    articlegénérique = models.BooleanField(db_column='ArticleGénérique')  # Field name made lowercase.
    qgérerenstock = models.BooleanField(db_column='QGérerEnStock')  # Field name made lowercase.
    produitfini = models.BooleanField(db_column='ProduitFini')  # Field name made lowercase.
    conduni = models.CharField(db_column='CondUni', max_length=5, blank=True, null=True)  # Field name made lowercase.
    condqte = models.DecimalField(db_column='CondQte', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    longueur = models.DecimalField(db_column='Longueur', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    largeur = models.DecimalField(db_column='Largeur', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    epaisseur = models.DecimalField(db_column='Epaisseur', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    adr1 = models.CharField(db_column='Adr1', max_length=15, blank=True, null=True)  # Field name made lowercase.
    adr2 = models.CharField(db_column='Adr2', max_length=5, blank=True, null=True)  # Field name made lowercase.
    adr3 = models.CharField(db_column='Adr3', max_length=5, blank=True, null=True)  # Field name made lowercase.
    operation = models.BooleanField()
    codeatelier = models.CharField(db_column='codeAtelier', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cfab = models.CharField(db_column='CFab', max_length=10, blank=True, null=True)  # Field name made lowercase.
    annule = models.BooleanField(db_column='Annule')  # Field name made lowercase.
    typeart = models.SmallIntegerField(db_column='TypeArt', blank=True, null=True)  # Field name made lowercase.
    poidsunite = models.DecimalField(db_column='PoidsUnite', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    poidsfeuille = models.DecimalField(db_column='PoidsFeuille', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    surface = models.DecimalField(db_column='Surface', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    volume = models.DecimalField(db_column='Volume', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    densite = models.DecimalField(db_column='Densite', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    coeftolerance = models.DecimalField(db_column='CoefTolerance', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    modegestion = models.SmallIntegerField(db_column='ModeGestion', blank=True, null=True)  # Field name made lowercase.
    codecompta = models.CharField(db_column='codeCompta', max_length=15, blank=True, null=True)  # Field name made lowercase.
    codeanalytique = models.CharField(db_column='codeAnalytique', max_length=20, blank=True, null=True)  # Field name made lowercase.
    modestock = models.SmallIntegerField(db_column='modeStock', blank=True, null=True)  # Field name made lowercase.
    modeappro = models.SmallIntegerField(db_column='modeAppro', blank=True, null=True)  # Field name made lowercase.
    moderesa = models.SmallIntegerField(db_column='modeResa', blank=True, null=True)  # Field name made lowercase.
    chutemini = models.DecimalField(db_column='chuteMini', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    dimsecu = models.DecimalField(db_column='dimSecu', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    esrecep = models.SmallIntegerField(db_column='ESRecep', blank=True, null=True)  # Field name made lowercase.
    histpiece = models.BooleanField(db_column='histPiece')  # Field name made lowercase.
    modefact = models.SmallIntegerField(db_column='ModeFact', blank=True, null=True)  # Field name made lowercase.
    ophommachine = models.BooleanField(db_column='OPHomMachine')  # Field name made lowercase.
    postecharge = models.CharField(db_column='posteCharge', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tpsavant = models.DecimalField(db_column='tpsAvant', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    tpsavanthw = models.BooleanField(db_column='tpsAvantHW')  # Field name made lowercase.
    tpsprepa = models.DecimalField(db_column='tpsPrepa', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    tpsope = models.DecimalField(db_column='tpsOpe', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    tpsmac = models.DecimalField(db_column='tpsMac', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    tpsctrl = models.DecimalField(db_column='tpsCtrl', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    tpsapres = models.DecimalField(db_column='tpsApres', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    tpsapreshw = models.BooleanField(db_column='tpsApresHW')  # Field name made lowercase.
    nbope = models.DecimalField(db_column='nbOpe', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    tpsfixe = models.DecimalField(db_column='tpsFixe', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    tpsvar = models.DecimalField(db_column='tpsVar', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    tpsu = models.DecimalField(db_column='tpsU', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    pieddocument = models.BooleanField(db_column='PiedDocument')  # Field name made lowercase.
    delaiappro = models.DecimalField(db_column='delaiAppro', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtefixe = models.BooleanField(db_column='qteFixe')  # Field name made lowercase.
    artdiv = models.BooleanField(db_column='Artdiv')  # Field name made lowercase.
    poidsnet = models.DecimalField(db_column='poidsNet', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    repere2 = models.CharField(db_column='Repere2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    repereplan = models.CharField(db_column='reperePlan', max_length=255, blank=True, null=True)  # Field name made lowercase.
    indice = models.CharField(max_length=255, blank=True, null=True)
    zone1 = models.CharField(max_length=255, blank=True, null=True)
    zone2 = models.CharField(max_length=255, blank=True, null=True)
    nuance = models.DecimalField(db_column='Nuance', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    parametre = models.DecimalField(db_column='Parametre', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    indictracabilite = models.BooleanField(db_column='indicTracabilite')  # Field name made lowercase.
    qteecolot = models.DecimalField(db_column='qteEcoLot', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    delai_fab = models.DecimalField(db_column='delai_Fab', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    class_stock = models.CharField(db_column='class_Stock', max_length=1, blank=True, null=True)  # Field name made lowercase.
    type_gestion = models.CharField(db_column='type_Gestion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    type_produit = models.CharField(db_column='type_Produit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vente_sem = models.DecimalField(db_column='vente_Sem', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    vente_mois = models.DecimalField(db_column='vente_Mois', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    delai_montage = models.DecimalField(max_digits=28, decimal_places=15, blank=True, null=True)
    datecreation = models.DateTimeField(db_column='dateCreation', blank=True, null=True)  # Field name made lowercase.
    typest = models.SmallIntegerField(db_column='typeST', blank=True, null=True)  # Field name made lowercase.
    coderem = models.CharField(db_column='codeRem', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datemajstock = models.DateTimeField(db_column='dateMajStock', blank=True, null=True)  # Field name made lowercase.
    cadence = models.DecimalField(max_digits=28, decimal_places=15, blank=True, null=True)
    codepalette = models.CharField(db_column='codePalette', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nbpiecepalette = models.DecimalField(db_column='nbPiecePalette', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    moderesafab = models.SmallIntegerField(db_column='modeResaFab', blank=True, null=True)  # Field name made lowercase.
    saisieateliermatiere = models.BooleanField(db_column='saisieAtelierMatiere')  # Field name made lowercase.
    datemodification = models.DateTimeField(db_column='dateModification', blank=True, null=True)  # Field name made lowercase.
    typepic = models.BooleanField(db_column='typePIC')  # Field name made lowercase.
    stocksecu = models.DecimalField(db_column='stockSecu', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    stocksecukg = models.DecimalField(db_column='stockSecuKG', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    stockalerte = models.DecimalField(db_column='stockAlerte', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    stockalertekg = models.DecimalField(db_column='stockAlerteKG', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    stockmaxi = models.DecimalField(db_column='stockMaxi', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    stockmaxikg = models.DecimalField(db_column='stockMaxiKG', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    datedpa = models.DateTimeField(db_column='dateDPA', blank=True, null=True)  # Field name made lowercase.
    compteachattvaexo = models.CharField(db_column='compteAchatTVAExo', max_length=17, blank=True, null=True)  # Field name made lowercase.
    compteachattvaexohorscee = models.CharField(db_column='compteAchatTVAExoHorsCEE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    periodecouverture = models.SmallIntegerField(db_column='periodeCouverture', blank=True, null=True)  # Field name made lowercase.
    numerotationstock = models.IntegerField(db_column='numerotationStock', blank=True, null=True)  # Field name made lowercase.
    gestionperemption = models.BooleanField(db_column='gestionPeremption')  # Field name made lowercase.
    delaiperemption = models.SmallIntegerField(db_column='delaiPeremption', blank=True, null=True)  # Field name made lowercase.
    codedouane = models.CharField(db_column='codeDouane', max_length=8, blank=True, null=True)  # Field name made lowercase.
    extensiondouane = models.CharField(db_column='extensionDouane', max_length=2, blank=True, null=True)  # Field name made lowercase.
    statut = models.SmallIntegerField(blank=True, null=True)
    statutdate = models.DateTimeField(db_column='statutDate', blank=True, null=True)  # Field name made lowercase.
    compteachattvaexofrance = models.CharField(db_column='compteAchatTVAExoFrance', max_length=17, blank=True, null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    creationpar = models.CharField(db_column='creationPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modifdate = models.DateTimeField(db_column='modifDate', blank=True, null=True)  # Field name made lowercase.
    modifpar = models.CharField(db_column='modifPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    editiondate = models.DateTimeField(db_column='editionDate', blank=True, null=True)  # Field name made lowercase.
    editionpar = models.CharField(db_column='editionPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codeusermodif = models.CharField(db_column='codeUserModif', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codemo = models.CharField(db_column='codeMo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    tpsmo = models.DecimalField(db_column='tpsMo', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    delaidlu = models.SmallIntegerField(db_column='delaiDLU', blank=True, null=True)  # Field name made lowercase.
    matiereid = models.IntegerField(db_column='matiereId', blank=True, null=True)  # Field name made lowercase.
    nuancematiereid = models.IntegerField(db_column='nuanceMatiereId', blank=True, null=True)  # Field name made lowercase.
    codeprofil = models.IntegerField(db_column='codeProfil', blank=True, null=True)  # Field name made lowercase.
    diametre = models.DecimalField(max_digits=28, decimal_places=15, blank=True, null=True)
    operationreglage = models.BooleanField(db_column='operationReglage')  # Field name made lowercase.
    modelereglageid = models.IntegerField(db_column='modeleReglageId', blank=True, null=True)  # Field name made lowercase.
    gainrgpreglage = models.SmallIntegerField(db_column='gainRgpReglage', blank=True, null=True)  # Field name made lowercase.
    codearticlemetre = models.CharField(db_column='codeArticleMetre', max_length=25, blank=True, null=True)  # Field name made lowercase.
    multitva = models.BooleanField(db_column='multiTVA')  # Field name made lowercase.
    numcontrol = models.IntegerField(db_column='numControl', blank=True, null=True)  # Field name made lowercase.
    matiereindiceid = models.IntegerField(db_column='matiereIndiceId', blank=True, null=True)  # Field name made lowercase.
    coursmatiere = models.DecimalField(db_column='coursMatiere', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    operationabsence = models.BooleanField(db_column='operationAbsence')  # Field name made lowercase.
    operationchantier = models.BooleanField(db_column='operationChantier')  # Field name made lowercase.
    distancekm = models.SmallIntegerField(db_column='distanceKM', blank=True, null=True)  # Field name made lowercase.
    numcouleur = models.DecimalField(db_column='numCouleur', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    codebarre = models.CharField(db_column='codeBarre', max_length=13, blank=True, null=True)  # Field name made lowercase.
    selonarticlegenerique = models.BooleanField(db_column='selonArticleGenerique')  # Field name made lowercase.
    volumenet = models.DecimalField(db_column='volumeNet', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    modifautorise = models.BooleanField(db_column='modifAutorise')  # Field name made lowercase.
    numphase = models.IntegerField(db_column='numPhase', blank=True, null=True)  # Field name made lowercase.
    repertoireged = models.TextField(db_column='repertoireGED', blank=True, null=True)  # Field name made lowercase.
    lancementunite = models.BooleanField(db_column='lancementUnite')  # Field name made lowercase.
    codeanalytiquevente = models.CharField(db_column='codeAnalytiqueVente', max_length=20, blank=True, null=True)  # Field name made lowercase.
    postconso = models.SmallIntegerField(db_column='postConso', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'B50-Composants'
        unique_together = (('t50_1_code_bibli', 't50_2_code_comp'),)

class B99Affaires(models.Model):
    t99_0_code_affaire = models.CharField(db_column='T99-0-Code affaire', primary_key=True, max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_1_nom_affaire = models.CharField(db_column='T99-1-Nom affaire', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_2_code_client = models.CharField(db_column='T99-2-Code client', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_3_date_de_demande = models.DateTimeField(db_column='T99-3-Date de demande', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_4_date_premier_devis = models.DateTimeField(db_column='T99-4-Date premier devis', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_5_date_accord = models.DateTimeField(db_column='T99-5-Date accord', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_6_date_début_livraison = models.DateTimeField(db_column='T99-6-Date début livraison', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_7_date_de_clôture = models.DateTimeField(db_column='T99-7-Date de clôture', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_8_code_provenance = models.CharField(db_column='T99-8-Code provenance', max_length=7, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_9_code_action_commerciale = models.CharField(db_column='T99-9-Code action commerciale', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_10_commentaire = models.TextField(db_column='T99-10-commentaire', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_11_prescripteur = models.CharField(db_column='T99-11-Prescripteur', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_12_commercial = models.CharField(db_column='T99-12-Commercial', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_13_technique = models.CharField(db_column='T99-13-Technique', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_14_ca = models.DecimalField(db_column='T99-14-CA', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_16_marge = models.DecimalField(db_column='T99-16-Marge', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_18_situation_du_dossier = models.CharField(db_column='T99-18-Situation du dossier', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_25_numero_dossier = models.IntegerField(db_column='T99-25-Numero dossier', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_26_type = models.CharField(db_column='T99-26-Type', max_length=7, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_27_date_decision = models.DateTimeField(db_column='T99-27-Date decision', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_28_priorite_de_traitement = models.SmallIntegerField(db_column='T99-28-Priorite de traitement', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t99_29_ole = models.BinaryField(db_column='T99-29-Ole', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tauxreussite = models.DecimalField(db_column='TauxReussite', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    produit = models.CharField(db_column='Produit', max_length=7, blank=True, null=True)  # Field name made lowercase.
    coderelation = models.CharField(db_column='CodeRelation', max_length=15, blank=True, null=True)  # Field name made lowercase.
    t99_30_entreprise = models.SmallIntegerField(db_column='T99-30-Entreprise', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    clidiv = models.BooleanField(db_column='CliDiv')  # Field name made lowercase.
    codeetat = models.SmallIntegerField(db_column='codeEtat', blank=True, null=True)  # Field name made lowercase.
    nomdemandeur = models.CharField(db_column='nomDemandeur', max_length=60, blank=True, null=True)  # Field name made lowercase.
    refclientdemande = models.CharField(db_column='refClientDemande', max_length=60, blank=True, null=True)  # Field name made lowercase.
    codezonegeo = models.CharField(db_column='codeZoneGeo', max_length=5, blank=True, null=True)  # Field name made lowercase.
    adr_nom = models.CharField(max_length=60, blank=True, null=True)
    adr_adresse = models.CharField(max_length=60, blank=True, null=True)
    adr_adresse2 = models.CharField(max_length=60, blank=True, null=True)
    adr_cp = models.CharField(db_column='adr_CP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    adr_ville = models.CharField(max_length=60, blank=True, null=True)
    adr_pays = models.CharField(max_length=60, blank=True, null=True)
    adr_codepays = models.CharField(db_column='adr_CodePays', max_length=2, blank=True, null=True)  # Field name made lowercase.
    adr_tel = models.CharField(max_length=20, blank=True, null=True)
    adr_telvoiture = models.CharField(db_column='adr_telVoiture', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adr_fax = models.CharField(max_length=20, blank=True, null=True)
    adr_email = models.CharField(max_length=255, blank=True, null=True)
    adr_interlocuteur = models.CharField(max_length=70, blank=True, null=True)
    adrf_nom = models.CharField(db_column='adrF_nom', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_adresse = models.CharField(db_column='adrF_adresse', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_adresse2 = models.CharField(db_column='adrF_adresse2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_cp = models.CharField(db_column='adrF_CP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    adrf_ville = models.CharField(db_column='adrF_ville', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_pays = models.CharField(db_column='adrF_pays', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_codepays = models.CharField(db_column='adrF_codePays', max_length=2, blank=True, null=True)  # Field name made lowercase.
    adrf_tel = models.CharField(db_column='adrF_tel', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adrf_telvoiture = models.CharField(db_column='adrF_telVoiture', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adrf_fax = models.CharField(db_column='adrF_fax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adrf_email = models.CharField(db_column='adrF_email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adrf_interlocuteur = models.CharField(db_column='adrF_interlocuteur', max_length=70, blank=True, null=True)  # Field name made lowercase.
    codeactivite = models.IntegerField(db_column='codeActivite', blank=True, null=True)  # Field name made lowercase.
    codesecteur = models.IntegerField(db_column='codeSecteur', blank=True, null=True)  # Field name made lowercase.
    codedevis = models.CharField(db_column='codeDevis', max_length=20, blank=True, null=True)  # Field name made lowercase.
    codeof = models.CharField(db_column='codeOF', max_length=20, blank=True, null=True)  # Field name made lowercase.
    codefacture = models.CharField(db_column='codeFacture', max_length=20, blank=True, null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    creationpar = models.CharField(db_column='creationPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    planifdate = models.DateTimeField(db_column='planifDate', blank=True, null=True)  # Field name made lowercase.
    planifpar = models.CharField(db_column='planifPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    validedate = models.DateTimeField(db_column='valideDate', blank=True, null=True)  # Field name made lowercase.
    validepar = models.CharField(db_column='validePar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    terminedate = models.DateTimeField(db_column='termineDate', blank=True, null=True)  # Field name made lowercase.
    terminepar = models.CharField(db_column='terminePar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bafdate = models.DateTimeField(db_column='BAFDate', blank=True, null=True)  # Field name made lowercase.
    bafpar = models.CharField(db_column='BAFPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nonfacturedate = models.DateTimeField(db_column='nonFactureDate', blank=True, null=True)  # Field name made lowercase.
    nonfacturepar = models.CharField(db_column='nonFacturePar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    accescode1 = models.CharField(db_column='accesCode1', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accescode2 = models.CharField(db_column='accesCode2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accesinterphone = models.CharField(db_column='accesInterphone', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accesbatiment = models.CharField(db_column='accesBatiment', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accesescalier = models.CharField(db_column='accesEscalier', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accesetage = models.CharField(db_column='accesEtage', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accesporte = models.CharField(db_column='accesPorte', max_length=60, blank=True, null=True)  # Field name made lowercase.
    codeprioritesav = models.CharField(db_column='codePrioriteSAV', max_length=10, blank=True, null=True)  # Field name made lowercase.
    numseriesav = models.CharField(db_column='numSerieSAV', max_length=255, blank=True, null=True)  # Field name made lowercase.
    modifdate = models.DateTimeField(db_column='modifDate', blank=True, null=True)  # Field name made lowercase.
    modifpar = models.CharField(db_column='modifPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    editiondate = models.DateTimeField(db_column='editionDate', blank=True, null=True)  # Field name made lowercase.
    editionpar = models.CharField(db_column='editionPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codeusermodif = models.CharField(db_column='codeUserModif', max_length=10, blank=True, null=True)  # Field name made lowercase.
    maildate = models.DateTimeField(db_column='mailDate', blank=True, null=True)  # Field name made lowercase.
    mailpar = models.CharField(db_column='mailPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    repertoireged = models.TextField(db_column='repertoireGED', blank=True, null=True)  # Field name made lowercase.
    numdossierged = models.IntegerField(db_column='numDossierGED', blank=True, null=True)  # Field name made lowercase.
    adr_gln = models.CharField(db_column='adr_GLN', max_length=13, blank=True, null=True)  # Field name made lowercase.
    adrf_gln = models.CharField(db_column='adrF_GLN', max_length=13, blank=True, null=True)  # Field name made lowercase.
    criterelibre1 = models.CharField(db_column='critereLibre1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre2 = models.CharField(db_column='critereLibre2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre3 = models.CharField(db_column='critereLibre3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre4 = models.CharField(db_column='critereLibre4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre5 = models.CharField(db_column='critereLibre5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre6 = models.CharField(db_column='critereLibre6', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre7 = models.CharField(db_column='critereLibre7', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre8 = models.CharField(db_column='critereLibre8', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre9 = models.CharField(db_column='critereLibre9', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre10 = models.CharField(db_column='critereLibre10', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre11 = models.CharField(db_column='critereLibre11', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre12 = models.CharField(db_column='critereLibre12', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre13 = models.CharField(db_column='critereLibre13', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre14 = models.CharField(db_column='critereLibre14', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre15 = models.CharField(db_column='critereLibre15', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre16 = models.CharField(db_column='critereLibre16', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre17 = models.CharField(db_column='critereLibre17', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre18 = models.CharField(db_column='critereLibre18', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre19 = models.CharField(db_column='critereLibre19', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre20 = models.CharField(db_column='critereLibre20', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre21 = models.CharField(db_column='critereLibre21', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre22 = models.CharField(db_column='critereLibre22', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre23 = models.CharField(db_column='critereLibre23', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre24 = models.CharField(db_column='critereLibre24', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre25 = models.CharField(db_column='critereLibre25', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre26 = models.CharField(db_column='critereLibre26', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre27 = models.CharField(db_column='critereLibre27', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre28 = models.CharField(db_column='critereLibre28', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre29 = models.CharField(db_column='critereLibre29', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre30 = models.CharField(db_column='critereLibre30', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre31 = models.CharField(db_column='critereLibre31', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre32 = models.CharField(db_column='critereLibre32', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre33 = models.CharField(db_column='critereLibre33', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre34 = models.CharField(db_column='critereLibre34', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre35 = models.CharField(db_column='critereLibre35', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre36 = models.CharField(db_column='critereLibre36', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre37 = models.CharField(db_column='critereLibre37', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre38 = models.CharField(db_column='critereLibre38', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre39 = models.CharField(db_column='critereLibre39', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre40 = models.CharField(db_column='critereLibre40', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'B99-Affaires'

class Etattypearticle(models.Model):
    code = models.CharField(primary_key=True, max_length=1)
    libelle = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'etatTypeArticle'

#liste des clients
class C100Clients(models.Model):
    t100_1_code_client = models.CharField(db_column='T100-1-Code client', primary_key=True, max_length=10)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_2_intitulé = models.CharField(db_column='T100-2-Intitulé', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civcli = models.CharField(db_column='CivCli', max_length=5, blank=True, null=True)  # Field name made lowercase.
    t100_3_nom = models.CharField(db_column='T100-3-Nom', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_4_adresse_1 = models.CharField(db_column='T100-4-Adresse 1', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_5_adresse_2 = models.CharField(db_column='T100-5-Adresse 2', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_6_cp = models.CharField(db_column='T100-6-CP', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_7_ville_pays = models.CharField(db_column='T100-7-Ville Pays', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_8_tél_1 = models.CharField(db_column='T100-8-Tél 1', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_9_tél_2 = models.CharField(db_column='T100-9-Tél 2', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_10_fax = models.CharField(db_column='T100-10-Fax', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civresp = models.CharField(db_column='CivResp', max_length=5, blank=True, null=True)  # Field name made lowercase.
    t100_11_nom_responsable = models.CharField(db_column='T100-11-Nom responsable', max_length=65, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_12_date_création = models.DateTimeField(db_column='T100-12-Date création', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_13_date_de_maj = models.DateTimeField(db_column='T100-13-Date de MAJ', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_14_compte_num = models.CharField(db_column='T100-14-Compte num', max_length=17, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_15_compte_alpha = models.CharField(db_column='T100-15-Compte alpha', max_length=9, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_16_code_métier = models.CharField(db_column='T100-16-code métier', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_17_code_ape = models.CharField(db_column='T100-17-code APE', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_18_code_insee_stat = models.CharField(db_column='T100-18-code INSEE Stat', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_19_siret = models.CharField(db_column='T100-19-SIRET', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_20_code_provenance = models.CharField(db_column='T100-20-code provenance', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_21_commentaire = models.TextField(db_column='T100-21-commentaire', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_22_ca_année_n_1 = models.DecimalField(db_column='T100-22-CA année n-1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_23_ca_année_en_cours = models.DecimalField(db_column='T100-23-CA année en cours', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_24_ca_en_portefeuille = models.DecimalField(db_column='T100-24-CA en portefeuille', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_25_marge_année_n_1 = models.DecimalField(db_column='T100-25-marge année n-1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_26_marge_année_en_cours = models.DecimalField(db_column='T100-26-marge année en cours', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_27_marge_en_portefeuille = models.DecimalField(db_column='T100-27-marge en portefeuille', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_28_zone_géographique = models.CharField(db_column='T100-28-zone géographique', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_29_route = models.TextField(db_column='T100-29-route', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t100_99_client = models.BooleanField(db_column='T100-99-Client')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    qualite = models.IntegerField(db_column='Qualite', blank=True, null=True)  # Field name made lowercase.
    intitulé = models.CharField(db_column='Intitulé', max_length=40, blank=True, null=True)  # Field name made lowercase.
    prénom = models.CharField(db_column='Prénom', max_length=30, blank=True, null=True)  # Field name made lowercase.
    adresse3 = models.CharField(db_column='Adresse3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    codepays = models.CharField(db_column='codePays', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pays = models.CharField(db_column='Pays', max_length=60, blank=True, null=True)  # Field name made lowercase.
    téldom2 = models.CharField(db_column='Téldom2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    télbur2 = models.CharField(db_column='Télbur2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    faxbureau = models.CharField(db_column='FaxBureau', max_length=20, blank=True, null=True)  # Field name made lowercase.
    télvoiture = models.CharField(db_column='TélVoiture', max_length=20, blank=True, null=True)  # Field name made lowercase.
    profession = models.CharField(db_column='Profession', max_length=50, blank=True, null=True)  # Field name made lowercase.
    origine = models.CharField(db_column='Origine', max_length=30, blank=True, null=True)  # Field name made lowercase.
    sélection = models.CharField(db_column='Sélection', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vendeur = models.CharField(db_column='Vendeur', max_length=10, blank=True, null=True)  # Field name made lowercase.
    banque = models.CharField(db_column='Banque', max_length=30, blank=True, null=True)  # Field name made lowercase.
    rib = models.CharField(db_column='RIB', max_length=26, blank=True, null=True)  # Field name made lowercase.
    code_banque = models.CharField(db_column='Code_Banque', max_length=5, blank=True, null=True)  # Field name made lowercase.
    code_guichet = models.CharField(db_column='Code_Guichet', max_length=5, blank=True, null=True)  # Field name made lowercase.
    n_compte = models.CharField(db_column='N_Compte', max_length=14, blank=True, null=True)  # Field name made lowercase.
    cle = models.CharField(db_column='Cle', max_length=2, blank=True, null=True)  # Field name made lowercase.
    adresse_banque = models.CharField(db_column='Adresse_Banque', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ville_banque = models.CharField(db_column='Ville_Banque', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cp_banque = models.CharField(db_column='CP_Banque', max_length=10, blank=True, null=True)  # Field name made lowercase.
    responsable_banque = models.CharField(db_column='Responsable_Banque', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tel_banque = models.CharField(db_column='Tel_Banque', max_length=20, blank=True, null=True)  # Field name made lowercase.
    codefournisseur = models.CharField(db_column='CodeFournisseur', max_length=15, blank=True, null=True)  # Field name made lowercase.
    fournisseur = models.BooleanField(db_column='Fournisseur')  # Field name made lowercase.
    département = models.CharField(db_column='Département', max_length=3, blank=True, null=True)  # Field name made lowercase.
    région = models.CharField(db_column='Région', max_length=3, blank=True, null=True)  # Field name made lowercase.
    mailing = models.CharField(db_column='Mailing', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qfacturegroupe = models.SmallIntegerField(db_column='QFactureGroupe', blank=True, null=True)  # Field name made lowercase.
    codeechéance = models.CharField(db_column='CodeEchéance', max_length=2, blank=True, null=True)  # Field name made lowercase.
    t200_groupeclient = models.IntegerField(db_column='T200-GroupeClient', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t201_paiement = models.CharField(db_column='T201-Paiement', max_length=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t202_echéance = models.CharField(db_column='T202-Echéance', max_length=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    codefacturation = models.CharField(db_column='CodeFacturation', max_length=2, blank=True, null=True)  # Field name made lowercase.
    effectif = models.IntegerField(db_column='Effectif', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=7, blank=True, null=True)
    zone_commerce = models.CharField(db_column='Zone_Commerce', max_length=5, blank=True, null=True)  # Field name made lowercase.
    zone_géo_fact = models.CharField(db_column='Zone_Géo_Fact', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tf_fournituredetail = models.BooleanField(db_column='TF_FournitureDetail')  # Field name made lowercase.
    tf_modetail = models.BooleanField(db_column='TF_MoDetail')  # Field name made lowercase.
    tf_montanttotal = models.BooleanField(db_column='TF_MontantTotal')  # Field name made lowercase.
    tf_brutremise = models.BooleanField(db_column='TF_BrutRemise')  # Field name made lowercase.
    detaxe = models.SmallIntegerField(db_column='Detaxe', blank=True, null=True)  # Field name made lowercase.
    bl_chiffre = models.BooleanField(db_column='BL_Chiffre')  # Field name made lowercase.
    cbanq = models.CharField(db_column='CBanq', max_length=10, blank=True, null=True)  # Field name made lowercase.
    sfacmt = models.DecimalField(db_column='SFACmt', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    sfacdate = models.DateTimeField(db_column='SFACdate', blank=True, null=True)  # Field name made lowercase.
    sfacdem = models.DecimalField(db_column='SFACdem', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    sfacactif = models.BooleanField(db_column='SFACActif')  # Field name made lowercase.
    clidiv = models.BooleanField(db_column='CliDiv')  # Field name made lowercase.
    monnaieedition = models.CharField(db_column='monnaieEdition', max_length=3, blank=True, null=True)  # Field name made lowercase.
    nbincid = models.IntegerField(db_column='NbIncid', blank=True, null=True)  # Field name made lowercase.
    depbilind = models.BooleanField(db_column='DepBilInd')  # Field name made lowercase.
    depbildat = models.DateTimeField(db_column='DepBilDat', blank=True, null=True)  # Field name made lowercase.
    forjur = models.CharField(db_column='ForJur', max_length=15, blank=True, null=True)  # Field name made lowercase.
    capital = models.DecimalField(db_column='Capital', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMail', max_length=255, blank=True, null=True)  # Field name made lowercase.
    livraison = models.CharField(db_column='Livraison', max_length=2, blank=True, null=True)  # Field name made lowercase.
    seuilfranco = models.DecimalField(db_column='SeuilFranco', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    franco = models.BooleanField()
    radicalpiece = models.CharField(db_column='radicalPiece', max_length=15, blank=True, null=True)  # Field name made lowercase.
    numpiece = models.SmallIntegerField(db_column='numPiece', blank=True, null=True)  # Field name made lowercase.
    fam1piece = models.CharField(db_column='fam1Piece', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fam2piece = models.CharField(db_column='fam2Piece', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fam3piece = models.CharField(db_column='fam3Piece', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fam4piece = models.CharField(db_column='fam4Piece', max_length=10, blank=True, null=True)  # Field name made lowercase.
    titrerep2 = models.CharField(db_column='titreRep2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    titrerepereplan = models.CharField(db_column='titreReperePlan', max_length=255, blank=True, null=True)  # Field name made lowercase.
    titreindice = models.CharField(db_column='titreIndice', max_length=20, blank=True, null=True)  # Field name made lowercase.
    titrezone1 = models.CharField(db_column='titreZone1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    titrezone2 = models.CharField(db_column='titreZone2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    titrenuance = models.CharField(db_column='titreNuance', max_length=20, blank=True, null=True)  # Field name made lowercase.
    titreparam = models.CharField(db_column='titreParam', max_length=20, blank=True, null=True)  # Field name made lowercase.
    siteweb = models.TextField(db_column='siteWeb', blank=True, null=True)  # Field name made lowercase.
    delaitransport = models.SmallIntegerField(db_column='delaiTransport', blank=True, null=True)  # Field name made lowercase.
    tvaintracee = models.CharField(db_column='TVAIntraCEE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    codetvaexo = models.SmallIntegerField(db_column='codeTVAExo', blank=True, null=True)  # Field name made lowercase.
    criterequalite1 = models.CharField(db_column='critereQualite1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite2 = models.CharField(db_column='critereQualite2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite3 = models.CharField(db_column='critereQualite3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite4 = models.CharField(db_column='critereQualite4', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite5 = models.CharField(db_column='critereQualite5', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite6 = models.CharField(db_column='critereQualite6', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite7 = models.CharField(db_column='critereQualite7', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite8 = models.CharField(db_column='critereQualite8', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite9 = models.CharField(db_column='critereQualite9', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite10 = models.CharField(db_column='critereQualite10', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite11 = models.CharField(db_column='critereQualite11', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite12 = models.CharField(db_column='critereQualite12', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite13 = models.CharField(db_column='critereQualite13', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite14 = models.CharField(db_column='critereQualite14', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite15 = models.CharField(db_column='critereQualite15', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite16 = models.CharField(db_column='critereQualite16', max_length=10, blank=True, null=True)  # Field name made lowercase.
    criterequalite17 = models.CharField(db_column='critereQualite17', max_length=10, blank=True, null=True)  # Field name made lowercase.
    repertoiredoc = models.CharField(db_column='repertoireDoc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iban = models.CharField(db_column='IBAN', max_length=34, blank=True, null=True)  # Field name made lowercase.
    bic = models.CharField(db_column='BIC', max_length=11, blank=True, null=True)  # Field name made lowercase.
    codetransporteur = models.CharField(db_column='codeTransporteur', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nbcopiedevis = models.SmallIntegerField(db_column='nbCopieDevis', blank=True, null=True)  # Field name made lowercase.
    nbcopiecde = models.SmallIntegerField(db_column='nbCopieCde', blank=True, null=True)  # Field name made lowercase.
    nbcopiebl = models.SmallIntegerField(db_column='nbCopieBL', blank=True, null=True)  # Field name made lowercase.
    nbcopiefacture = models.SmallIntegerField(db_column='nbCopieFacture', blank=True, null=True)  # Field name made lowercase.
    majorationtva = models.BooleanField(db_column='majorationTVA')  # Field name made lowercase.
    regimesuspensifnum = models.CharField(db_column='regimeSuspensifNum', max_length=60, blank=True, null=True)  # Field name made lowercase.
    regimesuspensifregime = models.CharField(db_column='regimeSuspensifRegime', max_length=60, blank=True, null=True)  # Field name made lowercase.
    regimesuspensifdatefin = models.DateTimeField(db_column='regimeSuspensifDateFin', blank=True, null=True)  # Field name made lowercase.
    codedepot = models.CharField(db_column='codeDepot', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nbcdeedi = models.IntegerField(db_column='nbCdeEDI', blank=True, null=True)  # Field name made lowercase.
    accescode1 = models.CharField(db_column='accesCode1', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accescode2 = models.CharField(db_column='accesCode2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accesinterphone = models.CharField(db_column='accesInterphone', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accesbatiment = models.CharField(db_column='accesBatiment', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accesescalier = models.CharField(db_column='accesEscalier', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accesetage = models.CharField(db_column='accesEtage', max_length=60, blank=True, null=True)  # Field name made lowercase.
    accesporte = models.CharField(db_column='accesPorte', max_length=60, blank=True, null=True)  # Field name made lowercase.
    clientsecondaire = models.BooleanField(db_column='clientSecondaire')  # Field name made lowercase.
    identifiantsociete = models.CharField(db_column='identifiantSociete', max_length=60, blank=True, null=True)  # Field name made lowercase.
    codemodeleedi = models.CharField(db_column='codeModeleEDI', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codeusermodif = models.CharField(db_column='codeUserModif', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    creationpar = models.CharField(db_column='creationPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modifdate = models.DateTimeField(db_column='modifDate', blank=True, null=True)  # Field name made lowercase.
    modifpar = models.CharField(db_column='modifPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    editiondate = models.DateTimeField(db_column='editionDate', blank=True, null=True)  # Field name made lowercase.
    editionpar = models.CharField(db_column='editionPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    couleur = models.IntegerField(blank=True, null=True)
    blmulticde = models.BooleanField(db_column='BLmultiCde')  # Field name made lowercase.
    numbanque = models.IntegerField(db_column='numBanque', blank=True, null=True)  # Field name made lowercase.
    codeincoterm = models.CharField(db_column='codeIncoterm', max_length=3, blank=True, null=True)  # Field name made lowercase.
    codeentreprise = models.SmallIntegerField(db_column='codeEntreprise', blank=True, null=True)  # Field name made lowercase.
    indiceprioriteplanning = models.SmallIntegerField(db_column='indicePrioritePlanning', blank=True, null=True)  # Field name made lowercase.
    prepaexpeditionmulticde = models.BooleanField(db_column='prepaExpeditionMultiCde')  # Field name made lowercase.
    tarifprixttc = models.BooleanField(db_column='tarifPrixTTC')  # Field name made lowercase.
    codemodelevaldevis = models.CharField(db_column='codeModeleValDevis', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codemodelevalcdeclient = models.CharField(db_column='codeModeleValCdeClient', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codemodelevalof = models.CharField(db_column='codeModeleValOF', max_length=10, blank=True, null=True)  # Field name made lowercase.
    gln = models.CharField(db_column='GLN', max_length=13, blank=True, null=True)  # Field name made lowercase.
    codeclientedi = models.CharField(db_column='codeClientEDI', max_length=60, blank=True, null=True)  # Field name made lowercase.
    numlangue = models.SmallIntegerField(db_column='numLangue', blank=True, null=True)  # Field name made lowercase.
    modeenvoifacture = models.SmallIntegerField(db_column='modeEnvoiFacture', blank=True, null=True)  # Field name made lowercase.
    anonymdate = models.DateTimeField(db_column='anonymDate', blank=True, null=True)  # Field name made lowercase.
    anonympar = models.CharField(db_column='anonymPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    montantencours = models.DecimalField(db_column='montantEncours', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    dateencours = models.DateTimeField(db_column='dateEncours', blank=True, null=True)  # Field name made lowercase.
    unefactureparemail = models.BooleanField(db_column='uneFactureParEmail')  # Field name made lowercase.
    siteweb2 = models.TextField(db_column='siteWeb2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'C100-Clients'

class C101DevisEnTte(models.Model):
    t101_1_code_devis = models.CharField(db_column='T101-1-Code devis', primary_key=True, max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_7_titre_du_dossier = models.CharField(db_column='T101-7-Titre du dossier', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_8_code_client = models.CharField(db_column='T101-8-Code client', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_8_0_code_commercial = models.CharField(db_column='T101-8-0-Code commercial', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_9_0_code_affaire = models.CharField(db_column='T101-9-0-Code Affaire', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_9_nom_affaire = models.CharField(db_column='T101-9-Nom affaire', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_9_code_technicien = models.CharField(db_column='T101-9-Code Technicien', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_10_1_date_création = models.DateTimeField(db_column='T101-10-1-Date création', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_10_2_date_modif = models.DateTimeField(db_column='T101-10-2-Date modif', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_10_3_date_impression = models.DateTimeField(db_column='T101-10-3-Date impression', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_10_4_date_accord = models.DateTimeField(db_column='T101-10-4-Date accord', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_10_5_date_facture = models.DateTimeField(db_column='T101-10-5-Date facture', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_10_6_date_chantier = models.DateTimeField(db_column='T101-10-6-Date chantier', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_10_7_date_cloture = models.DateTimeField(db_column='T101-10-7-Date cloture', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_11_1_référence_chantier = models.CharField(db_column='T101-11-1-Référence chantier', max_length=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_11_2_livraison = models.CharField(db_column='T101-11-2-Livraison', max_length=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_11_3_paiement = models.CharField(db_column='T101-11-3-Paiement', max_length=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_11_4_echéance = models.CharField(db_column='T101-11-4-Echéance', max_length=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_12_code_tva = models.SmallIntegerField(db_column='T101-12-Code TVA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_prix_revient_devis = models.DecimalField(db_column='T101-13-Prix revient devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_1_prix_de_revient_des_lignes_du_devis = models.DecimalField(db_column='T101-13-1-Prix de revient des lignes du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_2_tarif_1_des_lignes_du_devis = models.DecimalField(db_column='T101-13-2-Tarif 1 des lignes du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_3_prix_de_vente_des_lignes_du_devis = models.DecimalField(db_column='T101-13-3-Prix de vente des lignes du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_3_0_prix_de_vente_calculé_des_lignes_non_bloquées = models.DecimalField(db_column='T101-13-3-0-Prix de vente calculé des lignes non bloquées', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_3_1_prix_de_vente_imposé_des_lignes_du_devis = models.DecimalField(db_column='T101-13-3-1-Prix de vente imposé des lignes du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_3_2_prix_de_vente_imposé_ttc_des_lignes_du_devis = models.DecimalField(db_column='T101-13-3-2-Prix de vente imposé TTC des lignes du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_3_3_gestion_des_lignes_du_devis = models.DecimalField(db_column='T101-13-3-3-Gestion des lignes du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_3_4_frais_des_lignes_du_devis = models.DecimalField(db_column='T101-13-3-4-Frais des lignes du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_3_5_prix_de_vente_final_des_lignes_du_devis = models.DecimalField(db_column='T101-13-3-5-Prix de vente final des lignes du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_3_6_prix_de_vente_final_ttc_des_lignes_du_devis = models.DecimalField(db_column='T101-13-3-6-Prix de vente final TTC des lignes du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_4_prix_de_revient_des_niveaux_du_devis = models.DecimalField(db_column='T101-13-4-Prix de revient des niveaux du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_5_tarif_1_des_niveaux_du_devis = models.DecimalField(db_column='T101-13-5-Tarif 1 des niveaux du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_6_prix_de_vente_des_niveaux_du_devis = models.DecimalField(db_column='T101-13-6-Prix de vente des niveaux du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_6_1_prix_de_vente_calculé_des_niveaux_non_bloqués = models.DecimalField(db_column='T101-13-6-1-Prix de vente calculé des niveaux non bloqués', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_7_prix_de_vente_imposé_des_niveaux_du_devis = models.DecimalField(db_column='T101-13-7-Prix de vente imposé des niveaux du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_8_prix_de_vente_imposé_ttc_des_niveaux_du_devis = models.DecimalField(db_column='T101-13-8-Prix de vente imposé TTC des niveaux du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_9_gestion_des_niveaux_du_devis = models.DecimalField(db_column='T101-13-9-Gestion des niveaux du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_10_frais_des_niveaux_du_devis = models.DecimalField(db_column='T101-13-10-Frais des niveaux du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_11_prix_de_vente_final_des_niveaux_du_devis = models.DecimalField(db_column='T101-13-11-Prix de vente final des niveaux du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_12_prix_de_vente_final_ttc_des_niveaux_du_devis = models.DecimalField(db_column='T101-13-12-Prix de vente final TTC des niveaux du devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_14_coef_1 = models.DecimalField(db_column='T101-14-Coef 1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_15_prix_1 = models.DecimalField(db_column='T101-15-Prix 1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_16_coef_2 = models.DecimalField(db_column='T101-16-Coef 2', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_17_prix_de_vente_calculé = models.DecimalField(db_column='T101-17-Prix de vente calculé', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_18_prix_de_vente_imposé = models.DecimalField(db_column='T101-18-Prix de vente imposé', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_18_0_prix_de_vente_calculé_non_bloqué = models.DecimalField(db_column='T101-18-0-Prix de vente calculé non bloqué', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_18_1_gestion = models.DecimalField(db_column='T101-18-1-Gestion', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_18_2_frais = models.DecimalField(db_column='T101-18-2-Frais', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_18_3_prix_de_vente_final = models.DecimalField(db_column='T101-18-3-Prix de vente final', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_19_prix_de_vente_imposé_ttc = models.DecimalField(db_column='T101-19-Prix de vente imposé TTC', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_19_1_prix_de_vente_final_ttc = models.DecimalField(db_column='T101-19-1-Prix de vente final TTC', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_20_coef_de_vente_ht = models.DecimalField(db_column='T101-20-Coef de vente HT', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_21_taux_de_marge = models.DecimalField(db_column='T101-21-Taux de marge', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_22_temps_total = models.DecimalField(db_column='T101-22-Temps total', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_23_marge_brute = models.DecimalField(db_column='T101-23-Marge brute', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_24_marge_par_heure = models.DecimalField(db_column='T101-24-Marge par heure', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_25_déboursé_matière_heure = models.DecimalField(db_column='T101-25-Déboursé matière/heure', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_26_lettre_d_envoi = models.TextField(db_column="T101-26-Lettre d'envoi", blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_27_texte_de_présentation = models.TextField(db_column='T101-27-Texte de présentation', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_28_texte_de_fin_de_devis = models.TextField(db_column='T101-28-Texte de fin de devis', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_29_intitulé_de_lettre = models.CharField(db_column='T101-29-Intitulé de lettre', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_30_nom_du_destinataire = models.CharField(db_column='T101-30-Nom du destinataire', max_length=70, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_31_lieu = models.CharField(db_column='T101-31-Lieu', max_length=30, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_32_date = models.DateTimeField(db_column='T101-32-Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_33_objet = models.CharField(db_column='T101-33-Objet', max_length=30, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_34_n_ref = models.CharField(db_column='T101-34-N/Ref', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_35_v_ref = models.CharField(db_column='T101-35-V/Ref', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_40_1_chantier = models.CharField(db_column='T101-40-1-Chantier', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_40_2_maître_d_oeuvre = models.CharField(db_column="T101-40-2-Maître d'oeuvre", max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_40_3_bureau_d_étude_1 = models.CharField(db_column="T101-40-3-Bureau d'étude 1", max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_40_4_bureau_d_étude_2 = models.CharField(db_column="T101-40-4-Bureau d'étude 2", max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_40_5_bureau_d_étude_3 = models.CharField(db_column="T101-40-5-Bureau d'étude 3", max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_40_6_bureau_d_étude_4 = models.CharField(db_column="T101-40-6-Bureau d'étude 4", max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_40_7_bureau_d_étude_5 = models.CharField(db_column="T101-40-7-Bureau d'étude 5", max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_41_6_date_acompte = models.DateTimeField(db_column='T101-41-6-Date_Acompte', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_41_6_acompte = models.DecimalField(db_column='T101-41-6-Acompte', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_41_7_accepter = models.BooleanField(db_column='T101-41-7-Accepter')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_41_7_refuser = models.BooleanField(db_column='T101-41-7-Refuser')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_41_7_cloturer = models.BooleanField(db_column='T101-41-7-Cloturer')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_41_8_montant_tva = models.DecimalField(db_column='T101-41-8-Montant_TVA', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_41_9_tva_ok = models.BooleanField(db_column='T101-41-9-TVA_OK')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_103_type = models.IntegerField(db_column='T101-103-Type', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gest_stock = models.BooleanField(db_column='Gest_Stock')  # Field name made lowercase.
    gest_mo = models.BooleanField(db_column='Gest_Mo')  # Field name made lowercase.
    t101_103_1_sectact = models.IntegerField(db_column='T101-103-1-SectAct', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    codegroupe = models.IntegerField(db_column='CodeGroupe', blank=True, null=True)  # Field name made lowercase.
    tarif = models.CharField(db_column='Tarif', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detaxe = models.BooleanField(db_column='Detaxe')  # Field name made lowercase.
    t101_42_texte_condition_reglement = models.TextField(db_column='T101-42-Texte-Condition-Reglement', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_14_entreprise = models.SmallIntegerField(db_column='T101-14-Entreprise', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    clidiv = models.BooleanField(db_column='CliDiv')  # Field name made lowercase.
    coefpv = models.DecimalField(db_column='CoefPV', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    mtf = models.DecimalField(db_column='mtF', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    mte = models.DecimalField(db_column='mtE', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    t101_18_3_avantremise = models.DecimalField(db_column='T101-18-3-AvantRemise', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_18_3_avantremisef = models.DecimalField(db_column='T101-18-3-AvantRemiseF', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_18_3_avantremisee = models.DecimalField(db_column='T101-18-3-AvantRemiseE', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_41_7_type = models.CharField(db_column='T101-41-7-Type', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_50_ajustement_devis = models.DecimalField(db_column='T101-50-Ajustement-Devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_51_ajustement_gestion = models.DecimalField(db_column='T101-51-Ajustement-Gestion', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_52_ajustement_frais = models.DecimalField(db_column='T101-52-Ajustement-Frais', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_60_marge_devis = models.DecimalField(db_column='T101-60-Marge-Devis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_99_ecart_vente = models.DecimalField(db_column='T101-99-Ecart vente', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_100_dessin = models.BinaryField(db_column='T101-100-Dessin', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t12_1_code = models.CharField(db_column='T12-1-Code', max_length=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_4_0_débourséouvrage = models.DecimalField(db_column='T101-13-4-0-DébourséOuvrage', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_13_4_1_débourséfraischantier = models.DecimalField(db_column='T101-13-4-1-DébourséFraisChantier', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_15_adresse = models.IntegerField(db_column='T101-15-Adresse', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_101_devori = models.CharField(db_column='T101-101-DevOri', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_101_devcopie = models.CharField(db_column='T101-101-DevCopie', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t101_102_tcre = models.SmallIntegerField(db_column='T101-102-TCre', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    lgrad = models.SmallIntegerField(db_column='lgRad', blank=True, null=True)  # Field name made lowercase.
    cptligne = models.IntegerField(db_column='cptLigne', blank=True, null=True)  # Field name made lowercase.
    délaisemaine = models.CharField(db_column='DélaiSemaine', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar1 = models.CharField(db_column='ValPar1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar2 = models.CharField(db_column='ValPar2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar3 = models.CharField(db_column='ValPar3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar4 = models.CharField(db_column='ValPar4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar5 = models.CharField(db_column='ValPar5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar6 = models.CharField(db_column='ValPar6', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar7 = models.CharField(db_column='ValPar7', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar8 = models.CharField(db_column='ValPar8', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar9 = models.CharField(db_column='ValPar9', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar10 = models.CharField(db_column='ValPar10', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar11 = models.CharField(db_column='ValPar11', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar12 = models.CharField(db_column='ValPar12', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar13 = models.CharField(db_column='ValPar13', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar14 = models.CharField(db_column='ValPar14', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar15 = models.CharField(db_column='ValPar15', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar16 = models.CharField(db_column='ValPar16', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar17 = models.CharField(db_column='ValPar17', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar18 = models.CharField(db_column='ValPar18', max_length=255, blank=True, null=True)  # Field name made lowercase.
    bloque = models.BooleanField(db_column='Bloque')  # Field name made lowercase.
    cptchapitre = models.IntegerField(db_column='cptChapitre', blank=True, null=True)  # Field name made lowercase.
    monnaiecreation = models.CharField(db_column='monnaieCreation', max_length=3, blank=True, null=True)  # Field name made lowercase.
    modelivraisonimpose = models.BooleanField(db_column='modeLivraisonImpose')  # Field name made lowercase.
    dateexport = models.DateTimeField(db_column='dateExport', blank=True, null=True)  # Field name made lowercase.
    indiccalcul = models.BooleanField(db_column='indicCalcul')  # Field name made lowercase.
    adr_nom = models.CharField(max_length=60, blank=True, null=True)
    adr_adresse = models.CharField(max_length=60, blank=True, null=True)
    adr_adresse2 = models.CharField(max_length=60, blank=True, null=True)
    adr_cp = models.CharField(db_column='adr_CP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    adr_ville = models.CharField(max_length=60, blank=True, null=True)
    adr_tel = models.CharField(max_length=20, blank=True, null=True)
    adr_fax = models.CharField(max_length=20, blank=True, null=True)
    adr_interlocuteur = models.CharField(max_length=70, blank=True, null=True)
    adr_telvoiture = models.CharField(db_column='adr_TelVoiture', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adr_email = models.CharField(db_column='adr_Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codedevise = models.CharField(db_column='codeDevise', max_length=3, blank=True, null=True)  # Field name made lowercase.
    coursdevise = models.DecimalField(db_column='coursDevise', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    archive = models.BooleanField()
    bibpiece = models.BooleanField(db_column='bibPiece')  # Field name made lowercase.
    franco = models.BooleanField()
    daterelance = models.DateTimeField(db_column='dateRelance', blank=True, null=True)  # Field name made lowercase.
    datederniererelance = models.DateTimeField(db_column='dateDerniereRelance', blank=True, null=True)  # Field name made lowercase.
    typeemballage = models.CharField(db_column='typeEmballage', max_length=10, blank=True, null=True)  # Field name made lowercase.
    poidsemballage = models.DecimalField(db_column='poidsEmballage', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    nbcolis = models.IntegerField(db_column='nbColis', blank=True, null=True)  # Field name made lowercase.
    poidsnet = models.DecimalField(db_column='poidsNet', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    adrf_nom = models.CharField(db_column='adrF_nom', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_adresse = models.CharField(db_column='adrF_adresse', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_adresse2 = models.CharField(db_column='adrF_adresse2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_cp = models.CharField(db_column='adrF_CP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    adrf_ville = models.CharField(db_column='adrF_ville', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_tel = models.CharField(db_column='adrF_tel', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adrf_fax = models.CharField(db_column='adrF_fax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adrf_interlocuteur = models.CharField(db_column='adrF_interlocuteur', max_length=70, blank=True, null=True)  # Field name made lowercase.
    adrf_codeclient = models.CharField(db_column='adrF_codeClient', max_length=10, blank=True, null=True)  # Field name made lowercase.
    encombrement = models.CharField(max_length=60, blank=True, null=True)
    adr_commentaire = models.TextField(blank=True, null=True)
    adrf_commentaire = models.TextField(db_column='adrF_commentaire', blank=True, null=True)  # Field name made lowercase.
    codeusermodif = models.CharField(db_column='codeUserModif', max_length=10, blank=True, null=True)  # Field name made lowercase.
    adr_codepays = models.CharField(db_column='adr_codePays', max_length=2, blank=True, null=True)  # Field name made lowercase.
    adr_pays = models.CharField(max_length=60, blank=True, null=True)
    adrf_codepays = models.CharField(db_column='adrF_codePays', max_length=2, blank=True, null=True)  # Field name made lowercase.
    adrf_pays = models.CharField(db_column='adrF_pays', max_length=60, blank=True, null=True)  # Field name made lowercase.
    validiteoffre = models.CharField(db_column='validiteOffre', max_length=255, blank=True, null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    creationpar = models.CharField(db_column='creationPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modifdate = models.DateTimeField(db_column='modifDate', blank=True, null=True)  # Field name made lowercase.
    modifpar = models.CharField(db_column='modifPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    editiondate = models.DateTimeField(db_column='editionDate', blank=True, null=True)  # Field name made lowercase.
    editionpar = models.CharField(db_column='editionPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    maildate = models.DateTimeField(db_column='mailDate', blank=True, null=True)  # Field name made lowercase.
    mailpar = models.CharField(db_column='mailPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    poids = models.DecimalField(max_digits=28, decimal_places=15, blank=True, null=True)
    volume = models.DecimalField(max_digits=28, decimal_places=15, blank=True, null=True)
    surface = models.DecimalField(max_digits=28, decimal_places=15, blank=True, null=True)
    codemotifrefusdevis = models.CharField(db_column='codeMotifRefusDevis', max_length=10, blank=True, null=True)  # Field name made lowercase.
    asynchroserveur = models.BooleanField(db_column='aSynchroServeur')  # Field name made lowercase.
    datesynchroserveur = models.DateTimeField(db_column='dateSynchroServeur', blank=True, null=True)  # Field name made lowercase.
    datedebut = models.DateTimeField(db_column='dateDebut', blank=True, null=True)  # Field name made lowercase.
    datefin = models.DateTimeField(db_column='dateFin', blank=True, null=True)  # Field name made lowercase.
    planif = models.BooleanField()
    numbanque = models.IntegerField(db_column='numBanque', blank=True, null=True)  # Field name made lowercase.
    codeincoterm = models.CharField(db_column='codeIncoterm', max_length=3, blank=True, null=True)  # Field name made lowercase.
    versionreference = models.BooleanField(db_column='versionReference')  # Field name made lowercase.
    datedelailivraison = models.DateTimeField(db_column='dateDelaiLivraison', blank=True, null=True)  # Field name made lowercase.
    tarifprixttc = models.BooleanField(db_column='tarifPrixTTC')  # Field name made lowercase.
    repertoireged = models.TextField(db_column='repertoireGED', blank=True, null=True)  # Field name made lowercase.
    adr_gln = models.CharField(db_column='adr_GLN', max_length=13, blank=True, null=True)  # Field name made lowercase.
    adrf_gln = models.CharField(db_column='adrF_GLN', max_length=13, blank=True, null=True)  # Field name made lowercase.
    dateenvoiedi = models.DateTimeField(db_column='dateEnvoiEdi', blank=True, null=True)  # Field name made lowercase.
    envoiedipar = models.CharField(db_column='envoiEDIpar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    volumenet = models.DecimalField(db_column='volumeNet', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    lieuincoterm = models.CharField(db_column='lieuIncoterm', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numlangue = models.SmallIntegerField(db_column='numLangue', blank=True, null=True)  # Field name made lowercase.
    codemateriel = models.CharField(db_column='codeMateriel', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'C101-Devis en tête'

class C601ChantierEnTte(models.Model):
    t601_1_code_chantier = models.CharField(db_column='T601-1-Code chantier', primary_key=True, max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_2_titre_du_chantier = models.CharField(db_column='T601-2-Titre du chantier', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_3_adresse_1 = models.CharField(db_column='T601-3-Adresse 1', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_4_adresse_2 = models.CharField(db_column='T601-4-Adresse 2', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_5_cp = models.CharField(db_column='T601-5-CP', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_6_ville = models.CharField(db_column='T601-6-Ville', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_7_tél_1 = models.CharField(db_column='T601-7-Tél 1', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_8_tél_2 = models.CharField(db_column='T601-8-Tél 2', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_9_fax = models.CharField(db_column='T601-9-Fax', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_11_etat_du_chantier = models.CharField(db_column='T601-11-Etat du chantier', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_12_code_client = models.CharField(db_column='T601-12-Code client', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_13_date_création_chantier = models.DateTimeField(db_column='T601-13-Date création chantier', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_14_date_cloture = models.DateTimeField(db_column='T601-14-Date cloture', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_15_prix_revient_chantier = models.DecimalField(db_column='T601-15-Prix revient chantier', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_26_commentaire = models.TextField(db_column='T601-26-commentaire', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_13_date_création = models.DateTimeField(db_column='T601-13-Date création', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    codeaffaire = models.CharField(db_column='CodeAffaire', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t601_30_entreprise = models.SmallIntegerField(db_column='T601-30-Entreprise', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    resp = models.CharField(db_column='Resp', max_length=10, blank=True, null=True)  # Field name made lowercase.
    delai = models.DateTimeField(blank=True, null=True)
    delaidemande = models.DateTimeField(db_column='delaiDemande', blank=True, null=True)  # Field name made lowercase.
    facture = models.IntegerField(db_column='Facture', blank=True, null=True)  # Field name made lowercase.
    refcli = models.CharField(db_column='RefCli', max_length=60, blank=True, null=True)  # Field name made lowercase.
    avoir = models.BooleanField(db_column='Avoir')  # Field name made lowercase.
    facsep = models.SmallIntegerField(db_column='FacSep', blank=True, null=True)  # Field name made lowercase.
    echeance = models.CharField(db_column='Echeance', max_length=2, blank=True, null=True)  # Field name made lowercase.
    livraison = models.CharField(db_column='Livraison', max_length=2, blank=True, null=True)  # Field name made lowercase.
    reglement = models.CharField(db_column='Reglement', max_length=2, blank=True, null=True)  # Field name made lowercase.
    datedeb = models.DateTimeField(db_column='DateDeb', blank=True, null=True)  # Field name made lowercase.
    datefin = models.DateTimeField(db_column='DateFin', blank=True, null=True)  # Field name made lowercase.
    datedebcal = models.DateTimeField(db_column='DateDebCal', blank=True, null=True)  # Field name made lowercase.
    datefincal = models.DateTimeField(db_column='DateFinCal', blank=True, null=True)  # Field name made lowercase.
    sectact = models.IntegerField(db_column='SectAct', blank=True, null=True)  # Field name made lowercase.
    tf_fournituredetail = models.BooleanField(db_column='TF_FournitureDetail')  # Field name made lowercase.
    tf_modetail = models.BooleanField(db_column='TF_MoDetail')  # Field name made lowercase.
    tf_montanttotal = models.BooleanField(db_column='TF_MontantTotal')  # Field name made lowercase.
    tf_brutremise = models.BooleanField(db_column='TF_BrutRemise')  # Field name made lowercase.
    codegroupe = models.IntegerField(db_column='CodeGroupe', blank=True, null=True)  # Field name made lowercase.
    tarif = models.CharField(db_column='Tarif', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detaxe = models.BooleanField(db_column='Detaxe')  # Field name made lowercase.
    codadr = models.IntegerField(db_column='CodAdr', blank=True, null=True)  # Field name made lowercase.
    clidiv = models.BooleanField(db_column='CliDiv')  # Field name made lowercase.
    coefpv = models.DecimalField(db_column='coefPV', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    indicdelai = models.CharField(db_column='IndicDelai', max_length=2, blank=True, null=True)  # Field name made lowercase.
    nominterl = models.CharField(db_column='nomInterl', max_length=70, blank=True, null=True)  # Field name made lowercase.
    depot = models.BooleanField()
    bl_chiffre = models.BooleanField(db_column='BL_Chiffre')  # Field name made lowercase.
    t601_30_nom_du_destinataire = models.CharField(db_column='T601-30-Nom du destinataire', max_length=70, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_31_code_tva = models.SmallIntegerField(db_column='T601-31-Code TVA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    valpar1 = models.CharField(db_column='ValPar1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar2 = models.CharField(db_column='ValPar2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar3 = models.CharField(db_column='ValPar3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar4 = models.CharField(db_column='ValPar4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar5 = models.CharField(db_column='ValPar5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar6 = models.CharField(db_column='ValPar6', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar7 = models.CharField(db_column='ValPar7', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar8 = models.CharField(db_column='ValPar8', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar9 = models.CharField(db_column='ValPar9', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar10 = models.CharField(db_column='ValPar10', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar11 = models.CharField(db_column='ValPar11', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar12 = models.CharField(db_column='ValPar12', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar13 = models.CharField(db_column='ValPar13', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar14 = models.CharField(db_column='ValPar14', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar15 = models.CharField(db_column='ValPar15', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar16 = models.CharField(db_column='ValPar16', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar17 = models.CharField(db_column='ValPar17', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valpar18 = models.CharField(db_column='ValPar18', max_length=255, blank=True, null=True)  # Field name made lowercase.
    t601_8_0_code_commercial = models.CharField(db_column='T601-8-0-Code commercial', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_9_code_technicien = models.CharField(db_column='T601-9-Code Technicien', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    planif = models.BooleanField()
    planiffixe = models.BooleanField(db_column='planifFixe')  # Field name made lowercase.
    valid = models.BooleanField(db_column='Valid')  # Field name made lowercase.
    montantht_brut = models.DecimalField(db_column='montantHT_brut', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    montantht_net = models.DecimalField(db_column='montantHT_net', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    t601_32_ttc = models.DecimalField(db_column='T601-32-TTC', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t601_33_tva = models.DecimalField(db_column='T601-33-TVA', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    codedevise = models.CharField(db_column='codeDevise', max_length=3, blank=True, null=True)  # Field name made lowercase.
    coursdevise = models.DecimalField(db_column='coursDevise', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    archive = models.BooleanField()
    textedebut = models.TextField(db_column='texteDebut', blank=True, null=True)  # Field name made lowercase.
    textefin = models.TextField(db_column='texteFin', blank=True, null=True)  # Field name made lowercase.
    datecreation = models.DateTimeField(db_column='dateCreation', blank=True, null=True)  # Field name made lowercase.
    marche = models.BooleanField()
    portfranco = models.BooleanField(db_column='portFranco')  # Field name made lowercase.
    francoimpose = models.BooleanField(db_column='francoImpose')  # Field name made lowercase.
    montantacompte = models.DecimalField(db_column='montantAcompte', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    montantecheance = models.DecimalField(db_column='montantEcheance', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    adrf_nom = models.CharField(db_column='adrF_nom', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_adresse = models.CharField(db_column='adrF_adresse', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_adresse2 = models.CharField(db_column='adrF_adresse2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_cp = models.CharField(db_column='adrF_CP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    adrf_ville = models.CharField(db_column='adrF_ville', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_tel = models.CharField(db_column='adrF_tel', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adrf_fax = models.CharField(db_column='adrF_fax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adrf_interlocuteur = models.CharField(db_column='adrF_interlocuteur', max_length=70, blank=True, null=True)  # Field name made lowercase.
    adrf_codeclient = models.CharField(db_column='adrF_codeClient', max_length=10, blank=True, null=True)  # Field name made lowercase.
    adrl_nom = models.CharField(db_column='adrL_nom', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrl_interlocuteur = models.CharField(db_column='adrL_interlocuteur', max_length=70, blank=True, null=True)  # Field name made lowercase.
    codetransporteur = models.CharField(db_column='codeTransporteur', max_length=10, blank=True, null=True)  # Field name made lowercase.
    indicavancement = models.CharField(db_column='indicAvancement', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nivrevuecontrat = models.SmallIntegerField(db_column='nivRevueContrat', blank=True, null=True)  # Field name made lowercase.
    typeemballage = models.CharField(db_column='typeEmballage', max_length=10, blank=True, null=True)  # Field name made lowercase.
    poidsemballage = models.DecimalField(db_column='poidsEmballage', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    nbcolis = models.IntegerField(db_column='nbColis', blank=True, null=True)  # Field name made lowercase.
    poidsnet = models.DecimalField(db_column='poidsNet', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    encombrement = models.CharField(max_length=60, blank=True, null=True)
    datelancementauplustot = models.DateTimeField(db_column='dateLancementAuPlusTot', blank=True, null=True)  # Field name made lowercase.
    datelancementauplustard = models.DateTimeField(db_column='dateLancementAuPlusTard', blank=True, null=True)  # Field name made lowercase.
    datefinauplustot = models.DateTimeField(db_column='dateFinAuPlusTot', blank=True, null=True)  # Field name made lowercase.
    datefinauplustard = models.DateTimeField(db_column='dateFinAuPlusTard', blank=True, null=True)  # Field name made lowercase.
    acomptecodearticle = models.CharField(db_column='acompteCodeArticle', max_length=25, blank=True, null=True)  # Field name made lowercase.
    acomptecodepg = models.CharField(db_column='acompteCodePG', max_length=5, blank=True, null=True)  # Field name made lowercase.
    acomptecodetva = models.SmallIntegerField(db_column='acompteCodeTVA', blank=True, null=True)  # Field name made lowercase.
    acomptecodefacture = models.CharField(db_column='acompteCodeFacture', max_length=20, blank=True, null=True)  # Field name made lowercase.
    acomptemodededuction = models.SmallIntegerField(db_column='acompteModeDeduction', blank=True, null=True)  # Field name made lowercase.
    acomptesoldededuction = models.DecimalField(db_column='acompteSoldeDeduction', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    adrf_commentaire = models.TextField(db_column='adrF_commentaire', blank=True, null=True)  # Field name made lowercase.
    adrl_commentaire = models.TextField(db_column='adrL_commentaire', blank=True, null=True)  # Field name made lowercase.
    dateenvoiedi = models.DateTimeField(db_column='dateEnvoiEdi', blank=True, null=True)  # Field name made lowercase.
    numcdeedi = models.IntegerField(db_column='numCdeEdi', blank=True, null=True)  # Field name made lowercase.
    idmailedi = models.CharField(db_column='idMailEdi', max_length=60, blank=True, null=True)  # Field name made lowercase.
    datemodification = models.DateTimeField(db_column='dateModification', blank=True, null=True)  # Field name made lowercase.
    adrl_codepays = models.CharField(db_column='adrL_codePays', max_length=2, blank=True, null=True)  # Field name made lowercase.
    adrl_pays = models.CharField(db_column='adrL_pays', max_length=60, blank=True, null=True)  # Field name made lowercase.
    adrf_codepays = models.CharField(db_column='adrF_codePays', max_length=2, blank=True, null=True)  # Field name made lowercase.
    adrf_pays = models.CharField(db_column='adrF_pays', max_length=60, blank=True, null=True)  # Field name made lowercase.
    codecontrat = models.CharField(db_column='codeContrat', max_length=15, blank=True, null=True)  # Field name made lowercase.
    cbndispo = models.BooleanField(db_column='CBNdispo')  # Field name made lowercase.
    cbnencours = models.BooleanField(db_column='CBNencours')  # Field name made lowercase.
    codeusermodif = models.CharField(db_column='codeUserModif', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    creationpar = models.CharField(db_column='creationPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modifdate = models.DateTimeField(db_column='modifDate', blank=True, null=True)  # Field name made lowercase.
    modifpar = models.CharField(db_column='modifPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    editiondate = models.DateTimeField(db_column='editionDate', blank=True, null=True)  # Field name made lowercase.
    editionpar = models.CharField(db_column='editionPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ventecomptoir = models.BooleanField(db_column='venteComptoir')  # Field name made lowercase.
    envoiedipar = models.CharField(db_column='envoiEDIpar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    maildate = models.DateTimeField(db_column='mailDate', blank=True, null=True)  # Field name made lowercase.
    mailpar = models.CharField(db_column='mailPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    poids = models.DecimalField(max_digits=28, decimal_places=15, blank=True, null=True)
    volume = models.DecimalField(max_digits=28, decimal_places=15, blank=True, null=True)
    numbanque = models.IntegerField(db_column='numBanque', blank=True, null=True)  # Field name made lowercase.
    codeincoterm = models.CharField(db_column='codeIncoterm', max_length=3, blank=True, null=True)  # Field name made lowercase.
    numordreplanning = models.IntegerField(db_column='numOrdrePlanning', blank=True, null=True)  # Field name made lowercase.
    tarifprixttc = models.BooleanField(db_column='tarifPrixTTC')  # Field name made lowercase.
    depotnomenclatureof = models.BooleanField(db_column='depotNomenclatureOF')  # Field name made lowercase.
    adrl_gln = models.CharField(db_column='adrL_GLN', max_length=13, blank=True, null=True)  # Field name made lowercase.
    adrf_gln = models.CharField(db_column='adrF_GLN', max_length=13, blank=True, null=True)  # Field name made lowercase.
    repertoireged = models.TextField(db_column='repertoireGED', blank=True, null=True)  # Field name made lowercase.
    volumenet = models.DecimalField(db_column='volumeNet', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    lieuincoterm = models.CharField(db_column='lieuIncoterm', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numlangue = models.SmallIntegerField(db_column='numLangue', blank=True, null=True)  # Field name made lowercase.
    codemateriel = models.CharField(db_column='codeMateriel', max_length=25, blank=True, null=True)  # Field name made lowercase.
    codefournisseur = models.CharField(db_column='codeFournisseur', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'C601-Chantier en tête'

class C7001Phases(models.Model):
    codephase = models.CharField(db_column='CodePhase', max_length=25, blank=True, null=True)  # Field name made lowercase.
    codechantier = models.CharField(db_column='CodeChantier', primary_key=True, max_length=20)  # Field name made lowercase.
    datedeb = models.DateTimeField(db_column='DateDeb', blank=True, null=True)  # Field name made lowercase.
    datefin = models.DateTimeField(db_column='DateFin', blank=True, null=True)  # Field name made lowercase.
    libphase = models.CharField(db_column='LibPhase', max_length=60, blank=True, null=True)  # Field name made lowercase.
    codedevis = models.CharField(db_column='CodeDevis', max_length=20)  # Field name made lowercase.
    comm = models.TextField(db_column='Comm', blank=True, null=True)  # Field name made lowercase.
    etat = models.CharField(db_column='Etat', max_length=2, blank=True, null=True)  # Field name made lowercase.
    delai = models.DateTimeField(db_column='Delai', blank=True, null=True)  # Field name made lowercase.
    datecreation = models.DateTimeField(db_column='DateCreation', blank=True, null=True)  # Field name made lowercase.
    codesalarie = models.CharField(db_column='CodeSalarie', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dbesoin = models.DateTimeField(db_column='DBesoin', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=2, blank=True, null=True)  # Field name made lowercase.
    indicdelai = models.CharField(db_column='IndicDelai', max_length=2, blank=True, null=True)  # Field name made lowercase.
    natureof = models.CharField(db_column='natureOF', max_length=10, blank=True, null=True)  # Field name made lowercase.
    typeof = models.CharField(db_column='typeOF', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cc_approuve = models.CharField(db_column='CC_Approuve', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cc_applique = models.CharField(db_column='CC_Applique', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cc_controle = models.CharField(db_column='CC_Controle', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fin_bl = models.TextField(db_column='Fin_BL', blank=True, null=True)  # Field name made lowercase.
    debut_bl = models.TextField(db_column='Debut_BL', blank=True, null=True)  # Field name made lowercase.
    of_commande = models.BooleanField(db_column='OF_Commande')  # Field name made lowercase.
    nonqualite = models.CharField(db_column='NonQualite', max_length=5, blank=True, null=True)  # Field name made lowercase.
    numnonqualite = models.CharField(db_column='numNonQualite', max_length=60, blank=True, null=True)  # Field name made lowercase.
    mtfactant = models.DecimalField(db_column='MtFactAnt', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    mtfactper = models.DecimalField(db_column='MtFactPer', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    daterecette = models.DateTimeField(db_column='DateRecette', blank=True, null=True)  # Field name made lowercase.
    simulok = models.BooleanField(db_column='simulOK')  # Field name made lowercase.
    etatplanif = models.SmallIntegerField(db_column='etatPlanif', blank=True, null=True)  # Field name made lowercase.
    codefacture = models.CharField(db_column='codeFacture', max_length=20, blank=True, null=True)  # Field name made lowercase.
    codeofrgp = models.CharField(db_column='codeOFRgp', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dateexport = models.DateTimeField(db_column='dateExport', blank=True, null=True)  # Field name made lowercase.
    codetransporteur = models.CharField(db_column='codeTransporteur', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nbcolis = models.IntegerField(db_column='nbColis', blank=True, null=True)  # Field name made lowercase.
    poidscolis = models.DecimalField(db_column='poidsColis', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    etattransport = models.CharField(db_column='etatTransport', max_length=5, blank=True, null=True)  # Field name made lowercase.
    adr_nom = models.CharField(max_length=60, blank=True, null=True)
    adr_adresse = models.CharField(max_length=60, blank=True, null=True)
    adr_adresse2 = models.CharField(max_length=60, blank=True, null=True)
    adr_cp = models.CharField(db_column='adr_CP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    adr_ville = models.CharField(max_length=60, blank=True, null=True)
    adr_tel = models.CharField(max_length=20, blank=True, null=True)
    adr_fax = models.CharField(max_length=20, blank=True, null=True)
    adr_interlocuteur = models.CharField(max_length=70, blank=True, null=True)
    adr_telvoiture = models.CharField(db_column='adr_TelVoiture', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adr_email = models.CharField(db_column='adr_Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    delaiinitial = models.DateTimeField(db_column='delaiInitial', blank=True, null=True)  # Field name made lowercase.
    postecharge = models.CharField(db_column='posteCharge', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datelancementauplustot = models.DateTimeField(db_column='dateLancementAuPlusTot', blank=True, null=True)  # Field name made lowercase.
    codeofpere = models.CharField(db_column='codeOFPere', max_length=20, blank=True, null=True)  # Field name made lowercase.
    numlignecde = models.DecimalField(db_column='numLigneCde', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    planiffixe = models.BooleanField(db_column='planifFixe')  # Field name made lowercase.
    ventile = models.BooleanField()
    datelancementauplustard = models.DateTimeField(db_column='dateLancementAuPlusTard', blank=True, null=True)  # Field name made lowercase.
    datefinauplustot = models.DateTimeField(db_column='dateFinAuPlusTot', blank=True, null=True)  # Field name made lowercase.
    datefinauplustard = models.DateTimeField(db_column='dateFinAuPlusTard', blank=True, null=True)  # Field name made lowercase.
    encombrement = models.CharField(max_length=60, blank=True, null=True)
    stockclient = models.BooleanField(db_column='stockClient')  # Field name made lowercase.
    codenc = models.CharField(db_column='codeNC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adr_commentaire = models.TextField(blank=True, null=True)
    dateenvoiedi = models.DateTimeField(db_column='dateEnvoiEdi', blank=True, null=True)  # Field name made lowercase.
    adr_codepays = models.CharField(db_column='adr_codePays', max_length=2, blank=True, null=True)  # Field name made lowercase.
    adr_pays = models.CharField(max_length=60, blank=True, null=True)
    calculdebut = models.DateTimeField(db_column='calculDebut', blank=True, null=True)  # Field name made lowercase.
    calculfin = models.DateTimeField(db_column='calculFin', blank=True, null=True)  # Field name made lowercase.
    codedevise = models.CharField(db_column='codeDevise', max_length=3, blank=True, null=True)  # Field name made lowercase.
    equilibragevalide = models.BooleanField(db_column='equilibrageValide')  # Field name made lowercase.
    codedepotpiece = models.CharField(db_column='codeDepotPiece', max_length=20, blank=True, null=True)  # Field name made lowercase.
    codeoflettreofpere = models.CharField(db_column='codeOFLettreOFPere', max_length=3, blank=True, null=True)  # Field name made lowercase.
    codeofnum = models.SmallIntegerField(db_column='codeOFNum', blank=True, null=True)  # Field name made lowercase.
    datecalculbesoinnet = models.DateTimeField(db_column='dateCalculBesoinNet', blank=True, null=True)  # Field name made lowercase.
    numlignebesoinnet = models.IntegerField(db_column='numLigneBesoinNet', blank=True, null=True)  # Field name made lowercase.
    codeusermodif = models.CharField(db_column='codeUserModif', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    creationpar = models.CharField(db_column='creationPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modifdate = models.DateTimeField(db_column='modifDate', blank=True, null=True)  # Field name made lowercase.
    modifpar = models.CharField(db_column='modifPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    editiondate = models.DateTimeField(db_column='editionDate', blank=True, null=True)  # Field name made lowercase.
    editionpar = models.CharField(db_column='editionPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datepreparation = models.DateTimeField(db_column='datePreparation', blank=True, null=True)  # Field name made lowercase.
    userpreparation = models.CharField(db_column='userPreparation', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dateattenteappro = models.DateTimeField(db_column='dateAttenteAppro', blank=True, null=True)  # Field name made lowercase.
    userattenteappro = models.CharField(db_column='userAttenteAppro', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dateattente = models.DateTimeField(db_column='dateAttente', blank=True, null=True)  # Field name made lowercase.
    userattente = models.CharField(db_column='userAttente', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dateproduction = models.DateTimeField(db_column='dateProduction', blank=True, null=True)  # Field name made lowercase.
    userproduction = models.CharField(db_column='userProduction', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datebloque = models.DateTimeField(db_column='dateBloque', blank=True, null=True)  # Field name made lowercase.
    userbloque = models.CharField(db_column='userBloque', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datesuspendu = models.DateTimeField(db_column='dateSuspendu', blank=True, null=True)  # Field name made lowercase.
    usersuspendu = models.CharField(db_column='userSuspendu', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datealivrer = models.DateTimeField(db_column='dateALivrer', blank=True, null=True)  # Field name made lowercase.
    useralivrer = models.CharField(db_column='userALivrer', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datelivre = models.DateTimeField(db_column='dateLivre', blank=True, null=True)  # Field name made lowercase.
    userlivre = models.CharField(db_column='userLivre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datetermine = models.DateTimeField(db_column='dateTermine', blank=True, null=True)  # Field name made lowercase.
    usertermine = models.CharField(db_column='userTermine', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datebonafacturer = models.DateTimeField(db_column='dateBonAFacturer', blank=True, null=True)  # Field name made lowercase.
    userbonafacturer = models.CharField(db_column='userBonAFacturer', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datefacture = models.DateTimeField(db_column='dateFacture', blank=True, null=True)  # Field name made lowercase.
    userfacture = models.CharField(db_column='userFacture', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datenonfacture = models.DateTimeField(db_column='dateNonFacture', blank=True, null=True)  # Field name made lowercase.
    usernonfacture = models.CharField(db_column='userNonFacture', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codeoforigine = models.CharField(db_column='codeOFOrigine', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nbpalette = models.SmallIntegerField(db_column='nbPalette', blank=True, null=True)  # Field name made lowercase.
    envoiedipar = models.CharField(db_column='envoiEDIpar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    maildate = models.DateTimeField(db_column='mailDate', blank=True, null=True)  # Field name made lowercase.
    mailpar = models.CharField(db_column='mailPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    envoieditransportpar = models.CharField(db_column='envoiEDItransportPar', max_length=10, blank=True, null=True)  # Field name made lowercase.
    envoieditransportdate = models.DateTimeField(db_column='envoiEDItransportDate', blank=True, null=True)  # Field name made lowercase.
    poids = models.DecimalField(max_digits=28, decimal_places=15, blank=True, null=True)
    volume = models.DecimalField(max_digits=28, decimal_places=15, blank=True, null=True)
    entetebl = models.BooleanField(db_column='enteteBL')  # Field name made lowercase.
    datevalidav = models.DateTimeField(db_column='DateValidAv', blank=True, null=True)  # Field name made lowercase.
    numpda = models.SmallIntegerField(db_column='numPDA', blank=True, null=True)  # Field name made lowercase.
    numexport = models.IntegerField(db_column='numExport', blank=True, null=True)  # Field name made lowercase.
    numordreplanning = models.IntegerField(db_column='numOrdrePlanning', blank=True, null=True)  # Field name made lowercase.
    adr_gln = models.CharField(db_column='adr_GLN', max_length=13, blank=True, null=True)  # Field name made lowercase.
    numlangue = models.SmallIntegerField(db_column='numLangue', blank=True, null=True)  # Field name made lowercase.
    codemateriel = models.CharField(db_column='codeMateriel', max_length=25, blank=True, null=True)  # Field name made lowercase.
    criterelibre1 = models.CharField(db_column='critereLibre1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre2 = models.CharField(db_column='critereLibre2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre3 = models.CharField(db_column='critereLibre3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre4 = models.CharField(db_column='critereLibre4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre5 = models.CharField(db_column='critereLibre5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre6 = models.CharField(db_column='critereLibre6', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre7 = models.CharField(db_column='critereLibre7', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre8 = models.CharField(db_column='critereLibre8', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre9 = models.CharField(db_column='critereLibre9', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre10 = models.CharField(db_column='critereLibre10', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre11 = models.CharField(db_column='critereLibre11', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre12 = models.CharField(db_column='critereLibre12', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre13 = models.CharField(db_column='critereLibre13', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre14 = models.CharField(db_column='critereLibre14', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre15 = models.CharField(db_column='critereLibre15', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre16 = models.CharField(db_column='critereLibre16', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre17 = models.CharField(db_column='critereLibre17', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criterelibre18 = models.CharField(db_column='critereLibre18', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codecdetransport = models.CharField(db_column='codeCdeTransport', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nbemballage1 = models.SmallIntegerField(db_column='nbEmballage1', blank=True, null=True)  # Field name made lowercase.
    nbemballage2 = models.SmallIntegerField(db_column='nbEmballage2', blank=True, null=True)  # Field name made lowercase.
    nbemballage3 = models.SmallIntegerField(db_column='nbEmballage3', blank=True, null=True)  # Field name made lowercase.
    nbemballage4 = models.SmallIntegerField(db_column='nbEmballage4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        ordering = ("-codephase",)
        db_table = 'C700-1-Phases'
        unique_together = (('codechantier', 'codedevis'),)

#liste des commande - BL
class C701Ouvraof(models.Model):
    codechantier = models.CharField(db_column='CodeChantier', primary_key=True, max_length=20)  # Field name made lowercase.
    codeof = models.CharField(db_column='CodeOF', max_length=20)  # Field name made lowercase.
    numlig = models.DecimalField(db_column='NumLig', max_digits=28, decimal_places=15)  # Field name made lowercase.
    codouv = models.CharField(db_column='CodOuv', max_length=25, blank=True, null=True)  # Field name made lowercase.
    titre = models.CharField(db_column='Titre', max_length=60, blank=True, null=True)  # Field name made lowercase.
    descriptif = models.TextField(db_column='Descriptif', blank=True, null=True)  # Field name made lowercase.
    unite = models.CharField(db_column='Unite', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pg = models.CharField(db_column='PG', max_length=5, blank=True, null=True)  # Field name made lowercase.
    qte1 = models.DecimalField(db_column='Qte1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qte2 = models.DecimalField(db_column='Qte2', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qte3 = models.DecimalField(db_column='Qte3', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qte4 = models.DecimalField(db_column='Qte4', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    nbre = models.DecimalField(db_column='Nbre', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    long = models.DecimalField(db_column='Long', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    larg = models.DecimalField(db_column='Larg', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    epai = models.DecimalField(db_column='Epai', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    pvu1 = models.DecimalField(db_column='PVU1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    pvt1 = models.DecimalField(db_column='PVT1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    pru = models.DecimalField(db_column='PRU', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    prt = models.DecimalField(db_column='PRT', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    coef1 = models.DecimalField(db_column='Coef1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    coef2 = models.DecimalField(db_column='Coef2', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    pvbase = models.DecimalField(db_column='PVBase', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    rem = models.DecimalField(db_column='Rem', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    pvu = models.DecimalField(db_column='PVU', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    pvt = models.DecimalField(db_column='PVT', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    pue = models.DecimalField(db_column='PUE', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    puf = models.DecimalField(db_column='PUF', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    mte = models.DecimalField(db_column='mtE', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    mtf = models.DecimalField(db_column='mtF', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    ctva = models.SmallIntegerField(db_column='CTVA', blank=True, null=True)  # Field name made lowercase.
    sstk = models.BooleanField(db_column='SStk')  # Field name made lowercase.
    qtsstk = models.DecimalField(db_column='QtSStk', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtcc = models.DecimalField(db_column='QtCC', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qral = models.DecimalField(db_column='QRal', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    bledit = models.BooleanField(db_column='BLEdit')  # Field name made lowercase.
    poids = models.DecimalField(db_column='Poids', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    surf = models.DecimalField(db_column='Surf', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    vol = models.DecimalField(db_column='Vol', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    poidstotal = models.DecimalField(db_column='PoidsTotal', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    surftotal = models.DecimalField(db_column='SurfTotal', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    voltotal = models.DecimalField(db_column='VolTotal', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    nuance = models.DecimalField(db_column='Nuance', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    parametre = models.DecimalField(db_column='Parametre', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    repere1 = models.CharField(db_column='Repere1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    repere2 = models.CharField(db_column='Repere2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codeof_ref = models.CharField(db_column='CodeOF_Ref', max_length=20, blank=True, null=True)  # Field name made lowercase.
    numlig_ref = models.DecimalField(db_column='NumLig_Ref', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    poidsnet = models.DecimalField(db_column='PoidsNet', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    volnet = models.DecimalField(db_column='VolNet', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtéprisestk = models.DecimalField(db_column='QtéPriseStk', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtébesfab = models.DecimalField(db_column='QtéBesFab', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtéfab = models.DecimalField(db_column='QtéFab', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtérebus = models.DecimalField(db_column='QtéRebus', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtéastker = models.DecimalField(db_column='QtéAStker', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    estk = models.BooleanField(db_column='EStk')  # Field name made lowercase.
    longmm = models.DecimalField(db_column='longMM', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    largmm = models.DecimalField(db_column='largMM', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    epmm = models.DecimalField(db_column='epMM', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    repereplan = models.CharField(db_column='reperePlan', max_length=255, blank=True, null=True)  # Field name made lowercase.
    indice = models.CharField(max_length=255, blank=True, null=True)
    zone1 = models.CharField(max_length=255, blank=True, null=True)
    zone2 = models.CharField(max_length=255, blank=True, null=True)
    priximpose = models.BooleanField(db_column='prixImpose')  # Field name made lowercase.
    numnonqualite = models.CharField(db_column='numNonQualite', max_length=60, blank=True, null=True)  # Field name made lowercase.
    methode = models.SmallIntegerField(blank=True, null=True)
    delai = models.DateTimeField(blank=True, null=True)
    delaiinitial = models.DateTimeField(db_column='delaiInitial', blank=True, null=True)  # Field name made lowercase.
    delaiansem = models.CharField(db_column='delaiANSEM', max_length=7, blank=True, null=True)  # Field name made lowercase.
    delaiinitialansem = models.CharField(db_column='delaiInitialANSEM', max_length=7, blank=True, null=True)  # Field name made lowercase.
    libelleclient = models.CharField(db_column='LibelleClient', max_length=255, blank=True, null=True)  # Field name made lowercase.
    repere1devis = models.CharField(db_column='repere1Devis', max_length=30, blank=True, null=True)  # Field name made lowercase.
    typeligne = models.CharField(db_column='typeLigne', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qtefact = models.DecimalField(db_column='qteFact', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    qtestockee = models.DecimalField(db_column='qteStockee', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    originetarif = models.SmallIntegerField(db_column='origineTarif', blank=True, null=True)  # Field name made lowercase.
    remqte = models.DecimalField(db_column='remQte', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    remgroupeclient = models.DecimalField(db_column='remGroupeClient', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    etatqte = models.SmallIntegerField(db_column='etatQte', blank=True, null=True)  # Field name made lowercase.
    codefournisseur = models.CharField(db_column='codeFournisseur', max_length=10, blank=True, null=True)  # Field name made lowercase.
    descriptiftechnique = models.TextField(db_column='descriptifTechnique', blank=True, null=True)  # Field name made lowercase.
    ediecartclient = models.SmallIntegerField(db_column='ediEcartClient', blank=True, null=True)  # Field name made lowercase.
    qteresaencoursprod = models.IntegerField(db_column='qteResaEncoursProd', blank=True, null=True)  # Field name made lowercase.
    avecetude = models.BooleanField(db_column='avecEtude')  # Field name made lowercase.
    codeetude = models.CharField(db_column='codeEtude', max_length=20, blank=True, null=True)  # Field name made lowercase.
    numligneetude = models.IntegerField(db_column='numLigneEtude', blank=True, null=True)  # Field name made lowercase.
    suivimodif = models.CharField(db_column='suiviModif', max_length=2, blank=True, null=True)  # Field name made lowercase.
    numordre = models.IntegerField(db_column='numOrdre', blank=True, null=True)  # Field name made lowercase.
    numerotationstock = models.IntegerField(db_column='numerotationStock', blank=True, null=True)  # Field name made lowercase.
    indicregroupementof = models.CharField(db_column='indicRegroupementOF', max_length=3, blank=True, null=True)  # Field name made lowercase.
    reffournisseur = models.CharField(db_column='refFournisseur', max_length=60, blank=True, null=True)  # Field name made lowercase.
    repens = models.CharField(db_column='repEns', max_length=255, blank=True, null=True)  # Field name made lowercase.
    repmont = models.CharField(db_column='repMont', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lignesolde = models.BooleanField(db_column='ligneSolde')  # Field name made lowercase.
    montantremisettc = models.DecimalField(db_column='montantRemiseTTC', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    tauxremisettc = models.DecimalField(db_column='tauxRemiseTTC', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    prepaexpeditionid = models.CharField(db_column='prepaExpeditionId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prepaexpeditionligneid = models.IntegerField(db_column='prepaExpeditionLigneId', blank=True, null=True)  # Field name made lowercase.
    indicepiece = models.CharField(db_column='indicePiece', max_length=10, blank=True, null=True)  # Field name made lowercase.
    numversion = models.IntegerField(db_column='numVersion', blank=True, null=True)  # Field name made lowercase.
    montantremiseht = models.DecimalField(db_column='montantRemiseHT', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    unitecond = models.CharField(db_column='uniteCond', max_length=5, blank=True, null=True)  # Field name made lowercase.
    qtecond = models.DecimalField(db_column='qteCond', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'C701_OuvraOF'
        unique_together = (('codechantier', 'codeof', 'numlig'),)

class C101DevisClient(models.Model):
    codedevis = models.CharField(db_column='codeDevis', primary_key=True, max_length=20)  # Field name made lowercase.
    codeclient = models.CharField(db_column='codeClient', max_length=10)  # Field name made lowercase.
    destinataire = models.CharField(max_length=30, blank=True, null=True)
    refclient = models.CharField(db_column='refClient', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dateimpression = models.DateTimeField(db_column='dateImpression', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'C101-Devis_Client'
        unique_together = (('codedevis', 'codeclient'),)

#ligne de devis
class C105LignesDeDevis(models.Model):
    t105_1_code_devis = models.CharField(db_column='T105-1-Code devis', primary_key=True, max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_2_code_niveau_1 = models.DecimalField(db_column='T105-2-Code niveau 1', max_digits=38, decimal_places=17)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_3_code_niveau_2 = models.DecimalField(db_column='T105-3-Code niveau 2', max_digits=38, decimal_places=17)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_4_code_niveau_3 = models.DecimalField(db_column='T105-4-Code niveau 3', max_digits=38, decimal_places=17)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_5_n_ligne_du_devis = models.DecimalField(db_column='T105-5-N° ligne du devis', max_digits=38, decimal_places=17)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_6_code_composant = models.CharField(db_column='T105-6-Code composant', max_length=25, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_24_unité_de_vente = models.CharField(db_column='T105-24-Unité de vente', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_25_prix_de_revient_par_unité_de_vente = models.DecimalField(db_column='T105-25-Prix de revient par unité de vente', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_26_coef_1 = models.DecimalField(db_column='T105-26-Coef 1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_27_tarif_1 = models.DecimalField(db_column='T105-27-Tarif 1', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_28_coef_2 = models.DecimalField(db_column='T105-28-Coef 2', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_29_prix_de_vente_unitaire_calculé = models.DecimalField(db_column='T105-29-Prix de vente unitaire calculé', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_30_prix_de_vente_unitaire_imposé = models.DecimalField(db_column='T105-30-Prix de vente unitaire  imposé', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_30_1_remise = models.DecimalField(db_column='T105-30-1-Remise', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_30_2_code_tva = models.SmallIntegerField(db_column='T105-30-2-Code TVA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_30_3_prix_de_vente_unitaire_final = models.DecimalField(db_column='T105-30-3-Prix de vente unitaire final', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_31_prix_de_vente_calculé = models.DecimalField(db_column='T105-31-Prix de vente calculé', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_32_prix_de_vente_imposé = models.DecimalField(db_column='T105-32-Prix de vente imposé', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_32_1_gestion = models.DecimalField(db_column='T105-32-1-Gestion', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_32_2_frais = models.DecimalField(db_column='T105-32-2-Frais', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_32_3_prix_de_vente_final = models.DecimalField(db_column='T105-32-3-Prix de vente final', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_33_code_famille_de_gestion = models.CharField(db_column='T105-33-Code famille de gestion', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_34_qté_vendue = models.DecimalField(db_column='T105-34-Qté vendue', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_35_nombre = models.DecimalField(db_column='T105-35-Nombre', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_36_cadence = models.DecimalField(db_column='T105-36-Cadence', max_digits=28, decimal_places=15)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_37_1_longueur = models.DecimalField(db_column='T105-37-1-Longueur', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_37_2_largeur = models.DecimalField(db_column='T105-37-2-Largeur', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_37_3_qte = models.DecimalField(db_column='T105-37-3-Qte', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_37_4_epaisseur = models.DecimalField(db_column='T105-37-4-Epaisseur', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_39_code_édition = models.CharField(db_column='T105-39-Code édition', max_length=3, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_40_titre_de_ligne = models.CharField(db_column='T105-40-Titre de ligne', max_length=60, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_41_descriptif_court = models.TextField(db_column='T105-41-Descriptif court', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_42_descriptif_long = models.TextField(db_column='T105-42-Descriptif long', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_43_indicateur_qté_métré = models.CharField(db_column='T105-43-Indicateur qté métré', max_length=1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_44_indicateur_montant_imposé = models.BooleanField(db_column='T105-44-Indicateur montant imposé')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_44_1_indicateur_coefficients_imposés = models.BooleanField(db_column='T105-44-1-Indicateur coefficients imposés')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_45_coef_de_vente_ht = models.DecimalField(db_column='T105-45-Coef de vente HT', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_46_taux_de_marge = models.DecimalField(db_column='T105-46-Taux de marge', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_47_temps_total = models.DecimalField(db_column='T105-47-Temps total', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_48_marge_totale = models.DecimalField(db_column='T105-48-Marge totale', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_49_marge_totale_heure = models.DecimalField(db_column='T105-49-Marge totale / heure', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_50_déboursé_matière_heure = models.DecimalField(db_column='T105-50-Déboursé matière / heure', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_55_indicateur_sous_detail = models.BooleanField(db_column='T105-55-Indicateur-Sous-Detail')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_56_indicateur_métré = models.BooleanField(db_column='T105-56-Indicateur-Métré')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_57_indicateur_descriptif2 = models.BooleanField(db_column='T105-57-Indicateur-Descriptif2')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_58_mo_unitaire = models.DecimalField(db_column='T105-58-MO-Unitaire', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_59_mo_qte_unitaire = models.DecimalField(db_column='T105-59-MO-Qte-Unitaire', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_60_mo_total = models.DecimalField(db_column='T105-60-MO-Total', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_61_mo_qte_total = models.DecimalField(db_column='T105-61-MO-Qte-Total', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_62_achat_unitaire = models.DecimalField(db_column='T105-62-Achat-Unitaire', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_63_achat_total = models.DecimalField(db_column='T105-63-Achat-Total', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    t105_64_prix_revient_total = models.DecimalField(db_column='T105-64-Prix-Revient-Total', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    poids = models.DecimalField(db_column='Poids', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    surf = models.DecimalField(db_column='Surf', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    vol = models.DecimalField(db_column='Vol', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    poidstotal = models.DecimalField(db_column='PoidsTotal', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    surftotal = models.DecimalField(db_column='SurfTotal', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    voltotal = models.DecimalField(db_column='VolTotal', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    modegestion = models.SmallIntegerField(db_column='ModeGestion', blank=True, null=True)  # Field name made lowercase.
    puf = models.DecimalField(db_column='PUF', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    pue = models.DecimalField(db_column='PUE', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    mtf = models.DecimalField(db_column='MtF', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    mte = models.DecimalField(db_column='MtE', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    repere1 = models.CharField(db_column='Repere1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    repere2 = models.CharField(db_column='Repere2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    libelleclient = models.CharField(db_column='LibelleClient', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nuance = models.DecimalField(db_column='Nuance', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    parametre = models.DecimalField(db_column='Parametre', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    cdevalide = models.BooleanField(db_column='CdeValide')  # Field name made lowercase.
    poidsm = models.DecimalField(db_column='PoidsM', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    surfm = models.DecimalField(db_column='SurfM', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    volm = models.DecimalField(db_column='VolM', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    codeof = models.CharField(db_column='CodeOF', max_length=20, blank=True, null=True)  # Field name made lowercase.
    refcli = models.CharField(db_column='RefCli', max_length=20, blank=True, null=True)  # Field name made lowercase.
    codechantier = models.CharField(db_column='CodeChantier', max_length=20, blank=True, null=True)  # Field name made lowercase.
    longmm = models.DecimalField(db_column='longMM', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    largmm = models.DecimalField(db_column='largMM', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    epmm = models.DecimalField(db_column='epMM', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    repereplan = models.CharField(db_column='reperePlan', max_length=255, blank=True, null=True)  # Field name made lowercase.
    indice = models.CharField(max_length=255, blank=True, null=True)
    zone1 = models.CharField(max_length=255, blank=True, null=True)
    zone2 = models.CharField(max_length=255, blank=True, null=True)
    rgpof = models.CharField(db_column='rgpOF', max_length=3, blank=True, null=True)  # Field name made lowercase.
    genof = models.BooleanField(db_column='genOF')  # Field name made lowercase.
    margenet = models.DecimalField(db_column='margeNet', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    margeglobal = models.DecimalField(db_column='margeGlobal', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    poidsnet = models.DecimalField(db_column='poidsNet', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    postecharge = models.CharField(db_column='posteCharge', max_length=10, blank=True, null=True)  # Field name made lowercase.
    originetarif = models.SmallIntegerField(db_column='origineTarif', blank=True, null=True)  # Field name made lowercase.
    remqte = models.DecimalField(db_column='remQte', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    remgroupeclient = models.DecimalField(db_column='remGroupeClient', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    delailivraison = models.DecimalField(db_column='delaiLivraison', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    importe = models.BooleanField()
    libellerecalcul = models.BooleanField(db_column='libelleRecalcul')  # Field name made lowercase.
    indicepiece = models.CharField(db_column='indicePiece', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datedelailivraison = models.DateTimeField(db_column='dateDelaiLivraison', blank=True, null=True)  # Field name made lowercase.
    puttc = models.DecimalField(db_column='PUTTC', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    montantttc = models.DecimalField(db_column='montantTTC', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    margenette = models.DecimalField(db_column='margeNette', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    volumenet = models.DecimalField(db_column='volumeNet', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.
    unitecond = models.CharField(db_column='uniteCond', max_length=5, blank=True, null=True)  # Field name made lowercase.
    qtecond = models.DecimalField(db_column='qteCond', max_digits=28, decimal_places=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'C105-Lignes de devis'
        unique_together = (('t105_1_code_devis', 't105_2_code_niveau_1', 't105_3_code_niveau_2', 't105_4_code_niveau_3', 't105_5_n_ligne_du_devis'),)
