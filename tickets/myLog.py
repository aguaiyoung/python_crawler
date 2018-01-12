# encoding:utf-8  
import sys  
import logging  
import time  
       
def writeLog(message):  
    logger=logging.getLogger("Ticket")  
    formatter = logging.Formatter('%(asctime)s %(levelname)-4s: %(message)s')
    handler=logging.FileHandler("ticket.log")  
    handler.setFormatter(formatter)
    logger.addHandler(handler)  
    logger.setLevel(logging.INFO)  
    logger.info(message)
       
if __name__ == '__main__':         
     writeLog("hello")  
