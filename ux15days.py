import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


df = pd.read_csv('tubulent2.csv', header=None, names=['timestamp','index', 'ux', 'uy', 'uz'])


for col in ["index", "ux", "uy", "uz"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df['timestamp']=pd.to_datetime(df['timestamp'])


start_time=pd.Timestamp('2015-05-12 00:00:00')
end_time=pd.Timestamp('2015-05-26 23:59:59')

df_turbulent=df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]

df_turbulent['second_of_day']=df_turbulent['timestamp'].dt.hour * 3600 + df_turbulent['timestamp'].dt.minute * 60 + df_turbulent['timestamp'].dt.second

mean_15=df_turbulent.groupby('second_of_day')['ux'].mean()

may_12=df_turbulent[(df['timestamp'] >= start_time) & (df['timestamp'] <= pd.Timestamp('2015-05-12 23:59:59'))]

may_12['second_of_day']=may_12['timestamp'].dt.hour * 3600 + may_12['timestamp'].dt.minute * 60 + may_12['timestamp'].dt.second

merged_data=pd.merge(may_12,mean_15,on='second_of_day', how='left', suffixes=('','_mean'))

merged_data['ux_difference']=merged_data['ux']-merged_data['ux_mean']

print(merged_data['ux_difference'].sum()/86400)

plt.plot(mean_15.index/3600,mean_15.values, label="mean ux of 15 days",color='blue')

plt.plot(merged_data.index/3600,merged_data['ux_difference'], label="ux prime of may 12",color='red',alpha=0.3)

plt.xlabel("hour of day")

plt.ylabel("uxprime over mean of 15 days")

plt.xticks(range(0,24,2))

plt.grid()

plt.show()

