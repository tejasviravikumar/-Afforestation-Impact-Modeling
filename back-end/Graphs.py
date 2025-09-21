import json
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('fivethirtyeight')

with open('tree-species.json') as f:
    data = json.load(f)['species']

yrs = np.arange(1, 21)
spec = list(data.keys())

def yearly(s):
    b = data[s]['Avg_Biomass_kg_per_year']
    c = data[s]['Carbon_Content_Ratio']
    f = data[s]['CO2_Conversion_Factor']
    surv = data[s]['Survival_Rate']
    life = data[s]['Lifespan_Years']
    k = 0.3
    max_b = b * life
    y = []
    for t in yrs:
        g = max_b / (1 + np.exp(-k*(t-10)))
        co2 = g * c * f * surv
        y.append(co2 if t <= life else y[-1])
    return np.array(y)

cum = {s: np.cumsum(yearly(s)) for s in spec}
ann = {s: yearly(s) for s in spec}

top = sorted(spec, key=lambda s: cum[s][-1], reverse=True)[:10]
cols = plt.cm.tab10(np.linspace(0,1,len(top)))

plt.figure(figsize=(16,7))
for i,s in enumerate(top):
    plt.plot(yrs, cum[s], label=s, color=cols[i], lw=2)
plt.title('Cumulative CO₂ Sequestration Over 20 Years', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('CO₂ Captured (kg)', fontsize=12)
plt.grid(True, ls='--', alpha=0.5)
plt.legend(fontsize=10, loc='upper left', frameon=True)
plt.show()

plt.figure(figsize=(16,7))
for i,s in enumerate(top):
    plt.plot(yrs, ann[s], label=s, color=cols[i], lw=2)
plt.title('Annual CO₂ Sequestration Rate', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('CO₂ Captured (kg)', fontsize=12)
plt.grid(True, ls='--', alpha=0.5)
plt.legend(fontsize=10, loc='upper left', frameon=True)
plt.show()

plt.figure(figsize=(16,7))
vals = [cum[s][-1] for s in top]
plt.bar(top, vals, color=cols)
plt.title('Total CO₂ Captured by Each Species', fontsize=14)
plt.xlabel('Species', fontsize=12)
plt.ylabel('CO₂ Captured (kg)', fontsize=12)
plt.grid(True, ls='--', alpha=0.5)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.show()
