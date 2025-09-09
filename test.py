import streamlit as st

from tax_calculation import tax_cal
from ati_calculation import sad_cal, od_cal, ati_cal

st.title("Tax Deduction Calculator")
st.caption("此计算器仅供员工选择年金个人缴费比例测试使用")

#个人信息
st.subheader("个人信息")
no = st.text_input("工号：")
grade = st.selectbox("职级：",options=["","",""])
entity = st.selectbox("所属公司：",options=[])
genre = st.selectbox("工作类型：",options=["蓝领","白领"])
city = st.text_input("所在城市:", value="上海")
yos = st.selectbox("服务年限：",options=range(1,51))
plantype = st.selectbox("原计划组成情况",options=["仅养老计划","储蓄计划和养老计划组合"])

st.divider()

#界面分块，创建三列
col1, col2, col3, col4, col5 = st.columns([1, 0.05, 1, 0.05, 1])

#第一块内容（综合收入所得）
with col1:
    st.subheader("综合收入所得")
    ms = st.number_input("工资月薪（税前）：",value=2000, min_value=2000)
    allowance = st.number_input("每月津贴：", value=0, min_value=0)
    bonus = st.number_input("年终奖：", value=0, min_value=0)
    ws = ms * 13 + allowance + bonus #工资薪金所得，假设十三薪

    sr = st.number_input("劳务报酬所得:", value=0, min_value=0)
    mr = st.number_input("稿酬所得:", value=0, min_value=0)
    ri = st.number_input("特许使用费所得:", value=0, min_value=0)

    #储蓄计划和养老计划超出部分

with col2:
    st.markdown("<div style='height:840px; margin:0 6px; border-left:1px solid #d3d3d3;'></div>",
                unsafe_allow_html=True)

with col3:
    st.subheader("专项附加扣除")
    babymonth = st.number_input("三岁以下婴幼儿照护月份数:", value=0, min_value=0, max_value=36)
    cemonth = st.number_input("子女教育月份数:", value=0, min_value=0, max_value = 100)

    acemonth = st.number_input("学历继续教育月份数:", value=0, min_value=0, max_value=12,
                               placeholder="如：9月入学填4；6月毕业填6；连续就读填12；最多连续48个月")
    pqce = st.number_input("当年职业资格继续教育证书获得数量:", value=0, min_value=0)

    mimonth = st.number_input("首套住房贷款利息支付月份数:", value=0, min_value=0, max_value=12)
    hrmonth = st.number_input("房租租金支付月份数:", value=0, min_value=0, max_value=12)

    agedmonth = st.number_input("赡养老人月份数:", value=0, min_value=0)
    sibling = st.number_input("亲兄弟姐妹数量:", value=0, min_value=0)

    medical = st.number_input("大病医疗医保范围内自付费用:", value=0, min_value=0)

with col4:
    st.markdown("<div style='height:840px; margin:0 6px; border-left:1px solid #d3d3d3;'></div>",
                unsafe_allow_html=True)

with col5:
    st.subheader("其他扣除")
    tahi = st.number_input("符合国家规定的税优健康险每月减免额度:", value=0, min_value=0, max_value=200)
    tari = st.number_input("符合国家规定的税优养老险每月减免额度:", value=0, min_value=0)
    st.divider()
    st.subheader("捐赠")
    donation = st.number_input("公益性捐赠支出：",value=0, max_value = ws)

st.divider()
st.subheader("年金计划选择")
ec = st.selectbox("员工个人年金缴费比例:", options=["0", "1%", "2%", "3%", "4%"])

sd  = 3000 #员工每月个人缴纳五险一金，等待数据，需修改

st.divider()

if st.button("计算个人所得税优惠"):
    #其他附加扣除，不受选择改变
    sad_amount = sad_cal(cemonth, acemonth, pqce, mimonth, hrmonth, city, agedmonth, sibling, medical,babymonth)

    salary = 10000 #员工上年度平均月工资，等数据，暂时设为固定值
    od_org = od_cal(6, salary, tahi, tari) #不缴年金的其他扣除
    od_new = od_cal(ec, salary, tahi, tari) #缴年金的其他扣除
    ati_org = ati_cal(ws, sr, mr, ri, sd, sad_amount, od_org, donation)
    ati_new = ati_cal(ws, sr, mr, ri, sd, sad_amount, od_new, donation)

    tax_org = tax_cal(ati_org)
    tax_new = tax_cal(ati_new)
    tax_deduction = tax_org - tax_new

    st.write("不缴年金时，全年应纳税所得额为", ati_org,"元；应缴纳个人所得税",tax_org,"元。")
    st.write("选择",ec,"档个人年金缴费比例时，全年应纳税所得额为",ati_new, "元；应缴纳个人所得税", tax_new, "元。")
    st.write("应缴纳个人所得税优惠金额为", tax_deduction)
