def sad_cal(cemonth, acemonth, pqce, mimonth, hrmonth, city, agedmonth, sibling, medical,babymonth):
    """

    :param cemonth: 子女教育月数
    :param acemonth: 学历继续教育月数
    :param pqce: 职业资格继续教育
    :param mimonth: 首套住房贷款利息支付月数
    :param hrmonth: 房租
    :param city: 所在城市
    :param agedmonth: 赡养老人数
    :param sibling: 亲兄弟姐妹数
    :param medical: 自付大病医疗费用
    :param babymonth:三岁以下婴幼儿照护月数
    :return: 专项附加扣除金额
    """
    rank1_cities = ["上海","苏州","南京","长沙","成都","重庆","杭州"]
    rank2_cities = ["无锡"]
    rank3_cities = []

    ce_amount = cemonth * 2000 #子女教育
    ace_amount = acemonth * 400 #学历继续教育
    pqce_amount = pqce * 3600 #职业资格继续教育

    mi_amount = mimonth * 1000 #首套住房贷款利息
    #租金
    if city in rank1_cities:
        hr_amount = hrmonth * 1500
    elif city in rank2_cities:
        hr_amount = hrmonth * 1100
    elif city in rank3_cities:
        hr_amount = hrmonth * 800
    else:
        raise Exception("city not found in system")

    aged_amount = (agedmonth * 3000) / (sibling+1) #赡养老人
    medical_amount = min(medical-15000, 80000) #大病医疗
    baby_amount = babymonth * 3000

    total_amount = ce_amount + ace_amount + pqce_amount + mi_amount + hr_amount + aged_amount + medical_amount + baby_amount
    return total_amount

def od_cal(ec, salary, tahi, tari):
    """

    :param ec: 员工个人缴费比例，五档
    :param salary: 缴费工资
    :param tahi: 税优健康险每月减免金额
    :param tari: 税优养老险每月减免金额
    :return: 员工个人缴费年金
    """
    if ec == '0':
        ec_amount = 1
    elif ec == '1%':
        ec_amount = 0.01 * salary
    elif ec == '2%':
        ec_amount = 0.02 * salary
    elif ec == '3%':
        ec_amount = 0.03 * salary
    elif ec == '4%':
        ec_amount = 0.04 * salary
    else:
        ec_amount = 0

    od_amount = ec_amount + min (tahi,200) * 12 + tari * 12
    return od_amount

def ati_cal(ws,sr,mr,ri,sd,sad,od,donation):
    """

    :param ws: 工资、薪金所得
    :param sr: 劳务报酬所得，80%计入综合所得
    :param mr: 稿酬所得，70%计入综合所得
    :param ri: 特许权使用费所得，80%计入综合所得
    :param sd: 专项扣除，每月个人缴纳五险一金
    :param sad: 专项附加扣除
    :param od: 其他扣除t=
    :param donation: 公益性捐赠支出
    :return: 返回全年应纳税所得额
    """

    earnings = ws + sr*0.8 + mr*0.7 + ri*0.8
    #未考虑储蓄计划和养老计划超出部分

    taxable = earnings - sd*12 - sad - od -60000
    ati = taxable - min(donation, 0.3*taxable)

    return ati #基本起征点60000
