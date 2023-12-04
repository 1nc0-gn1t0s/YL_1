import sqlite3
import sys
import random

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QImage, QColor, QTransform
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSlider
from PIL import Image, ImageFilter, ImageEnhance


class Photoshop(QMainWindow):
    def __init__(self):
        super(Photoshop, self).__init__()

        uic.loadUi('YL_1.ui', self)

        self.filename = QFileDialog.getOpenFileName(
            self, 'Выберите картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]

        con = sqlite3.connect('YLdb_1.db')
        cursor = con.cursor()
        cursor.execute('''INSERT INTO ColorSliders VALUES (0, 0, 'red'), (0, 0, 'green'), (0, 0, 'blue'),
                          (0, 0, 'rotate')''')
        con.commit()
        con.close()

        QtGui.QImageReader.supportedImageFormats()

        self.last_images = []
        self.orig_image = QImage(self.filename)
        self.curr_image = self.orig_image.copy()
        self.last_images.append(self.curr_image)
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)
        self.pixmap = QPixmap('photomaster.jpg')
        self.logo.setPixmap(self.pixmap)

        self.RedSlider.valueChanged.connect(self.change_color_red)
        self.GreenSlider.valueChanged.connect(self.change_color_green)
        self.BlueSlider.valueChanged.connect(self.change_color_blue)
        self.BlackWhite.clicked.connect(self.make_baw)
        self.BlackWhiteNoGray.clicked.connect(self.make_baw_no_gray)
        self.Inversion.clicked.connect(self.make_inversion)
        self.OneStepBack1.clicked.connect(self.go_one_step_back)
        self.OneStepBack2.clicked.connect(self.go_one_step_back)
        self.Back.clicked.connect(self.cancel_all)
        self.ClockwiseRotation.clicked.connect(self.right_rotate)
        self.CounterclockwiseRotation.clicked.connect(self.left_rotate)
        self.DegreeChanger.valueChanged.connect(self.rotate)
        self.VisibilitySlider.valueChanged.connect(self.visibility)
        self.Sharpness.clicked.connect(self.make_sharper)
        self.Smoothing.clicked.connect(self.make_smoother)
        self.Borders.clicked.connect(self.borders)
        self.MoreBright.clicked.connect(self.make_brighter)
        self.LessBright.clicked.connect(self.make_less_bright)
        self.Fading.clicked.connect(self.fading)
        self.Contrast.clicked.connect(self.contrast)
        self.Random.clicked.connect(self.random)

    #  ДОРАБОТАТЬ (добавить остальные функции)
    def random(self):   # применяет один рандомный фильтр
        self.last_images.append(self.curr_image.copy())

        con = sqlite3.connect('YLdb_1.db')
        cursor = con.cursor()
        n = random.randint(0, 5)
        k = cursor.execute(f"""SELECT name FROM AllFunctions WHERE id = {n}""").fetchone()[0]
        con.commit()
        con.close()

        eval(k)()

        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def contrast(self):  # добавляет контраста
        self.last_images.append(self.curr_image.copy())

        self.curr_image.save('img.png', "PNG", -1)
        img = Image.open('img.png')
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.05)
        img.save('img2.png')

        self.curr_image = QImage('img2.png')
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def fading(self):  # делает фото более блеклым
        self.last_images.append(self.curr_image.copy())

        self.curr_image.save('img.png', "PNG", -1)
        img = Image.open('img.png')
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(0.95)
        img.save('img2.png')

        self.curr_image = QImage('img2.png')
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def make_less_bright(self):  # понижает яркость фотографии
        self.last_images.append(self.curr_image.copy())

        self.curr_image.save('img.png', "PNG", -1)
        img = Image.open('img.png')
        img = ImageEnhance.Brightness(img)
        img = img.enhance(0.95)
        img.save('img2.png')

        self.curr_image = QImage('img2.png')
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def make_brighter(self):  # повышает яркость фотографии
        self.last_images.append(self.curr_image.copy())

        self.curr_image.save('img.png', "PNG", -1)
        img = Image.open('img.png')
        img = ImageEnhance.Brightness(img)
        img = img.enhance(1.05)
        img.save('img2.png')

        self.curr_image = QImage('img2.png')
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    # ИСПРАВИТЬ ПРОБЛЕМСЫ (сместить повернутое фото в начало координат..?)
    def rotate(self):  # поворачивает фото вправо на указанное количество градусов
        self.last_images.append(self.curr_image.copy())

        value = int(self.DegreeChanger.value())

        con = sqlite3.connect('YLdb_1.db')
        cursor = con.cursor()
        m = cursor.execute("""SELECT id FROM ColorSliders WHERE color = 'rotate' ORDER BY id DESC LIMIT 1""").fetchone()
        m = m[0]
        cursor.execute(f"""INSERT INTO ColorSliders VALUES ({m + 1}, {value}, 'rotate')""")
        n = cursor.execute(f"""SELECT value FROM ColorSliders WHERE color = 'rotate' AND id = {m}""").fetchone()
        n = n[0]
        k = value - n
        con.commit()
        con.close()

        self.curr_image = self.curr_image.transformed(QTransform().rotate(k))

        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def change_color_red(self):  # добавляет больше красного оттенка фотографии
        self.last_images.append(self.curr_image.copy())

        value = int(self.RedSlider.value())

        con = sqlite3.connect('YLdb_1.db')
        cursor = con.cursor()
        m = cursor.execute("""SELECT id FROM ColorSliders WHERE color = 'red' ORDER BY id DESC LIMIT 1""").fetchone()
        m = m[0]
        cursor.execute(f"""INSERT INTO ColorSliders VALUES ({m + 1}, {value}, 'red')""")
        n = cursor.execute(f"""SELECT value FROM ColorSliders WHERE color = 'red' AND id = {m}""").fetchone()
        n = n[0]
        k = value - n
        con.commit()
        con.close()

        x, y = self.curr_image.size().width(), self.curr_image.size().height()

        for i in range(x):
            for j in range(y):
                r, g, b, _ = self.curr_image.pixelColor(i, j).getRgb()
                r += k
                r = 255 if r > 255 else r
                r = 0 if r < 0 else r
                self.curr_image.setPixelColor(QPoint(i, j),
                                              QColor(r, g, b))

        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def change_color_green(self):  # добавляет больше зеленого оттенка фотографии
        self.last_images.append(self.curr_image.copy())

        value = int(self.RedSlider.value())

        con = sqlite3.connect('YLdb_1.db')
        cursor = con.cursor()
        m = cursor.execute("""SELECT id FROM ColorSliders WHERE color = 'green' ORDER BY id DESC LIMIT 1""").fetchone()
        m = m[0]
        cursor.execute(f"""INSERT INTO ColorSliders VALUES ({m + 1}, {value}, 'green')""")
        n = cursor.execute(f"""SELECT value FROM ColorSliders WHERE color = 'green' AND id = {m}""").fetchone()
        n = n[0]
        k = value - n
        con.commit()
        con.close()

        x, y = self.curr_image.size().width(), self.curr_image.size().height()

        for i in range(x):
            for j in range(y):
                r, g, b, _ = self.curr_image.pixelColor(i, j).getRgb()
                g += k
                g = 255 if g > 255 else g
                g = 0 if g < 0 else g
                self.curr_image.setPixelColor(QPoint(i, j),
                                              QColor(r, g, b))

        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def change_color_blue(self):  # добавляет больше синего оттенка фотографии
        self.last_images.append(self.curr_image.copy())

        value = int(self.RedSlider.value())

        x, y = self.curr_image.size().width(), self.curr_image.size().height()

        con = sqlite3.connect('YLdb_1.db')
        cursor = con.cursor()
        m = cursor.execute("""SELECT id FROM ColorSliders WHERE color = 'blue' ORDER BY id DESC LIMIT 1""").fetchone()
        m = m[0]
        cursor.execute(f"""INSERT INTO ColorSliders VALUES ({m + 1}, {value}, 'blue')""")
        n = cursor.execute(f"""SELECT value FROM ColorSliders WHERE color = 'blue' AND id = {m}""").fetchone()
        n = n[0]
        k = value - n
        con.commit()
        con.close()

        for i in range(x):
            for j in range(y):
                r, g, b, _ = self.curr_image.pixelColor(i, j).getRgb()
                b += k
                b = 255 if b > 255 else b
                b = 0 if b < 0 else b
                self.curr_image.setPixelColor(QPoint(i, j),
                                              QColor(r, g, b))

        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def borders(self):  # создает черное изображение с белым контуром объектов на изначальном изображении
        self.last_images.append(self.curr_image.copy())

        self.curr_image.save('img.png', "PNG", -1)
        img = Image.open('img.png')
        img = img.convert('L')
        img = img.filter(ImageFilter.FIND_EDGES)
        img.save('img2.png')

        self.curr_image = QImage('img2.png')
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def make_sharper(self):  # накладывает фильтр сглаживания
        self.last_images.append(self.curr_image.copy())

        self.curr_image.save('img.png', "PNG", -1)
        img = Image.open('img.png')
        img = img.filter(ImageFilter.SHARPEN)
        img.save('img2.png')

        self.curr_image = QImage('img2.png')
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def make_smoother(self):  # накладывает фильтр резкости
        self.last_images.append(self.curr_image.copy())

        self.curr_image.save('img.png', "PNG", -1)
        img = Image.open('img.png')
        img = img.filter(ImageFilter.SMOOTH)
        img.save('img2.png')

        self.curr_image = QImage('img2.png')
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def visibility(self):  # изменяет прозрачность изображения
        self.last_images.append(self.curr_image.copy())

        v = int(self.VisibilitySlider.value())

        self.curr_image.save('img.png', "PNG", -1)
        img = Image.open('img.png')
        img.putalpha(v)
        img.save('img2.png')

        self.curr_image = QImage('img2.png')
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def right_rotate(self):  # поворачивает фото на 90 градусов вправо (по часовой стрелке)
        self.last_images.append(self.curr_image.copy())

        t = QTransform().rotate(90)
        self.curr_image = self.curr_image.transformed(t)

        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def left_rotate(self):  # поворачивает фото на 90 градусов влево (против часовой стрелки)
        self.last_images.append(self.curr_image.copy())

        t = QTransform().rotate(-90)
        self.curr_image = self.curr_image.transformed(t)

        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def cancel_all(self):  # эта функция отменяет все изменения
        self.last_images.append(self.curr_image.copy())

        self.pixmap = QPixmap.fromImage(self.orig_image)
        self.curr_image = self.orig_image.copy()
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def go_one_step_back(self):  # эта функция отменяет последнее изменение
        self.pixmap = QPixmap.fromImage(self.last_images[-1])
        self.curr_image = self.last_images[-1].copy()
        self.last_images = self.last_images[:-2]
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def make_inversion(self):  # делает инверсию фотографии
        self.last_images.append(self.curr_image.copy())

        x, y = self.curr_image.size().width(), self.curr_image.size().height()

        for i in range(x):
            for j in range(y):
                r, g, b, _ = self.curr_image.pixelColor(i, j).getRgb()
                r1 = 255 - r
                g1 = 255 - g
                b1 = 255 - b

                if r1 < 0:
                    r1 = 0

                if g1 < 0:
                    g1 = 0

                if b1 < 0:
                    b1 = 0

                self.curr_image.setPixelColor(QPoint(i, j),
                                              QColor(r1, g1, b1))

        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def make_baw_no_gray(self):  # делает ч/б фото без серого цвета
        self.last_images.append(self.curr_image.copy())

        x, y = self.curr_image.size().width(), self.curr_image.size().height()

        for i in range(x):
            for j in range(y):
                r, g, b, _ = self.curr_image.pixelColor(i, j).getRgb()
                n = (r + g + b) // 3
                if n >= 128:
                    self.curr_image.setPixelColor(QPoint(i, j),
                                                  QColor(255, 255, 255))
                else:
                    self.curr_image.setPixelColor(QPoint(i, j),
                                                  QColor(0, 0, 0))

        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)

    def make_baw(self):  # делает фотографию черно-белой
        self.last_images.append(self.curr_image.copy())

        x, y = self.curr_image.size().width(), self.curr_image.size().height()

        for i in range(x):
            for j in range(y):
                r, g, b, _ = self.curr_image.pixelColor(i, j).getRgb()
                n = (r + g + b) // 3
                self.curr_image.setPixelColor(QPoint(i, j),
                                              QColor(n, n, n))

        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.picture1.setPixmap(self.pixmap)
        self.picture2.setPixmap(self.pixmap)


def clean_all():  # удаляет все ненужные записи из баз данных
    con = sqlite3.connect('YLdb_1.db')
    cursor = con.cursor()
    cursor.execute('''DELETE FROM ColorSliders''')
    con.commit()
    con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Photoshop()
    ex.show()

    app.exec()

    clean_all()

    sys.exit()