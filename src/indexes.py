#indexes.py
#il modulo raccoglie tutti gli indici, ed i metodi per calcolarli
#Define an interface
class CustomIndex():
    def __init__(self, _tradeList):
        self.__trade_list__ = _tradeList
        self.value = None
    #calculate and return the index
    def calculate(self):
        pass
#Extract name of Trading system or set to Portfolio
class Name(CustomIndex):
    #calculate and return the index
    def calculate(self):
        value = ""
        tl = self.__trade_list__
        tl_first = tl[0]
        prev_ts_name = tl_first[1] #prende il nome del ts 
        #check if it is a portfolio or a system
        for trade in self.__trade_list__:
            ts_name = trade[2]
            if not(prev_ts_name == ts_name):
                #It's a portfolio
                value = "Portfolio"
                break
            else:
                value = ts_name
        return value
#Extract Symbol of Trading system (Formatted to fit the name of ts)
class FormattedSymbol(CustomIndex):
    #calculate and return the index
    def calculate(self):
        value = ""
        temp_name = Name(self.__trade_list__)

        if(temp_name.calculate() == "Portfolio"):
            value = ""
        else:
            tl = self.__trade_list__
            tl_first = tl[0]
            value = " - " + tl_first[2] #prende il nome del ts     
        return value
#Extract Symbol of Trading system
class Symbol(CustomIndex):
    #calculate and return the index
    def calculate(self):
        value = ""
        temp_name = Name(self.__trade_list__)

        if(temp_name.calculate() == "Portfolio"):
            value = ""
        else:
            tl = self.__trade_list__
            tl_first = tl[0]
            value = tl_first[2] #prende il nome del ts     
        return value
#Calculate the equity (final)
class Equity(CustomIndex):
    #calculate and return the index
    def calculate(self):
        equity = 0
        for trade in self.__trade_list__:
            equity = equity + trade[-2]
        return round(equity, 2)
#Calculate maximum drawdown
class MaximumDrawdown (CustomIndex):
    #calculate and return the index
    def calculate(self):
        max_dd = 0
        max_equity = 0
        min_equity = 0
        equity = 0
        for trade in self.__trade_list__:
            equity = equity + trade[-2]
            if equity > max_equity:
                max_equity = equity
            elif equity < max_equity:
                min_equity = equity
                if (max_equity - min_equity) > max_dd:
                    max_dd = max_equity - min_equity
        return round(max_dd * -1, 2)
#Calculate Drawdown, returning a list of values
class Drawdown(CustomIndex):
    #calculate and return the index
    def calculate(self):
        dd_values = []
        y_values = []
        cumulative_lose = 0
        for trade in self.__trade_list__:
            current_net = trade[-2]
            if current_net < 0:
                dd_values.append(current_net)
            else:
                if dd_values :
                    for value in dd_values:
                        cumulative_lose = cumulative_lose + value
                    y_values.append(cumulative_lose)
                    dd_values = []
                cumulative_lose = 0
                
        return y_values
#Calculate Gross Profit
class GrossProfit(CustomIndex):
    def calculate(self):
        gross_profit = 0
        for trade in self.__trade_list__:
            if trade[-2] > 0:
                gross_profit = gross_profit + trade[-2]
        return round(gross_profit, 2)
#Calculate Gross Loss
class GrossLoss(CustomIndex):
    def calculate(self):
        gross_loss = 0
        for trade in self.__trade_list__:
            if trade[-2] < 0:
                gross_loss = gross_loss + trade[-2]
        return round(gross_loss, 2)
#Calculate Profit factor
class ProfitFactor(CustomIndex):
    def calculate(self):
        gp = GrossProfit(self.__trade_list__)
        gp_value = gp.calculate()
        gl = GrossLoss(self.__trade_list__)
        gl_value = gl.calculate() * -1

        if gp_value > 0 and gl_value > 0: 
            return round(gp_value / gl_value, 2)
        else:
            return 0
#Count number of trades
class TotalNumberOfTrades(CustomIndex):
    def calculate(self):
        t_num_of_trades = 0
        for _ in self.__trade_list__:
            t_num_of_trades += 1
        return t_num_of_trades
#Count number of winning trades
class WinningTrades(CustomIndex):
    def calculate(self):
        t_win_of_trades = 0
        for trade in self.__trade_list__:
            if trade[-2] > 0:
                t_win_of_trades += 1
        return t_win_of_trades
#Count number of losing trades
class LosingTrades(CustomIndex):
    def calculate(self):
        t_los_of_trades = 0
        for trade in self.__trade_list__:
            if trade[-2] < 0:
                t_los_of_trades += 1
        return t_los_of_trades
