import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

#Canvas class to manage a chart
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, _yLabel="", _xLabel=""):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_ylabel(_yLabel)
        self.axes.set_xlabel(_xLabel)
        super(MplCanvas, self).__init__(fig)