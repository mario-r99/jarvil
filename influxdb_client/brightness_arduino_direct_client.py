import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import pyfirmata
import time

if __name__ == '__main__':
    # You can generate a Token from the "Tokens Tab" in the UI
    token = "V_g3T7i-QyHF3e_uDvBE05MRVKd-234xHwLDACXuw457UnhEBFOVP1Cr5IVb1EclrG6IRS5uBjMbOhMidnu8kA=="
    org = "jarvil"
    bucket = "jarvil-bucket"
    client = InfluxDBClient(url="http://localhost:8086", token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    board = pyfirmata.Arduino('COM6')
    board.analog[0].mode = pyfirmata.INPUT  
    it = pyfirmata.util.Iterator(board)  
    it.start()  
    print("Communication Successfully started")
    
    while True:
        brightness = board.analog[0].read()
        print("Brightness:",brightness)
        if brightness != None:
            data = "measurement,host=arduino1 brightness="+str(brightness)
            write_api.write(bucket, org, data)
            # write_api.write(bucket, org, [{"measurement": "environment", "tags": {"location": "room1"}, "fields": {"brighness": brightness}, "time": t}])
        time.sleep(1)
