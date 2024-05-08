import config
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import requests, json

match config.file_format:
    case "fit":
        extension = ".fit"
        type = "0"
    case "gpx":
        extension = ".gpx"
        type = "1"
    case "tcx":
        extension = ".tcx"
        type = "2"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    "Accept-Encoding" : "gzip, deflate",
}

session = requests.session()

# login account
print("Synchronize iGPSPORT data")

url = "https://i.igpsport.com/Auth/Login"
data = {
    'username': config.username,
    'password': config.password,
}
res = session.post(url, data, headers=headers)

# get igpsport list
url = "https://i.igpsport.com/Activity/ActivityList"
res = session.get(url)

result = json.loads(res.text, strict=False)

activities = result["item"]
timezone = ZoneInfo('Europe/Budapest')

sync_data = []
for activity in activities:
    dt        = datetime.strptime(activity["StartTime"], "%Y-%m-%d %H:%M:%S")
    dt2       = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=timezone)
    s_time    = dt2.timestamp()
    mk_time   = int(s_time) * 1000

    if os.path.exists(config.save_folder+str(activity["RideId"])+extension):
        print(str(activity["RideId"])+" already exist")
    else:
        sync_data.append(activity)

if len(sync_data) == 0:
    print("no data need sync")
else:
    #download file
    for sync_item in sync_data:
        rid     = sync_item["RideId"]
        rid     = str(rid)
        print("sync rid:" + rid)

        fit_url = "https://i.igpsport.com/fit/activity?type="+type+"&rideid="+rid
        res     = session.get(fit_url)
        
        export_path = config.save_folder+rid+extension
        if not os.path.exists(export_path):
            if res.status_code == 200:
                with open(export_path, 'wb') as f:
                    f.write(res.content)