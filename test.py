import streamlit as st

from tax_calculation import tax_cal
from ati_calculation import ws_cal, sad_cal, od_cal, ati_cal

st.title("Tax Deduction Calculator")
st.caption("此计算器仅供员工选择年金个人缴费比例测试使用")

#个人信息
st.subheader("个人信息")
grade = st.selectbox("职级：",options=["1","2","3","4","5","6","7","8","9","SL1","SL2","SL3"])
# genre:蓝领/白领
city = st.selectbox("所在城市:", ["上海","苏州","南京","长沙","成都","重庆","杭州"])
yos = st.selectbox("服务年限：",options=range(1,51))
plantype = st.selectbox("原计划组成情况",options=["仅养老计划","储蓄计划和养老计划组合"])

st.divider()

#界面分块，创建三列
col1, col2, col3, col4, col5 = st.columns([1, 0.05, 1, 0.05, 1])

#第一块内容（综合收入所得）
with col1:
    st.subheader("综合收入所得")

    ms = st.number_input("工资月薪（税前）：",value=3000, min_value=3000)
    month = st.selectbox("工资月数：",options=[12,13])

    allowance = st.number_input("每月津贴：", value=1000, min_value=0)

    #bonus 按照级别的目标年终奖比例，计算好放入
    bonus_map = {
        "6": 0.1875, "7": 0.1875, "8": 0.1875, "9": 0.1875,
        "SL1": 0.225,
        "SL2": 0.2625,
        "SL3": 0.4125
    }
    bonus_percent = bonus_map.get(grade, 0)
    bonus = bonus_percent * ms * month
    bonus_choice = st.selectbox("奖金是否单独计税：",options=["奖金单独计税","奖金不单独计税"])

    sr = st.number_input("劳务报酬所得:", value=0, min_value=0)
    mr = st.number_input("稿酬所得:", value=0, min_value=0)
    ri = st.number_input("特许使用费所得:", value=0, min_value=0)


with col2:
    st.markdown("<div style='height:840px; margin:0 6px; border-left:1px solid #d3d3d3;'></div>",
                unsafe_allow_html=True)

with col3:
    st.subheader("专项附加扣除")

    baby = st.selectbox("三岁以下婴幼儿数:", options=[0,1,2,3])
    ce = st.selectbox("接受义务教育、高中阶段教育、高等教育子女数:", options=range(0,9))

    ace = st.selectbox("学历继续教育", options=["进行学历继续教育","未进行学历继续教育"])
    pqce = st.selectbox("职业资格继续教育:",options=range(0,3))

    mimonth = st.selectbox("支付首套住房贷款利息月份数:", options=range(0,13))
    hrmonth = st.selectbox("支付房租租金月份数:", options=range(0,13))

    aged = st.selectbox("赡养老人数:", options=range(0,5))
    sibling = st.selectbox("亲兄弟姐妹数量:", options=range(0,7))

    medical = st.number_input("大病医疗医保范围内自付费用（元）:", value=0, min_value=0)

with col4:
    st.markdown("<div style='height:840px; margin:0 6px; border-left:1px solid #d3d3d3;'></div>",
                unsafe_allow_html=True)

with col5:
    st.subheader("其他扣除")
    tahi = st.number_input("符合国家规定的税优健康险每月减免额度:", value=0, min_value=0, max_value=200)
    tari = st.number_input("符合国家规定的税优养老险每月减免额度:", value=0, min_value=0)
    st.divider()
    st.subheader("捐赠")
    donation = st.number_input("公益性捐赠支出：",value=0)

st.divider()
st.subheader("年金计划选择")
ec = st.selectbox("员工个人年金缴费比例:", options=["0", "1%", "2%", "3%", "4%"])

st.divider()

if st.button("计算个人所得税优惠"):
    #工资、薪酬所得
    ws = ws_cal(ms, month, allowance, bonus, bonus_choice, yos, plantype)

    #缴纳基数
    salary = ws/12
    cityavg_map = {} #社平工资字典
    cityavg = cityavg_map.get(city, 10000)  #社平工资
    base = min(3*cityavg, salary)

    # 专项附加扣除
    sad = sad_cal(baby, ce, ace, pqce, mimonth, hrmonth, city, aged, sibling, medical)

    #专项扣除
    sd_map = {}
    sd_percent = sd_map.get(city, 0)
    sd = sd_percent * base * 12 #个人缴纳五险一金

    #其他扣除
    od_org = od_cal(6, salary, cityavg,  tahi, tari) #不缴年金的其他扣除
    od_new = od_cal(ec, salary, cityavg, tahi, tari) #缴年金的其他扣除

    ati_org = ati_cal(ws, sr, mr, ri, sd, sad, od_org, donation)
    ati_new = ati_cal(ws, sr, mr, ri, sd, sad, od_new, donation)

    tax_org = tax_cal(ati_org)
    tax_new = tax_cal(ati_new)
    tax_deduction = tax_org - tax_new

    st.write("不缴年金时，全年应纳税所得额为", ati_org,"元；应缴纳个人所得税",tax_org,"元。")
    st.write("选择",ec,"档个人年金缴费比例时，全年应纳税所得额为",ati_new, "元；应缴纳个人所得税", tax_new, "元。")
    st.write("应缴纳个人所得税优惠金额为", tax_deduction,"元。")
