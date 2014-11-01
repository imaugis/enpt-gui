#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.QtCore import (QPoint, QString, QFile, QRegExp, QTextStream, Qt,
                          QIODevice, QProcess, QTimer, SIGNAL, QLocale,
                          QTranslator, QLibraryInfo, QTextCodec)
import os
import grp
import math
from shutil import copy

from enpt_gui_db1 import Ui_Dialog1
from enpt_gui_db2 import Ui_Dialog2
#-----------------------------------------------------------------------------------------------------------------------------------------

param = ['00', '01', '10', '11', '12', '20', '21', '22', '23', '26', '27', '29', '30', '31', '32', '33', '36', '37', '39']

d = {29: []}
rep_theme = rep_theme1 = theme = fond = ''
rep_config = "/etc/enpt-gui/"
#rep_config="./"
tb1 = []              # tableau des boutons de type 1
cwd = os.getcwd()     # chemin courant
fondF2 = None         # menu 2
fenetre_princ = None  # fenêtre de l'interface
fconfig = {'admin': 'configAdmin.rc', 'enseignant': 'configEnseignant.rc',
           'eleve': 'configEleve.rc'}  # dico des noms de fichier
intitule = {'admin': 'administrateur', 'enseignant': 'enseignant',
            'eleve': 'élève'}  # dico des intitulés
modif = 0             # variable qui indique qu'une modification a été faite dans l'interface courante
dia = None            # boite de dialogue des bouton 1 ou 2
diaout = None         # valeur de retour des boites de dialogue de modification des bouton 1 et 2

Vide = 1111           # constante utilisée dans les menu contextuels
enseignant, admin, eleve = 0, 0, 0
interface = None


def int1(s):        # Convertit chaine en entier.
    """Convertit chaine en entier."""
    try:
        ret = int(s)
    except ValueError:
        #Try float.
        ret = int(float(s))
    return ret


def float1(s):      # Convertit chaine en float.
    """Convertit chaine en float."""
    try:
        ret = float(s)
    except ValueError:
        ret = 0.0
    return ret


def conv_conf():    # convertit le dictionnaire de config
    """ convertit le dictionnaire de config """
    global rep_theme, rep_theme1, theme, fond
# taille de la fenêtre
    if 0 in d:
        FenPrinc.sx = int1(d[0][0])
        FenPrinc.sy = int1(d[0][1])
# ratio d'affichage des icones niveau 1
    if 1 in d:
        FenPrinc.ratio = float1(d[1][0])
# répertoire de thème
    if 10 in d:
        rep_theme = d[10][0]
        rep_theme1 = rep_theme
# sous rép de thème
    if 11 in d:
        theme = d[11][0]
        rep_theme += theme
# fond d'écran niveau 1
    if 12 in d:
        FenPrinc.fond = d[12][0]
#---------------bouton 1-----------------------
# fond bouton non sélectionné; le convertit directement dans le bon format pour les stylesheet de QT
    if 20 in d:
        B1.nsel = "QWidget {image: url(" + (rep_theme if d[20][0] != '/' else '') + d[20][0] + ");}"
# fond bouton sélectionné; le convertit directement dans le bon format pour les stylesheet de QT
    if 21 in d:
        B1.sel = "QWidget {image: url(" + (rep_theme if d[21][0] != '/' else '') + d[21][0] + ");}"
# reflet bouton et coord x,y; le convertit directement dans le bon format pour les stylesheet de QT
    if 22 in d:
        B1.reflet = "QWidget {image: url(" + (rep_theme if d[22][0] != '/' else '') + d[22][0] + ");}"
        B1.refletx = int1(d[22][1])
        B1.reflety = int1(d[22][2])
# taille bouton, l,h,espace entre les boutons, pos y de l'icone dans le bouton
    if 23 in d:
        B1.size_x = int1(d[23][0])
        B1.size_y = int1(d[23][1])
        B1.esp = int1(d[23][2])
        B1.yicone = int1(d[23][3])
# taille et pos label 1 ligne  -> style police,x,y,l,h
    if 26 in d:
        B1.lstyle1 = d[26][0].strip("'\"")
        B1.l1x = int1(d[26][1])
        B1.l1y = int1(d[26][2])
        B1.l1l = int1(d[26][3])
        B1.l1h = int1(d[26][4])
# taille et pos label 2 lignes -> style police,x1,y1,x2,y2,l,h
    if 27 in d:
        B1.lstyle2 = d[27][0].strip("'\"")
        B1.l2x1 = int1(d[27][1])
        B1.l2y1 = int1(d[27][2])
        B1.l2x2 = int1(d[27][3])
        B1.l2y2 = int1(d[27][4])
        B1.l2l = int1(d[27][5])
        B1.l2h = int1(d[27][6])
#---------------bouton 2-----------------------
# fond bouton non sélectionné
    if 30 in d:
        B2.nsel = "QWidget {image: url(" + (rep_theme if d[30][0] != '/' else '') + d[30][0] + ");}"
# fond bouton sélectionné
    if 31 in d:
        B2.sel = "QWidget {image: url(" + (rep_theme if d[31][0] != '/' else '') + d[31][0] + ");}"
# reflet bouton et coord x,y
    if 32 in d:
        B2.reflet = "QWidget {image: url(" + (rep_theme if d[32][0] != '/' else '') + d[32][0] + ");}"
        B2.refletx = int1(d[32][1])
        B2.reflety = int1(d[32][2])
# taille bouton, l,h,espace entre les boutons, pos y de l'icone dans le bouton
    if 33 in d:
        B2.size_x = int1(d[33][0])
        B2.size_y = int1(d[33][1])
        B2.esp = int1(d[33][2])
        B2.yicone = int1(d[33][3])
# taille et pos label 1 ligne  -> style police,x,y,l,h
    if 36 in d:
        B2.lstyle1 = d[36][0].strip("'\"")
        B2.l1x = int1(d[36][1])
        B2.l1y = int1(d[36][2])
        B2.l1l = int1(d[36][3])
        B2.l1h = int1(d[36][4])
# taille et pos label 2 lignes -> style police,x1,y1,x2,y2,l,h
    if 37 in d:
        B2.lstyle2 = d[37][0].strip("'\"")
        B2.l2x1 = int1(d[37][1])
        B2.l2y1 = int1(d[37][2])
        B2.l2x2 = int1(d[37][3])
        B2.l2y2 = int1(d[37][4])
        B2.l2l = int1(d[37][5])
        B2.l2h = int1(d[37][6])


