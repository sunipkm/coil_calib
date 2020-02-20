#%%
import numpy as np
import matplotlib.pyplot as plt
import scipy as scp


# %%
data = np.loadtxt('coil_data_V55.csv', delimiter=',').transpose()
data.shape
# %%
bx = data[2]
by = data[3]
bz = data[4]

bx2 = data[5]
by2 = data[6]
bz2 = data[7]

# %%
sbx = np.sqrt(bx2 - bx*bx)
sby = np.sqrt(by2 - by*by)
sbz = np.sqrt(bz2 - bz*bz)

# %%
bx_0 = bx[np.where(data[0]==0)]
bx_1 = bx[np.where(data[0]==1)]
bx_2 = bx[np.where(data[0]==2)]

sbx_0 = sbx[np.where(data[0]==0)]
sbx_1 = sbx[np.where(data[0]==1)]
sbx_2 = sbx[np.where(data[0]==2)]

by_0 = by[np.where(data[0]==0)]
by_1 = by[np.where(data[0]==1)]
by_2 = by[np.where(data[0]==2)]

sby_0 = sby[np.where(data[0]==0)]
sby_1 = sby[np.where(data[0]==1)]
sby_2 = sby[np.where(data[0]==2)]

bz_0 = bz[np.where(data[0]==0)]
bz_1 = bz[np.where(data[0]==1)]
bz_2 = bz[np.where(data[0]==2)]

sbz_0 = sbz[np.where(data[0]==0)]
sbz_1 = sbz[np.where(data[0]==1)]
sbz_2 = sbz[np.where(data[0]==2)]

# %%
plt.errorbar(range(82), bx_0, yerr=sbx_0, ls='', marker='')
plt.plot(range(82), bx_0)

# %%
coeff, covar = np.polyfit(range(82), bx_0, 1, full=False, cov=True)

# %%
covar

# %%
ax_0 = coeff[0]; cx_0 = coeff[1]

# %%
coeff, covar = np.polyfit(range(82), bx_1, 1, full=False, cov=True)

# %%
covar

# %%
ax_1 = coeff[0]; cx_1 = coeff[1]

# %%
coeff, covar = np.polyfit(range(82), bx_2, 1, full=False, cov=True)
print(covar)
ax_2 = coeff[0]; cx_2 = coeff[1]

# %%
plt.plot(bx_2)
plt.plot(ax_2*range(82)+cx_2)

# %%
coeff, covar = np.polyfit(range(82), by_0, 1, full=False, cov=True)
print(covar)
ay_0 = coeff[0]; cy_0 = coeff[1]

coeff, covar = np.polyfit(range(82), by_1, 1, full=False, cov=True)
print(covar)
ay_1 = coeff[0]; cy_1 = coeff[1]

coeff, covar = np.polyfit(range(82), by_2, 1, full=False, cov=True)
print(covar)
ay_2 = coeff[0]; cy_2 = coeff[1]


# %%
coeff, covar = np.polyfit(range(82), bz_0, 1, full=False, cov=True)
print(covar)
az_0 = coeff[0]; cz_0 = coeff[1]

coeff, covar = np.polyfit(range(82), bz_1, 1, full=False, cov=True)
print(covar)
az_1 = coeff[0]; cz_1 = coeff[1]

coeff, covar = np.polyfit(range(82), bz_2, 1, full=False, cov=True)
print(covar)
az_2 = coeff[0]; cz_2 = coeff[1]

# %%
A = np.array([[ax_0, ax_1, ax_2], [ay_0, ay_1, ay_2], [az_0, az_1, az_2]])

# %%
C = np.array([[cx_0+cx_1+cx_2],[cy_0+cy_1+cy_2],[cz_0+cz_1+cz_2]])

# %%
A

# %%
ax_0, ax_1, ax_2

# %%
C

# %%
np.linalg.inv(A)

# %%
np.matmul(np.linalg.inv(A), -C)

# %%
"""
Results:
A = array([[-13.79575756,   1.36932119,  92.13342584],
       [115.13807316,   1.78930247,   5.19229438],
       [  0.74730031, -55.83940641,   2.51575298]])

C = array([[10142.0730238 ],
       [-3396.34663532],
       [-4635.4686747 ]])

InvA = array([[-0.00049326,  0.00862441,  0.00026426],
       [ 0.00047875,  0.00017349, -0.0178912 ],
       [ 0.01077285,  0.00128881,  0.00030548]])

vec(Coil) = InvA * (vec(B) - vec(C)) [ B, C in uT]
vec(B) = A * vec(Coil) + vec(C)
"""

# %%
