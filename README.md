# micropython-pzem004t
Micropython communication library for Peacefair PZEM-004T Energy monitor 

```
import pzem
emon=pzem.PZEM004T()
#emon=pzem.PZEM004T(id) default id=0 
emon.isRead() #set Address (return True or Flase)
emon.readVoltage()
emon.readCurrent()
emon.readPower()
emon.readEnergy()
emon.readAll()
emon.setPowerAlarm(20) #set power alarm threshold:20 KW
```
