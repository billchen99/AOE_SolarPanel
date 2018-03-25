import math
import matplotlib.pyplot as plt
import scipy.integrate as integrate

AU = 1.496*10**11 # m
P0 = 3.8*10**26 # W
SHIELD = 0.75
latitude_deg = 40.8107
longitude_deg = 73.9561

V = 120 #VAC
I = 20 #amps
T = 2 #hrs
E = V*I*T #w-hr

def get_distance(day):
    return (1-0.01672*math.cos(2*math.pi/365.256363*(day-4))) # AU

def get_intensity(day):
    r = get_distance(day)*AU
    return P0/(4*math.pi*r**2)

def get_declination_angle(day):
    return 23.45*(math.pi/180)*math.sin((284+day)*2*math.pi/365.256363) # radians

def get_max_zenith_angle(day):
    return latitude_deg*math.pi/180 - get_declination_angle(day) # radians

def get_hour_angle(time): 
    return (time-12)*15*math.pi/180

def get_altitude_angle(day,time): # elevation angle in deg
    hour_angle = get_hour_angle(time)
    latitude = latitude_deg*math.pi/180
    declination_angle = get_declination_angle(day)
    x = math.cos(hour_angle)*math.cos(declination_angle)*math.cos(latitude)+math.sin(declination_angle)*math.sin(latitude)
    return math.asin(x)*180/math.pi
    
def get_effective_intensity(day,time):
    elevation = get_altitude_angle(day,time)*math.pi/180
    return get_intensity(day)*SHIELD*math.sin(elevation)

def get_surface_energy_horizontal(day,time1,time2): # energy per square meter when panel is flat on the ground
    result = integrate.quad(lambda t: get_effective_intensity(day,t), time1, time2)
    return result[0]

def get_surface_energy_tracking(day,duration): # energy per square meter when panel is elevated
    result = integrate.quad(lambda t: get_effective_intensity(day,t), 12-duration/2, 12+duration/2)
    return result[0]
    # panel's angle of elevation = get_altitude_angle(day,time)
    
plot_data = {}
for t in range(365):
    plot_data[t] = get_surface_energy_tracking(t,8)
plt.plot(plot_data.values())
plt.ylabel("Energy/m^2 per day in watt hours")
plt.xlabel("Day of the year in day")
plt.title("Daily Total Energy Exposure per Meter at Ground Level in New York")
plt.show()

print(E,get_surface_energy_tracking(1,9))
