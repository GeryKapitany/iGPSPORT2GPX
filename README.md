
# iGPSPORT2GPX

This script is a modified version of kvnZero's awesome IGPSPORT2Xingzhe Python script.

It's dowloading all activities from iGPSPORT website in the desired fomart (fit/gpx/tcx).

## Docker
```
git clone https://github.com/GeryKapitany/iGPSPORT2GPX
cd iGPSPORT2GPX
nano config.py
docker build -t igpsport-alpine .
docker run --name igpsport-alpine -v /data/docker/iGPSPORT2GPX/data/:/export igpsport-alpine
```