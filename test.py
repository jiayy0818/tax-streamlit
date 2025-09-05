import streamlit as st

from tax_calculation import tax_cal
from ati_calculation import sad_cal, od_cal, ati_cal

st.title("Tax Deduction Calculator")

cemonth = st.number_input("子女教育月份数:", value =0, min_value=0)
st.caption("子女教育包括义务教育（小学、初中）、高中阶段教育（职业技术学校、高中、中专）、高等教育（本科、硕士研究生、博生研究生）。"
           "若9月入学，填写4；若6月毕业，填写6；若连续就读，填写12。多子女家庭可累加计算。")
acemonth = st.number_input("学历继续教育月份数:", value =0, min_value=0, max_value=12)
st.caption("若9月入学，填写4；若6月毕业，填写6；若连续就读，填写12，连续最多48个月。")
pqce = st.number_input("当年职业资格继续教育证书获得数量:", value =0, min_value=0)
mimonth = st.number_input("首套住房贷款利息支付月份数:", value =0, min_value=0, max_value=12)
hrmonth = st.number_input("房租租金支付月份数:", value =0, min_value=0, max_value=12)
city = st.text_input("所在城市:", value="上海")
agedmonth = st.number_input("赡养老人月份数:", value =0, min_value=0)
sibling = st.number_input("亲兄弟姐妹数量:", value =0, min_value=0)
medical = st.number_input("大病医疗医保范围内自付费用:", value =0, min_value=0)
ec = st.selectbox("员工个人年金缴费比例:", options=["0", "1%", "2%", "3%", "4%"])
tahi = st.number_input("符合国家规定的税优健康险每月减免额度:", value =0,  min_value=0, max_value=200)
tari = st.number_input("符合国家规定的税优养老险每月减免额度:", value =0, min_value =0)
ws = st.number_input("工资、薪酬所得:", value =0, min_value =0)
sr = st.number_input("劳务报酬所得:", value =0, min_value =0)
mr = st.number_input("稿酬所得:", value =0, min_value =0)
ri = st.number_input("特许使用费所得:", value =0, min_value =0)
sd  = st.number_input("个人缴纳五险一金:", value =0, min_value =0)

if st.button("计算个人所得税优惠"):
    sad_amount = sad_cal(cemonth, acemonth, pqce, mimonth, hrmonth, city, agedmonth, sibling, medical)
    od_org = od_cal(6, ws, tahi, tari)
    od_new = od_cal(ec, ws, tahi, tari)
    ati_org = ati_cal(ws, sr, mr, ri, sd, sad_amount, od_org)
    ati_new = ati_cal(ws, sr, mr, ri, sd, sad_amount, od_new)

    tax_deduction = tax_cal(ati_org) - tax_cal(ati_new)
    st.write("应缴纳个人所得税优惠金额为", tax_deduction)
