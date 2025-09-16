def ati_cal(ws,sr,mr,ri,sd,sad,od,donation):
    """

    :param ws: 工资、薪金所得
    :param sr: 劳务报酬所得，80%计入综合所得
    :param mr: 稿酬所得，70%计入综合所得
    :param ri: 特许权使用费所得，80%计入综合所得
    :param sd: 专项扣除，每月个人缴纳五险一金
    :param sad: 专项附加扣除
    :param od: 其他扣除
    :param donation: 公益性捐赠支出
    :return: 返回全年应纳税所得额
    """

    earnings = ws + sr*0.8 + mr*0.7 + ri*0.8
    #未考虑储蓄计划和养老计划超出部分

    taxable = max(0,earnings - sd*12 - sad - od -60000)  #基本起征点60000
    ati = taxable - min(donation, 0.3*taxable)

    return ati
