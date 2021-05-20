import pyfirmata
import time
if __name__ == '__main__':
    board = pyfirmata.Arduino('/dev/ttyACM0')
    board.analog[0].mode = pyfirmata.INPUT  
    it = pyfirmata.util.Iterator(board)  
    it.start()  
    print("Communication Successfully started")
    
    while True:
        print("Brightness:",board.analog[0].read())
        time.sleep(1)
