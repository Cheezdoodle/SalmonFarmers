import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad  # approximativa integralen med kvadratur
rng = np.random.default_rng() 

#Parameters
n0 = 10000  #Initial fish population
m = 0.1  #Mortality
w_inf = 6  #Biomass limit
H0=3 #kr/kg biomass, harvesting cost
F0=7 #kr/kg food, feeding cost

#Starting parameters given by project
a = 1.113
b = 1.097
c = 1.43

t = np.linspace(0, 60, 800)

#_________________________________________________________
#Nuber of fish in the pound
#n(t)
def fish_population(t):
    return n0 * np.exp(-m * t)

#Growth over time in terms of biomass (kg)
#w(t)
def biomass_growth(t):
    return w_inf * (a - b * np.exp(-c * t))**3

# Derivative of the biomass growth
#dw/dt
def biomass_growth_derivative(t):
    return 3 * w_inf * b * c * np.exp(-c * t) * (a - b * np.exp(-c * t))**2

#Total biomass of the farm
#B(t)
def total_biomass(t):
    return fish_population(t) * biomass_growth(t)

#The harvesting costs per kg
#H(t)
def harvesting_cost(t):
    return H0*total_biomass(t)

#Instant price
#f(t)
def instant_feeding_cost(t):
    return F0 * fish_population(t) * biomass_growth_derivative(t)


r=0.03

def feeding_cost_overT(t):
    discounted_costs = np.zeros_like(t)
    for i in range(0, len(t)-1):
        discounted_cost, _ = quad(lambda s: np.exp(-r * s) * instant_feeding_cost(s), 0, t[i])
        discounted_costs[i] = discounted_cost
    return discounted_costs

#t_test=10
#print(f"Fish population at t={t_test}: {fish_population(t_test)}")
#print(f"Biomass growth at t={t_test}: {biomass_growth(t_test)}")
#print(f"Biomass growth derivative at t={t_test}: {biomass_growth_derivative(t_test)}")
#print(f"Total biomass at t={t_test}: {total_biomass(t_test)}")
#print(f"Harvesting cost at t={t_test}: {harvesting_cost(t_test)}")
#print(f"Instant feeding cost at t={t_test}: {instant_feeding_cost(t_test)}")

n_t = fish_population(t)
w_t = biomass_growth(t)
B_t = total_biomass(t)
f_t= instant_feeding_cost(t)
F_t= feeding_cost_overT(t)



#Plotta derivatan bara för att se
#plt.figure(figsize=(8, 5))
#plt.plot(t,biomass_growth_derivative(t) , color='royalblue', linewidth=2, label='dw/dt') 

#För att kolla hur exponnten såg ut
#plt.figure(figsize=(8, 5))
#plt.plot(t, np.exp(-r*t), color='royalblue', linewidth=2, label=r'F(t)= $\int_0^t e^{-r s} \, f(s) \, ds$') 

#Plott för priset för att mata fiskarna fram till tiden t
max_feed= max(F_t)
plt.figure(figsize=(8, 5))
plt.plot(t, F_t, color='royalblue', linewidth=2, label=r'F(t)= $\int_0^t e^{-r s} \, f(s) \, ds$') 
plt.axhline(y=max_feed, color='gray', linestyle='--', linewidth=2, label=f'Maximum feeding cost = {max_feed:.2f}')  
#plt.text(35, n0 * 0.75, f'Mortality rate m = {m}', bbox=dict(facecolor='lightgray', alpha=0.7, edgecolor='black'), fontsize=12)  
plt.title('Feeding costs over time ', fontsize=16, fontweight='bold')
plt.xlabel('Time (t) [days]', fontsize=14)
plt.ylabel('Feeding costs [SEK]', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)  
plt.legend(frameon=True, edgecolor='black')  
plt.tick_params(labelsize=12) 
plt.tight_layout()
plt.show()