#Count Winning/TotalNumberOFtrades*100
class PercentProfitable(CustomIndex):
    def calculate(self):
        t_n_of_t = TotalNumberOfTrades(self.__trade_list__)
        wt = WinningTrades(self.__trade_list__)

        return round(wt.calculate() / t_n_of_t.calculate() * 100, 2)
#Count number of even trades
class EvenTrades(CustomIndex):
    def calculate(self):
        t_even_of_trades = 0
        for trade in self.__trade_list__:
            if trade[-2] == 0:
                t_even_of_trades += 1
        return t_even_of_trades
#Average profit per trade
class AvgTradeNetProfit(CustomIndex):
    def calculate(self):
        #NetProfit/TotalNumberOfTrades
        eq = Equity(self.__trade_list__)
        eq_value = eq.calculate()
        tnot = TotalNumberOfTrades(self.__trade_list__)
        tnot_value = tnot.calculate()

        return round(eq_value/tnot_value, 2)
#Average profit per winning trade
class AvgWinningTrade(CustomIndex):
    def calculate(self):
        gp = GrossProfit(self.__trade_list__)
        gp_value = gp.calculate()
        wt = WinningTrades(self.__trade_list__)
        wt_value = wt.calculate()

        return round(gp_value/wt_value, 2)
#Average profit per losing trade
class AvgLosingTrade(CustomIndex):
    def calculate(self):
        gl = GrossLoss(self.__trade_list__)
        gl_value = gl.calculate()
        lt = LosingTrades(self.__trade_list__)
        lt_value =lt.calculate()

        if gl_value < 0 and lt_value > 0:
            return round(gl_value/lt_value, 2)
        else:
            return 0
#Return larget winning trade
class LargestWinningTrade(CustomIndex):
    def calculate(self):
        lt = 0
        for trade in self.__trade_list__:
            if trade[-2] > lt :
                lt = trade[-2]
        return lt  
#Return larget losing trade
class LargestLosingTrade(CustomIndex):
    def calculate(self):
        lt = 0
        for trade in self.__trade_list__:
            if trade[-2] < lt :
                lt = trade[-2]
        return lt  
#Calculate max consecutive winning trades
class MaxWinningStreak(CustomIndex):
    def calculate(self):
        mws = 0
        current_ws = 0
        for trade in self.__trade_list__:
            if trade[-2] > 0 :
                current_ws += 1
            else:
                if current_ws > mws:
                    mws = current_ws
                current_ws = 0
        return mws  
#Calculate max consecutive losing trades
class MaxLosingStreak(CustomIndex):
    def calculate(self):
        mls = 0
        current_ls = 0
        for trade in self.__trade_list__:
            if trade[-2] < 0 :
                current_ls += 1
            else:
                if current_ls > mls:
                    mls = current_ls
                current_ls = 0
        return mls  
#Calculate Size required
class SizeRequirement(CustomIndex):
    def calculate(self):
        md = MaximumDrawdown(self.__trade_list__)
        
        return round(-2 * md.calculate(), 2)
#Monthly return
class MonthlyReturn(CustomIndex):
    def calculate(self):
        first_trade = self.__trade_list__[0]
        for column in first_trade:
            if len(str(column)) == 16:
                if (column[2] == "/") and (column[5] == "/") and (column[13] == ":") :
                    starting_month = int(column[:2])
        #Simulating elapsing months    
        cm = starting_month #current_month
        month_return = []
        list_of_monthly_returns = []
        for trade in self.__trade_list__:
            for column in trade:
                if len(str(column)) == 16:
                    if (column[2] == "/") and (column[5] == "/") and (column[13] == ":") :
                        tm = int(column[:2]) #this_month
                        if int(tm) != int(cm) :
                            jump = tm - cm
                            #Jump is from a month of <year-1> to a month of <year>
                            if jump < 1:
                                jump = (12 - cm) + tm
                                print("DEBUG: Jump over next year")
                                print("--------------------------")
                                
                            #Jump is from a month of <year> to a month of <year>
                            elif jump > 1:
                                jump = tm - cm
                                print("DEBUG: Jump over multiple months")
                                print("--------------------------")

                            #Looping over <empty> trading months
                            if jump > 1:
                                list_of_monthly_returns.append(month_return)
                                month_return = []
                                month_return.append(0)
                                for _ in range(jump-1):
                                    list_of_monthly_returns.append(month_return)
                                month_return = []
                                month_return.append(trade[-2])
                            elif jump == 1:
                                list_of_monthly_returns.append(month_return)
                                month_return = []
                                month_return.append(trade[-2])
                        else:
                            #It is the same month
                            month_return.append(trade[-2])
                        #Assigning the current month
                        cm = tm
                        jump = 0
                            
        for month in list_of_monthly_returns:
            if not month:
                month.append(0)
                print("INFO: A month has been found empty, reset to <0>.")
            print(month)
            

