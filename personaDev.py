import sys
from pathlib import Path
import platform
import datetime
import csv

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QTimer, QDateTime

from personafun.ardconn import BoardConn
from personafun.figurediagram import MplCanvas


#### Resource Path
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', Path(__file__).resolve().parent)
    return str(Path.joinpath(base_path,relative_path))

#### ui connect
ui_form = resource_path("personaGui.ui")
form_class = loadUiType(ui_form)[0]

#### Window class
class BaseWindow(QMainWindow, form_class):

    def __init__(self, *args, **kwargs):
        super(BaseWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('Persona Simulator')
        self.initUI()
        self.initCanvas()
        self.initStart()
        self.pushBtn_run.setEnabled(True)
        self.system_cnt = 0

    #### initial UI contents : Logo
    def initUI(self):
        # Top Logo
        self.labelTopLogo.setStyleSheet('border-image:url(./img/python_logo.svg);border:0px;')
        # Sub Logo
        self.labelpersonaLogo.setStyleSheet('border-image:url(./img/logo_persona_450_150.png);border:0px;')
        
    def initCanvas(self):
        self.canvas1 = MplCanvas()
        self.graph1_verticalLayout.addWidget(self.canvas1)
    
    def initStart(self):
        self.text_display("Start Loop")
        dateTimeVar = QDateTime.currentDateTime()
        self.text_display(dateTimeVar.toString("yyyy-MM-dd | hh:mm:ss"))
        self.text_display("Platform Check : {}".format(platform_check[0:5]))
        
        self.timer = QTimer()
        self.timer.setInterval(sample_time)
        self.timer.timeout.connect(self.start_loop)
        self.timer.start()

        ## Button connect
        self.pushBtn_run.clicked.connect(self.run_btn)
        self.pushBtn_quit.clicked.connect(self.quit_btn)
    
    ########== Button Fun ==###############################################    
    def run_btn(self):
        global data_sum
        self.system_cnt = 0
        data_sum = []
        self.text_display("Daq Run....")
        self.pushBtn_run.setDisabled(True)
        
        self.timer = QTimer()
        self.timer.setInterval(sample_time)
        self.timer.timeout.connect(self.daq_loop)
        self.timer.start()
        
    def quit_btn(self):
        BoardConn(baud_rate).close_ser()
        self.close()
        
    ########== UI Display ==###############################################    
    def text_display(self,to_text):
        self.textBrowser.append(to_text)
    
    def lcd_display_update(self, loop_cnt, data):
        dateTimeVar = QDateTime.currentDateTime()
        self.lcdID.display(loop_cnt)
        self.lcdID.setDigitCount(4)
        self.lcdTime.display(dateTimeVar.toString("yy-MM-dd,hh:mm:ss"))
        self.lcdTime.setDigitCount(17)
        self.lcdSampleTime.display(data[3])
        self.lcdSampleTime.setDigitCount(5)
        self.lcdADC.setDigitCount(17)
        self.lcdADC.display(data[4])
        self.lcdADC.setDigitCount(5)
        
    def plot_show(self,data_sum):
        x = []
        y = []
        for data in data_sum:
            x.append(int(data[0]))
            y.append(round(float(data[4]),1))
        self.canvas1.axes.cla()
        self.canvas1.axes.set_facecolor("black")
        self.canvas1.axes.plot(x,y,'ro-',label="temp")
        self.canvas1.axes.xaxis.set_tick_params(color='white',labelcolor='white')
        self.canvas1.axes.yaxis.set_tick_params(color='white',labelcolor='white',)
        self.canvas1.axes.set_title("Temp. vs Time",color='white')
        self.canvas1.axes.set_xlabel('Time[sec]',color='white')
        self.canvas1.axes.set_ylabel('Temp.[oC]',color='white')
        self.canvas1.axes.legend(loc="lower right")
        self.canvas1.axes.grid()
        self.canvas1.draw()    
        
    ## start loop
    def start_loop(self):
        global baud_rate, data_sum
        test_loop = 200
        self.system_cnt += 1
        datetime_now = QDateTime.currentDateTime()
        date_now = datetime_now.toString("yyMMdd")
        time_now = datetime_now.toString("hhmmss")
        
        datetime_list = [self.system_cnt, date_now, time_now]
        get_sim_data = BoardConn(baud_rate).get_data()
        data_now = datetime_list + get_sim_data
        print(data_now)
        self.lcd_display_update(self.system_cnt, data_now)
        
        data_sum.append(data_now)
        self.plot_show(data_sum)
        
        if self.system_cnt % test_loop == 0:
            data_sum = []
            self.system_cnt = 0
    
    ## run loop after push Run
    def daq_loop(self):
        global baud_rate, data_sum, save_cnt
        self.system_cnt += 1
        datetime_now = QDateTime.currentDateTime()
        date_now = datetime_now.toString("yyMMdd")
        time_now = datetime_now.toString("hhmmss")
        
        datetime_list = [self.system_cnt, date_now, time_now]
        get_sim_data = BoardConn(baud_rate).get_data()
        data_now = datetime_list + get_sim_data
        print(data_now)
        self.lcd_display_update(self.system_cnt, data_now)
            
        data_sum.append(data_now)
        self.plot_show(data_sum)
        
        if self.system_cnt % save_cnt == 0:
            self.timer.stop()
            BoardConn(baud_rate).close_ser()
            self.close()
        else:
            with open(save_path, 'a') as fb:
                wr = csv.writer(fb)
                wr.writerow(data_now)
                

#### Start Code ####
## initial variable
baud_rate = 9600
sample_time = 100
save_cnt = 500
data_sum = []

## check form
platform_check = platform.platform()

## define: data header
# data_header = ['id','date','time','sampletime','aivalue']

## define: save path
#### save base path set
base_path = Path(__file__).resolve().parent
save_dir_name = 'savedata'
save_base = base_path.joinpath(save_dir_name)
#### save path from time: year-month-day_hour:minute:second
datetime_now = datetime.datetime.now()
save_sub_name_from_time = datetime_now.strftime("%y%m%d_%H%M%S")
save_path = save_base.joinpath(save_sub_name_from_time)

if save_base.is_dir() == False:
    save_base.mkdir()

#### End Code ####


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = BaseWindow()
    window.show()
    app.exec()