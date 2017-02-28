# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Par Hector MISSIAEN
"""
import Tkinter as Tk
from PIL import Image, ImageTk
import numpy as np
import tkFileDialog
import math
import matplotlib.pyplot as plt

#class used to import an image and convert it to Tkinter format
class cImage:
    
    def __init__(self, nomFichier=""):
        
        self.nomFic = nomFichier
        self.imageTK= None
        self.image = None
        self.ouvert = False
        self.histoL = []
    def ouvrir(self, nb = False):
        if self.nomFic !="" and self.ouvert == False:
            self.image=Image.open(self.nomFic)
            if nb == True:
                self.image = self.image.convert("L")
            self.pixels= np.array(self.image, dtype = 'i')
            print self.pixels
#            self.image = self.image.resize((400, 400), Image.ANTIALIAS)
            self.imageTK=ImageTk.PhotoImage(self.image)
            self.ouvert = True
            
    def moyen(self):
        self.ouvert = False
        arrayMod = np.copy(self.pixels)
        for i in range(1,len(self.pixels)-1): #iterating on lines
            for j in range(1,len(self.pixels[0])-1): #iterating on columns
                sumLum = self.pixels[i][j] + self.pixels[i][j+1] + self.pixels[i][j-1] + self.pixels[i-1][j] + self.pixels[i+1][j] + self.pixels[i-1][j-1] + self.pixels[i+1][j-1] + self.pixels[i-1][j+1] + self.pixels[i+1][j+1]
                arrayMod[i][j] = int(sumLum//9)
        self.pixels = arrayMod
        self.image = Image.fromarray(self.pixels)
        self.imageTK = ImageTk.PhotoImage(self.image)
        self.ouvert = True
        return
    
    def gaussien(self):
        arrayMod = np.copy(self.pixels)
        for i in range(1,len(self.pixels)-1): #iterating on lines
            for j in range(1,len(self.pixels[0])-1): #iterating on columns
                sumLum = 4*self.pixels[i][j] + self.pixels[i][j+1] + self.pixels[i][j-1] + self.pixels[i-1][j] + self.pixels[i+1][j]
                arrayMod[i][j] = int(sumLum//8)
        self.pixels = arrayMod
        self.image = Image.fromarray(self.pixels)
        self.imageTK = ImageTk.PhotoImage(self.image)
    
    def prewitt(self):
        arrayMod = np.copy(self.pixels)    
        for i in range(1,len(self.pixels)-1): #iterating on lines
            for j in range(1,len(self.pixels[0])-1): #iterating on columns
                sumLumX = self.pixels[i][j+1] + self.pixels[i-1][j+1] + self.pixels[i+1][j+1] - self.pixels[i][j-1] - self.pixels[i-1][j-1] - self.pixels[i+1][j-1]
                sumLumY = self.pixels[i+1][j] + self.pixels[i+1][j-1] + self.pixels[i+1][j+1] - self.pixels[i-1][j] - self.pixels[i-1][j-1] - self.pixels[i-1][j+1]
                grad = int(math.sqrt(sumLumX**2 + sumLumY**2))
                arrayMod[i][j] = grad
        self.pixels = arrayMod
        self.image = Image.fromarray(self.pixels)
        self.imageTK = ImageTk.PhotoImage(self.image)
        
    def laplacien(self):
        arrayMod = np.copy(self.pixels)    
        for i in range(1,len(self.pixels)-1): #iterating on lines
            for j in range(1,len(self.pixels[0])-1): #iterating on columns
                sumLum = 8*self.pixels[i][j] - self.pixels[i][j+1] - self.pixels[i][j-1] - self.pixels[i-1][j] - self.pixels[i+1][j] - self.pixels[i-1][j-1] - self.pixels[i+1][j-1] - self.pixels[i-1][j+1] - self.pixels[i+1][j+1]
                arrayMod[i][j] = sumLum
        self.pixels = arrayMod
        self.image = Image.fromarray(self.pixels)
        self.imageTK = ImageTk.PhotoImage(self.image)
    
    def seuillageManuel(self,seuil):
        arrayMod = np.copy(self.pixels)
        for i in range(0, len(self.pixels)):
            for j in range(0, len(self.pixels[0])):
                if self.pixels[i][j] >= seuil:
                    arrayMod[i][j] = 255
                else:
                    arrayMod[i][j] = 0
        self.pixels = arrayMod
        self.image = Image.fromarray(self.pixels)
        self.imageTK = ImageTk.PhotoImage(self.image)

    def seuillageAutomatique(self):
        s=128
        #entropy
        #variance
        if self.histoL == []:
            self.histogramme()
        sEntropie = self.seuillageEntropie(self.histoL)
        sVariance = self.seuillageVariance(s, self.histoL, 0)
        print sEntropie,sVariance
        return 
    
    def seuillageEntropie(self, histoL):
        s = 0    
        
        for s in range(0,255):    
            for i in range(0, len(histoL)): #get number of pixels and weighted average before and after the ceiling
                nbPixelsBefore = 0
                nbPixelsAfter = 0
                moyBefore = 0
                moyAfter = 0
                while i <= s:
                    nbPixelsBefore += histoL[i]
                    moyBefore += i*histoL[i]
                else : 
                    nbPixelsAfter += histoL[i]
                    moyAfter += (i*histoL[i]) 
                -(nbPixelsBefore)*math.log(nbPixelsBefore)
        
    def seuillageVariance(self, s, histoL, x):
        nbPixelsBefore = 0
        nbPixelsAfter = 0
        moyBefore = 0
        moyAfter = 0
        for i in range(0, len(histoL)): #get number of pixels and weighted average before and after the ceiling
            while i <= s:
                nbPixelsBefore += histoL[i]
                moyBefore += (i+x)*histoL[i]
            else : 
                nbPixelsAfter += histoL[i]
                moyAfter += (i+x)*histoL[i]
        moyBefore /= nbPixelsBefore
        print moyBefore
        moyAfter /= nbPixelsAfter
        print moyAfter
        if s == abs(moyBefore + moyAfter)//2 :
            return s
        else:
            if abs(moyBefore + moyAfter)//2 > s:
                histoL = histoL[:s]
                x = s + len(histoL)
                s = s + len(histoL)/2
                print s
                self.seuillageVariance(s, histoL, x)
            else: 
                x= s
                histoL = histoL[s:]
                s = s - len(histoL)/2
                print s
                self.seuillageVariance(s, histoL, x)
                
        #3 classes

    def histo(self,k):
        count = 0
        for i in range(1,len(self.pixels)): #iterating on lines
            for j in range(1,len(self.pixels[0])): #iterating on columns
                if self.pixels[i][j] == k:
                    count += 1
        return count
    
    def histogramme(self):
        histoI = [0]
        for i in range(0,255):
            histoI.append(histoI[-1]+1)
        self.histoL = [0] * 256
        for i in range(0,255):
            print i
            self.histoL[i] = self.histo(i)
        plt.plot(histoI, self.histoL, "g")
        
    def imageSave(self):
            f = tkFileDialog.asksaveasfilename(defaultextension = '.gif')
            title = "Photo Editor - " + f
            root.title(title)
            self.image.save(f)
            
#define the window and all its components
class App:
    
    def __init__(self, master):
        
        self.h = 700
        self.w = 900
        
        #widget zone
        zone_wid=Tk.Frame(master).grid(column=0, sticky = "nw", padx=10)
        
        #filter widget zone
        filtre = Tk.LabelFrame(zone_wid, text="Filtrage",padx=10, pady=10)
        filtre.grid(padx=10, pady=10)
        listeFiltre =("Moyen","Gaussien","Prewitt","Laplacien")
        self.v = Tk.StringVar()
        self.v.set(listeFiltre[0])
        listeDer = Tk.OptionMenu(filtre, self.v, *listeFiltre)
        listeDer.grid(row=0, column=0)
        Tk.Button(filtre, text="Appliquer filtre", command=lambda : self.applyFilter(imageMod)).grid(row = 0, column = 1)
        
        #ceiling/floor widget zone
        seuillage = Tk.LabelFrame(zone_wid, text="Seuillage", padx=10, pady=10)
        seuillage.grid(padx=10, pady=10)
        self.scale = Tk.Scale(seuillage, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Niveau de seuillage')
        self.scale.grid(column = 0, row = 0)
        Tk.Button(seuillage, text="Seuillage", command = self.seuillage).grid(row = 0, column = 1)
        Tk.Button(seuillage, text="Seuillage automatique", command = self.seuillageAutomatique).grid(row = 1)
        
        #rotation widget zone
        rotation = Tk.LabelFrame(zone_wid, text="Rotation", padx=10, pady=10)
        rotation.grid(padx=10, pady=10)
        Tk.Button(rotation, text="90° gauche").grid(row=0,column=0)
        Tk.Button(rotation, text="90° droite").grid(row=0,column=1)
        
        #Frame for modification button
        modif = Tk.LabelFrame(zone_wid, text = "Modifier la photo", padx=10, pady = 10)     
        modif.grid(padx=10,pady=10)
        #reset button
        reset = Tk.Button(modif, text = "Annuler", command = self.reset)
        reset.grid(column=1,row=0, padx=5, pady=5)
        
        #apply button
        valider = Tk.Button(modif, text = "Valider", command = self.valider)
        valider.grid(column=0,row=0,padx=5, pady=5)
        
        #canvas for image printing
        self.zoneDess=Tk.Canvas(master,height = self.h,width = self.w, bg="grey")
        self.zoneDess.grid(column = 1, row = 1, rowspan = 4, sticky = "ne")
        
        #menu bar at top of window
        menubar = Tk.Menu(master)
        menu1 = Tk.Menu(menubar, tearoff=0)
        menu1.add_command(label="Ouvrir", command= lambda : self.chargerImageglobale())
        menu1.add_command(label="Enregistrer sous...", command = image.imageSave)
        menu1.add_command(label="Quitter", command=master.destroy)
        menubar.add_cascade(label="Fichier", menu=menu1)
        
        root.config(menu=menubar)
        
        # attach popup to canvas (right click)
        self.popup = Tk.Menu(root, tearoff=0)
        self.popup.add_command(label="Histogramme", command = self.popupHistogramme)
        
        self.zoneDess.bind("<Button-3>", self.popupCanvas)       
        
        
    #from value in OptionMenu, apply right filter to image
    def applyFilter(self,imageMod):
        print self.v.get()
        if self.v.get() == "Moyen":
            imageMod.moyen()
            self.showImage(imageMod,3)
        elif self.v.get() == "Gaussien":
            imageMod.gaussien()
            self.showImage(imageMod,3)
        elif self.v.get() == "Prewitt":
            imageMod.prewitt()
            self.showImage(imageMod,3)
        elif self.v.get() == "Laplacien":
            imageMod.laplacien()
            self.showImage(imageMod,3)
            
    #do thing for seuillageing the photo ^^        
    def seuillage(self):
        seuil = self.scale.get()
        imageMod.seuillageManuel(seuil)
        self.showImage(imageMod,3)
    def seuillageAutomatique(self):
        imageMod.seuillageAutomatique()
        self.showImage(imageMod,3)
        
    #function to reset photo to previous unmodified state        
    def reset(self):
        imageMod.pixels = image.pixels
        imageMod.image = Image.fromarray(imageMod.pixels)
        imageMod.imageTK = ImageTk.PhotoImage(imageMod.image)
        self.showImage(imageMod,3)
    
    #set reference photo to modified state       
    def valider(self):
        image.pixels = imageMod.pixels
        image.image = Image.fromarray(image.pixels)
        image.imageTK = ImageTk.PhotoImage(image.image)
        self.showImage(image)
    
    #create a popup when right clicking canvas
    def popupCanvas(self,event):
        self.popup.post(event.x_root, event.y_root)
    
    #function linked to popup
    def popupHistogramme(self):
        imageMod.histogramme()
            

        
    #from window with event as filename, open filename
    def chargerImageglobale(self):
        filepath = tkFileDialog.askopenfilename(title="Ouvrir une image",filetypes=[('gif files','.gif'),('all files','.*')])        
        image.ouvert=False
        image.nomFic=filepath
        image.ouvrir()
        self.showImage(image)
        
        imageMod.ouvert = False
        imageMod.nomFic=filepath
        imageMod.ouvrir(True) #True for greyscale and False or null for no change
        self.showImage(imageMod,3)
    
    def showImage(self, image, coeff=1):
        self.zoneDess.create_image(self.w/4 * coeff, self.h/2, image=image.imageTK)
        
    
image = cImage()
imageMod = cImage()
root=Tk.Tk()    
root.title("Photo Editor")
app = App(root)
root.mainloop()




 
