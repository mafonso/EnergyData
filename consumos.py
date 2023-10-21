# import pandas lib as pd
import pandas as pd
from datetime import datetime, time

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "hangas"
url = "http://172.16.15.223:8086"
bucket = "consumos"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# read excel file
consumo = pd.read_excel('data/consumos/consumos_06.xlsx', skiprows=8, header=None)

# cpe = consumo.iloc[1, 1]
# print(cpe)

# print(consumo)

for index, row in consumo.iterrows():
    date = datetime.strptime(consumo.iloc[index, 0], '%Y/%m/%d').date()
    time = datetime.strptime(consumo.iloc[index, 1], '%H:%M').time()
    active_power = consumo.iloc[index, 2]/24

    dt = date + pd.DateOffset(hours=time.hour, minutes=time.minute)

    point = (
        Point("consumo")
        .time(dt)
        .field("active_power", active_power)
        .tag("CPE", "PT0002000088766546AG")
    )

    write_api.write(bucket=bucket, org="hangas", record=point)
    write_api.flush()

write_client.close()
