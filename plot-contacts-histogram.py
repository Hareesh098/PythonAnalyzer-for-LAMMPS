from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import maxwell
from datetime import datetime
import matplotlib.ticker as mtick
# Ensure LaTeX is properly set up
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"
# Set the precision high enough
from decimal import Decimal, getcontext
getcontext().prec = 10
from datetime import datetime


data = np.loadtxt('a.dat')
values = data[:, 1]

#Plot the histogram and the KDE curve
#Plotting here
fig, ax = subplots(figsize=(6.4, 4.8))  # Create a figure and axes

#For pdf
# Plotting the histogram with density instead of frequency
#sns.histplot(values, bins=15, kde=False, stat='density', color='green', alpha=0.5, edgecolor='black')
# Adding a KDE curve with customized styling
#sns.kdeplot(values, linewidth=2, linestyle='--', color='blue')

# For frequency
# Calculate the bin width and scaling factor
counts, bin_edges = np.histogram(values, bins=15)
bin_width = bin_edges[1] - bin_edges[0]
scaling_factor = len(values) * bin_width

# Plot histogram with frequency counts
sns.histplot(values, bins=15, kde=False, color='green', alpha=0.5, edgecolor='black')

# Fit a Maxwell distribution
params = maxwell.fit(values)

# Generate fitted distribution for plotting
x = np.linspace(min(values), max(values), len(values))
pdf_fitted = maxwell.pdf(x, *params) * scaling_factor

# Plot the fitted Maxwell distribution
plt.plot(x, pdf_fitted, color='red', linestyle='-', linewidth=2, label='Maxwell fit')

# Plot KDE, scaling it to match the histogram
sns.kdeplot(values, color='blue', linestyle='--', linewidth=2)
plt.gca().lines[-1].set_ydata(plt.gca().lines[-1].get_ydata() * scaling_factor)

# Add labels and title
plt.title('Contacts dustrubution during the motion nAtom=130304, \n Fy=1e-4,Fx=6e-5',fontsize=15)
plt.ylabel('f(Ncon)',fontsize=15)
plt.xlabel('Ncon',fontsize=15)
ax.tick_params(axis='both', which='both', direction='in',labelsize=15)
Figaname = '../plots/Contacts-Histogram-nAtom130304-Z5.9894-Fy1e-4-Fx6e-5'
plt.savefig(Figaname+'.pdf')
# Show the plot
plt.show()

