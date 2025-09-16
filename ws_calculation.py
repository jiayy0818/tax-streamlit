def bonus_cal(grade, ms, month):
    # bonus 按照级别的目标年终奖比例，计算好放入
    bonus_map = {
        "6": 0.1875, "7": 0.1875, "8": 0.1875, "9": 0.1875,
        "SL1": 0.225,
        "SL2": 0.2625,
        "SL3": 0.4125
    }
    bonus_percent = bonus_map.get(grade, 0)
    bonus = bonus_percent * ms * month
    return bonus

def exceed_cal(plantype, yos, ms):
    if plantype == "仅养老计划":
        if yos >= 9:
            exceed = ms * 12 * 0.04
        elif 5 <= yos <= 9:
            exceed = ms * 12 * 0.02
        else:
            exceed = 0
    else:
        exceed = ms * 12 * 0.05
    return exceed

def ws_cal(ms, month, allowance, grade, bonus_choice, yos, plantype):
    bonus = bonus_cal(grade, ms, month)
    exceed = exceed_cal(plantype, yos, ms)

    if bonus_choice == "奖金不单独计税":
        ws = ms * month + allowance * 12 + bonus + exceed
    else:
        ws = ms * month + allowance * 12 + exceed

    return ws