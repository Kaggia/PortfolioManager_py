#app_detail_window.py
#Libreria contenente la finestra secondaria, printing dei dati
#Libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from operator import itemgetter
from copy import deepcopy
import os
import numpy as np
import pandas as pd
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
#My Modules
import CONSTANTS as directory
from os_interactors import FileManager
from trading_system import TradingSystem
from indexes import *
from options import Option
from date import Date
from date import reset_to_monday
from tab_equity import EquityChartTab
from tab_drawdown import DrawdownChartTab
from tab_optimization import OptimizationTab
from tab_options import OptionTab
from tab_report import ReportTab
from subwindows_report_tab import subwindow_trades_list

#Window where various details are shown
class DetailWindow:
    def __init__(self, _unordered_list_of_trades):
        self.trades_default = deepcopy(_unordered_list_of_trades)
        self.trades = deepcopy(_unordered_list_of_trades)

        self.__order_raw_trade_list__(self.trades_default)
        self.__order_raw_trade_list__(self.trades)

        self.frame = QtWidgets.QMainWindow()
        self.frame.resize(720, 480)
        self.frame.setWindowTitle("cTrader - Portfolio Manager - Detail window")
        self.frame.setMinimumSize(QtCore.QSize(720, 480))
        self.frame.setMaximumSize(QtCore.QSize(720, 480))
        self.font = QtGui.QFont()
        
        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget(self.frame)
        self.tab_report = ReportTab(2, 17, 100, 20) #(index_per_column, spacingX, spacingY)
        self.tab_drawdown = DrawdownChartTab(self.trades)
        self.tab_equity = EquityChartTab(self.trades)
        self.tab_options = OptionTab(self.trades, self)
        self.tab_optimization = OptimizationTab()
        self.tabs.resize(720,480)
        # Add tabs
        self.tabs.addTab(self.tab_options,"General options")
        self.tabs.addTab(self.tab_report,"Report")
        self.tabs.addTab(self.tab_drawdown,"Drawdown analysis")
        self.tabs.addTab(self.tab_equity,"Equity analysis")
        self.tabs.addTab(self.tab_optimization,"Optimization")

        #Load Tabs content
        self.__tab_report_loader__()
        self.__tab_equity_loader()
        self.__tab_drawdownChart_loader()
        self.__tab_options_loader()
        self.__tab_optimization_loader()

        self.frame.show()      
    #load report tab 
    def __tab_report_loader__(self):
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

        self.tab_report.add_text(name_of_ts.calculate() + symbol_of_ts.calculate())
        self.tab_report.add_new_index("Net Profit: ", equity.calculate())
        self.tab_report.add_new_index("Drawdown(max): ", max_dd.calculate())
        self.tab_report.add_new_index("Gross Profit: ", gross_profit.calculate())
        self.tab_report.add_new_index("Gross Loss: ", gross_loss.calculate())
        self.tab_report.add_new_index("Profit Factor: ", profit_factor.calculate())
        self.tab_report.add_text("")
        self.tab_report.add_text("Trades info")
        self.tab_report.add_new_index("Total trades: ", total_trades.calculate())
        self.tab_report.add_new_index("Winning trades: ", winning_trades.calculate())
        self.tab_report.add_new_index("Losing trades: ", losing_trades.calculate())
        self.tab_report.add_new_index("Percent profitable: ", str(percent_profitable.calculate()) + " %")
        self.tab_report.add_new_index("Even trades: ", even_trades.calculate())
        self.tab_report.add_new_index("Avg profit per trade: ", avg_trade_net_profit.calculate())
        self.tab_report.add_new_index("Avg Winning trade: ", avg_winning_trade.calculate())
        self.tab_report.add_new_index("Avg Losing trade: ", avg_losing_trade.calculate())
        self.tab_report.add_new_index("Largest winning: ", largest_win_trade.calculate())
        self.tab_report.add_new_index("Largest losing: ", largest_los_trade.calculate())
        self.tab_report.add_text("")
        self.tab_report.add_new_index("Max Win streak: ", max_win_streak.calculate())
        self.tab_report.add_new_index("Max Lose streak: ", max_los_streak.calculate())
        self.tab_report.add_new_index("Size required: ", size_require.calculate())
        self.tab_report.add_new_index("Avg monthly return: ", monthly_return.calculate())    
    #load dd tab <NONE>
    def __tab_drawdownChart_loader(self):
        pass
    #load equity tab <NONE>
    def __tab_equity_loader(self):
        pass
    #Load Options tab <NONE>
    def __tab_options_loader(self):
        pass
    #Load Optimization tab
    def __tab_optimization_loader(self):
        pass
    #order tradelist passed
    def __order_raw_trade_list__(self, listoftrades):
        #index_of_date = 0
        #Get the ID of column with dates_format
        for trade in listoftrades:
            for column in trade:
                if len(str(column)) == 16:
                    if (column[2] == "/") and (column[5] == "/") and (column[13] == ":") :
                        #Column found is a valid date 
                        internal_date = self.__convert_date_to_internalDate__(column[0:2], column[3:5], column[6:11], column[11:13], column[14:])
                        trade.append(internal_date)
                        break  
               
        #For every trade add a column with value, derived from date format
        ordered_list = sorted(self.trades, key=itemgetter(-1))
        self.trades = ordered_list
        #re-assign progressive ids
        trade_id = 0
        for trade in self.trades:
            trade[0] = trade_id
            trade_id += 1
        
        #fm = FileManager()
        #fm.dump_list_of_list("dump.txt", self.trades)      
    #convert a date(string) to a internalDate Value, letting the list be ordered
    def __convert_date_to_internalDate__(self, _month, _day, _year, _hour, _minute):
        day_value = (int(_day) - 1 ) * 1440
        month_value = (int(_month) - 1 ) * 43800
        year_value = (int(_year) - 2000 ) * 524160
        hour_value = int(_hour) * 60
        minute_value = int(_minute)
        sum_of_minutes = day_value + month_value + year_value + hour_value + minute_value

        return sum_of_minutes
    #Get Index of date-column
    def __get_index_of_date_column__(self):
        single_trade = self.trades[0]
        index = -1
        i = 0
        for column in single_trade:
            if len(str(column)) == 16 and (column[2] == "/") and (column[5] == "/") and (column[13] == ":") :
                index = i
                break
            else:
                i += 1
        return index
    #Filter trades
    def filter_trades_by_option (self, _options):
        new_trades = deepcopy(self.trades)
        trades_to_return = []
        #GetStartingDateAsValue
        starting_date_as_value = self.__convert_date_to_internalDate__(_options.startDate.m, _options.startDate.d, _options.startDate.y, 0, 0)
        #GetEndingDateAsValue
        ending_date_as_value = self.__convert_date_to_internalDate__(_options.endDate.m, _options.endDate.d, _options.endDate.y, 23, 59)
        #Filtering by Start and end date
        index_of_date_column = self.__get_index_of_date_column__()

        for trade in new_trades:
            current_internal_date = self.__convert_date_to_internalDate__(trade[index_of_date_column][0:2], trade[index_of_date_column][3:5], trade[index_of_date_column][6:11], trade[index_of_date_column][11:13], trade[index_of_date_column][14:])
            if (current_internal_date >= starting_date_as_value) and (current_internal_date <= ending_date_as_value) :
                trades_to_return.append(trade)
        #Filtering by time window  
        if _options.time_window == 'D':
            filtered_list_of_trades = []
            for trade in trades_to_return:
                filtered_list_of_trades.append(trade)

        elif _options.time_window == 'd':
            print("Daily filtering options algo")
            list_to_sum = []
            day = []
            DIFF_DAY = self.__convert_date_to_internalDate__(1, 2, 2001, 0, 0) - self.__convert_date_to_internalDate__(1, 1, 2001, 0, 0)
            last_date_of_trade_as_value = self.__convert_date_to_internalDate__(trades_to_return[0][index_of_date_column][0:2], trades_to_return[0][index_of_date_column][3:5], trades_to_return[0][index_of_date_column][6:11], 0, 0)
            print("DIFF_DAY: ", DIFF_DAY)
            for trade in trades_to_return:
                current_date = trade[index_of_date_column]
                current_date_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], current_date[11:13], current_date[14:])
                if (current_date_as_value - last_date_of_trade_as_value) <= DIFF_DAY:
                    print("Differenza tra due trade date<intraday>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    day.append(trade)
                    last_date_of_trade_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], 0, 0)
                else:
                    print("Differenza tra due trade date<out of a day>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    list_to_sum.append(day)
                    day = []
                    day.append(trade)
                    last_date_of_trade_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], 0, 0)

            #Merging data from the same time interval
            filtered_list_of_trades = []
            index = 0
            name = trades_to_return[0][1]
            symbol = trades_to_return[0][2]
            volume = trades_to_return[0][3]
            closing_date =  None
            net_cumulative = 0
            for day_c in list_to_sum:
                for d in day_c:
                    net_cumulative = net_cumulative + d[-2]
                    closing_date = d[-3][:-6] + " 00:00"
                    name = d[1]
                    symbol = d[2]
                    volume = d[3]
                filtered_list_of_trades.append([index, name, symbol, volume, closing_date, float(net_cumulative), 0])
                net_cumulative = 0
                index += 1

        elif _options.time_window == 'w':
            print("Weekly filtering options algo")
            list_to_sum = []
            week = []
            DIFF_WEEK = (self.__convert_date_to_internalDate__(1, 2, 2001, 0, 0) - self.__convert_date_to_internalDate__(1, 1, 2001, 0, 0)) * 7
            day_tmp = Date(trades_to_return[0][index_of_date_column][3:5], trades_to_return[0][index_of_date_column][0:2], trades_to_return[0][index_of_date_column][6:11])
            #Reset to closer Monday
            last_date_of_trade_as_value = reset_to_monday(day_tmp, self.__convert_date_to_internalDate__(trades_to_return[0][index_of_date_column][0:2], trades_to_return[0][index_of_date_column][3:5], trades_to_return[0][index_of_date_column][6:11], 0, 0))
            
            print("DIFF_WEEK: ", DIFF_WEEK)
            for trade in trades_to_return:
                current_date = trade[index_of_date_column]
                current_date_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], current_date[11:13], current_date[14:])
                if (current_date_as_value - last_date_of_trade_as_value) <= DIFF_WEEK:
                    print("Differenza tra due trade date<intraweek>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    week.append(trade)
                    last_date_of_trade_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], 0, 0)
                else:
                    print("Differenza tra due trade date<out of a week>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    list_to_sum.append(week)
                    week = []
                    week.append(trade)
                    day_tmp = Date(current_date[3:5], current_date[0:2], current_date[6:11])
                    #Reset to closer Monday
                    last_date_of_trade_as_value = reset_to_monday(day_tmp, self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], 0, 0))

            #Merging data from the same time interval
            filtered_list_of_trades = []
            index = 0
            name = trades_to_return[0][1]
            symbol = trades_to_return[0][2]
            volume = trades_to_return[0][3]
            closing_date =  None
            net_cumulative = 0
            for week_c in list_to_sum:
                for d in week_c:
                    net_cumulative = net_cumulative + d[-2]
                    closing_date = d[-3][:-6] + " 00:00"
                    name = d[1]
                    symbol = d[2]
                    volume = d[3]
                filtered_list_of_trades.append([index, name, symbol, volume, closing_date, float(net_cumulative), 0])
                net_cumulative = 0
                index += 1

        elif _options.time_window == 'm':
            print("Monthly filtering options algo")
            list_to_sum = []
            month = []
            DIFF_MONTH = self.__convert_date_to_internalDate__(2, 1, 2001, 0, 0) - self.__convert_date_to_internalDate__(1, 1, 2001, 0, 0)
            last_date_of_trade_as_value = self.__convert_date_to_internalDate__(trades_to_return[0][index_of_date_column][0:2], 1, trades_to_return[0][index_of_date_column][6:11], 0, 0)
            print("DIFF_MONTH: ", DIFF_MONTH)
            for trade in trades_to_return:
                current_date = trade[index_of_date_column]
                current_date_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], current_date[11:13], current_date[14:])
                if (current_date_as_value - last_date_of_trade_as_value) <= DIFF_MONTH:
                    print("Differenza tra due trade date<intraday>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    month.append(trade)
                    last_date_of_trade_as_value = self.__convert_date_to_internalDate__(current_date[0:2], 1, current_date[6:11], 0, 0)
                else:
                    print("Differenza tra due trade date<out of a day>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    list_to_sum.append(month)
                    month = []
                    month.append(trade)
                    last_date_of_trade_as_value = self.__convert_date_to_internalDate__(current_date[0:2], 1, current_date[6:11], 0, 0)

            #Merging data from the same time interval
            filtered_list_of_trades = []
            index = 0
            name = trades_to_return[0][1]
            symbol = trades_to_return[0][2]
            volume = trades_to_return[0][3]
            closing_date =  None
            net_cumulative = 0
            for month_c in list_to_sum:
                for m in month_c:
                    net_cumulative = net_cumulative + m[-2]
                    closing_date = m[index_of_date_column][0:2] + "/" + m[index_of_date_column][6:-6] + " 00:00"
                    name = m[1]
                    symbol = m[2]
                    volume = m[3]
                filtered_list_of_trades.append([index, name, symbol, volume, closing_date, float(net_cumulative), 0])
                net_cumulative = 0
                index += 1

        #IMPLEMENT
        for trade in filtered_list_of_trades:
            print(trade)

        return filtered_list_of_trades
    #Reloading the tabs 
    def reload_tabs(self, _options):
        #Load trades by options
        filtered_trades_list = self.filter_trades_by_option(_options)
        #for trade in filtered_trades_list:
        #    print(trade)
        #Reload all tabs by removing them and calling them back again
        #<REMOVING>
        self.tabs.removeTab(self.tabs.indexOf(self.tab_options))
        self.tabs.removeTab(self.tabs.indexOf(self.tab_report))
        self.tabs.removeTab(self.tabs.indexOf(self.tab_drawdown))
        self.tabs.removeTab(self.tabs.indexOf(self.tab_optimization))
        self.tabs.removeTab(self.tabs.indexOf(self.tab_equity))
        
        #<ADDING>
        self.tab_report = ReportTab(2, 17, 100, 20) #(index_per_column, spacingX, spacingY)
        self.tab_drawdown = DrawdownChartTab(filtered_trades_list)
        self.tab_equity = EquityChartTab(filtered_trades_list)
        self.tab_options = OptionTab(filtered_trades_list, self)
        self.tab_options.load_state(_options)
        self.tab_optimization = OptimizationTab()

        self.tabs.addTab(self.tab_options,"General options")
        self.tabs.addTab(self.tab_report,"Report")
        self.tabs.addTab(self.tab_drawdown,"Drawdown analysis")
        self.tabs.addTab(self.tab_equity,"Equity analysis")
        self.tabs.addTab(self.tab_optimization,"Optimization")

        #Load Tabs content
        self.__tab_report_loader__()
        self.__tab_equity_loader()
        self.__tab_drawdownChart_loader()
        self.__tab_options_loader()
        self.__tab_optimization_loader()