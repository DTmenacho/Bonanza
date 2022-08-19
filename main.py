from pickle import TRUE
import sys
import requests
import random
import json
from PyQt5 import QtCore
import pandas as pd

from PyQt5.QtWidgets import QApplication, QPushButton, QMenu
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
from PyQt5.QtCore import QDate, QSize, QTime, QTimer, Qt, QEvent
from PyQt5.QtGui import QFont, QIcon

#variables
LINK = 'https://swapi.dev/api/people/'
IMAGEN = 'lista.png'

# Segunda pantalla para mostrar
class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        
    def settxt(self,df):
        
        #Titulo de la ventana
        self.setWindowTitle('Información detallada de ' + str(df['name'].values[0]))
        
        font = QFont('Arial', 10, QFont.Bold)

        self.lista_labels = []

        # Extraer los atributos del dataframe
        # Representarlos en labels
        for atributo in df.columns:
            if atributo == 'name' : continue
            valor = str(df[atributo].values[0])
            self.lista_labels.append(QLabel(atributo+":     "+valor))
            self.lista_labels[-1].setAlignment(Qt.AlignHCenter) 
            self.lista_labels[-1].setFont(font)
            self.layout.addWidget(self.lista_labels[-1]) 

        self.setLayout(self.layout)

# Pantalla principal
class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.w = None

        # Titulo de la ventana
        self.setWindowTitle("Postulante para ROBOTILSA S.A")

        self.setFixedSize(QSize(400, 400))

        # Label del tiempo
        layout = QVBoxLayout()
        font = QFont('Arial', 20, QFont.Bold)
        self.label_time = QLabel()
        self.label_time.setAlignment(Qt.AlignHCenter)
        self.label_time.setFont(font)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        # Actualización por cada segundo
        timer.start(1000)
        layout.addWidget(self.label_time)

        # Label de la fecha   
        self.label_date = QLabel()
        self.label_date.setAlignment(Qt.AlignHCenter)
        self.label_date.setFont(font)
        current_date = QDate.currentDate()
        label_date = current_date.toString('dd/MM/yyyy')
        self.label_date.setText(label_date)
        layout.addWidget(self.label_date,1)

        # Creación del DataFrame a partir del json
        self.df = pd.DataFrame(columns = ['name', 'height', 'mass', 
        'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender'])

        # Creación del boton de actulización del request
        self.breq = QPushButton("REQUEST",self)
        self.breq.setIcon(QIcon(IMAGEN))
        self.breq.clicked.connect(self.updatelistwidget)
        layout.addWidget(self.breq,2)

        self.listWidget = QListWidget()

        # Evento del click derecho que abre un menu
        self.listWidget.installEventFilter(self)
        
        layout.addWidget(self.listWidget)

        # Mostras el layout final
        self.setLayout(layout)

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.listWidget:
            menu = QMenu()
            menu.addAction('Información del personaje')
            
            # Ejecucion el menu deslizante
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                # Extraer el nombre del personaje para obtener sus datos
                df_per = self.df[self.df['name']==item.text()]
                print(df_per)
                self.w = AnotherWindow()
                self.w.settxt(df_per)
                self.w.show()
            return True
        return super().eventFilter(source, event)

    def updatelistwidget(self):
        # limpiar el listWidget
        self.listWidget.clear()
        # limpiar el dataframe
        self.df = self.df.iloc[0:0]
        random_number= random.sample(range(1,83),10)
    
        for n in random_number:
            # realizar request de get para ello se requiere añadir el numero aleatorio
            link_new = LINK + str(n)
            response= requests.get(link_new)
            result_get = json.loads(response.content)
            # completar el data frame con los personajes y sus caracteristicas
            # la actualización toma un poco de tiempo
            self.df = self.df.append({'name' : result_get['name'], 
                  'height' : result_get['height'], 
                  'mass' : result_get['mass'], 
                  'hair_color' : result_get['hair_color'], 
                  'skin_color' : result_get['skin_color'], 
                  'eye_color' : result_get['eye_color'], 
                  'birth_year' : result_get['birth_year'],
                  'gender' : result_get['gender']}, 
                ignore_index = True) 
            self.listWidget.addItem(result_get['name'])    
                 
    def showTime(self):
        # mostrar el tiempo actual
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.label_time.setText(label_time)

app = QApplication(sys.argv)

window = Window()
window.show()

app.exec()