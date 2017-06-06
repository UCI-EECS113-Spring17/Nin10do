#initial
from pynq import Overlay
from pynq.board import LED
from pynq.iop import Pmod_KYPD
from pynq.iop import Pmod_JYSK
from pynq.iop import PMODB
from pynq.iop import PMODA
import time

Overlay("base.bit").download()
#create instance
MAX_LEDS = 4
i = 0

print("Hello world")
#kypd = Pmod_KYPD(PMODB)
jysk = Pmod_JYSK(PMODA)

leds = [0] * MAX_LEDS


for i in range(MAX_LEDS):
    leds[i] = LED(i)
    
#clear
def clear_LEDs(LED_nos=list(range(MAX_LEDS))):
    """Clear LEDS LD3-0 or the LEDs whose numbers appear in the list"""
    for i in LED_nos:
        leds[i].off()
        
clear_LEDs()

# operation
while True:
    tmp = jysk.read()
    #print(tmp)
    if tmp>=120 and tmp<=130:
        print("down")
    elif tmp>=160 and tmp<=170:
        print("up")
    #print(kypd.read())
    #print("{0:b}".format(kypd.read()))
    time.sleep(0.1)
    i=i+1
    if i==1000:
        break

    

clear_LEDs()