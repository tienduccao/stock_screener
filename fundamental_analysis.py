from unibit_api import financial_report


def string_to_number(s):
    return float(s.replace(',', ''))


def dict_reports(financial_report, interval='annual'):
    reports = list(financial_report['result_data'].values())[0]
    # TODO extract month and year from reportDate is interval is quarterly
    return {report['reportDate'].split('/')[-1]: report for \
            report in reports}


def compute_ratios(ticker, ratio_function, interval='annual'):
    ic = financial_report(ticker, \
                          'income_statement', \
                          interval)
    bs = financial_report(ticker, \
                          'balance_sheet', \
                          interval)
    cf = financial_report(ticker, \
                          'cash_flow', \
                          interval)

    return ratio_function(dict_reports(ic, interval), \
                          dict_reports(bs, interval), \
                          dict_reports(cf, interval))


def comparable_periods(dict_report_a, dict_report_b):
    periods_a = set(dict_report_a.keys())
    periods_b = set(dict_report_b.keys())
    periods = periods_a.intersection(periods_b)
    # TODO sort for quarterly interval
    sorted_periods = sorted([int(p) for p in periods])
    return [str(p) for p in sorted_periods]


def dividend_to_net_income(ticker, interval='annual'):
    def _ratio(dict_ic, dict_bs, dict_cf):
        periods = comparable_periods(dict_ic, dict_cf)
        for period in periods:
            try:
                ratio = abs(string_to_number(dict_cf[period]['dividendsPaid']) / \
                           string_to_number(dict_ic[period]['netIncome']))
            except:
                ratio = '-'
            yield {period: ratio}

    return compute_ratios(ticker, _ratio, interval)
