import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from decimal import Decimal, getcontext
# Set the precision high enough
getcontext().prec = 10
from datetime import datetime
import matplotlib.ticker as mtick
from matplotlib.colors import LogNorm, Normalize
# Ensure LaTeX is properly set up
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"

# Parameters for simulation
fy_values = [0.0001, 0.0002, 0.0004, 0.0008, 0.0016]  # Different fy values
fx_over_fy = 0.6  # Fixed ratio fx/fy
time_extended = np.linspace(1, 10000, 500)  # Extended time range

# Function to simulate Vx over time for the numerical solution
def simulate_vx(fy, fx_over_fy, time):
    fx = fy * fx_over_fy
    damping_factor = fy * 1.0  # approximate damping scaling with fy
    initial_acceleration = fx
    M = 1 # assume block mass
    Vx = (initial_acceleration / damping_factor) * (1 - np.exp((-damping_factor * time)/M))
    return Vx

# Linear function for contact density scaling with fy
def contact_density_linear(fy):
    return 0.01 + (fy - 0.0001) * (0.16 - 0.01) / (0.0016 - 0.0001)

# Refined analytical function with nonlinear scaling of contact density
def refined_analytical_vx(fy, time):
    fx = fy * fx_over_fy
    zeta_b = 1  # body damping constant
    zeta_v = 1  # interface damping constant
    M = 100  # assume block mass
    contact_density_effect = contact_density_linear(fy) ** 1.5  # nonlinear scaling
    zeta_total = zeta_b + zeta_v * contact_density_effect
    Vx_analytical = (fx / zeta_total) * (1 - np.exp(-zeta_total * time / M))
    return Vx_analytical

# Plotting both analytical (refined) and numerical results on scaled axes
fig, ax = subplots(figsize=(6.4, 4.8))  # Create a figure and axes
for fy in fy_values:
    scaled_time = time_extended * fy
    Vx_numerical = simulate_vx(fy, fx_over_fy, time_extended) / fy
    Vx_analytical = refined_analytical_vx(fy, time_extended) / fy

    # Plot numerical and refined analytical solutions
    ax.plot(scaled_time, Vx_numerical, linewidth="0.8",linestyle="-",label=f'$f_y = {fy}$')
    #ax.plot(scaled_time, Vx_analytical, label=f'Refined Analytical $f_y = {fy}$', linestyle='--', alpha=0.7)

ax.set_xlabel('$t \\cdot f_y$',fontsize=15)
ax.set_ylabel('$V_x / f_y$',fontsize=15)
ax.set_title('Analytical Results',fontsize=15)
ax.tick_params(axis='both', which='both', direction='in',labelsize=15)
ax.set_xscale('log')
ax.set_yscale('log')

# Adjust legend and make sure each line is clear
leg = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10, borderaxespad=0)
for line in leg.get_lines():
    line.set_linewidth(1.0)

#Add timestamp text
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')
tight_layout()


tight_layout()
plt.savefig("../plots/VxT-Analytical.pdf",bbox_inches='tight', pad_inches=0)
plt.show()

