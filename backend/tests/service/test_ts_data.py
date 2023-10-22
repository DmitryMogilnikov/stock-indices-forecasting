from backend.src.service import ts_data as td


def test_calc_integral_sum():
    # The case when input data is empty
    assert td.calc_integral_sum(td.pd.DataFrame()).equals(td.pd.DataFrame())

    # Correct evaluating #1
    data = td.pd.DataFrame([{'TRADEDATE': '2023-10-16', 'OPEN': 264, 'CLOSE': 268.15, 'HIGH': 269.2,
             'LOW': 263.51, 'VALUE': 14344201420.1},
            {'TRADEDATE': '2023-10-17', 'OPEN': 268.3, 'CLOSE': 270, 'HIGH': 271.97,
             'LOW': 266.91, 'VALUE': 13825850433.3},
            {'TRADEDATE': '2023-10-18', 'OPEN': 270, 'CLOSE': 267.9,
             'HIGH': 271.19, 'LOW': 266.11, 'VALUE': 10845314693.3},
            {'TRADEDATE': '2023-10-19', 'OPEN': 267.13, 'CLOSE': 268.65,
             'HIGH': 271, 'LOW': 266.28, 'VALUE': 9007682323.1}])
    df = td.pd.DataFrame([{'TRADEDATE': '2023-10-16', 'OPEN': 264, 'CLOSE': 268.15, 'HIGH': 269.2,
             'LOW': 263.51, 'VALUE': 14344201420.1, 'integ_val': 264},
            {'TRADEDATE': '2023-10-17', 'OPEN': 268.3, 'CLOSE': 270, 'HIGH': 271.97,
             'LOW': 266.91, 'VALUE': 13825850433.3, 'integ_val': 532.3},
            {'TRADEDATE': '2023-10-18', 'OPEN': 270, 'CLOSE': 267.9,
             'HIGH': 271.19, 'LOW': 266.11, 'VALUE': 10845314693.3, 'integ_val': 802.3},
            {'TRADEDATE': '2023-10-19', 'OPEN': 267.13, 'CLOSE': 268.65,
             'HIGH': 271, 'LOW': 266.28, 'VALUE': 9007682323.1, 'integ_val': 1069.43}])
    assert td.calc_integral_sum(data).equals(df)

    # The case when input column is wrong
    assert td.calc_integral_sum(data, column='open').equals(td.pd.DataFrame())

    # The case when input column is not exist
    assert td.calc_integral_sum(data, column='sum').equals(td.pd.DataFrame())

    # Correct evaluating #2
    data = td.pd.DataFrame([{'TRADEDATE': '2023-10-16', 'OPEN': 2528.8, 'CLOSE': 2530,
             'HIGH': 2552, 'LOW': 2520.8, 'VALUE': 1714654649.2},
            {'TRADEDATE': '2023-10-17', 'OPEN': 2527, 'CLOSE': 2527.4,
             'HIGH': 2540.6, 'LOW': 2509.6, 'VALUE': 1358663128.6},
            {'TRADEDATE': '2023-10-18', 'OPEN': 2522.2, 'CLOSE': 2527.2,
             'HIGH': 2539, 'LOW': 2511.8, 'VALUE': 1370957296.4},
            {'TRADEDATE': '2023-10-19', 'OPEN': 2520.8, 'CLOSE': 2660.6,
             'HIGH': 2675.4, 'LOW': 2517, 'VALUE': 8599584035}])
    df = td.pd.DataFrame([{'TRADEDATE': '2023-10-16', 'OPEN': 2528.8, 'CLOSE': 2530,
             'HIGH': 2552, 'LOW': 2520.8, 'VALUE': 1714654649.2, 'integ_val': 2528.8},
            {'TRADEDATE': '2023-10-17', 'OPEN': 2527, 'CLOSE': 2527.4,
             'HIGH': 2540.6, 'LOW': 2509.6, 'VALUE': 1358663128.6,'integ_val': 5055.8},
            {'TRADEDATE': '2023-10-18', 'OPEN': 2522.2, 'CLOSE': 2527.2,
             'HIGH': 2539, 'LOW': 2511.8, 'VALUE': 1370957296.4,'integ_val': 7578},
            {'TRADEDATE': '2023-10-19', 'OPEN': 2520.8, 'CLOSE': 2660.6,
             'HIGH': 2675.4, 'LOW': 2517, 'VALUE': 8599584035,'integ_val': 10098.8}])
    assert td.calc_integral_sum(data).equals(df)

    # The case when the calculated column is selected
    data = td.pd.DataFrame([{'TRADEDATE': '2023-10-16', 'OPEN': 2528.8, 'CLOSE': 2530,
             'HIGH': 2552, 'LOW': 2520.8, 'VALUE': 1714654649.2},
            {'TRADEDATE': '2023-10-17', 'OPEN': 2527, 'CLOSE': 2527.4,
             'HIGH': 2540.6, 'LOW': 2509.6, 'VALUE': 1358663128.6},
            {'TRADEDATE': '2023-10-18', 'OPEN': 2522.2, 'CLOSE': 2527.2,
             'HIGH': 2539, 'LOW': 2511.8, 'VALUE': 1370957296.4},
            {'TRADEDATE': '2023-10-19', 'OPEN': 2520.8, 'CLOSE': 2660.6,
             'HIGH': 2675.4, 'LOW': 2517, 'VALUE': 8599584035}])
    df = td.pd.DataFrame([{'TRADEDATE': '2023-10-16', 'OPEN': 2528.8, 'CLOSE': 2530,
                           'HIGH': 2552, 'LOW': 2520.8, 'VALUE': 1714654649.2, 'integ_val': 2530.0},
                          {'TRADEDATE': '2023-10-17', 'OPEN': 2527, 'CLOSE': 2527.4,
                           'HIGH': 2540.6, 'LOW': 2509.6, 'VALUE': 1358663128.6, 'integ_val': 5057.4},
                          {'TRADEDATE': '2023-10-18', 'OPEN': 2522.2, 'CLOSE': 2527.2,
                           'HIGH': 2539, 'LOW': 2511.8, 'VALUE': 1370957296.4, 'integ_val': 7584.6},
                          {'TRADEDATE': '2023-10-19', 'OPEN': 2520.8, 'CLOSE': 2660.6,
                           'HIGH': 2675.4, 'LOW': 2517, 'VALUE': 8599584035, 'integ_val': 10245.2}])
    assert td.calc_integral_sum(data, column='CLOSE').equals(df)

