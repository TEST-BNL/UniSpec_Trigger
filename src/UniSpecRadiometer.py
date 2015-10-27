import timeimport mathimport configparserimport serial

class Radiometer:
   
    SerialNumber = ''    serialConnection = ""    IntegrationTime = 720    NoOfScansToAverage = 10    PauseDuringBufferReading = 0.02 # 0.005: 0.005 works in Matlab, but not in Python ... but that is platform dependent    PauseForDataCollection = 0.5    InstrumentTemperature  = 0    BattV = 0    A1 = 0    A2 = 0    A3 = 0    A4 = 0        CHL1 = []    CHL2 = []
    def write_ascii_char(self, pause_value, i):        self.serialConnection.write(bytes([i]))        time.sleep(pause_value)
    def write_char(self, pause_value, c):        self.serialConnection.write(bytes([ord(c)]))        time.sleep(pause_value)        
    def __init__(self, config_file):        config = configparser.ConfigParser()        config.read(config_file)                
        ictrl = config['InstrumentControl']        iinfo = config['InstrumentInfo']        sctrl = config['SerialControl']
        self.serialConnection = serial.Serial()        self.serialConnection.baudrate = 9600        self.serialConnection.port = sctrl['ComPortName']   
        if (self.serialConnection.isOpen() == False) :            self.serialConnection.open()    
        self.SerialNumber = iinfo['SerialNumber']               self.IntegrationTime = int(ictrl['IntegrationTime'])        self.NoOfScansToAverage = int(ictrl['ScansToAverage'])        self.PauseDuringBufferReading = float(sctrl['PauseDuringBufferReading'])         self.PauseForDataCollection = float(sctrl['PauseForDataCollection'])             def init(self):        print("Initializing UniSpec ...")
        # Send 27, 82, 255, 27, 82...;        self.write_ascii_char(30/1000, 27);        self.write_ascii_char(30/1000, 82);        self.write_ascii_char(30/1000, 255);        self.write_ascii_char(30/1000, 27);        self.write_ascii_char(30/1000, 82);
        # sleep for approx 1 sec        time.sleep(1)
        for iChannelCounter in range(1,3):            if iChannelCounter==2:                print("Initialize chl 2...");                # switch baud rate back to 9600                self.serialConnection.baudrate = 9600;                self. write_ascii_char(30/1000, 89);            else:                print("Initialize chl 1...");
            self.write_ascii_char(30/1000, 27);            self.write_ascii_char(30/1000, 66);
            time.sleep(5/1000)            self.write_ascii_char(30/1000, 49);            time.sleep(5/1000)            # switch  baud rate to 115200            self.serialConnection.baudrate = 115200;                        time.sleep(5/1000)
            if iChannelCounter==2:                self.write_ascii_char(30/1000, 89);
            self.write_ascii_char(30/1000, 27);                time.sleep(5/1000)            self.write_ascii_char(30/1000, 76);
            # characters to send = [S,2,0,8,0,1,0,0,0,0,7,A,0,0,3,0,0,0,4,C,S,8,0,4,0,0,0,0,0,0,F,B]            chars_to_send = ['S','2','0','8','0','1','0','0','0','0','7','A','0','0','3','0','0','0','4','C','S','8','0','4','0','0','0','0','0','0','F','B']
            for i in chars_to_send:                               self.write_char(30/1000, i);
            # send 27            time.sleep(70/1000)            self.write_ascii_char(30/1000, 27);            self.write_ascii_char(30/1000, 74);            time.sleep(300/1000)            self.write_ascii_char(30/1000, 83);
            self.SetUnispecParameters()
            time.sleep(3/1000)
    def __del__(self):                self.serialConnection.close()
    def stop(self):        self.serialConnection.close()        
    def SetUnispecParameters(self):            if self.IntegrationTime > 32767:            print("Selected integration time (" + str(self.IntegrationTime) + ") is greater than maximum.  Using 32767.")            self.IntegrationTime = 32767        if self.IntegrationTime < 40:            print("Selected integration time (" + str(self.IntegrationTime) + ") is less than minimum.  Using 40.")            self.IntegrationTime = 40                    if self.NoOfScansToAverage*self.IntegrationTime > 40000:            print("Selected number of scans (" + str(self.NoOfScansToAverage) + ") is greater than maximum possible.  Using " + round(40000/self.IntegrationTime) + ".")            self.NoOfScansToAverage = round(40000/self.IntegrationTime)                    time.sleep(100/1000)        # tell the system that now intensity values are to be send        self.write_ascii_char(100/1000, 1);
        # send MSB for integration time 2400: 0        iMSB=math.floor(self.IntegrationTime/256);        self.write_ascii_char(100/1000, iMSB); # integration time MSB 2400/256=9                # send LSB for integration time 2400: 2400/256*240=225        iLSB=self.IntegrationTime-(iMSB*256);        self.write_ascii_char(100/1000, iLSB);                # send MSB for averaging number 10 :0         # send LSB for averaging number 10 :0.0390625 *256=10        self.write_ascii_char(100/1000, 0);        self.write_ascii_char(100/1000, self.NoOfScansToAverage);
        # send MSB for intensity value 100        # send LSB for integration time 100/256*100        chars_to_send = [0,0,0,0,0,10,0,1]
        for i in chars_to_send:                           self.write_ascii_char(100/1000, i);
    def read_and_discard(self, i):        print('Clearing Ch.', i);
        self.write_ascii_char(self.PauseDuringBufferReading, 2)        for j in range(1,17): # 1:16             self.write_ascii_char(self.PauseDuringBufferReading, 5)
        self.ClearUnispecMemory();
    def ClearUnispecMemory(self):        #print("Clearing Unispec Memory ...")        for iChannelCounter in range(1,3):            if self.serialConnection.inWaiting()>0:                print("\tReading and dumping", self.serialConnection.inWaiting(), "bytes...")                self.serialConnection.read(self.serialConnection.inWaiting())
        if self.serialConnection.inWaiting() == 0:            return
        print("\tResetting buffer ...")
        for j in range(1,17): # 1:16             self.write_ascii_char(100/1000, 5)              if self.serialConnection.inWaiting()>0:                print("\tReading and dumping", self.serialConnection.inWaiting(), "bytes from bin", j, "/16...")                self.serialConnection.read(self.serialConnection.inWaiting())
        time.sleep(200/1000)    
        if self.serialConnection.inWaiting()>0:            self.serialConnection.read(self.serialConnection.inWaiting())
    # read data from unispec and store them in CHL1 and CHL2 attributes    # returns true if data read was successful, false otherwise            def get_data(self):          self.serialConnection.baudrate = 115200;        # read and discard the first two scans            for i in range(1,3): # counts up to 2 ...            self.read_and_discard(i)
        time.sleep(self.PauseForDataCollection)          # now send char 5 to get the unispec to send all the data        print("Trying to read valid data ...")        data = b''        total_bytes_read = 0        for j in range(1,17): # 1:16             self.write_ascii_char(self.PauseDuringBufferReading, 5)              #print("Number of bytes in buffer ", serialConnection.inWaiting())            if self.serialConnection.inWaiting()>0:                total_bytes_read = total_bytes_read + self.serialConnection.inWaiting()                this_data = self.serialConnection.read(self.serialConnection.inWaiting())                data = data + this_data                #print(this_data)
        self.ClearUnispecMemory();                     #print(data)    
        print('Number of bytes read:', total_bytes_read)        self.CHL1=[]        self.CHL2=[]    
        if (total_bytes_read == 1056):            # remove the last two bytes in each 66 byte block            valid_data = b''            index = 0            valid_range = 64
            while index+valid_range < len(data):                valid_data = valid_data+data[index:index+valid_range]   # first range: 0:63, hence, it must be 0:64 in python ...                index = index + valid_range + 2
            N1 = math.floor(len(valid_data)/2) # number of bytes of first band            # construct 16 bit values for the two channels            i = 1            while i < N1:                self.CHL1.append(valid_data[i-1]*256 +valid_data[i])                i = i + 2
            i = N1 + 1            while i < len(valid_data):                self.CHL2.append(valid_data[i-1]*256 +valid_data[i])                i = i + 2
            # calculate instrument temperature; calibration coeffs are not quite clear            #print(self.CHL2[253])            #print(len(self.CHL1))            #print(len(self.CHL2))
            self.InstrumentTemperature = round(self.CHL2[253] * 250 / 1024, 3)            self.BattV = round(self.CHL2[248] * .00975, 3)            self.A1 = self.CHL2[249]            self.A2 = self.CHL2[250]            self.A3 = self.CHL2[251]            self.A4 = self.CHL2[252]                        # cut last 8 values as channel 2 only holds housekeeping for them            #self.CHL1 = self.CHL1[0:-8]            #self.CHL2 = self.CHL2[0:-8]
            return True
        return False      
                
             
            
    
        
        
    
        
