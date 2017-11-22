# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Par Hector M.
"""
import Tkinter as Tk
from PIL import Image, ImageTk
import numpy as np
import tkFileDialog
import math
import matplotlib.pyplot as plt
import webbrowser

#class used to import an image and convert it to Tkinter format
class cImage:
    
    def __init__(self, nomFichier=""):
        
        self.nomFic = nomFichier
        self.imageTK = None
        self.image = None
        self.ouvert = False
        self.histoL = []
        self.sEntropie=0
        self.sVariance=0
        self.Entropie=0
        
    def ouvrir(self, nb = False):
        
        largeur = 400
        if self.nomFic !="" and self.ouvert == False:
            self.sEntropie=0
            self.sVariance=0
            self.histoL = []
            self.image=Image.open(self.nomFic)
            if nb == True:
                self.image = self.image.convert("L")
            if self.image.size[0] >= largeur:
                wpercent = (largeur/float(self.image.size[0]))
                hsize = int((float(self.image.size[1])*float(wpercent)))
                self.image = self.image.resize((largeur,hsize), Image.ANTIALIAS)
            self.pixels= np.array(self.image, dtype = 'i')
            self.imageTK=ImageTk.PhotoImage(self.image)
            self.ouvert = True
            
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

    def median(self):
        self.ouvert = False
        arrayMod = np.copy(self.pixels)
        for i in range(1,len(self.pixels)-1): #iterating on lines
            for j in range(1,len(self.pixels[0])-1): #iterating on columns
                sumLum = [self.pixels[i][j], self.pixels[i][j+1], self.pixels[i][j-1], self.pixels[i-1][j], self.pixels[i+1][j], self.pixels[i-1][j-1], self.pixels[i+1][j-1], self.pixels[i-1][j+1], self.pixels[i+1][j+1]]
                sumLum.sort()
                sumVal = sumLum[4]
                arrayMod[i][j] = int(sumVal)
        self.pixels = arrayMod
        self.image = Image.fromarray(self.pixels)
        self.imageTK = ImageTk.PhotoImage(self.image)
        self.ouvert = True
    
    def negatif(self):
        arrayMod = np.copy(self.pixels)
        for i in range(0,len(self.pixels)): #iterating on lines
            for j in range(0,len(self.pixels[0])): #iterating on columns
                arrayMod[i][j]= 255-self.pixels[i][j]
        self.pixels = arrayMod
        self.image = Image.fromarray(self.pixels)
        self.imageTK = ImageTk.PhotoImage(self.image)
        self.ouvert = True
    
    def custom(self, L):
        arrayMod = np.copy(self.pixels)
        cpt=0
        for i in L:
            cpt+=i
        for i in range(1,len(self.pixels)-1): #iterating on lines
            for j in range(1,len(self.pixels[0])-1): #iterating on columns
                sumLum = L[4]*self.pixels[i][j] + L[5]*self.pixels[i][j+1] + L[3]*self.pixels[i][j-1] + L[1]*self.pixels[i-1][j] + L[7]*self.pixels[i+1][j] + L[0]*self.pixels[i-1][j-1] + L[6]*self.pixels[i+1][j-1] + L[2]*self.pixels[i-1][j+1] + L[8]*self.pixels[i+1][j+1]
                arrayMod[i][j] = int(sumLum//cpt)
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

    def seuillageAutomatiqueV(self):
        s=127
        if self.histoL == []:
            self.histogramme()
        self.sVariance = self.seuillageVariance(s)
        self.seuillageManuel(self.sVariance)

    def seuillageAutomatiqueE(self):
        if self.histoL == []:
            self.histogramme()
        self.sEntropie = self.seuillageEntropie()
        self.seuillageManuel(self.sEntropie)

    def seuillageEntropie(self):
        s = 0    
        entropyMax = 0
        for s in range(0,255): 
            nbPixelsBefore = 0   
            nbPixelsAfter = 0    
            
            for i in range(0, len(self.histoL)): #get number of pixels and weighted average before and after the ceiling
                if i <= s:
                    nbPixelsBefore += self.histoL[i]                    
                else:
                    nbPixelsAfter += self.histoL[i]                    
            for i in range(0, len(self.histoL)):
                entropy = 0
                if i <= s:                
                    if self.histoL[i] != 0 and nbPixelsBefore != 0:
                        hMoy= float(self.histoL[i])/nbPixelsBefore
                        entropy -=  (hMoy)*math.log(hMoy)
                else :
                    if self.histoL[i] != 0 and nbPixelsAfter != 0:
                        hMoy = float(self.histoL[i])/nbPixelsAfter
                        entropy -= (hMoy)*math.log(hMoy)
           
            if entropy >= entropyMax : 
                indexEntropy= s
                entropyMax = entropy
                
        return indexEntropy
        
    def seuillageVariance(self, s):  
        it = 2
        while it <= 256 : 
            nbPixelsBefore = 0
            nbPixelsAfter = 0
            moyAfter = 0
            moyBefore = 0
            it *= 2
            for i in range(0, len(self.histoL)): #get number of pixels and weighted average before and after the ceiling
                if i <= s:
                    nbPixelsBefore += self.histoL[i]
                    moyBefore += i*self.histoL[i]
                else : 
                    nbPixelsAfter += self.histoL[i]
                    moyAfter += i*self.histoL[i]
            moyBefore /= nbPixelsBefore #weighted average
            print moyBefore
            moyAfter /= nbPixelsAfter
            print moyAfter
            if abs(moyBefore + moyAfter)//2 > s: #dichotomy process : if threshold is below average of both, set threshold to be in the right set of histogram
                s += len(self.histoL)//it
            else:
                s -= len(self.histoL)//it #dichotomy : if threshold is above average of both, set threshold to be in the left set of histogram
        return s

    def rotation(self, n):
        arrayMod = np.copy(self.pixels)
        arrayRMod = np.transpose(arrayMod)
        
        if n==2:
            arrayRMod = np.fliplr(arrayRMod)
        self.pixels = np.asarray(arrayRMod, dtype='i')
        self.image = Image.fromarray(arrayRMod)
        self.imageTK = ImageTk.PhotoImage(self.image)
    
    def symVert(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.imageTK = ImageTk.PhotoImage(self.image)

    def symHor(self):
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        self.imageTK = ImageTk.PhotoImage(self.image)
        
    def histogramme(self):
        histoI = [0]
        for i in range(0,255):
             histoI.append(histoI[-1]+1)
        self.histoL = [0] * 256
        for i in range(1,len(self.pixels)): #iterating on lines
            for j in range(1,len(self.pixels[0])): #iterating on columns
                    self.histoL[self.pixels[i][j]]+=1
        plt.plot(histoI, self.histoL, "g")
        plt.show()
        
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
        listeFiltre =("Moyen","Gaussien", "Median","Prewitt","Laplacien", "Negatif", "--------", "Contraste")
        self.v = Tk.StringVar()
        self.v.set(listeFiltre[0])
        listeDer = Tk.OptionMenu(filtre, self.v, *listeFiltre)
        listeDer.grid(row=0, column=0)
        Tk.Button(filtre, text="Appliquer filtre", command=lambda : self.applyFilter(imageMod)).grid(row = 0, column = 1)
        
        #permet la création de la matrice pour le filtre perso,et les boutons associés
        customFiltre = Tk.LabelFrame(zone_wid, text="Crée ton filtre")
        self.filtreGrid = Tk.Canvas(customFiltre, height=90, width=90, bg="black")
        self.listeValue=[0]*9
        self.val1=self.filtreGrid.create_text(15,15, text=str(0), fill="white")
        self.val2=self.filtreGrid.create_text(45,15, text=str(0), fill="white")
        self.val3=self.filtreGrid.create_text(75,15, text=str(0), fill="white")
        self.val4=self.filtreGrid.create_text(15,45, text=str(0), fill="white")
        self.val5=self.filtreGrid.create_text(45,45, text=str(0), fill="white")
        self.val6=self.filtreGrid.create_text(75,45, text=str(0), fill="white")
        self.val7=self.filtreGrid.create_text(15,75, text=str(0), fill="white")
        self.val8=self.filtreGrid.create_text(45,75, text=str(0), fill="white")
        self.val9=self.filtreGrid.create_text(75,75, text=str(0), fill="white")
        self.filtreGrid.create_line(30,0,30,90,fill="red")
        self.filtreGrid.create_line(60,0,60,90,fill="red")
        self.filtreGrid.create_line(0,30,90,30,fill="red")
        self.filtreGrid.create_line(0,60,90,60,fill="red")
        self.filtreGrid.bind("<Button-1>", self.customValue)
        self.filtreGrid.bind("<Button-3>", self.customValue)
        self.filtreGrid.bind("<Shift-Button-1>", self.customValue)
        self.filtreGrid.bind("<Shift-Button-3>", self.customValue)
        self.filtreGrid.grid()
        okCustom = Tk.Button(customFiltre, text="Ok", command=self.okCustom)
        resetCustom = Tk.Button(customFiltre, text = "Reset", command = self.resetCustom)
        resetCustom.grid()
        okCustom.grid()
        customFiltre.grid()


        #ceiling/floor widget zone
        seuillage = Tk.LabelFrame(zone_wid, text="Seuillage", padx=10, pady=10)
        seuillage.grid(padx=10, pady=10)
        self.scale = Tk.Scale(seuillage, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Niveau de seuillage')
        self.scale.grid(column = 0, row = 0)
        self.sV = Tk.IntVar()
        self.sE = Tk.IntVar()
        Tk.Button(seuillage, text="Seuillage", command = self.seuillage).grid(row = 0, column = 1)
        Tk.Label(seuillage, text="Seuillage automatique:").grid(row=1, column=0)
        Tk.Button(seuillage, text="Variance", command = self.seuillageAutomatiqueV).grid(row = 2, column=0, padx=2, pady=2)
        Tk.Label(seuillage, textvariable=self.sV).grid(row=2, column=1)
        Tk.Button(seuillage, text="Entropie", command = self.seuillageAutomatiqueE).grid(row = 3, column=0, padx=2, pady=2)
        Tk.Label(seuillage, textvariable=self.sE).grid(row=3, column=1)
        
        #rotation widget zone
        rotation = Tk.LabelFrame(zone_wid, text="Modifications géométriques", padx=10, pady=10)
        rotation.grid(padx=10, pady=10)
        Tk.Button(rotation, text="90° gauche", command = lambda : self.rotationIm(1)).grid(row=0,column=0)
        Tk.Button(rotation, text="90° droite", command = lambda : self.rotationIm(2)).grid(row=0,column=1)
        Tk.Button(rotation, text="Symétrie Verticale", command = self.symVert).grid(row=1,column=0, padx=1)
        Tk.Button(rotation, text="Symétrie Horizontale", command = self.symHor).grid(row=1,column=1, padx=1)

        #Frame for modification button
        modif = Tk.LabelFrame(zone_wid, text = "Modifier l'image", padx=10, pady = 10)     
        modif.grid(padx=10,pady=10)
        
        #reset button
        reset = Tk.Button(modif, text = "Annuler", command = self.reset)
        reset.grid(column=1,row=0, padx=5, pady=5)
        
        #apply button
        valider = Tk.Button(modif, text = "Valider", command = self.valider)
        valider.grid(column=0,row=0,padx=5, pady=5)
        
        #canvas for image printing
#        self.zoneDess = ResizingCanvas(frameCanvas)
        self.zoneDess=Tk.Canvas(master,height = self.h,width = self.w, bg="#616161")
        self.zoneDess.create_rectangle(100,580,350,620, fill="", outline="red")
        self.zoneDess.create_rectangle(535,580,815,620, fill="", outline="red")
        self.zoneDess.create_text(225,600, text="Image initiale", fill="white", font=('arial','30'))
        self.zoneDess.create_text(675,600, text="Image modifiée", fill="white", font=('helvetica','30'))
#        self.zoneDess.addtag_all("all")
        self.zoneDess.grid(column = 1, row = 1, rowspan = 5, sticky = "ne")

        
        #menu bar at top of window
        menubar = Tk.Menu(master)
        menu1 = Tk.Menu(menubar, tearoff=0)
        menu1.add_command(label="Ouvrir", command= lambda : self.chargerImageglobale())
        menu1.add_command(label="Enregistrer sous...", command = image.imageSave)
        menu1.add_command(label="Documentation", command=self.docu)
        menu1.add_command(label="Quitter", command=master.destroy)
        menubar.add_cascade(label="Fichier", menu=menu1)
        
        root.config(menu=menubar)
        
        # attach popup to canvas (right click)
        self.popup = Tk.Menu(root, tearoff=0)
        self.popup.add_command(label="Histogramme", command = self.popupHistogramme)
        
#        self.zoneDess.create_polygon([(0,0),(0,self.h),(60,self.h),(35, self.h/3)],fill="yellow")
#        self.zoneDess.create_polygon([(60,self.h),(90,self.h),(48,self.h-200)], fill="orange")
        self.zoneDess.bind("<Button-3>", self.popupCanvas)       
        
        
    # from value in OptionMenu, apply right filter to image
    def applyFilter(self,imageMod):
        print self.v.get()
        if self.v.get() == "Moyen":
            imageMod.custom([1,1,1,1,1,1,1,1,1])
            self.showImage(imageMod,3)
        elif self.v.get() == "Gaussien":
            imageMod.custom([0,1,0,1,4,1,0,1,0])
            self.showImage(imageMod,3)
        elif self.v.get() == "Prewitt":
            imageMod.prewitt()
            self.showImage(imageMod,3)
        elif self.v.get() == "Laplacien":
            imageMod.laplacien()
            self.showImage(imageMod,3)
        elif self.v.get() == "Median":
            imageMod.median()
            self.showImage(imageMod,3)
        elif self.v.get() == "Negatif":
            imageMod.negatif()
            self.showImage(imageMod,3)
        elif self.v.get() == "Contraste":
            imageMod.custom([0,-1,0,-1,5,-1,0,-1,0])
            self.showImage(imageMod,3)
    #applique le filtre perso
    def okCustom(self):
        imageMod.custom(self.listeValue)
        self.showImage(imageMod,3)
    
    #réinitialise la matrice du filtre perso
    def resetCustom(self):
        self.listeValue = [0,0,0,0,0,0,0,0,0]
        self.filtreGrid.itemconfigure(self.val1, text=str(0))       
        self.filtreGrid.itemconfigure(self.val2, text=str(0))
        self.filtreGrid.itemconfigure(self.val3, text=str(0))
        self.filtreGrid.itemconfigure(self.val4, text=str(0))
        self.filtreGrid.itemconfigure(self.val5, text=str(0))
        self.filtreGrid.itemconfigure(self.val6, text=str(0))
        self.filtreGrid.itemconfigure(self.val7, text=str(0))
        self.filtreGrid.itemconfigure(self.val8, text=str(0))
        self.filtreGrid.itemconfigure(self.val9, text=str(0))

    #détecte la valeur à incrémenter de la matrice du filtre pero
    def customValue(self, event):
        if event.num==1:
            n=2
        else:
            n=1
        c = (-1)**n
        
        if event.state ==9:
            c*=20
            
        if event.x<30 and event.y<30:
            self.listeValue[0]+=c
            print str(self.listeValue[0])
            self.filtreGrid.itemconfigure(self.val1, text=str(self.listeValue[0]))       
        elif event.x<60 and event.y<30:
            self.listeValue[1]+=c
            self.filtreGrid.itemconfigure(self.val2, text=str(self.listeValue[1]))
        elif event.x<90 and event.y<30:
            self.listeValue[2]+=c
            self.filtreGrid.itemconfigure(self.val3, text=str(self.listeValue[2]))
        elif event.x<30 and event.y<60:
            self.listeValue[3]+=c
            self.filtreGrid.itemconfigure(self.val4, text=str(self.listeValue[3]))
        elif event.x<60 and event.y<60:
            self.listeValue[4]+=c
            self.filtreGrid.itemconfigure(self.val5, text=str(self.listeValue[4]))
        elif event.x<90 and event.y<60:
            self.listeValue[5]+=c
            self.filtreGrid.itemconfigure(self.val6,text=str(self.listeValue[5]))
        elif event.x<30 and event.y<90:
            self.listeValue[6]+=c
            self.filtreGrid.itemconfigure(self.val7,text=str(self.listeValue[6]))
        elif event.x<60 and event.y<90:
            self.listeValue[7]+=c
            self.filtreGrid.itemconfigure(self.val8,text=str(self.listeValue[7]))
        elif event.x<90 and event.y<90:
            self.listeValue[8]+=c
            self.filtreGrid.itemconfigure(self.val9,text=str(self.listeValue[8]))
        print self.listeValue
    
    #effectue la somme des termes de la liste issue du filtre perso
    def sumListe(self):
        cpt=0
        for i in self.listeValue:
            cpt += i
        return cpt
    
    # appelle la fonction de symétrie verticale
    def symVert(self):
        imageMod.symVert()
        self.showImage(imageMod,3)
    
    # appelle la fonction de symétrie horizontale
    def symHor(self):
        imageMod.symHor()
        self.showImage(imageMod,3)

    #do thing for thresholding the photo ^       
    def seuillage(self):
        seuil = self.scale.get()
        imageMod.seuillageManuel(seuil)
        self.showImage(imageMod,3)
    
    def seuillageAutomatiqueV(self):
        imageMod.seuillageAutomatiqueV()
        self.sV.set(imageMod.sVariance)
        self.showImage(imageMod,3)
    
    def seuillageAutomatiqueE(self):
        imageMod.seuillageAutomatiqueE()
        self.sE.set(imageMod.sEntropie)
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
    
    def rotationIm(self,n):
        imageMod.rotation(n)
        self.showImage(imageMod, 3)                

    #from window with event as filename, open filename
    def chargerImageglobale(self):
        filepath = tkFileDialog.askopenfilename(title="Ouvrir une image",filetypes=[('gif files','.gif'),('all files','.*')])        
        image.ouvert=False
        image.nomFic=filepath
        image.ouvrir(True)
        self.showImage(image)
        
        imageMod.ouvert = False
        imageMod.nomFic=filepath
        imageMod.ouvrir(True) #True for greyscale and False or null for no change
        self.showImage(imageMod,3)
    
    def showImage(self, image, coeff=1):
        self.zoneDess.create_image(self.w/4 * coeff, self.h/2, image=image.imageTK)
    
    def docu(self):
        webbrowser.open_new(r"docu_photoprocessing.html") 

image = cImage()
imageMod = cImage()
root=Tk.Tk()    
root.title("Photo Editor")
app = App(root)
root.mainloop()


 
