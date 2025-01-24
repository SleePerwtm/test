from enum import Enum


class Campus(str, Enum):
    xls = "兴隆山"
    zx = "中心"
    hjl = "洪家楼"


print(Campus.xls)
print(Campus.zx)
print(Campus.hjl)
print(Campus.xls.value)
print(Campus.zx.value)
print(Campus.hjl.value)
