#Oggetto rappresentazione di una tab < report >
from PyQt5 import QtCore, QtGui, QtWidgets
from subwindows_report_tab import subwindow_trades_list
from copy import deepcopy
from indexes import *

#Instanciate and manage the report tab, printing all indexes
class ReportTab(QtWidgets.QTabWidget):
    def __init__(self, _trade_list, _columns, _rows, _spacingX, _spacingY):
        #Calling super <Tab>
        super().__init__()
        self.trades = deepcopy(_trade_list)
        #<self> variable refers to the <Tab>
        self.rows = _rows  
        self.grid_counting = {"X": 0, "Y": 0}
        self.column_distancing = self.width() / (_columns * 2)
        self.positioning_cursor = {"X": 10, "Y": -20} #Posizione del cursore per il posizionamento
        self.spacing = {"X": _spacingX, "Y": _spacingY} #Spazio tra gli elementi

        self.__load__()
    #add a new index specifying <index_name> and his <value>
    def add_new_index(self, _index_name, _index_value):
        #positioning in a new line
        self.positioning_cursor["Y"] += self.spacing["Y"]
        #index_text
        index_text_label = QtWidgets.QLabel(self)
        index_text_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + (self.column_distancing * self.grid_counting["Y"]), 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        index_text_label.setText(_index_name)
        #index_value
        index_value_label = QtWidgets.QLabel(self)
        index_value_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + self.spacing["X"] + (self.column_distancing * self.grid_counting["Y"]), 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        index_value_label.setText(str(_index_value))
        self.__grid_counting__()
    #add a new Subwindow<text, button> specifying <index_name> and his <value>
    def add_new_subwindow(self, _label_text, _btn_text, _handler):
        #positioning in a new line
        self.positioning_cursor["Y"] += self.spacing["Y"]
        #index_text
        index_text_label = QtWidgets.QLabel(self)
        index_text_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + (self.column_distancing * self.grid_counting["Y"]), 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        index_text_label.setText(_label_text)
        #button text value
        btn = QtWidgets.QPushButton(self)
        btn.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + self.spacing["X"] + (self.column_distancing * self.grid_counting["Y"]), 
                                                        self.positioning_cursor["Y"], 
                                                         75, 
                                                          25)
                                            )
        btn.setText(str(_btn_text))

        #Attach Handler
        btn.clicked.connect(_handler)
        self.__grid_counting__()
    #add a simple text
    def add_text(self, _text_to_show):
        #positioning in a new line
        self.positioning_cursor["Y"] += self.spacing["Y"]
        #index_text
        text_label = QtWidgets.QLabel(self)
        text_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + (self.column_distancing * self.grid_counting["Y"]), 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        text_label.setText(_text_to_show)
        self.__grid_counting__()
    #when you add a row, manage the colums
    def __grid_counting__(self):
        self.grid_counting["X"] += 1
        if self.grid_counting["X"] > self.rows :
            #si è superato il limite di righe
            self.grid_counting["X"] = 0
            self.grid_counting["Y"] += 1
            #Reset cursor for Y
            self.positioning_cursor["Y"] = -20
    #Load the entire report tab
    def __load__(self):
        _ = CustomIndex(self.trades)
        _ = Symbol(self.trades)
        name_of_ts = Name(self.trades)
        symbol_of_ts = FormattedSymbol(self.trades)
        equity = Equity(self.trades)
        max_dd = MaximumDrawdown(self.trades)
        gross_profit = GrossProfit(self.trades)
        gross_loss = GrossLoss(self.trades)
        profit_factor = ProfitFactor(self.trades)
        total_trades = TotalNumberOfTrades(self.trades)
        winning_trades = WinningTrades(self.trades)
        losing_trades = LosingTrades(self.trades)
        percent_profitable = PercentProfitable(self.trades)
        even_trades = EvenTrades(self.trades)
        avg_trade_net_profit = AvgTradeNetProfit(self.trades)
        avg_winning_trade = AvgWinningTrade(self.trades)
        avg_losing_trade = AvgLosingTrade(self.trades)
        largest_win_trade = LargestWinningTrade(self.trades)
        largest_los_trade = LargestLosingTrade(self.trades)
        max_win_streak = MaxWinningStreak(self.trades)
        max_los_streak = MaxLosingStreak(self.trades)
        size_require = SizeRequirement(self.trades)
        monthly_return = MonthlyReturn(self.trades)

        self.add_text(name_of_ts.calculate() + symbol_of_ts.calculate())
        self.add_new_index("Net Profit: ", equity.calculate())
        self.add_new_index("Drawdown(max): ", max_dd.calculate())
        self.add_new_index("Gross Profit: ", gross_profit.calculate())
        self.add_new_index("Gross Loss: ", gross_loss.calculate())
        self.add_new_index("Profit Factor: ", profit_factor.calculate())
        self.add_text("")
        self.add_text("Trades info")
        self.add_new_index("Total trades: ", total_trades.calculate())
        self.add_new_index("Winning trades: ", winning_trades.calculate())
        self.add_new_index("Losing trades: ", losing_trades.calculate())
        self.add_new_index("Percent profitable: ", str(percent_profitable.calculate()) + " %")
        self.add_new_index("Even trades: ", even_trades.calculate())
        self.add_new_index("Avg profit per trade: ", avg_trade_net_profit.calculate())
        self.add_new_index("Avg Winning trade: ", avg_winning_trade.calculate())
        self.add_new_index("Avg Losing trade: ", avg_losing_trade.calculate())
        self.add_new_index("Largest winning: ", largest_win_trade.calculate())
        self.add_new_index("Largest losing: ", largest_los_trade.calculate())
        self.add_text("")
        self.add_new_index("Max Win streak: ", max_win_streak.calculate())
        self.add_new_index("Max Lose streak: ", max_los_streak.calculate())
        self.add_new_index("Size required: ", size_require.calculate())
        self.add_new_index("Avg monthly return: ", monthly_return.calculate())

        #Buttons
        self.add_new_subwindow("Trades list: ", "Open", self.open_subwindow_trades_onClick)
    #handlers of subwindows-buttons
    def open_subwindow_trades_onClick(self):
        new_subw_trades = subwindow_trades_list.TradeListWindow(self.trades)