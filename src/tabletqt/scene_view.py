""" scene_view.py - create a vector drawing view in QT """

# System
import logging
from PyQt6.QtWidgets import QGraphicsView, QVBoxLayout, QGraphicsScene, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPageSize, QPageLayout
from PyQt6.QtPrintSupport import QPrinter
from pypdf import PdfWriter, PdfReader

_logger = logging.getLogger(__name__)

# A generated PDF leave extra space on the bottom or right side depending
# on the tablet dimensions. These are the crop values that seem to work
# determined experiementally for the height to width ratio for each
# standard sheet size and orientation.
# Thus, all keys less than zero are for landscape orientation
# Each corresponding value is the amount to crop the pdf on the bottom
# for landscape and off the right side for portrait
pdf_crop = { 0.65: 196, 0.71: 101, 0.75: 32, 0.77: 0, 1.29: 635, 1.33: 665, 1.55: 789}

class SceneView(QGraphicsView):
    def __init__(self, size, background):
        super().__init__()

        # Create a QGraphicsScene
        self.tablet_size = size
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

        self.crop_pdf(file_path)

    def crop_pdf(self, file_path):
        reader = PdfReader(file_path)
        writer = PdfWriter()
        hw_ratio = self.tablet_size.height / self.tablet_size.width

        sheet = reader.pages[0]
        crop_box = sheet.cropbox

        # Find the closest key by selecting the key with minimum distance
        # to the hw_ratio
        closest_key = min(pdf_crop.keys(), key=lambda k: abs(k - hw_ratio))

        # And that gives us an experimentally derived crop value
        crop = pdf_crop[closest_key]

        # I did compute a linear function based on the dictionary values that comes close
        # to the crop data set, but is sometimes off by a little too much.
        # So I left it commented out here for reference, but use the data set directly to get the best crop value
        if self.tablet_size.height > self.tablet_size.width: # portrait
            # crop = 582.65 * hw_ratio - 113.55
            crop_box.upper_right = (crop_box.upper_right[0] - crop, crop_box.upper_right[1])
            sheet.cropbox.upper_right = crop_box.upper_right
        else: # landscape
            # crop = -1635.53 * hw_ratio + 1259.99
            crop_box.lower_left = (crop_box.lower_left[0], crop_box.lower_left[1] + crop)
            sheet.cropbox.lower_left = crop_box.lower_left

        writer.add_page(sheet)
        with open(file_path, "wb") as fp:
            writer.write(fp)
        # with open("cropped.pdf", "wb") as fp:
        #     writer.write(fp)


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