def litConfig(fconfig):                  # lit le fichier de config
    f = open(rep_config + fconfig, 'r')  # ouvre le fichier en lecture
    while 1:                             # boucle infinie
        l = f.readline()                 # lit une ligne
        if l == '':                      # si ligne vide, alors fin
            break
        l = l.strip(' \n')               # retire le saut de ligne de fin de ligne
        n = l[0:2]                       # sépare les 2 premiers caractères
        if n not in param:
            continue                     # si les 2 caractères ne figurent pas dans la liste des paramètres, on ignore la ligne
        c = l[3:].split(',')             # on split la ligne après le 3ème caractère, avec la virgule comme séparateur
        n = int(n)                       # convertit le numéro de paramètre en entier
        if n == 39:                      # si c'est 39, c'est un bouton 2
            d[29][-1].append(c)          # dans ce cas, on ajoute cette def à la liste des def de bouton 2 associées au dernier bouton 1
        elif n == 29:                    # si c'est 29, il s'agit d'un bouton 1
            d[29].append([])            # création d'une nouvelle entrée bouton 1 dans la liste de def des boutons 1
            d[29][-1].append(c)         # ajoute la def du bouton 1
        else:
            d[n] = c                     # sinon ajoute le paramètre et sa def dans le dico des paramètres
    f.close()
    conv_conf()


def ecrit(f, val, *l):
    f.write('{}:'.format(val))
    for a in l[0:-1]:
        f.write(a)
        f.write(',')
    f.write(l[-1])
    f.write('\n')


def sauve_config():                 # écrit la configuration dans le fichier de config
    global fconfig, interface, d, modif
    f = open(rep_config + fconfig[interface], 'w')

    f.write('# 00: taille de la fenêtre l,h. si pas défini -> plein écran\n')
    if FenPrinc.sx != 0 and 0 in d:
        f.write('00:{},{}\n\n'.format(FenPrinc.sx, FenPrinc.sy))

    f.write("# 01: ratio d'affichage des icones niveau 1, automatique si pas défini\n")
    f.write('01:{}\n\n'.format(FenPrinc.ratio))

    f.write("# 10: répertoire thème\n")
    ecrit(f, '10', rep_theme1)

    f.write("\n# 11: thème dans le répertoire theme\n")
    ecrit(f, '11', theme)

    f.write("\n# 12: fond dans le répertoire theme\n")
    ecrit(f, '12', FenPrinc.fond)

    f.write("\n# 20: fond bouton 1 non sélectionné\n")
    ecrit(f, '20', d[20][0])

    f.write("\n# 21: fond bouton 1 sélectionné\n")
    ecrit(f, '21', d[21][0])

    f.write("\n# 22: reflet bouton 1,x,y\n")
    ecrit(f, '22', d[22][0], str(B1.refletx), str(B1.reflety))

    f.write("\n# 23: taille bouton 1  l,h,espace entre les boutons, pos y de l'icone dans le bouton\n")
    ecrit(f, '23', str(B1.size_x), str(B1.size_y), str(B1.esp), str(B1.yicone))

    f.write("\n# 26: taille et pos label 1 ligne  -> style police,x,y,l,h\n")
    ecrit(f, '26', B1.lstyle1, str(B1.l1x), str(B1.l1y), str(B1.l1l), str(B1.l1h))

    f.write("\n# 27: taille et pos label 2 lignes -> style police,x1,y1,x2,y2,l,h\n")
    ecrit(f, '27', B1.lstyle2, str(B1.l2x1), str(B1.l2y1), str(B1.l2x2), str(B1.l2y2), str(B1.l2l), str(B1.l2h))

    f.write("\n# 29: définition des boutons 1 -> logo, info-bulle,label1,label2\n"
            "#   39: définition des boutons 2 -> logo, info-bulle,label 1,label 2,commande\n")
    for b1 in tb1:
        b = b1.b1_[0]
        ecrit(f, '29', b[0], b[1], b[2], b[3], b[4] if len(b) > 4 else '')
        for b2 in b1.b1_[1:]:
            ecrit(f, '  39', b2[0], b2[1], b2[2], b2[3], b2[4])

    f.write("\n# 30: fond bouton 2 non sélectionné\n")
    ecrit(f, '30', d[30][0])

    f.write("\n# 31: fond bouton 2 sélectionné\n")
    ecrit(f, '31', d[31][0])

    f.write("\n# 32: reflet bouton 2,x,y\n")
    ecrit(f, '32', d[32][0], str(B2.refletx), str(B2.reflety))

    f.write("\n# 33: taille bouton 2: largeur,hauteur,espace entre les boutons, pos y de l'icone dans le bouton\n")
    ecrit(f, '33', str(B2.size_x), str(B2.size_y), str(B2.esp), str(B2.yicone))

    f.write("\n# 36: taille et pos label 1 ligne  -> style police,x,y,l,h\n")
    ecrit(f, '36', B2.lstyle1, str(B2.l1x), str(B2.l1y), str(B2.l1l), str(B2.l1h))

    f.write("\n# 37: taille et pos label 2 lignes -> style police,x1,y1,x2,y2,l,h\n")
    ecrit(f, '37', B2.lstyle2, str(B2.l2x1), str(B2.l2y1), str(B2.l2x2), str(B2.l2y2), str(B2.l2l), str(B2.l2h))

    f.close
    modif = 0
    fenetre_princ.setWindowTitle(FenPrinc.titre)


#-----------------------------------------------------------------------------------------------
class B1(QtGui.QWidget):      # boutons de niveau 1
    size_x = size_y = 0       # taille x et y
    esp = 0                   # espace entre boutons
    yicone = 0                # position y de l'icone dans le bouton
    refletx = reflety = 0     # position du reflet dans le bouton
    l1x = l1y = 0             # position de la ligne de label quand ligne unique
    l1l = l1h = 0             # taille de la ligne de label quand ligne unique
    l2x1 = l2y1 = 0           # position de la ligne 1 de label quand 2 lignes de label
    l2x2 = l2y2 = 0           # position de la ligne 2 de label quand 2 lignes de label
    l2h = l2l = 0             # taille des lignes de label quand 2 lignes
    sel = ''                  # image de fond du bouton quand bouton sélectionné
    nsel = ''                 # image de fond du bouton quand bouton non sélectionné
    reflet = ''               # image de reflet du bouton
    lstyle1 = ''              # style du label quand 1 ligne de label
    lstyle2 = ''              # style du label quand 2 ligne de label
    pasclicdroit1 = 0         # ni clic droit, ni Drop sur les icones B1 si != 0

    def __init__(self, parent, li=None, b1=None):
        super(B1, self).__init__(parent)
        self.hl = 0                 # (highlight) variable qui garde la trace de la mise en valeur du bouton
        if li:                      # a-t-on une définition d'un bouton ?
            self.b1_ = li           # on garde la liste des boutons 2 ainsi que le bouton 1 en local
        self.setFixedSize(B1.size_x, B1. size_y)  # QWidget de fond du bouton
        self.label1 = self.label2 = 0             # initialisation des labels
        if b1:                      # si on a un bouton comme original
            self.creer(b1.b1_[0])   # création du bouton
            self.bouge(b1.x, b1.y)  # mise en place
            self.highlight()        # mise en valeur
        else:                       # sinon création d'un bouton à partir de la définition
