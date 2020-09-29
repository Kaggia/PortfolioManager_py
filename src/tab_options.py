from PyQt5 import QtCore, QtGui, QtWidgets
from copy import deepcopy
from options import Option
from date import Date

#Instanciate and manage the Options tab
class OptionTab(QtWidgets.QTabWidget):
    def __init__(self, _trade_list,_current_window):
        #Calling super <Tab>
        super().__init__()
        #Trades
        self.trades = deepcopy(_trade_list)
        #Options image
        self.options_image = Option()
        #Get the current secondary window
        self.cw = _current_window
        #Content
        self.groupbox_date = None

        self.date_option_label = None

        self.checkbox_startdate = None
        self.button_startdate = None
        self.textbox_startdate = None

        self.checkbox_enddate = None
        self.button_enddate = None
        self.textbox_enddate = None
        #Attributes
        self.startDate = None
        self.endDate = None
        self.currentlySelectedCalendar = None
        #loading the UI
        self.__load_ui__()
        #Load dates on textboxes
        self.__load_dates_on_textbox__()
        #Load current options image
        startDate = str(self.trades[0][4])
        endDate = str(self.trades[-1][4])
        startDate = startDate[:-6]
        endDate = endDate[:-6]
        #Set Default values and current values of Option obj
        self.options_image.setValues(Date(int(startDate[3:5]), int(startDate[0:2]), int(startDate[-4:])), 
                                    Date(int(endDate[3:5]), int(endDate[0:2]), int(endDate[-4:])),
                                    'D')
    #Load the Graphical Content
    def __load_ui__(self):
        spacing_left = 10

        self.groupbox_date = QtWidgets.QGroupBox(self)
        self.groupbox_date.setGeometry(QtCore.QRect(0, 0, 175, 400))
        gridLayout = QtWidgets.QGridLayout() 

        #TextLabel
        self.date_option_label = QtWidgets.QLabel(self)
        self.date_option_label.setGeometry(QtCore.QRect(spacing_left, 25 , 150, 25))
        self.date_option_label.setText("Date options: ")
        #Group-StartDate-Checkbox
        self.checkbox_startdate = QtWidgets.QCheckBox(self)
        self.checkbox_startdate.setGeometry(QtCore.QRect(spacing_left, 50 , 100, 25))
        self.checkbox_startdate.setText("Start date")
        #Group-StartDate-threeDotButton
        self.button_startdate = QtWidgets.QPushButton(self)
        self.button_startdate.setGeometry(QtCore.QRect(spacing_left + 75, 55 , 50, 20))
        self.button_startdate.setText("Pick from calendar")
        #Group-StartDate-textbox
        self.textbox_startdate = QtWidgets.QLineEdit(self)
        self.textbox_startdate.setGeometry(QtCore.QRect(spacing_left + 150, 55 , 75, 20))
        self.textbox_startdate.setText("dd/mm/YYYY")
        self.textbox_startdate.setReadOnly(True)

        #Group-EndDate-Checkbox
        self.checkbox_enddate = QtWidgets.QCheckBox(self)
        self.checkbox_enddate.setGeometry(QtCore.QRect(spacing_left, 75 , 100, 25))
        self.checkbox_enddate.setText("Last date")
        #Group-EndDate-threeDotButton
        self.button_enddate = QtWidgets.QPushButton(self)
        self.button_enddate.setGeometry(QtCore.QRect(spacing_left + 75, 80 , 50, 20))
        self.button_enddate.setText("Pick from calendar")
        #Group-EndDate-textbox
        self.textbox_enddate = QtWidgets.QLineEdit(self)
        self.textbox_enddate.setGeometry(QtCore.QRect(spacing_left + 150, 80 , 75, 20))
        self.textbox_enddate.setText("dd/mm/YYYY")
        self.textbox_enddate.setReadOnly(True)
        #Separator
        self.separator_0 = QtWidgets.QLabel(self)
        self.separator_0.setGeometry(QtCore.QRect(spacing_left, 90 , 150, 25))
        self.separator_0.setText("_______________________")
        #RadioButtons
        self.radiobutton_custom_date = QtWidgets.QRadioButton(self)
        self.radiobutton_custom_date.setGeometry(QtCore.QRect(spacing_left + 150, 100 , 75, 20))
        self.radiobutton_custom_date.setText("Custom date filter")
        self.radiobutton_real_money_gain = QtWidgets.QRadioButton(self)
        self.radiobutton_real_money_gain.setGeometry(QtCore.QRect(spacing_left + 150, 110 , 75, 20))
        self.radiobutton_real_money_gain.setText("Real money gain filter")
        #Separator
        self.separator_1 = QtWidgets.QLabel(self)
        self.separator_1.setGeometry(QtCore.QRect(spacing_left, 120 , 150, 25))
        self.separator_1.setText("_______________________")
        #TextLabel
        self.select_time_window = QtWidgets.QLabel(self)
        self.select_time_window.setGeometry(QtCore.QRect(spacing_left, 130 , 150, 25))
        self.select_time_window.setText("Select Window time: ")
        #Combobox
        self.combobox_time_window = QtWidgets.QComboBox(self)
        self.combobox_time_window.setGeometry(QtCore.QRect(spacing_left, 140 , 150, 25))
        self.combobox_time_window.addItem('Default')
        self.combobox_time_window.addItem('Daily')
        self.combobox_time_window.addItem('Weekly')
        self.combobox_time_window.addItem('Monthly')
        self.combobox_time_window.setCurrentIndex(0)

        #ApplyButton
        self.button_apply = QtWidgets.QPushButton(self)
        self.button_apply.setGeometry(QtCore.QRect(spacing_left + 75, 150 , 50, 20))
        self.button_apply.setText("Apply")
        #ResetButton
        self.button_reset = QtWidgets.QPushButton(self)
        self.button_reset.setGeometry(QtCore.QRect(spacing_left + 125, 150 , 50, 20))
        self.button_reset.setText("Reset")

        #Calendar
        self.cal_frame = QtWidgets.QMainWindow()
        self.cal_frame.resize(325, 325)
        self.cal_frame.setWindowTitle("Calendar: Pick a day")
        self.cal_frame.setMinimumSize(QtCore.QSize(325, 305))
        self.cal_frame.setMaximumSize(QtCore.QSize(325, 305)) 
        self.cal = QtWidgets.QCalendarWidget(self.cal_frame)
        self.cal.setGeometry(0,0,325,300)
        self.cal.setGridVisible(False)
        self.__setMinAndMaxDateOnCalendar__()
        self.cal.clicked[QtCore.QDate].connect(self.getDate)
            
        gridLayout.addWidget(self.date_option_label)

        gridLayout.addWidget(self.checkbox_startdate)
        gridLayout.addWidget(self.button_startdate)
        gridLayout.addWidget(self.textbox_startdate)

        gridLayout.addWidget(self.checkbox_enddate)
        gridLayout.addWidget(self.button_enddate)
        gridLayout.addWidget(self.textbox_enddate)

        gridLayout.addWidget(self.separator_0)

        gridLayout.addWidget(self.radiobutton_custom_date)
        gridLayout.addWidget(self.radiobutton_real_money_gain)

        gridLayout.addWidget(self.separator_1)

        gridLayout.addWidget(self.select_time_window)
        gridLayout.addWidget(self.combobox_time_window)

        gridLayout.addWidget(self.button_apply)
        gridLayout.addWidget(self.button_reset)

        self.groupbox_date.setLayout(gridLayout)
        self.groupbox_date.show()

        #Event Connection
        self.button_startdate.clicked.connect(self.__openCalendar_startDate__)
        self.button_enddate.clicked.connect(self.__openCalendar_endDate__)
        self.checkbox_startdate.stateChanged.connect(self.__on_start_date_checked__)
        self.checkbox_enddate.stateChanged.connect(self.__on_end_date_checked__)
        self.button_apply.clicked.connect(self.__apply_changes_to_options__)
        self.button_reset.clicked.connect(self.__reset_changes_to_options__)

        #Setting checkbox and radiobuttons
        self.checkbox_startdate.setChecked(True)
        self.checkbox_enddate.setChecked(True)
        self.radiobutton_custom_date.setChecked(True)
        self.radiobutton_real_money_gain.setChecked(False)

        #Momentaneous disabling
        self.radiobutton_real_money_gain.setEnabled(False)
        self.combobox_time_window.setEnabled(True)
    #Enable and disable line based on checking - StartDate
    def __on_start_date_checked__(self):
        self.button_startdate.setEnabled(self.checkbox_startdate.isChecked())
        self.textbox_startdate.setEnabled(self.checkbox_startdate.isChecked())
        self.radiobutton_custom_date.setChecked(True)
    #Enable and disable line based on checking - EndDate
    def __on_end_date_checked__(self):
        self.button_enddate.setEnabled(self.checkbox_enddate.isChecked())
        self.textbox_enddate.setEnabled(self.checkbox_enddate.isChecked())
        self.radiobutton_custom_date.setChecked(True)
    #Load dates from list of trades
    def __load_dates_on_textbox__(self):
        self.textbox_startdate.setText(str(self.trades[0][4]))
        self.textbox_enddate.setText(str(self.trades[-1][4]))
        #Open the calendar - startDate
    #Set Min and Max date on calendar
    def __setMinAndMaxDateOnCalendar__(self):
        startDate = str(self.trades[0][4])
        endDate = str(self.trades[-1][4])
        startDate = startDate[:-6]
        endDate = endDate[:-6]
        self.cal.setMinimumDate(QtCore.QDate(int(startDate[-4:]), 
                                                int(startDate[3:5]),
                                                   int(startDate[0:2])
                                            )
                                )
        self.cal.setMaximumDate(QtCore.QDate(int(endDate[-4:]), 
                                                int(endDate[3:5]),
                                                   int(endDate[0:2])
                                            )
                                )
    #Open the calendar - startDate
    def __openCalendar_startDate__(self):
        self.currentlySelectedCalendar = 0
        self.cal_frame.show()
    #Open the calendar - endDate
    def __openCalendar_endDate__(self):
        self.currentlySelectedCalendar = 1
        self.cal_frame.show()
    #Apply the current Gui state to Option Obj
    def __apply_changes_to_options__(self): 
        startdate = self.textbox_startdate.text()[:-6]
        enddate = self.textbox_enddate.text()[:-6]
        cbox_value = self.combobox_time_window.currentText()
        time_window = None
        if cbox_value == 'Default':
            time_window = 'D'
        elif cbox_value == 'Daily':
            time_window = 'd'
        elif cbox_value == 'Weekly':
            time_window = 'w'
        elif cbox_value == 'Monthly':
            time_window = 'm'

        year_s = int(startdate[-4:].replace("/", ""))
        month_s = int(startdate[3:5].replace("/", ""))
        day_s = int(startdate[0:2].replace("/", ""))

        year_e = int(enddate[-4:].replace("/", ""))
        month_e = int(enddate[3:5].replace("/", ""))
        day_e = int(enddate[0:2].replace("/", ""))

        new_date_start = Date(month_s, day_s, year_s)
        new_date_end = Date(month_e, day_e, year_e)
        #load new values 
        self.options_image.setValues(new_date_start, new_date_end, time_window) 
        #Change list of trades
        self.cw.reload_tabs(self.options_image)       
    #Reset the current Gui state to Option Obj
    def __reset_changes_to_options__(self):
         #load new values 
        self.options_image.setValues(self.options_image.startDate_d, self.options_image.endDate_d, self.options_image.time_window_d) 
        #Change list of trades
        self.cw.reload_tabs(self.options_image)   
    #Get date from calendar widget
    def getDate(self):
      date = self.cal.selectedDate()
      if (self.currentlySelectedCalendar == 0):
          date_str = str(date.month()) + "/" + str(date.day()) + "/" + str(date.year()) + " 00:00"
          self.textbox_startdate.setText(date_str)
      else:
          date_str = str(date.month()) + "/" + str(date.day()) + "/" + str(date.year()) + " 23:59"
          self.textbox_enddate.setText(date_str)
      self.cal_frame.hide()
    #Load a particular state of GUI by specifying the options
    def load_state(self, _options):
        print("Loading previous state of options")
        self.textbox_startdate.setText(str(_options.startDate.m) + "/" + str(_options.startDate.d) + "/" + str(_options.startDate.y) + " 00:00" )
        self.textbox_enddate.setText(str(_options.endDate.m) + "/" + str(_options.endDate.d) + "/" + str(_options.endDate.y) + " 23:59")
        if _options.time_window == 'D':
            self.combobox_time_window.setCurrentIndex(self.combobox_time_window.findText('Default'))
        elif _options.time_window == 'd':
            self.combobox_time_window.setCurrentIndex(self.combobox_time_window.findText('Daily'))  
        elif _options.time_window == 'm':
            self.combobox_time_window.setCurrentIndex(self.combobox_time_window.findText('Monthly'))
        elif _options.time_window == 'w':
            self.combobox_time_window.setCurrentIndex(self.combobox_time_window.findText('Weekly'))


