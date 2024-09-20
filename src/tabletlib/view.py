""" view.py - create a vector drawing view in QT """

from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor

class View(QGraphicsView):
    def __init__(self, size):
        super().__init__()

        # Create a QGraphicsScene
        self.scene = QGraphicsScene(QRectF(0, 0, size.width, size.height))
        self.scene.setBackgroundBrush(QColor(100, 100, 100))

        # Set the scene to the view
        self.setScene(self.scene)