#            self.l=self.b1_[0]
            self.creer(self.b1_[0])          # création du bouton
        if admin and B1.pasclicdroit1 == 0:  # si on est Admin et pas en édition
            self.setAcceptDrops(True)        # le bouton 1 accepte les Drop

    def contextMenuEvent(self, event):       # clic droit sur bouton B1 (QContextMenuEven)
        global fondF2, admin
        if not fondF2:                            # si on n'a pas de sous-menu niveau 2
            menu = QtGui.QMenu("Niveau 1", self)  # création du menu contextuel
            if admin and B1.pasclicdroit1 == 0:   # si on est Admin et pas en édition
                modifAction = menu.addAction("Modification")
                suppAction = menu.addAction("Suppression") if len(tb1) > 1 else Vide
                avantAction = menu.addAction("Avant") if tb1.index(self) > 0 else Vide
                apresAction = menu.addAction("Après") if tb1.index(self) < (len(tb1) - 1) else Vide
                menu.addSeparator()
                rubriqueAction = menu.addAction("nouv. commande")
                action = menu.exec_(self.mapToGlobal(QPoint(event.x() + 3, event.y() + 3)))
                if action == modifAction:
                    rubrique(self)
                if action == suppAction:
                    self.suppression()
                if action == avantAction:
                    self.avant()
                if action == apresAction:
                    self.apres()
                if action == rubriqueAction:
                    self.nouveauB2()

    def dragEnterEvent(self, event):         # quand on passe en Drag sur le bouton 1
        if not self.hl:                     # si pas de highlight
            self.w.setStyleSheet(self.sel)  # highlight
        event.acceptProposedAction()        # on accepte l'événement

    def dragLeaveEvent(self, event):         # quand on sort du bouton en mode Drag
        if self.hl:
            self.w.setStyleSheet(self.nsel)  # on remet le bouton en normal
        event.accept()                       # on accepte l'événement

    def dropEvent(self, event):              # Drop
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            urlList = mimeData.urls()
            imax = len(urlList)
            if imax > 31:
                imax = 31
            text = QString()
            for i in range(0, imax):
                url = urlList[i].path()
                text += url
            b2 = B2(None, self.litDrop(text))  # on crée un bouton 2 dans le vide
            b2 = rubrique2(b2)                # édition dudit bouton
            if b2:                          # si OK à la boite de dialogue
                self.b1_.append(b2)         # rajoute le bouton 2 à la liste dur bouton 1 correspondant
        event.acceptProposedAction()        # on accepte l'événement pour valider le Drop

    def testfile(self, name):                # teste si le fichier existe
        file = QFile(name)
        # Si valid == true le fichier existe
        return file.exists()

    def name2file(self, name):               # on a un nom d'icone et on doit retrouver le nom du fichier
        nl = [name,
              "/usr/share/icons/hicolor/scalable/apps/" + name + ".svg",     # liste des répertoires où sont les icones
              "/usr/share/" + name + "/icons/" + name + ".svg",                   # on commence par les svg, puis les png
              "/usr/share/app-install/icons/" + name + ".svg",                # de résolution de plus en plus faible
              "/usr/share/icons/Humanity/apps/48/" + name + ".svg",
              "/usr/share/icons/gnome/scalable/apps/" + name + ".svg",
              "/usr/share/app-install/icons/" + name + ".png",
              "/usr/share/" + name + "/icons/" + name + ".png",
              "/usr/share/icons/hicolor/scalable/apps/" + name + ".png",
              "/usr/share/icons/hicolor/64x64/apps/" + name + ".png",
              "/usr/share/icons/hicolor/48x48/apps/" + name + ".png",
              "/usr/share/icons/hicolor/32x32/apps/" + name + ".png"]
        for n in nl:
            if self.testfile(n):        # test en boucle
                return n                        # si le test est positif, on retourne le nom du fichier
        return ""                       # sinon on retourne une chaine vide

    def litDrop(self, nf):                   # analyse du Drop (qui est un fichier Desktop)
        r = ["1/question.png", "", "", "", ""]    # définition vide d'un bouton 2
        com = ""                              # ni label, ni commande, ni icone
        file = QFile(nf)                      # création d'un QFile avec le nom du fichier
        regName = QRegExp("^Name(\\[fr(_FR)?\\])?=")  # RegExp pour retrouver le français dans le fichier
        regIcon = QRegExp("^Icon=")           # RegExp pour repérer l'icone
        regcapIcon = QRegExp("Icon=(.*)")     # RegExp pour séparer l'icone
        regExec = QRegExp("^Exec=")           # RegExp pour séparer la commande

        if not file.open(QIODevice.ReadOnly | QIODevice.Text):  # si on ne peut pas lire le fichier, on abandonne le Drop
            return r
        en = QTextStream(file)
        while not en.atEnd():
            line = en.readLine()               # on lit une ligne
            if line == "[Desktop Entry]":         # si on est dans un [Desktop Entry]
                while not en.atEnd():
                    line = en.readLine()
                    if line.startsWith("["):    # si on entre dans une autre rubrique
                        file.close()            # fin du traitement
                        return r
                    if line.contains(regName):
                        r[2] = line.split("=")[1]
                    elif line.contains(regIcon):
                        if regcapIcon.indexIn(line) > -1:
                            r[0] = self.name2file(regcapIcon.cap(1))
                    elif line.contains(regExec):
                        com = line.split("=")[1]
                        if "%" in com:
                            com = com.split("%")[0]
                            while com.endsWith(' '):
                                com.chop(1)
                        r[4] = com
        file.close()
        return r

    def nouveauB2(self):        # action "Nouvelle rubrique"
        b = rubrique2()
        if b:
            self.b1_.append(b)

    def suppression(self):      # action "Supression" du bouton
        global modif
        ret = QtGui.QMessageBox.question(self,  "Suppression", "Voulez-vous vraiment\nsupprimer ce bouton ?", QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes)
        if ret == QtGui.QMessageBox.Yes:    # OK
            nb1 = tb1.index(self)             # retrouve le bouton dans le tableau global de boutons 1
            max = len(tb1) - 1
            self.hide()                     # cache le bouton
            self.setParent(None)            # dissocie du parent
            if nb1 < max:
                for i in range(max, nb1, -1):
                    tb1[i].bouge(* tb1[i - 1].pos())        # décale les boutons à l'écran
            del(tb1[nb1])                   # supprime le bouton
            distribue()                     # redistribue les boutons à l'écran
            modifie()

    def inverse(self, a, b):                  # inverse les icones a et b (sert aux fonctions "avant" et "apres")
        global modif
        # on bouge les icones
        posa = tb1[a].pos()
        posb = tb1[b].pos()
        tb1[a].bouge(*posb)
        tb1[b].bouge(*posa)
        tb1[a], tb1[b] = tb1[b], tb1[a]
        modifie()

    def apres(self):                        # déplace le bouton courant -> après
        a = tb1.index(self)
        b = a + 1
        self.inverse(a, b)

    def avant(self):                        # déplace le bouton courant -> avant
        a = tb1.index(self)
        b = a - 1
        self.inverse(a, b)

    def creer(self, l):                              # création d'un bouton 1 avec la définition du bouton avec la liste dans 'l'
        self.w = QtGui.QWidget(self)                  # fond du bouton
        self.w.setFixedSize(B1.size_x, B1.size_y)    # définit taille du bouton
        self.w.setStyleSheet(self.nsel)             # image de fond du bouton

        self.ico = QtGui.QWidget(self)                # icone du bouton
        self.ico.setGeometry((B1.size_x - 120) // 2, self.yicone, 120, B1.size_y)
        self.ico.setStyleSheet("QWidget {image: url(%s);}" % ((rep_theme if l[0][0] != '/' else '') + l[0]))

        self.r = QtGui.QWidget(self)                  # reflet
        self.r.setFixedSize(B1.size_x, B1.size_y)
        self.r.setStyleSheet(self.reflet)
        self.r.move(self.refletx, self.reflety)

        if l[2]:                                    # si on a un label
            self.label1 = QtGui.QLabel(l[2], self)     # création d'un label
            self.label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)     # alignement du label
            if l[3]:                                # si on a un 2nd label
                self.label2 = QtGui.QLabel(l[3], self)
                self.label2.setStyleSheet(self.lstyle2)
                self.label1.setStyleSheet(self.lstyle2)
                self.label1.setFixedSize(self.l2l, self.l2h)
                self.label2.setFixedSize(self.l2l, self.l2h)
                self.label1.move(self.l2x1, self.l2y1)
                self.label2.move(self.l2x2, self.l2y2)
                self.label2.setAlignment(Qt.AlignHCenter)
            else:                                   # on n'a qu'un label
                self.label1.setStyleSheet(self.lstyle1.strip("'"))
                self.label1.setFixedSize(self.l1l, self.l1h)
                self.label1.move(self.l1x, self.l1y)

    def bouge(self, x, y):                            # bouge le bouton
        self.move(x, y)
        self.x = x
        self.y = y

    def enterEvent(self,  event):                   # on passe la souris au dessus
        self.w.setStyleSheet(self.sel)              # highlight du fond

    def leaveEvent(self, event):                   # la souris quitte le bouton
        if not self.hl:                             # si le bouton n'est pas en mode édition
            self.w.setStyleSheet(self.nsel)         # retire le highlight

    def mouseReleaseEvent(self, event):            # relaché de clic de souris
        global fondF2
        if event.button() == Qt.LeftButton:           # si clic gauche (normal)
            if fondF2:                              # si on a un menu 2
                fondF2.setParent(None)              # délie le parent
                fondF2 = None                         # détruit le menu 2
            else:
                if len(self.b1_) > 1:                 # si on a au moins un bouton B2
                    fondF2 = F2(fenetre_princ, self)   # création d'un menu 2
                else:                    # sinon
                    if len(self.b1_[0]) > 4 and self.b1_[0][4]:   # si commande pas vide
                        fenetre_princ.curseur_wait()            # met le curseur d'attente
                        QProcess.startDetached(self.b1_[0][4])  # exécute la commande

    def highlight(self):                    # force et bloque le highlight du bouton, quand on ouvre un menu 2
        self.w.setStyleSheet(self.sel)      # highlight du bouton
        self.hl = 1                           # active le blocage du highlight

    def pos(self):                          # retourne le tuple de la position du bouton
        return (self.x, self.y)


