#!/usr/bin/python

import re

from time import time
from time import sleep
from gi.repository import Notify

# Get ram available in MB
def get_mem_available(mem_file):
    raw_mem_available = ""
    for line in mem_file:
        if line.startswith("MemAvailable"):
            raw_mem_available = line
            break
    match = re.search('[0-9]+', raw_mem_available)
    return int(int(raw_mem_available[match.start():match.end()]) / 1000)

def send_notification(title, message):
    if not Notify.is_initted():
        Notify.init('Ram check')
    
    notif = Notify.Notification.new(title, message)
    notif.set_timeout(10*1000)
    notif.show()

def send_warning(memory):
    send_notification('Memory alert', 'Available memory is equal to '
            + str(memory) + 'Mo !')

def send_safe_message():
    send_notification('Memory alert', 'Available memory is back to normal state')

last_cold_warning_time = 0
last_hot_warning_time = 0


while True:
    with open('/proc/meminfo', 'r') as mem_file:
        ram_available = get_mem_available(mem_file)
        print("Current ram available : " + str(ram_available) + "MB")

        # Hot warning
        if ram_available < 400:
            if time() - last_hot_warning_time > 60:
                send_warning(ram_available)
                last_hot_warning_time = time()

        # Cold warning
        elif ram_available < 700:
            last_hot_warning_time = 0
            if time() - last_cold_warning_time > 60:
                send_warning(ram_available)
                last_cold_warning_time = time()

        else:
            if last_cold_warning_time != 0 or last_hot_warning_time != 0:
                send_safe_message()

            last_cold_warning_time = 0
            last_hot_warning_time = 0
        
    sleep(2)
