import matplotlib.pyplot as plt
import numpy as np
import platform
import random
import time

# Max sleep in seconds 
maxSleepTime = 0.01
 
# Data storage lists
reqSleepList = []
actSleepList = []

# Collect 1000 data points
for _ in range(1000):
   sleepTime = random.random() * maxSleepTime
   reqSleepList.append(sleepTime * 1000.0)

   start = time.time()
   time.sleep(sleepTime)
   end = time.time()

   actSleepList.append((end - start) * 1000.0)

# Calculate the best fit line and print result
z = np.polyfit(reqSleepList, actSleepList, 1)
f = np.poly1d(z)
print('y = {:<0.6f}x + {:<0.6f}'.format(z[0], z[1]))

# Create a figure
fig = plt.figure()
ax0 = plt.gca()

# Plot actual data and theoretical data
ax0.plot(reqSleepList, actSleepList, 'r+')
ax0.plot([0, maxSleepTime * 1000], [0, maxSleepTime * 1000.0], 'k--')
ax0.plot(reqSleepList, f(reqSleepList), 'k-')

# Figure formatting
ax0.set_title('Sleep behavior of:\n' + platform.platform(), fontsize=14, fontweight='bold')
ax0.set_xlabel('Requested Sleep Time [ms]', fontweight='bold')
ax0.set_ylabel('Actual Sleep Time [ms]', fontweight='bold')
ax0.set_xlim([0, maxSleepTime * 1000.0])
ax0.set_ylim([0, maxSleepTime * 1000.0])
ax0.legend(['Actual', 'Theoretical', 'Linear Best Fit'])

# Show and save
plt.grid()
plt.show()
fig.savefig('sleep_test' + platform.platform() + '.png', dpi=fig.dpi)
