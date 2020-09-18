#/usr/bin/env python
#from lor_deckcodes import LoRDeck, CardCodeAndCount
from twisted_fate import Deck
import requests
import tk
import sys
import json
import time
from twisted_fate import Card
from os import system, name
import math

from PyQt5 import QtGui, QtCore,QtWidgets
from PyQt5.QtWidgets import QMainWindow,QLabel, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QPainter,QPen, QColor, QPixmap, QBrush
from PyQt5.QtCore import Qt,QSize,QRect;



class DeckGUI(QWidget):
    def __init__(self,deck):
        QWidget.__init__(self)
        #self.setStyleSheet("background-color:#746967;")
        self.setStyleSheet("background-color:#b721c0;")
        self.setMinimumSize(QSize(1024,1024))
        self.setWindowTitle("Scary DeckTracker GUI")
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        count = 0
        heightvariable=256
        for thing in sorted(deck.cards,key= lambda card:card.cost):
            label = QLabel(thing.name)
            label.setStyleSheet("background-color:#769c5e;\ncolor: #610b66")
            label.setFont(QtGui.QFont("Verdana",15))
            label.setAlignment(Qt.AlignCenter)
            #label.setFixedHeight(heightvariable/2)
            grid_layout.addWidget(label,count,0)
            label2 = QLabel()
            #label3 = QLabel(thing.image_path_full)
            #print(thing.image_path_full)
            emptylabel=QLabel(str(thing.count))
            pixmap=QPixmap("./LOR_ART/FULL/"+thing.cardCode+"-full.png")
            if pixmap.height()<pixmap.width():
                pixmap=pixmap.copy(int(pixmap.width()/4),0,int(pixmap.width()/2),pixmap.height())
            tmp =pixmap.scaledToHeight(heightvariable).toImage()
            color =QColor()
            #print(pixmap.width(),tmp.width())

            #this colors every third of the deck
            referencepoint =int ( tmp.width()-(3-thing.count)/3*tmp.width()+1/2*tmp.height() )

            print("reference point",referencepoint)
            
            for i in range(tmp.height()):
                for j in range(referencepoint,tmp.width()-1):
                    color.setRgb(tmp.pixel(j,i))
                    color.setRgb(int(color.red()*0.2),int(color.blue()*0.2),int(color.green()*0.2))
                    tmp.setPixelColor(j,i,color)
                    
            counter = 0
            if thing.count<3:
                for i in range(tmp.height()):
                    counter+=1
                    #j=referencepoint-counter
                    for j in range(referencepoint-counter,referencepoint):
                        if 0>j or j>tmp.width()-1:
                            continue
                        color.setRgb(tmp.pixel(j,i))
                        color.setRgb(int(color.red()*0.2),int(color.blue()*0.2),int(color.green()*0.2))
                        tmp.setPixelColor(j,i,color)
            pixmap =pixmap.fromImage(tmp)
            print(pixmap.height())
            
            """
            for i in range(3-thing.count):
                print("from",math.floor(i*w/3),"to",math.floor(w/3))
                painter.drawPixmap(QRect(math.floor(i*w/3),0,math.floor(w/3),h),pixmap)
            """
            label2.setPixmap(pixmap)
            label2.setFixedHeight(45)
            #grid_layout.addWidget(label3,count,2)
            grid_layout.addWidget(label2,count,1)
            grid_layout.addWidget(emptylabel,count,2)
            
            count+=1
        
    


    def clicked2(self):
        print('Button 2 wurde angeklickt. Programmende')
        app.quit()

def GUI(deck):
    app= QtWidgets.QApplication([])
    win=DeckGUI(deck)
    win.show()
    sys.exit(app.exec_())

