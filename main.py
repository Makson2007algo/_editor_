from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QListWidget, QTextEdit, QLineEdit, QInputDialog, QFileDialog

import os

from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
from PyQt5.QtCore import Qt


app = QApplication([])
win = QWidget()


win.setWindowTitle('Easy Editor')
btn_dir = QPushButton('папка')
spisok = QListWidget()
text = QLabel('Картинка')
left = QPushButton('Лево')
right = QPushButton('Право') 
mirrow = QPushButton('Зеркало') 
rezk = QPushButton('Резкость') 
chb = QPushButton('Ч/Б')


win.resize(700, 400)


row = QHBoxLayout()
row_tools = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(spisok)
col2.addWidget(text)
row_tools.addWidget(left)
row_tools.addWidget(right)
row_tools.addWidget(mirrow)
row_tools.addWidget(rezk)
row_tools.addWidget(chb)
col2.addLayout(row_tools)
row.addLayout(col1)
row.addLayout(col2)
win.setLayout(row)


workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()



def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result


def showFilenamesList():
    chooseWorkdir()
    extensions = ['.jpg','.jpeg','.png','.gif','.bmp']
    filenames = filter(os.listdir(workdir), extensions)
    spisok.clear()
    for filename in filenames:
        spisok.addItem(filename)


class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = 'mi/'


    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)


    def showImage(self, path):
        text.hide()
        pixmapimage = QPixmap(path)
        w, h = text.width(), text.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        text.setPixmap(pixmapimage)
        text.show()


    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)


    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    

    def razm(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    

    def povorot(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    

    def povorot2(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    

    def zerkalo(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    



workimage = ImageProcessor()


def showChosenImage():
    if spisok.currentRow() >= 0:
        filename = spisok.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)









spisok.currentRowChanged.connect(showChosenImage)
btn_dir.clicked.connect(showFilenamesList)

chb.clicked.connect(workimage.do_bw)
left.clicked.connect(workimage.povorot2)
right.clicked.connect(workimage.povorot)
mirrow.clicked.connect(workimage.zerkalo)
# rezk.clicked.connect(workimage.razm)


win.show()
app.exec()