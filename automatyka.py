import math as mt
#from re import I
from matplotlib import pyplot as plt


def error(target,current):   
    return target-current

def signal(kp, tp, ti, td, errors):
    p = errors[-1]
    i = (tp/ti)*sum(errors)
    d = (td/tp)*(errors[-1]-errors[-2])
    return kp*(p+i+d)

def heat(efficiency, sig, Qd_max, Qd_min, sig_max, sig_min):
    return efficiency * sig * ( (Qd_max - Qd_min) / (sig_max - sig_min) )

def new_temp(temps, Qd, mass, heat_cap, wall, cond, surrounding, Tp, a, b, h, boiling_point):
    if (temps[-1] > boiling_point):
        return (1 / (mass * heat_cap)) * ( (-1)/wall * cond * (temps[-1] - surrounding) * Tp * (a*b*2 + a*h*2 + b*h*2)) + temps[-1]
    else:
        return (1 / (mass * heat_cap)) * (Qd - 1/wall * cond * (temps[-1] - surrounding) * Tp * (a*b + a*h* 2 + b*h* 2)) + temps[-1]
    
#Temperature parameters in Celsius
temp_min = 0
temp_max = 100
temp_initial = 10
temp_target = 57
temp_surrounding = 20 #Temperature around container
heat_capacity = 4186 #in J/(kg*c)
density = 997 #in kg/m^3

wall_breadth = 0.5 #in meters
a = 1
b = 2
h = 2
mass = a*b*h*997 
thermal_conductivity = 80 #in W/(m*K)


temps = [temp_initial]
periods = [0]
errors = [temp_target-temp_initial]

time = 7200
Tp=0.5 #sampling period
simulation_time = int(time/Tp)

Qd=0
Qd_max=500000
Qd_min=0

Kp=0.15
Ti=5
Td=250

signal_max=10
signal_min=0
efficiency = 0.66

regulation_time = 0
overshoot = 0
#===========================Begin=================================
for n in range(1,simulation_time):

    periods.append(n*Tp)
    error_new = error(temp_target,temps[n-1])
    errors.append(error_new)

    signal_new = signal(Kp, Tp, Ti, Td, errors)

    Qd = heat(efficiency,signal_new,Qd_max,Qd_min,signal_max,signal_min)

    temp_new = new_temp(temps,Qd,mass,heat_capacity,wall_breadth,thermal_conductivity,temp_surrounding,Tp,a,b,h,temp_max)
 
    if (temp_new > 1.05 * temp_target or temp_new < 0.95 * temp_target):
        regulation_time = Tp*n
    temps.append(temp_new)
#============================End==================================
e0 = errors[0]
i = 1
while(i<len(errors)-1):
    if (errors[i-1] > errors[i] < errors[i+1] or errors[i-1] < errors[i] > errors[i+1]):
        e1 = errors[i]
        break
    i+=1
overshoot = abs(e1/e0) * 100
t = [temp_target]*simulation_time
tim = [regulation_time] * simulation_time
plt.axvline(x=regulation_time)
plt.plot(periods,t,'g')
plt.plot(periods,temps,'b')
plt.plot(periods,errors,'r')
plt.xlim(0)
plt.show()
print(max(temps))
print("%.2f"%overshoot,"% overshoot")



