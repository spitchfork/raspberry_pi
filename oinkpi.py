###########################################
#                                         #
# Tinkerer: Stephen Pitchfork             #
# Email: s.pitchfork@googlemail.com       #
# Licence: MIT                            #
#                                         #
###########################################

# Standard libs
import time
import threading

# Custom libs
# lcd_1602 is something I knocked up while learning about 1602 displays
# I STRONGLY advise anyone to use https://github.com/dbrgn/RPLCD instead
# .. as it is much more mature! If I find the time I will migrate to RPLCD..
import lcd_1602

lcd = lcd_1602.Lcd()

PROG_VERSION = "v0.1"
NET_INTERFACE = "eth0" #TODO query this
SNORT_ALERT_LOG = "/home/yourname/snort_log/alert"

# This is a dirty approach, use RPLCD to clear the screen instead
DISP_MSG_EMPTY = "                "

# Screen messages..
DISP_MSG_ALERT = "Oink! Oink!"
DISP_MSG_PROG = "OinkPi " + PROG_VERSION
DISP_MSG_NIDS = "NIDS Mode Active"
DISP_MSG_INIT = "Initializing..."

# more dirt, use RPLCD to move the cursor to produce the dots
DISP_MSG_LISTEN_0 = "Monitoring      "
DISP_MSG_LISTEN_1 = "Monitoring.     "
DISP_MSG_LISTEN_2 = "Monitoring..    "
DISP_MSG_LISTEN_3 = "Monitoring...   "
DISP_MSG_NET = "Net: " + NET_INTERFACE # Not used.. yet.

test_ids_event = {
 "code": "1:1228:7",
 "class_line_one": "P2: Info Leak",
 "class_line_two": "SCAN nmap XMAS" 
}

new_alert = False


def follow(file, sleep_sec=1):
    """ Yield each line from a file as they are written.
    `sleep_sec` is the time to sleep after empty reads. """
    line = ''
    while True:
        tmp = file.readline()
        if tmp is not None:
            line += tmp
            if line.endswith("\n"):
                yield line
                line = ''
        else:
            time.sleep(sleep_sec)


def monitor_log(name):
 with open(SNORT_ALERT_LOG, "r") as file:
  for line in follow(file):
   if(test_ids_event["code"] in line):
    global new_alert
    new_alert = True


def alert_flash():
 
 lcd.display_line_one(DISP_MSG_EMPTY)
 lcd.display_line_two(DISP_MSG_EMPTY)

 for i in range(3):
  lcd.display_line_one(DISP_MSG_ALERT)
  lcd.display_line_two(DISP_MSG_EMPTY)
  time.sleep(0.3)
  lcd.display_line_one(DISP_MSG_EMPTY)
  lcd.display_line_two(DISP_MSG_EMPTY)

 lcd.display_line_one(test_ids_event["class_line_one"])
 lcd.display_line_two(test_ids_event["class_line_two"])
 time.sleep(5)


lcd.display_line_one(DISP_MSG_PROG)
lcd.display_line_two(DISP_MSG_INIT)

# Start a separate thread to monitor for alerts in the snort alert log
monitor_thread = threading.Thread(target=monitor_log, args=(1,), daemon=True)
monitor_thread.start()

# Wait for any existing alerts to be processed by the log monitor thread
# TODO this SHOULD be improved to discount existing alerts in the snort log  
# .. before this script runs OR the snort log could be cleared after each run
# This is just a quick and dirty approach to get something working.
time.sleep(3)
new_alert = False

while True:

 if(new_alert):
  alert_flash()
  new_alert = False

 lcd.display_line_one(DISP_MSG_NIDS)
 lcd.display_line_two(DISP_MSG_LISTEN_0)
 time.sleep(0.1)
 lcd.display_line_one(DISP_MSG_NIDS)
 lcd.display_line_two(DISP_MSG_LISTEN_1)
 time.sleep(0.1)
 lcd.display_line_one(DISP_MSG_NIDS)
 lcd.display_line_two(DISP_MSG_LISTEN_2)
 time.sleep(0.1)
 lcd.display_line_one(DISP_MSG_NIDS)
 lcd.display_line_two(DISP_MSG_LISTEN_3)
 time.sleep(0.1)
