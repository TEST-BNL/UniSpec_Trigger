import time

class Radiometer:
   
    SerialNumber = ''
    def write_ascii_char(self, pause_value, i):
    def write_char(self, pause_value, c):
    def __init__(self, config_file):
        ictrl = config['InstrumentControl']
        self.serialConnection = serial.Serial()
        if (self.serialConnection.isOpen() == False) :
        self.SerialNumber = iinfo['SerialNumber']   
        # Send 27, 82, 255, 27, 82...;
        # sleep for approx 1 sec
        for iChannelCounter in range(1,3):
            self.write_ascii_char(30/1000, 27);
            time.sleep(5/1000)
            if iChannelCounter==2:
            self.write_ascii_char(30/1000, 27);    
            # characters to send = [S,2,0,8,0,1,0,0,0,0,7,A,0,0,3,0,0,0,4,C,S,8,0,4,0,0,0,0,0,0,F,B]
            for i in chars_to_send:               
            # send 27
            self.SetUnispecParameters()
            time.sleep(3/1000)
    def __del__(self):        
    def stop(self):
    def SetUnispecParameters(self):
        # send MSB for integration time 2400: 0
        # send MSB for intensity value 100
        for i in chars_to_send:               
    def read_and_discard(self, i):
        self.write_ascii_char(self.PauseDuringBufferReading, 2)
        self.ClearUnispecMemory();
    def ClearUnispecMemory(self):
        if self.serialConnection.inWaiting() == 0:
        print("\tResetting buffer ...")
        for j in range(1,17): # 1:16 
        time.sleep(200/1000)    
        if self.serialConnection.inWaiting()>0:
    # read data from unispec and store them in CHL1 and CHL2 attributes
        time.sleep(self.PauseForDataCollection)  
        self.ClearUnispecMemory();             
        print('Number of bytes read:', total_bytes_read)
        if (total_bytes_read == 1056):
            while index+valid_range < len(data):
            N1 = math.floor(len(valid_data)/2) # number of bytes of first band
            i = N1 + 1
            # calculate instrument temperature; calibration coeffs are not quite clear
            self.InstrumentTemperature = round(self.CHL2[253] * 250 / 1024, 3)
            return True
        return False      
                
             
            
    
        
        
    
        