import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#### plot class
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=4, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='gray')
        self.axes = fig.add_subplot(111)
        fig.tight_layout(h_pad=-1, w_pad=-1)
        fig.subplots_adjust(wspace=0,hspace=1)
        super(MplCanvas, self).__init__(fig)