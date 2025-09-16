import streamlit as st
import pandas as pd

url = 'https://raw.githubusercontent.com/jiayy0818/tax-streamlit/main/rule.csv'
df = pd.read_csv(url)
ls_entity = list(set(df['RGB']))
ls_entity = sorted(ls_entity)
ls_city = list(set(df['缴纳地']))
ls_city = sorted(ls_city)

from ws_calculation import ws_cal
from sd_calculation import sd_cal
from sad_calculation import sad_cal
from od_calculation import od_cal


from ati_calculation import  ati_cal
from tax_calculation import tax_cal


st.title("Tax Deduction Calculator")
st.caption("此计算器仅供员工选择年金个人缴费比例测试使用")

#个人信息
st.subheader("个人信息")
grade = st.selectbox("职级：",options=["1","2","3","4","5","6","7","8","9","SL1","SL2","SL3"])
# genre:蓝领/白领
entity = st.selectbox("所属公司:",options=ls_entity)
city = st.selectbox("社保缴纳地:",options=ls_city)
yos = st.selectbox("服务年限：",options=range(1,51))
plantype = st.selectbox("原计划组成情况",options=["仅养老计划","储蓄计划和养老计划组合"])

st.divider()

#界面分块，创建三列
col1, col2, col3, col4, col5 = st.columns([1, 0.05, 1, 0.05, 1])

#第一块内容（综合收入所得）
with col1:
    st.subheader("综合收入所得")

    ms = st.number_input("工资月薪（税前）：",value=8000, min_value=3000)
    month = st.selectbox("工资月数：",options=[12,13])
    allowance = st.number_input("每月津贴：", value=1000, min_value=0)
    bonus_choice = st.selectbox("奖金是否单独计税：", options=["奖金单独计税", "奖金不单独计税"])

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

    ace = st.selectbox("学历继续教育", options=["进行学历继续教育","未进行学历继续教育"], index=1)
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

    ws = ws_cal(ms, month, allowance, grade, bonus_choice, yos, plantype)
    st.write('工资、薪酬所得',ws,'元/年。')

    #缴纳基数
    salary = ws/12

    # 专项附加扣除
    sad = sad_cal(baby, ce, ace, pqce, mimonth, hrmonth, city, aged, sibling, medical)
    st.write('专项附加扣除',sad,'元/年。')

    #专项扣除
    sd = sd_cal(df, entity, city, salary)
    st.write('专项扣除',sd,'元/月。')

    #其他扣除
    od_org = od_cal(df,6, salary, entity, city, tahi, tari)[0] #不缴年金的其他扣除
    od_new, ec_amount = od_cal(df, ec, salary, entity, city, tahi, tari) #缴年金的其他扣除

    ati_org = ati_cal(ws, sr, mr, ri, sd, sad, od_org, donation)
    ati_new = ati_cal(ws, sr, mr, ri, sd, sad, od_new, donation)

    tax_org = tax_cal(ati_org)
    tax_new = tax_cal(ati_new)
    tax_deduction = tax_org - tax_new


    st.write("不缴年金时，全年应纳税所得额为", ati_org,"元；应缴纳个人所得税",tax_org,"元。")
    st.write("选择",ec,"档个人年金缴费比例时，全年应纳税所得额为",ati_new, "元；应缴纳个人所得税", tax_new, "元。")

    st.write('缴纳年金金额为:',ec_amount,'元/年。')
    st.write("应缴纳个人所得税优惠金额为", tax_deduction,"元/年。")
