def rent_cal(hrmonth, city):
    #租金
    rank1_cities = ["上海","北京","南京","南昌","广州","长沙","成都","重庆","杭州","武汉","济南","深圳","西安","青岛"]
    rank2_cities = ["连云港","东莞","常州","无锡","珠海","苏州","苏州新区","苏州园区"]
    rank3_cities = ["牙克石"]
    if city in rank1_cities:
        hr_amount = hrmonth * 1500
    elif city in rank2_cities:
        hr_amount = hrmonth * 1100
    elif city in rank3_cities:
        hr_amount = hrmonth * 800
    else:
        raise Exception("city not found in system")
    return hr_amount

def sad_cal(baby, ce, ace, pqce, mimonth, hrmonth, city, aged, sibling, medical):
    baby_amount = baby * 12 * 3000
    ce_amount = ce * 2000 * 12 #子女教育

    ace_amount = 4800 if ace == "进行学历继续教育" else 0
    pqce_amount = pqce * 3600 #职业资格继续教育

    mi_amount = mimonth * 1000 #首套住房贷款利息
    hr_amount = rent_cal(hrmonth,city) #租金

    aged_amount = (aged * 12 * 3000) / (sibling+1) #赡养老人
    medical_amount = min(medical-15000, 80000) #大病医疗

    total_amount = baby_amount + ce_amount + ace_amount + pqce_amount + mi_amount + hr_amount + aged_amount + medical_amount

    return total_amount