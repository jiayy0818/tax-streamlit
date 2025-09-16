def od_cal(df, ec, salary, entity, city, tahi, tari):
    result = df[(df["RGB"] == entity) & (df["缴纳地"] == city)]
    row = result.iloc[0]
    upper_limit = row['社保-上限']

    if ec == '0':
        ec_amount = min(1, upper_limit)
    elif ec == '1%':
        ec_amount = min(0.01 * salary * 12, upper_limit * 12)
    elif ec == '2%':
        ec_amount = min(0.02 * salary * 12, upper_limit * 12)
    elif ec == '3%':
        ec_amount = min(0.03 * salary * 12,upper_limit * 12)
    elif ec == '4%':
        ec_amount = min(0.04 * salary * 12, upper_limit * 12)
    else:
        ec_amount = 0

    od_amount = ec_amount + min (tahi,200) * 12 + tari * 12
    return od_amount, ec_amount