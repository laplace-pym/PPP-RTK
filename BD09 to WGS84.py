# *************************************************************************************
# ************************* 坐标点从 BD09 转换为 WGS84 坐标系 *****************************
# *************************************************************************************

import math
import numpy as np

# 转换经度
def transformLat(x, y):
    pi = 3.14159265358979324
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * pi) + 40.0 * math.sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * pi) + 320.0 * math.sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret

# 转换纬度
def transformLon(x, y):
    pi = 3.14159265358979324
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret

# BD09 -> GCJ02
def BD09ToGCJ02(bd_lat, bd_lon):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gcj_lat = z * math.sin(theta)
    gcj_lon = z * math.cos(theta)
    return gcj_lat, gcj_lon

# GCJ02 -> WGS84
def GCJ02ToWGS84(lat, lon):
    pi = 3.14159265358979324
    a = 6378245.0
    ee = 0.00669342162296594323

    if lon < 72.004 or lon > 137.8347 or lat < 0.8293 or lat > 55.8271:
        return lat, lon

    dLat = transformLat(lon - 105.0, lat - 35.0)
    dLon = transformLon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * pi
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * pi)
    mgLat = lat - dLat
    mgLon = lon - dLon
    return mgLat, mgLon

# BD09 -> WGS84
def BD09ToWGS84(bd_lat, bd_lon):
    gcj_lat, gcj_lon = BD09ToGCJ02(bd_lat, bd_lon)
    wgs84_lat, wgs84_lon = GCJ02ToWGS84(gcj_lat, gcj_lon)
    return wgs84_lat, wgs84_lon


if __name__ == "__main__":
    # 118.716431,32.158834   校内
    # 118.70299，32.158545   校外
    # 118.716954,32.157479   校内2
    lat, lon = BD09ToWGS84(32.095087,118.605565)
    print("lat = ", lat)
    print("lon = ", lon)