#-----------------------------------------------------------------------------------------------
class B2(QtGui.QWidget):      # boutons de niveau 2
    size_x = size_y = 0       # taille x et y
    esp = 0                   # espace entre boutons
    yicone = 0                # position y de l'icone dans le bouton
    refletx = reflety = 0       # position du reflet dans le bouton
    l1x = l1y = 0               # position de la ligne de label quand ligne unique
    l1l = l1h = 0               # taille de la ligne de label quand ligne unique
    l2x1 = l2y1 = 0             # position de la ligne 1 de label quand 2 lignes de label
    l2x2 = l2y2 = 0             # position de la ligne 2 de label quand 2 lignes de label
    l2h = l2l = 0               # taille des lignes de label quand 2 lignes
    sel = ''                  # image de fond du bouton quand bouton sélectionné
    nsel = ''                 # image de fond du bouton quand bouton non sélectionné
    reflet = ''               # image de reflet du bouton
    lstyle1 = ''              # style du label quand 1 ligne de label
    lstyle2 = ''              # style du label quand 2 ligne de label
    pasclicdroit2 = 0         # pas de clic droit sur les icones B2 si ! =  0

    def __init__(self, parent, li):               # parent du bouton, li=liste de définition du bouton
        super(B2, self).__init__(parent)         # initialisation du QWidget
        if li:
            self.b2_ = li                      # on garde le bouton 2 en local
        self.setFixedSize(B2.size_x, B2.size_y)  # dimensionne le widget support
        self.label1 = self.label2 = 0               # initialisation des labels
        self.l = self.b2_[0]                      # image d'icone de la commande
#----widget de fond
        self.w = QtGui.QWidget(self)              # fond du bouton
        self.w.setFixedSize(B2.size_x, B2.size_y)
        self.w.setStyleSheet(self.nsel)         # application du fond du bouton