def test_calc_increase_percentage():
    # Case when input data is empty
    assert td.calc_increase_percentage(td.pd.DataFrame()) == []

    # Correct evaluating #1
    df = td.pd.DataFrame([{'TRADEDATE': '2023-10-16', 'OPEN': 3204.81, 'CLOSE': 3234.78,
                        'HIGH': 3235.66, 'LOW': 3202.94, 'VALUE': 65853279415.65, 'integ_val': 3204.81},
                       {'TRADEDATE': '2023-10-17', 'OPEN': 3239.37, 'CLOSE': 3247.15,
                        'HIGH': 3252.55, 'LOW': 3228.11, 'VALUE': 72231692204.35, 'integ_val': 6444.18},
                       {'TRADEDATE': '2023-10-18', 'OPEN': 3252.31, 'CLOSE': 3249.21,
                        'HIGH': 3262.54, 'LOW': 3225.44, 'VALUE': 81213914737.85, 'integ_val': 9696.49},
                       {'TRADEDATE': '2023-10-19', 'OPEN': 3245.26, 'CLOSE': 3255.16,
                        'HIGH': 3260.45, 'LOW': 3232.16, 'VALUE': 57371834112.9, 'integ_val': 12941.75}])
    assert td.calc_increase_percentage(df) == [0.0, 101.08, 50.47, 33.47]

    # Correct evaluating #2
    df = td.pd.DataFrame([{'TRADEDATE': '2023-10-16', 'OPEN': 5919.95, 'CLOSE': 5982.07,
                        'HIGH': 5989.39, 'LOW': 5917.99, 'VALUE': 40920835468.85, 'integ_val': 5919.95},
                       {'TRADEDATE': '2023-10-17', 'OPEN': 5989.32, 'CLOSE': 6017.67,
                        'HIGH': 6025.96, 'LOW': 5965.53, 'VALUE': 39914248155.45, 'integ_val': 11909.27},
                       {'TRADEDATE': '2023-10-18', 'OPEN': 5998.21, 'CLOSE': 6001.89,
                        'HIGH': 6024.95, 'LOW': 5957.7, 'VALUE': 48277844340.95, 'integ_val': 17907.48},
                       {'TRADEDATE': '2023-10-19', 'OPEN': 5998.72, 'CLOSE': 6028.53,
                        'HIGH': 6040.83, 'LOW': 5980.62, 'VALUE': 36195634128.45, 'integ_val': 23906.2}])
    assert td.calc_increase_percentage(df) == [0.0, 101.17, 50.37, 33.5]