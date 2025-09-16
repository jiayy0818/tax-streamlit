def sd_cal(df, entity, city, salary):
    import pandas as pd

    # 筛选出符合条件的行
    result = df[(df["RGB"] == entity) & (df["缴纳地"] == city)]

    if result.empty:
        return 0  # 如果没有匹配行，返回0 或者 raise Exception

    # 只取第一行，转成 Series
    row = result.iloc[0]

    def percent_to_float(s):
        if isinstance(s, str):
            return float(s.strip().replace('%', '')) / 100
    
    # 各类比例
    shebao_percent = percent_to_float(row['个人-养老']) + percent_to_float(row['个人-失业'])
    yiliao_percent = percent_to_float(row['个人-医疗'])
    gjj_percent = percent_to_float(row['个人-公积金'])
    # 大病保险金额（可能不存在）
    dabing_amount = float(row.get("个人-大病"))
    dabing_amount = 0 if pd.isna(dabing_amount) else dabing_amount

    # 上下限
    shebao_upper = float(row['社保-上限'])
    shebao_lower = float(row['社保-下限'])
    yiliao_upper = float(row['医疗-上限'])
    yiliao_lower = float(row['医疗-下限'])
    gjj_upper = float(row['公积金-上限'])
    gjj_lower = float(row['公积金-下限'])

    # 基数计算（保证在上下限之间）
    shebao_base = min(max(salary, shebao_lower), shebao_upper)
    yiliao_base = min(max(salary, yiliao_lower), yiliao_upper)
    gjj_base = min(max(salary, gjj_lower), gjj_upper)

    # 计算社保金额
    sd_amount = shebao_base * shebao_percent + yiliao_base * yiliao_percent + dabing_amount + gjj_base * gjj_percent

    return sd_amount