#----widget d'icone
        self.ico = QtGui.QWidget(self)            # icone du bouton
        self.ico.setGeometry((B2.size_x - 60) // 2, self.yicone, 60, B2.size_y)    # positionne l'icone dans le bouton
        self.ico.setStyleSheet("QWidget {image: url(" + (rep_theme if self.l[0] != '/' else '') + self.l + ");}")   # applique l'image de l'icone
#----widget de reflet
        self.r = QtGui.QWidget(self)                  # reflet
        self.r.setFixedSize(B2.size_x, B2.size_y)    # dimensionne le reflet
        self.r.setStyleSheet(self.reflet)           # applique l'image du reflet
        self.r.move(self.refletx, self.reflety)      # déplace le reflet à sa place
#----label
        if self.l[2]:                                       # si on a un label
            self.label1 = QtGui.QLabel(self.b2_[2], self)          # lit la ligne 1
            self.label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # centrage horizontal et vertical du label
            if self.b2_[3]:                                 # si on a un 2nd label
                self.label2 = QtGui.QLabel(self.b2_[3], self)      # création le second label
                self.label2.setStyleSheet(self.lstyle2)         # applique le style2 sur le 2nd label
                self.label1.setStyleSheet(self.lstyle2)         # applique le style2 sur le 1er label
                self.label1.setFixedSize(self.l2l, self.l2h)     # dimensionne les 2 lignes de label en taille2
                self.label2.setFixedSize(self.l2l, self.l2h)
                self.label1.move(self.l2x1, self.l2y1)               # bouge les 2 lignes de label
                self.label2.move(self.l2x2, self.l2y2)
                self.label2.setAlignment(Qt.AlignHCenter)       # centrage du 2nd label
            else:                                           # on n'a qu'un label
                self.label1.setStyleSheet(self.lstyle1.strip("'"))  # application du style 1 ligne de label
                self.label1.setFixedSize(self.l1l, self.l1h)         # dimensionne la ligne unique
                self.label1.move(self.l1x, self.l1y)                 # positionne la ligne

    def cache(self):                # cache le bouton
        self.hide()

    def bouge(self, x, y):            # déplace le bouton
        self.move(x, y)
        self.x = x
        self.y = y

    def pos(self):                # renvoie un tuple (x,y) de position du bouton
        return (self.x, self.y)

    def enterEvent(self, event):        # événement quand la souris passe au dessus du bouton
        self.w.setStyleSheet(self.sel)

    def leaveEvent(self, event):        # événement quand la souris sort du bouton
        self.w.setStyleSheet(self.nsel)

    def mouseReleaseEvent(self, event):    # événement quant on relache la souris au dessus du bouton
        if event.button() == Qt.LeftButton and not dia:    # si on relache la souris et qu'on n'est pas en cours d'édition de bouton
            fenetre_princ.curseur_wait()        # on met le curseur d'attente
            QProcess.startDetached(self.b2_[4],)    # exécute la commande
            fondF2.detruit()                # suppression du menu 2

    def contextMenuEvent(self, event):     # QContextMenuEvent # clic droit sur bouton B2
        global admin
        if admin and B2.pasclicdroit2 == 0:        # si on est en admin et qu'on n'est pas en édition
            menu = QtGui.QMenu("Niveau 2", self)            # création du menu contextuel
            modifAction = menu.addAction("Modification")
            suppAction = menu.addAction("Suppression")
            avantAction = menu.addAction("Avant") if F2.tb2.index(self) > 0 else Vide
            apresAction = menu.addAction("Après") if F2.tb2.index(self) < len(F2.tb2) - 1 else Vide
            action = menu.exec_(self.mapToGlobal(QPoint(event.x() + 3, event.y() + 3)))
            if action == modifAction:
                self.modification()
            if action == suppAction:
                self.suppression()
            if action == avantAction:
                self.avant()
            if action == apresAction:
                self.apres()

    def modification(self):        # modification du bouton
        b = rubrique2(self)        # appel de la boite de dialogue
        if b:                # si OK
            pos = self.pos()            # récupération des coordonnées du bouton
            i = F2.tb2.index(self)        # retrouve l'index du bouton dans le tableau des boutons 2 dans le menu
            self.setParent(None)        # suppression de la liaison parent
            self.hide()                # cache le bouton
            F2.tb2[i] = None            # suppression du bouton
            F2.tb2[i] = B2(F2.fm2, b)        # création du nouveau bouton
            F2.tb2[i].show()            # affichage du bouton
            F2.tb2[i].bouge(*pos)        # positionne le bouton à la place de l'ancien
            F2.b1_.b1_[i + 1] = b            # enregistre le bouton modifié

    def inverse(self, a, b):        # inverse les boutons a et b
        # on bouge les icones
        posa = F2.tb2[a].pos()        # lit la position des 2 boutons
        posb = F2.tb2[b].pos()
        F2.tb2[a].bouge(*posb)        # bouge les 2 boutons
        F2.tb2[b].bouge(*posa)
        F2.tb2[a], F2.tb2[b] = F2.tb2[b], F2.tb2[a]    # inverse les boutons dans le menu niveau 2
        # on inverse aussi les boutons 2 stockés dans les boutons 1
        tb1[F2.nb1].b1_[a + 1], tb1[F2.nb1].b1_[b + 1] = tb1[F2.nb1].b1_[b + 1], tb1[F2.nb1].b1_[a + 1]
        modifie()

    def apres(self):        # on demande de bouger l'icone vers la droite
        a = F2.tb2.index(self)
        b = a + 1
        self.inverse(a, b)

    def avant(self):        # on demande de bouger l'icone vers la gauche
        a = F2.tb2.index(self)
        b = a - 1
        self.inverse(a, b)

    def suppression(self):    # suppression du bouton
        global modif
        ret = QtGui.QMessageBox.question(fenetre_princ, "Suppression", "Voulez-vous vraiment\nsupprimer ce bouton ?", QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes)
        if ret == QtGui.QMessageBox.Yes:    # si oui
            nb2 = F2.tb2.index(self)            # retrouve l'index dans le tableau de boutons 2
            max = len(F2.tb2) - 1                # compte le nbre de boutons 2
            self.hide()                    # cache le bouton
            self.setParent(None)            # supprime la liaison parent
            if nb2 < max:                    # si ce n'est pas le dernier bouton
                for i in range(max, nb2, -1):            # décale les boutons
                    F2.tb2[i].bouge(*F2.tb2[i - 1].pos())
            del(F2.tb2[nb2])                # supprime le bouton
            del(tb1[F2.nb1].b1_[nb2 + 1])        # supprime le bouton de la table globale des boutons
            modifie()


#-----------------------------------------------------------------------------------------------
class F2(QtGui.QWidget):    # fenêtre où se trouvent les boutons 2
    b1 = 0    # icone B1 highlight
    nb1 = 0    # numéro de bouton B1 dans tb1
    b2 = 0    # tableau de boutons niveau 2
    fm = 0    # fond menu
    fm2 = 0    # fond menu transparent
    n2 = 0    # compteur de bouton l2
    tb2 = []    # liste des boutons B2
    b1_ = 0    # icone B1 d'origine

    def __init__(self, parent, b1o):
        global dia
        super(F2, self).__init__(parent)            # initialisation du QWidget
        B1.pasclicdroit1 = 1                        # dans le cas de sous menu, on n'autorise pas le drag & drop sur les icones B1
        self.setGeometry(0, 0, FenPrinc.sx, FenPrinc.sy)    # dimensionne comme la fenetre_princ
        self.fond = QtGui.QWidget(self)                # création du fond gris foncé de qui recouvre le fenetre_princ
        self.fond.setStyleSheet("border: none; image: none; background-color: rgba(0, 0, 0, 160);")    # pas de bord, pas d'image, et du noir avec transparence
        self.fond.setGeometry(0, 0, FenPrinc.sx, FenPrinc.sy)    # dimensionnement du fond gris
        self.b1 = B1(self, b1=b1o)                # recrée un bouton 1 par dessus, celui sur lequel on a cliqué pour arriver ici
        posx, posy = b1o.pos()                    # lit la position du bouton 1
        n2 = len(b1o.b1_) - 1                    # calcule le nbre de boutons 2 associés à ce bouton 1
        F2.nb1 = tb1.index(b1o)                    # retrouve la pos de b1o dans le tableau global de boutons 1
        F2.b1_ = b1o                        # on garde en local une copie du bouton 1 ainsi que les boutons 2 associés
        nbx = int(((FenPrinc.sx * 4) / 6 - 2 * B1.esp) / (B2.size_x + B2.esp))    # nbre de boutons maxi en largeur
        nl = int(math.ceil(float(n2) / float(nbx)))        # nbre de lignes du menu
        nbx = math.ceil(float(n2) / float(nl))
        larg = int((nbx if n2 > nbx else n2) * (B2.size_x + B2.esp) - B2.esp + 2 * B1.esp)    # largeur du sous menu
        if posx + B1.size_x > FenPrinc.sx / 6 + larg:
            departx = posx + B1.esp - larg
        else:
            departx = int(FenPrinc.sx / 6)                # x de départ du sous menu
        haut = int(2 * B1.esp + (B2.size_y + B2.esp) * nl - B2.esp)    # hauteur du menu

        F2.fm = QtGui.QWidget(self)                # création du QWidget pour le fond du menu 2 en couleur
        F2.fm.setGeometry(departx, (posy - 5 - haut) if (posy + B1.size_y + 5 + haut) >= FenPrinc.sy else posy + B1.size_y + 5, larg, haut)
        F2.fm.setStyleSheet("image: none; background-color: rgba(134, 204, 85, 255); border: 2px solid black; border-radius: 15px;")
        F2.fm2 = QtGui.QWidget(F2.fm)                # création du QWidget pour le fond du menu 2 transparent sur lequel on va mettre les icones boutons 2
        F2.fm2.setStyleSheet("background-color: none; border: none;")

        posx = B1.esp
        posy = posx        # positionne le départ des icones
        self.i2 = 0
        F2.tb2 = []
        for b2a in b1o.b1_[1:]:        # on parcourt la liste des boutons 2 dans la copie locale du bouton 1
            F2.tb2.append(B2(F2.fm2, b2a))    # crée le bouton 2 dans le QWidget fm2
            F2.tb2[-1].bouge(posx, posy)    # le positionne
            self.i2 += 1
            if self.i2 == nbx:            # si on est au bout de la ligne
                posx = B1.esp
                posy += B2.size_y + B2.esp    # saute une ligne
                self.i2 = 0
            else:
                posx += B2.esp + B2.size_x    # sinon on bouge vers la droite
        self.show()                # affiche le tout

    def mouseReleaseEvent(self, event):    # relaché de clic de souris
        if event.button() == Qt.LeftButton:
            self.detruit()

    def contextMenuEvent(self, event):    # clic droit sur le fond
        pass    # on ne fait rien

    def detruit(self):
        global fondF2
        self.setParent(None)
        fondF2 = None

    def __del__(self):
        global fondF2
        self.b1 = None
        self.hide()
        self.fond = None
        if B2 is not None:
            B2.tb2 = []
        fondF2 = None
        if B1 is not None:
            B1.pasclicdroit1 = 0


#-----------------------------------------------------------------------------------------------
class FenPrinc(QtGui.QMainWindow):    # fenêtre principale
    sx = sy = 0        # taille de l'écran (lu dans le sytème ou pris dans le fichier de config)
    ratio = 0        # ratio de l'écran (calculé ou pris dans le fichier de config)
    fond = ''        # fond de la fenêtre
    titre = ''        # titre de la fenêtre

    def __init__(self):
        global tb1, modif            # tableau de bouton 1 et témoin de modif
        super(FenPrinc, self).__init__()    # initialisation de QMainWindow
        modif = 0                    # pas de modif
        FenPrinc.titre = 'Enpt-Gui'        # def du titre de la fenêtre
        self.setWindowTitle(FenPrinc.titre)    # association du titre à la fenêtre
        self.setStatusBar(None)        # suppression de la barre de status
        if 0 not in d:                    # si pas de définition de taille de fenêtre dans le fichier de config
            self.setWindowFlags(Qt.FramelessWindowHint)        # on enlève les décors
            self.setWindowState(Qt.WindowFullScreen)            # on passe en plein écran
            self.setStyleSheet("background:transparent;")        # pas de fond
            self.setStyleSheet("image: none")                # pas d'image de fond
            self.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop)
            self.setAttribute(Qt.WA_TranslucentBackground)        # transparent
            self.setGeometry(QtGui.QApplication.desktop().screenGeometry())
            ecran = QtGui.QApplication.desktop().screenGeometry()    # lecture de la taille d'écran
            FenPrinc.sx = ecran.width()                    # largeur d'écran
            FenPrinc.sy = ecran.height()                # hauteur d'écran
        else:                        # si oui
            self.setFixedSize(self.sx, self.sy)            # fixe la taille de la fenêtre avec celle donnée dans le fichier de config
                                # apose une image de image de fond si elle a été définie
            self.setStyleSheet("QMainWindow {image: url(" + (rep_theme if FenPrinc.fond[0] != '/' else '') + FenPrinc.fond + ");}")
        for b1 in d[29]:            # lecture des def de boutons 1
            tb1.append(B1(self, li=b1))            # céation des boutons
        distribue()                # ditribution des boutons

    def __del__(self):        # cache le bouton
        self.hide()

    def montre(self):        # montre le bouton
        self.show()

    def curseur_wait(self):    # affiche un curseur d'attente
        self.setCursor(Qt.WaitCursor)            # sélection du curseur d'attente
        QTimer.singleShot(3000, self.curseur_normal)    # active une autre fonction au bout de 3 secondes

    def curseur_normal(self):    # affiche un curseur standard
        self.setCursor(Qt.ArrowCursor)

    def contextMenuEvent(self, event):    # clic droit sur fond (QContextMenuEvent)
        if not eleve:                                # si on n'est pas élève
            menu = QtGui.QMenu(self)                            # création menu contextuel
            adminAction = menu.addAction("Admin") if admin else Vide            # si on est Admin, ajoute un item Admin
            if admin and interface == "admin":
                adminAction.setEnabled(False)        # si on est en interface Admin, l'item est grisé
            ensAction = menu.addAction("Enseignant")                    # ajoute l'item Enseignant
            elevAction = menu.addAction("Élève")                    # ajoute l'item Eleve
            menu.addSeparator()                            # un séparateur
            saveAction = menu.addAction("Sauvegarder") if admin else Vide    # ajoute l'item Sauvegarder si on est Admin
            if admin and not modif:
                saveAction.setEnabled(False)            # il est grisé si pas de modif
            rstAction = menu.addAction("Restaurer") if admin else Vide    # ajoute l'item Restaurer si on est Admin
            rubriqueAction = menu.addAction("Nouv. rubrique") if admin else Vide    # ajoute l'item Nouvelle Rubrique si on est Admin
            action = menu.exec_(self.mapToGlobal(QPoint(event.x() + 3, event.y() + 3)))    # positionne le menu à 3 pixels vers la droite et en bas et l'exécute
            if action == adminAction:        # si on clique sur Admin
                adminconfig()
            elif action == ensAction:        # si on clique sur Enseignant
                ensconfig()
            elif action == elevAction:        # si on clique sur Eleve
                elevconfig()
            elif action == saveAction:        # si on clique sur Sauvegarder
                if QtGui.QMessageBox.warning(self, "Sauvegarde", "Vous allez sauvegarder la configuration \"%s\"\nÊtes-vous d'accord ?" % intitule[interface], QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
                    sauve_config()
            elif action == rstAction:        # si on clique sur Restaurer
                if QtGui.QMessageBox.warning(self, "Restauration", "Vous êtes sur le point de restaurer \nla configuration \"%s\"\nÊtes-vous d'accord ?" % intitule[interface], QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
                    restaure()
            elif action == rubriqueAction:    # si on clique sur Nouvelle Rubrique
                rubrique()


def rubrique(b1=None):            # si none->nouveau, si b1 -> modif
    global dia, diaout, tb1, fenetre_princ
    B1.pasclicdroit1 = 1        # pour évider le drop vers B1 dans les boites de dialogue et le clic droit
    dia = dial1(b1)        # ouverture de la boite de dialogue
    dia.show()            # affichage de la boite
    if dia.exec_():        # exec de la boite avec OK en sortie
        B1.pasclicdroit1 = 0            # réautorisation du clic droit
        if b1:                # s'il s'agit d'une modif
            b = b1.b1_
            b[0] = diaout
            pos = b1.pos()        # récupération de la position du bouton 1
            b1.hide()            # cache le bouton 1
            b1.setParent(None)        # dissocie du parent
            n = tb1.index(b1)        # retrouve la position du bouton dans la table des boutons 1
            tb1[n] = B1(fenetre_princ, b)    # recrée le bouton en écrasant l'autre, ce qui détruit l'ancien
            tb1[n].bouge(*pos)        # repositionne le nouveau bouton
            tb1[n].show()        # affiche le nouveau bouton
        else:                        # il s'agit d'un ajout
            tb1.append(B1(fenetre_princ, [diaout]))    # crée le bouton à la suite des autres
            tb1[-1].show()                # affiche le nouveau bouton
            tb1[-1].setAcceptDrops(True)        # accepte le drag&drop
            distribue()                    # reditribue les boutons 1 dans la fenetre
        modifie()                # affiche dans la barre de titre qu'il y a eu modif
    dia = None                # détruit la boite de dialogue
    B1.pasclicdroit1 = 0        # réautorisation du clic droit


def rubrique2(b2=None):            # si none->nouveau, si b2 -> modif
# la fonction retourne le B2 créé ou le B2 modifié
    global dia, diaout
    B2.pasclicdroit2 = 1    # interdiction du clic droit sur les icones 2
    dia = dial2(b2)    # ouverture de la boite de dialogue
    dia.show()        # affichage de la boite
    if dia.exec_():    # exécution de la boite et test du OK
        B2.pasclicdroit2 = 0    # réautorisation du clic droit
        modifie()        # affichage de modif dans la barre de titre
        dia = None        # destruction de la boite de dialogue
        return diaout        # retourne la définition d'un bouton 2
    else:        # annulation dans la boite
        dia = None        # destruction de la boite de dialogue
        B2.pasclicdroit2 = 0        # réautorisation de la boite de dialogue
        return None        # retourne une def de bouton 2 à None


def distribue():        # redistribue les icones niveau 1 sur le fond
    global d        # config
    if 1 not in d:                # si ratio non défini dans le fichier de config
        FenPrinc.ratio = float(sx) / float(sy)    # on calcule le ratio de l'écran
    nb1 = len(tb1)
    for nl in xrange(1, nb1 + 1):  # recherche le nombre de lignes
        if not float((B1.size_x + B1.esp) * int(nb1 / nl)) / (nl * (B1.size_y + B1.esp)) > FenPrinc.ratio:
            break

    nx = int(math.ceil((float(nb1)) / nl))                    # nbre de boutons en x
    px = int(FenPrinc.sx / 2 - ((nx * (B1.size_x + B1.esp)) - B1.esp) / 2)        # coord de départ des boutons
    py = int(FenPrinc.sy / 2 - ((nl * (B1.size_y + B1.esp)) - B1.esp) / 2)        # coord de départ des boutons
    n2 = 0
    x1 = px

    nb1 = 0
    for b1 in tb1:
        b1.bouge(x1, py)
        n2 += 1
        if n2 == nx:
            n2 = 0
            x1 = px
            py += B1.size_y + B1.esp
        else:
            x1 += B1.size_x + B1.esp


#-----------------------------------------------------------------------------------------------
class dial1(QtGui.QDialog):    # boite de dialogue de création ou modification d'une icone B1
    def __init__(self, b=None):
        global tb1, modif, diaout
        super(dial1, self).__init__()    # initialisation de QDialog
        self.ui = Ui_Dialog1()        # création de la boite de dialogue pour les icone B1
        self.ui.setupUi(self)        # initialisation de la boite de dialogue
        if b:                            # a-t-on un bouton d'origine ?
            b1t = b.b1_[0:1]                        # on ne prend que la def du bouton 1
            if len(b1t[0][3]) == 0:
                b1t[0][3] = "--------"            # si on n'a pas de label 2
            self.wa = B1(self.ui.Wa, b1t)                    # création du bouton
        else:                            # sinon, on crée un bouton vierge
            self.wa = B1(self.ui.Wa, [['1/question.png', '', '------', '------']])
        self.ui.LElabel1.setText(self.wa.b1_[0][2])        # association du label1 à la ligne d'édition
        self.ui.LElabel2.setText(self.wa.b1_[0][3])        # idem label 2
        self.commande = self.wa.b1_[0][4] if len(self.wa.b1_[0]) > 4 else ""    # test pour vérifier si on a une commande
        self.ui.LEcom.setText(self.commande)            # idem pour la commande
        # centrage du bouton dans la zone prévue dans la boite de dialogue
        self.wa.bouge((self.ui.Wa.width() - B1.size_x) / 2, (self.ui.Wa.height() - B1.size_y) / 2)
        self.filename = self.wa.b1_[0][0]
        self.label1 = self.wa.b1_[0][2]
        self.label2 = self.wa.b1_[0][3]
        self.connect(self.ui.PBvalide, SIGNAL("clicked()"), self.valide)        # association des signaux aux fonctions
        self.connect(self.ui.PBicone,  SIGNAL("clicked()"), self.icone)
        self.connect(self.ui.PBannule, SIGNAL("clicked()"), self.annule)
        self.connect(self.ui.PBcom,    SIGNAL("clicked()"), self.com)
        self.connect(self.ui.LElabel1, SIGNAL("textEdited(QString)"), self.texte1)
        self.connect(self.ui.LElabel2, SIGNAL("textEdited(QString)"), self.texte2)

    def valide(self):        # clic sur OK
        global diaout, dia
        diaout = [self.filename, '', self.ui.LElabel1.text(), self.ui.LElabel2.text()]
        self.commande = self.ui.LEcom.text()
        if len(self.commande):
            diaout.append(self.commande)
        self.done(1)

    def com(self):        # clic sur Commande
        o = QtGui.QFileDialog.getOpenFileName(self, "Sélection de commande", "~", "Fichiers Commande (*.*)")
        if o:
            self.commande = o
            self.ui.LEcom.setText(self.commande)

    def icone(self):        # clic sur icone
        o = QtGui.QFileDialog.getOpenFileName(self, "Sélection d'image", "~", "Image Files (*.png *.jpg *.bmp)")
        if o:
            self.filename = o
            if self.filename.startsWith(rep_theme):  # startsWith : fonction Qt
                self.filename = self.filename[len(rep_theme):]
            self.wa.ico.setStyleSheet("QWidget {image: url(" + (rep_theme if self.filename[0] != '/' else '') + self.filename + ");}")

    def annule(self):        # clic sur Annule
        global diaout
        diaout = None
        self.done(0)

    def texte2(self):        # on tape dans la seconde ligne de texte
        self.label2 = self.ui.LElabel2.text()
        self.wa.label2.setText(self.label2)

    def texte1(self):        # on tape dans la première ligne de texte
        self.label1 = self.ui.LElabel1.text()
        self.wa.label1.setText(self.label1)


#-----------------------------------------------------------------------------------------------
class dial2(QtGui.QDialog):    # boite de dialogue de création ou modification d'une icone B2
    def __init__(self, b=None):  # li = liste de déf du bouton 2 et b= bouton 2 à éditer
        global diaout, dia
        super(dial2, self).__init__()    # initialisation de QDialog
        self.ui = Ui_Dialog2()        # création de la boite de dialogue pour les icone B2
        self.ui.setupUi(self)        # initialisation de la boite de dialogue
        if b:                            # a-t-on un bouton d'origine ?
            b2t = b.b2_                        # b2 temporaire
            if len(b2t[3]) == 0:                    # si on n'a pas de label 2
                b2t[3] = "--------"                # on mets des pointillés dans label2
        else:
            b2t = ['1/question.png', '', '------', '------', '------']    # sinon on définit un bouton 2 vierge
        self.wa = B2(self.ui.Wa, b2t)                    # création du bouton
        # remplissage des champs
        self.ui.LElabel1.setText(self.wa.b2_[2])
        self.ui.LElabel2.setText(self.wa.b2_[3])
        self.commande = self.wa.b2_[4]
        self.ui.LEcom.setText(self.commande)
        # centrage du bouton dans la zone prévue dans la boite de dialogue
        self.wa.bouge((self.ui.Wa.width() - B2.size_x) / 2, (self.ui.Wa.height() - B2.size_y) / 2)
        self.filename = self.wa.b2_[0]
        self.label1 = self.wa.b2_[2]
        self.label2 = self.wa.b2_[3]
        self.connect(self.ui.PBvalide, SIGNAL("clicked()"), self.valide)
        self.connect(self.ui.PBicone, SIGNAL("clicked()"), self.icone)
        self.connect(self.ui.PBannule, SIGNAL("clicked()"), self.annule)
        self.connect(self.ui.PBcom, SIGNAL("clicked()"), self.com)
        self.connect(self.ui.LElabel1, SIGNAL("textEdited(QString)"), self.texte1)
        self.connect(self.ui.LElabel2, SIGNAL("textEdited(QString)"), self.texte2)

    def valide(self):
        global diaout, dia
        if len(self.ui.LEcom.text()):   # si on a quelque chose dans commande
            diaout = [self.filename, '', self.ui.LElabel1.text(), self.ui.LElabel2.text(), self.ui.LEcom.text()]
            dia = None
            self.done(1)
        else:
            QtGui.QMessageBox.warning(self, "création de commande", "Vous devez entrer\nune commande", QtGui.QMessageBox.Close)
            self.ui.LEcom.setFocus()

    def com(self):
        o = QtGui.QFileDialog.getOpenFileName(self, "Sélection de commande", "~", "Fichiers Commande (*.*)")
        if o:
            self.commande = o
            self.ui.LEcom.setText(self.commande)

    def icone(self):
        o = QtGui.QFileDialog.getOpenFileName(self, "Sélection d'image", "~", "Image Files (*.png *.jpg *.bmp)")
        if o:
            self.filename = o
            if self.filename.startsWith(rep_theme):  # startsWith : fonction Qt
                self.filename = self.filename[len(rep_theme):]
            self.wa.ico.setStyleSheet("QWidget {image: url(" + (rep_theme if self.filename[0] != '/' else '') + self.filename + ");}")

    def annule(self):
        global diaout
        diaout = None
        self.done(0)

    def texte2(self):
        self.label2 = self.ui.LElabel2.text()
        self.wa.label2.setText(self.label2)

    def texte1(self):
        self.label1 = self.ui.LElabel1.text()
        self.wa.label1.setText(self.label1)


#-----------------------------------------------------------------------------------------------
def restaure():            # restaure le fichier de configuration de l'interface en cours
    dest = os.path.join(rep_config, fconfig[interface])
    if os.path.isfile(dest):
        os.unlink(dest)
    copy(os.path.join(rep_config, "sauve_config", fconfig[interface]), dest)
    config(interface)    # réaffiche l'interface


def modifie():        # positionne la variable globale de modification et affiche un astérisque dans la barre de titre
    global modif
    modif = 1
    fenetre_princ.setWindowTitle(FenPrinc.titre + '*')


def config(i):        # détruit l'affichage courant et réaffiche la nouvelle interface
    global fenetre_princ, tb1, d, interface, fconfig, modif
    if not modif or QtGui.QMessageBox.warning(fenetre_princ, "Changement d'interface", "Vous allez quitter l'interface \"" + intitule[interface] + "\"\nalors que des modifications on eu lieu.\nVoulez-vous continuer ?", QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
        tb1 = []      # on détruit les boutons B1
        d = {29: []}   # on détruit le dictionnaire de config des boutons B1 et B2
        fenetre_princ = None        # destruction de la fenêtre principale
        modif = 0                # pas de modifications en cours
        interface = i            # modifie la variable globale interface
        litConfig(fconfig[i])        # lecture du fichier de config
        fenetre_princ = FenPrinc()    # création de la fenetre_princ
        fenetre_princ.montre()        # affichage de la fenetre_princ


def adminconfig():    # commute vers l'interface Admin
    config("admin")        # appel de la config Admin


def ensconfig():    # commute vers l'interface Enseignant
    config("enseignant")    # appel de la config Enseignant


def elevconfig():    # commute vers l'interface Eleve
    config("eleve")        # appel de la config Eleve


def quel_groupe():
    global admin, enseignant, eleve
    g = [grp.getgrgid(i)[0] for i in os.getgroups()]
    if "enseignant" in g:
        enseignant = 1
        ensconfig()
    elif "adm" in g:
        admin = 1
        adminconfig()
    else:
        eleve = 1
        config("eleve")

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)        # création de l'application
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))    # passage de qt en utf-8 par défaut
    locale = QLocale.system().name().section('_', 0, 0)        # passage dans la langue locale
    translator = QTranslator()
    translator.load("qt_" + locale, QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)
    quel_groupe()                            # vérification du groupe de l'utilisateur courant
    sys.exit(app.exec_())                        # exécution de l'interface
