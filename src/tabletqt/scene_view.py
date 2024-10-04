""" scene_view.py - create a vector drawing view in QT """

import logging
from PyQt6.QtWidgets import QGraphicsView, QVBoxLayout, QGraphicsScene, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPageSize, QPageLayout
from PyQt6.QtPrintSupport import QPrinter
from pypdf import PdfWriter, PdfReader

_logger = logging.getLogger(__name__)


class SceneView(QGraphicsView):
    def __init__(self, size, background):
        super().__init__()

        # Create a QGraphicsScene
        self.scene = QGraphicsScene()
        self.setSceneRect(0, 0, size.width, size.height)
        pad = 10
        self.setFixedSize(size.width + pad, size.height + pad)
        if background:
            _logger.info(f"Setting scene background to RGB: {background}")
            self.scene.setBackgroundBrush(QColor(*background))

        # Set the scene to the view
        self.setScene(self.scene)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        # self.setRenderHint(QPainter.RenderHint.Antialiasing)
        # self.setRenderHint(QPainter.RenderHint.TextAntialiasing)

    def save_as_pdf(self, file_path):
        # Create a QPrinter object and set the output format to PDF
        printer = QPrinter(QPrinter.PrinterMode.PrinterResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        # printer.setPageSize(QPageSize(self.size))
        ps = QPageSize(QPageSize.PageSizeId.AnsiC)
        printer.setPageSize(ps)
        printer.setPageOrientation(QPageLayout.Orientation.Landscape)
        # printer.setPageMargins(QMarginsF(0, 0, 0, 0))
        printer.setFullPage(True)
        printer.setOutputFileName(str(file_path))

        # Create a QPainter to render the view content onto the printer
        painter = QPainter(printer)

        # Render the entire scene to the printer (the PDF)
        self.render(painter)

        # Finish the painting process
        painter.end()

        # self.crop_pdf(file_path)

    def crop_pdf(self, file_path):
        reader = PdfReader(file_path)
        writer = PdfWriter()
        crop = 10

        sheet = reader.pages[0]
        crop_box = sheet.cropbox
        crop_box.lower_left = (crop_box.lower_left[0], crop_box.lower_left[1] + crop)
        sheet.cropbox.lower_left = crop_box.lower_left
        writer.add_page(sheet)
        with open("cropped.pdf", "wb") as fp:
            writer.write(fp)


class MainWindow(QWidget):
    def __init__(self, title, size, background):
        super().__init__()

        # Set up the layout and graphics view
        layout = QVBoxLayout()
        self.graphics_view = SceneView(size, background)
        layout.addWidget(self.graphics_view)

        self.setLayout(layout)
        self.setWindowTitle(title)
        self.setGeometry(500, 100, size.width, size.height)  # Position and size of the main window on the screen
