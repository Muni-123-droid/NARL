import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df=pd.read_csv('tubulent2.csv',header=None,names=['timestamp','index','ux','uy','uz'],parse_dates=['timestamp'],low_memory=False)
df.set_index('timestamp',inplace=True)

for col in ["index", "ux", "uy", "uz"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

start_time=pd.Timestamp('2015-05-12 00:00:00')
end_time=pd.Timestamp('2015-05-12 23:59:59')

time_range=pd.date_range(start=start_time,end=end_time,freq='S')
df=df.reindex(time_range)
df['ux_mean']=df['ux'].resample('5T').transform('mean')

plt.plot(df.index,df['ux'],label='Instaneous ux',color='blue',linewidth=0.8,alpha=0.2)
plt.plot(df.index,df['ux_mean'],label='mean ux',color='red',linestyle='--',linewidth=1.2)
plt.xlabel('Timestamp')
plt.ylabel('ux values')
plt.title('Turbulence Data Analysis (May 12,2015): Instantaneous and 5-minute mean of ux over 24 hours')
plt.legend()
plt.grid()

ax=plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.tight_layout()
plt.show()

