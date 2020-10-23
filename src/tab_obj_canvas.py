#Oggetto rappresentazione di un canvas per il printing di un grafico su tab < drawdown >
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

#Canvas class to manage a chart
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent, width=5, height=4, dpi=100, _yLabel="", _xLabel=""):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_ylabel(_yLabel)
        self.axes.set_xlabel(_xLabel)
        self.parent = parent
        super(MplCanvas, self).__init__(fig)
    def load_and_display_bar_chart(self, x_axe_data, y_axe_data, color_axe, page_to_show):
        #print the page
        #self.canvas_chart = MplCanvas(self.frame, width=12, height=4, dpi=70, _yLabel="Profit/Loss", _xLabel="Years")
        if len(page_to_show) <12:
            self.axes.bar(x_axe_data, y_axe_data, align='center', color=color_axe, width=0.25) #xList, ylist, align, list_of_colors
        else:
            self.axes.bar(x_axe_data, y_axe_data, align='center', color=color_axe, width=0.10) #xList, ylist, align, list_of_colors
        #Print values on bars
        y_pos = 0
        for index, value in enumerate(y_axe_data):
            if value >= 0:
                y_pos = value +40
            else:
                y_pos = value -40
            self.axes.text(y=y_pos, x=index, s=str(value), color='black', va='center', fontweight='bold') 

        self.axes.axhline(y=0, color='black', linestyle='--')
        self.setParent(self.parent)
        self.show()