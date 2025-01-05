import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from windrose import WindroseAxes



df=pd.read_csv('tubulent2.csv',header=None,names=['timestamp','index','ux','uy','uz'],parse_dates=['timestamp'],low_memory=False)
df.set_index('timestamp',inplace=True)
for col in ["index", "ux", "uy", "uz"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
start_time=pd.Timestamp('2015-05-12 00:00:00')
end_time=pd.Timestamp('2015-05-12 23:59:59')
time_range=pd.date_range(start=start_time,end=end_time,freq='S')
df=df.reindex(time_range)
df['ux_mean']=df['ux'].resample('10T').transform('mean')
df['ux_prime']=df['ux']-df['ux_mean']
df['uy_mean']=df['ux'].resample('10T').transform('mean')
df['uy_prime']=df['ux']-df['ux_mean']
df['uz_mean']=df['ux'].resample('10T').transform('mean')
df['uz_prime']=df['ux']-df['ux_mean']
df['turbulenceintensity']=((((df['ux_prime'])**2)+((df['uy_prime'])**2)+((df['uz_prime'])**2))**0.5)/(((df['ux_mean']**2)+(df['uy_mean']**2)+(df['uz_mean']**2))**0.5)


# Step 2: Calculate wind direction (in degrees) from Ux, Uy
df['direction'] = np.degrees(np.arctan2(df['uy'], df['ux'])) % 360

# Step 3: Plot Wind Rose
fig = plt.figure(figsize=(8, 8))

# Create wind rose axes
ax = WindroseAxes.from_ax(fig=fig)

# Plot the wind rose (turbulence intensity vs. direction)
ax.bar(df['direction'], df['turbulenceintensity'], normed=True, opening=0.8, edgecolor='black')

# Customize the wind rose plot
ax.set_legend(title="turbulence intensity")
ax.set_title("Wind Rose Diagram with respect to wind direction and turbulence intensity taking mean over 10 minutes of timing window on 12-05-2015_(24 hrs)")

# Show the wind rose plot
plt.show()




