from mq import *
import sys, time

try:
    print("Press CTRL+C to abort.")
    
    mq = MQ();
    while True:
        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("CO2: %g ppm, CO: %g ppm, Alcohol: %g ppm" % (perc["GAS_CO2"], perc["CO"], perc["ALCOHOL"]))
        sys.stdout.flush()
        time.sleep(0.1)

except:
    print("\nAbort by user")