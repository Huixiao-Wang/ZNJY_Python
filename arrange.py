import math
import numpy as np
import target
import config

def sort_targets(targets):
    """
    按照 label_priority 设定的优先级排序，如果 label 相同，则按距离排序。

    :param targets: 需要排序的目标列表
    """
    targets.sort(key=lambda x: (config.LABEL_PRIORITY.get(x.label, float('inf')), x.distance))
    return targets