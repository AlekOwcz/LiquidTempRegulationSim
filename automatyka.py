import math as mt
#from re import I
from matplotlib import pyplot as plt


def error(target,current):   
    return target-current

def signal(kp, tp, ti, td, errors):
    P = errors[-1]
    I = (tp/ti)*sum(errors)
    D = (td/tp)*(errors[-1]-errors[-2])
    #return kp*(errors[-1]+(tp/ti)*sum(errors)+(td/tp)*(errors[-1]-errors[-2]))
    return kp*(P+I+D)

#Temperature parameters in Celsius
temp_min = 0
temp_max = 100
temp_initial = 10
temp_target = 87
temp_surrounding = 20 #Temperature of surroundings
heat_capacity = 4186 #in J/(kg*c)
density = 997

wall_breadth = 0.5 #in meters
a = 1
b = 2
h = 2
mass = a*b*h*997 
thermal_conductivity = 80 #in W/(m*K)


temps = [temp_initial]
periods = [0]
errors = [temp_target-temp_initial]

time = 1900
Tp=0.5 #sampling period
simulation_time = int(time/Tp)

Qd=0
Qd_max=36000000
Qd_min=0

Kp=0.015
Ti=8
Td=1

signal_max=10
signal_min=0
efficiency = 0.4

for n in range(1,simulation_time):

    error_new = error(temp_target,temps[n-1])
    errors.append(error_new)

    signal_new = signal(Kp, Tp, Ti, Td, errors)
    if(temps[-1] < temp_target): #turning off the heater when te system reaches or overshoots the target temperature
        Qd = efficiency * signal_new * ((Qd_max-Qd_min)/(signal_max-signal_min))
    else:
        Qd = 0

    periods.append(n*Tp)
    temp_new = (1 / (mass * heat_capacity)) * (Qd - 1/wall_breadth * thermal_conductivity * (temps[-1] - temp_surrounding) * Tp * 2 * (a*b + a*h + b*h)) + temps[-1]
    temps.append(temp_new)

t = [temp_target]*simulation_time
plt.plot(periods,t,'g')
plt.plot(periods,temps,'b')
#plt.plot(periods,errors,'r')
plt.xlim(0)
plt.show()



