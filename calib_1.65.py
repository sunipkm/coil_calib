#%%
import numpy as np
import matplotlib.pyplot as plt
import scipy as scp


# %%
data = np.loadtxt('coil_data_1.65.csv', delimiter=',').transpose()
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
plt.ylim(-65,65)
plt.xlim(7,10)

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
A = np.array([[-20.55978712,   1.7934894 , 140.20104374],
       [174.01474516,   2.50270894,   8.25791513],
       [  0.50886473, -85.273913  ,   3.60570085]])

C = array([[ 8584.03790773],
       [-5982.76708786],
       [-3477.67081986]])

InvA = array([[-3.40207795e-04,  5.70597522e-03,  1.60309708e-04],
       [ 2.97293197e-04,  6.93934327e-05, -1.17186265e-02],
       [ 7.07892168e-03,  8.35865243e-04,  1.73416440e-04]])

vec(Coil) = InvA * (vec(B) - vec(C)) [ B, C in uT]
vec(B) = A * vec(Coil) + vec(C)
"""

# %%
def getB(val):
       global A, C
       val = np.array(val)
       val.shape = (3,1)
       return np.matmul(np.linalg.inv(A),(val - C))


# %%
getB([0, 0, 0])

# %%
getB([1000,-7000,-3000])

# %%
np.matmul(A,np.array([[100],[100],[100]]))+C

# %%
