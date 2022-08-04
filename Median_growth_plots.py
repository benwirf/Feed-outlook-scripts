import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
  
# create data

fy_months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

part_months = ['Jul', 'Aug']

# Southern AS District
median = [232 for i in range(12)]

fy_20_21 = [0,
3.028296947,
3.028296947,
27.78310204,
29.49085236,
52.2272892,
70.18850327,
106.3097229,
172.952919,
237.2338867,
247.345871,
250.9003143]

fy_21_22 = [0,
0,
0,
1.137521029,
121.7705116,
147.6960678,
227.0223618,
403.2336578,
421.091568,
421.7874603,
422.4819183,
441.9855042]

fy_22_23 = [0, 0]
#fy_22_23 = [0, 100]

# Interpolate data points for smooth lines
idx = range(len(fy_months))
xnew = np.linspace(min(idx), max(idx), 300)

spl_20_21 = make_interp_spline(idx, fy_20_21, k=3)
smooth_20_21 = spl_20_21(xnew)

spl_21_22 = make_interp_spline(idx, fy_21_22, k=3)
smooth_21_22 = spl_21_22(xnew)

  
# plot lines without smoothing
plt.plot(fy_months, median, label='Median', color='grey', linewidth=5) # Median is constant (doesn't need smoothing)
#plt.plot(fy_months, fy_20_21, label='2020/2021', color='Blue', linewidth=3)
#plt.plot(fy_months, fy_21_22, label='2021/2022', color='Red', linewidth=3)
#plt.plot(part_months, fy_22_23, label='2022/2023', color='Green', linewidth=3)

# Plot smoothed lines
plt.plot(xnew, smooth_20_21, label='2020/2021', color='blue', linewidth=5)
plt.plot(xnew, smooth_21_22, label='2021/2022', color='red', linewidth=5)
plt.plot(part_months, fy_22_23, label='2022/2023', color='lawngreen', linewidth=5)

plt.legend(fontsize=18)
plt.xticks(fontsize=18, rotation=90)
plt.yticks(np.arange(0, 800, step=250), fontsize=18)
plt.gca().yaxis.grid(linestyle='dashed')
plt.show()