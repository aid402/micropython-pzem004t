# micropython-pzem004t
Micropython communication library for Peacefair PZEM-004T Energy monitor 

```
import pzem
emon=pzem.PZEM004T()
#or emon=pzem.PZEM004T(id)
#id --> uart id, default id=0 
emon.isRead() #set Address (return True or Flase)
emon.readVoltage()
emon.readCurrent()
emon.readPower()
emon.readEnergy()
emon.readAll()
```
