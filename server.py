import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from threading import Timer
import time
import datetime

# Create a timer object for running a function repeatedly
class RepeatedTimer(object):
    def __init__(self, start_time, interval, function, *args):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.is_running = False
        self.start_time = start_time
        self.initialize = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args)

    def start(self):
        if not self.is_running:
            if not self.initialize:
                self.initialize = True
                self._timer = Timer(self.start_time, self._run)
            else:
                self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def check_last_file_receieve(sec):
    # Calculate the time difference between now and the time last file was uploaded
    time_diff = time.time() - customFTPHandler.last_receive_time
    
    # If the time difference is greater than a criteria, execute the action
    if time_diff > sec:
        print("No file was uploaded to server for {} seconds".format(time_diff))


class customFTPHandler(FTPHandler):
    last_receive_time = time.time()
    first_check_time = None

    # Update the time when a file is uploade to server
    def on_file_received(self, file):
        customFTPHandler.last_receive_time = time.time()
        print('\n {} has been uploaded to the server.\n'.format(file))


# Set the time for the on_file_receive is run for the first time
def setTime(hour, minute, sec):
    time_now = datetime.datetime.now()
    
    # If the input time has passed for today, set the time to tomorrow at the same time 
    if datetime.datetime(time_now.year, time_now.month, time_now.day, hour, minute, sec) > time_now:
        target_time = datetime.datetime(time_now.year, time_now.month, time_now.day, hour, minute, sec)
    else:
        target_time = datetime.datetime(time_now.year, time_now.month, time_now.day+1, hour, minute, sec)

    customFTPHandler.first_check_time = (target_time - time_now).total_seconds()


def main():
    authorizer = DummyAuthorizer()

    authorizer.add_anonymous(os.getcwd(), perm="elradfmw")

    handler = customFTPHandler
    handler.authorizer = authorizer

    address = ('127.0.0.1', 2121)
    server = FTPServer(address, handler)

    # Set the time for check_last_file_receieve function to be run at 17:00:00 
    setTime(17, 0, 0)

    # Run the function once every day
    interval = 60*60*24

    # If the no file was uploaded in the past two hours, trigger check_last_file_receieve
    last_time_update_diff = 60*60*2

    RepeatedTimer(customFTPHandler.first_check_time, interval, check_last_file_receieve, last_time_update_diff)

    server.serve_forever()

if __name__ == '__main__':
    main()