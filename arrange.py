import math
import numpy as np
import target

def sort_targets(targets):
    # 按距离排序
    targets.sort(key=lambda x: x.distance)
    return targets