def printdeck(deck,maximal,minimal):
    if maximal:
        for i in sorted(deck.cards,key= lambda card:card.cost):
            #print(i.cardType)
            if i.cardType != "Spell":
                print(str(i.count)+'x',i.name,i.keywords,"["+str(i.attack)+"|"+str(i.cost)+"]")
            else:
                print(str(i.count)+'x',i.name,i.keywords,"\""+i.description.replace("\n"," ").replace("\r"," ")+"\"")
    elif minimal:
        for i in sorted(deck.cards,key= lambda card:card.cost):
            print(str(i.count)+'x'+" "+str(i.cost)+" "+i.name)

### main
maximal= False
minimal= False
deck=None
for i in sys.argv:
    if i =="-max":
        maximal=True
        deck = Deck.decode(sys.argv[1])
    if i =="-min":
        minimal=True
        deck = Deck.decode(sys.argv[1])
printdeck(deck,maximal,minimal)

### 


if sys.argv[1]=="gui":
    deck=Deck.decode(sys.argv[2])
    GUI(deck)

### Tracking    
if sys.argv[1]=="watch":
    cardCode_to_ID={}

    def init(s):
        for i in s :    
            #print(str(i.count)+'x'+" "+str(i.cost)+" "+i.name,i.cardCode)
            cardCode_to_ID[i.cardCode]=[]

    def minimallist(s):
        for i in trackerlist :    
            print(str(i.count)+'x'+" "+str(i.cost)+" "+i.name,i.cardCode)
    

    print("Waiting for a game...")
    while requests.get("http://localhost:21337/positional-rectangles").json()["GameState"]=="Menus":
        time.sleep(2.5)
    system('cls')
    
    #https://stackoverflow.com/questions/24153519/how-to-read-html-from-a-url-in-python-3
    static_decklist =requests.get("http://localhost:21337/static-decklist").json()
    #print(static_decklist)


    decklist=static_decklist["DeckCode"]
    trackerlist=sorted(Deck.decode(decklist).cards,key= lambda card:card.cost)
    init(trackerlist)
    print(cardCode_to_ID)
    count = 0
    change=""
    knownids=[]
    while decklist!=None :
        static_decklist1=requests.get("http://localhost:21337/static-decklist").json()

        #print(static_decklist1)

        decklist=static_decklist1["DeckCode"]
        #print(decklist)
        temp=requests.get("http://localhost:21337/static-decklist").json()["DeckCode"]
        GameState=requests.get("http://localhost:21337/positional-rectangles").json()

        listchange= False 

        for j in sorted(GameState["Rectangles"], key=lambda card:card["CardCode"]):  #counts copies
            #print(tmp.cardCode,tmp.cardCode,j["LocalPlayer"])
            if j["CardCode"]=="face":
                continue
            tmp = Card(CardCode=j["CardCode"],CardID=j["CardID"])
            if tmp.cardCode in knownids:
                continue
            
            if j["LocalPlayer"]==False:
                continue
            if tmp.id<0:
                print(tmp.id)
                continue
            if tmp.cardCode not in cardCode_to_ID.keys(): #generated cards like trundle pillar
                knownids.append(tmp.id)
                change+="Generated "+str(tmp.id)+": "+tmp.name+"\n"
                continue

            if tmp.id not in cardCode_to_ID[tmp.cardCode]:
                knownids.append(tmp.id)
                cardCode_to_ID[tmp.cardCode].append(tmp.id)
                change+="Drawn "+str(tmp.id)+": "+tmp.name+"\n"    
                for card in trackerlist:
                    if card.cardCode==tmp.cardCode:
                        card.count-=1
                        listchange = True
                        break
                continue
        if listchange:
            
            system("cls")
            count+=1
            #print(change)
            minimallist(trackerlist)

            print("-------------------------------------------------------------\n")
    cards=[]
    for cardcord in cardCode_to_ID.keys():
        cards.append(Card(CardCode=cardcord))
    
    print("This many draws",count)
    #for x in cardCode_to_ID.keys():
    #   print(x,"->", cardCode_to_ID[x])
    #print(knownids)


    sys.exit(0)

#print(dir(deck.cards[0]))






