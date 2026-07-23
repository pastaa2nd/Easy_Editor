import os  # PART 2: untuk mengakses file & folder di sistem
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, # Dialogue for opening files (and folders)
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)

# ================== TAMBAHAN PART 3 ==================
from PyQt5.QtCore import Qt        # untuk menjaga rasio gambar (tidak gepeng)
from PyQt5.QtGui import QPixmap    # untuk menampilkan gambar ke layar
from PIL import Image             # untuk membuka gambar
# ======================================================
# ================== TAMBAHAN PART 5 ==================
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
# ======================================================

app = QApplication([])
win = QWidget()       
win.resize(700, 500) 
win.setWindowTitle('Easy Editor')
lb_image = QLabel("Image")
btn_dir = QPushButton("Folder")
lw_files = QListWidget()


btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_flip = QPushButton("Mirror")
btn_sharp = QPushButton("Sharpness")
btn_bw = QPushButton("B/W")


row = QHBoxLayout()          # Main line
col1 = QVBoxLayout()         # divided into two columns
col2 = QVBoxLayout()
col1.addWidget(btn_dir)      # in the first - directory selection button
col1.addWidget(lw_files)     # and file list
col2.addWidget(lb_image, 95) # in the second - image
row_tools = QHBoxLayout()    # and button bar
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)


row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)


win.show()

#-----------------------------------Part 2-------------------------------------#

workdir = ''  # PART 2: variabel global untuk menyimpan folder yang dipilih user


def filter(files, extensions):  # PART 2: fungsi untuk menyaring file berdasarkan ekstensi gambar
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result


def chooseWorkdir():  # PART 2: fungsi untuk memilih folder
   global workdir
   workdir = QFileDialog.getExistingDirectory()  # membuka dialog pilih folder


def showFilenamesList():  # PART 2: fungsi utama untuk tampilkan daftar gambar
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']  # format gambar yang didukung
   chooseWorkdir()  # panggil fungsi pilih folder
   filenames = filter(os.listdir(workdir), extensions)  # ambil file dari folder lalu filter
   lw_files.clear()  # kosongkan list sebelumnya
   for filename in filenames:
       lw_files.addItem(filename)  # tampilkan file ke list widget


btn_dir.clicked.connect(showFilenamesList)  # PART 2: saat tombol "Folder" diklik, jalankan fungsi

# ================== PART 3 (MENAMPILKAN GAMBAR) ==================

class ImageProcessor():
   def __init__(self):
       self.image = None     # menyimpan gambar
       self.dir = None       # folder gambar
       self.filename = None  # nama file
       self.save_dir = "Modified/"  # folder hasil edit (dipakai nanti)

   def loadImage(self, dir, filename):
       '''membuka gambar dan simpan datanya'''
       self.dir = dir
       self.filename = filename

       # gabungkan folder + nama file
       image_path = os.path.join(dir, filename)

       # buka gambar pakai PIL
       self.image = Image.open(image_path)

   def showImage(self, path):
       '''menampilkan gambar ke layar'''
       lb_image.hide()  # sembunyikan dulu (biar refresh)

       # ubah jadi format tampilan
       pixmapimage = QPixmap(path)

       # ambil ukuran label
       w, h = lb_image.width(), lb_image.height()

       # resize gambar tanpa merusak rasio
       pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)

       # tampilkan ke label
       lb_image.setPixmap(pixmapimage)
       lb_image.show()

# ================== PART 4 (EDIT GAMBAR) ==================

   def do_bw(self):
       self.image = self.image.convert("L")  # PART 4: ubah gambar jadi hitam putih (grayscale)

       self.saveImage()  # PART 4: simpan hasil edit ke folder baru

       image_path = os.path.join(self.dir, self.save_dir, self.filename)  # PART 4: buat path gambar hasil edit
       self.showImage(image_path)  # PART 4: tampilkan gambar hasil edit ke layar
# ================== PART 5 (EDIT GAMBAR) ==================
   def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


   def do_right(self):
       self.image = self.image.transpose(Image.ROTATE_270)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


   def do_flip(self):
       self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


   def do_sharpen(self):
       self.image = self.image.filter(SHARPEN)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)
# ==========================================================

   def saveImage(self):
       path = os.path.join(self.dir, self.save_dir)  # PART 4: gabungkan folder asli + folder "Modified"

       if not(os.path.exists(path) or os.path.isdir(path)):  # PART 4: cek apakah folder sudah ada
           os.mkdir(path)  # PART 4: jika belum ada, buat folder baru

       image_path = os.path.join(path, self.filename)  # PART 4: buat path lengkap untuk file baru
       self.image.save(image_path)  # PART 4: simpan gambar hasil edit
# =====================================================

# buat object pengolah gambar
workimage = ImageProcessor()


def showChosenImage():
   # fungsi saat user klik file di list
   if lw_files.currentRow() >= 0:  # pastikan ada yang dipilih
       filename = lw_files.currentItem().text()  # ambil nama file

       # load gambar
       workimage.loadImage(workdir, filename)

       # buat path lengkap
       image_path = os.path.join(workimage.dir, workimage.filename)

       # tampilkan gambar
       workimage.showImage(image_path)


# saat user klik file → tampilkan gambar
lw_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)  # PART 4: saat tombol B/W diklik → jalankan fungsi ubah gambar
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)


# ================== JALANKAN APP ==================
app.exec()