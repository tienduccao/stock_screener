import numpy as np
from unibit_api import financial_report


UNKNOWN_VALUE = np.nan


def string_to_number(s):
    try:
        return float(s.replace(',', ''))
    except:
        return UNKNOWN_VALUE


def dict_reports(financial_report, interval='annual'):
    def _to_float(dictionary):
        "Convert all values of a dictionary to float data type"
        return {key: string_to_number(value) \
                for key, value in dictionary.items()}

    reports = list(financial_report['result_data'].values())[0]
    # TODO extract month and year from reportDate is interval is quarterly
    return {report['reportDate'].split('/')[-1]: _to_float(report) for \
            report in reports}


def compute_ratios(ticker, ratio_function, select_periods, interval='annual'):
    ic = financial_report(ticker, \
                          'income_statement', \
                          interval)
    bs = financial_report(ticker, \
                          'balance_sheet', \
                          interval)
    cf = financial_report(ticker, \
                          'cash_flow', \
                          interval)

    dict_ic = dict_reports(ic, interval)
    dict_bs = dict_reports(bs, interval)
    dict_cf = dict_reports(cf, interval)

    for period in select_periods(dict_ic, dict_bs, dict_cf):
        try:
            ratio = ratio_function(
                dict_ic[period],
                dict_bs[period],
                dict_cf[period]
            )
        except:
            ratio = UNKNOWN_VALUE
        yield (int(period), ratio)


def sorted_periods(periods):
    sorted_periods = sorted([int(p) for p in periods])
    return [str(p) for p in sorted_periods]


def shared_periods(dict_report_a, dict_report_b):
    periods_a = set(dict_report_a.keys())
    periods_b = set(dict_report_b.keys())
    periods = periods_a.intersection(periods_b)
    # TODO sort for quarterly interval
    return sorted_periods(periods)


def dividend_to_net_income(ticker, interval='annual'):
    def _ratio(dict_ic, dict_bs, dict_cf):
        return abs(dict_cf['dividendsPaid'] / dict_ic['netIncome'])

    return compute_ratios(ticker, _ratio, \
        lambda ic, bs, cf: shared_periods(ic, cf),
        interval)


def current_ratio(ticker, interval='annual'):
    return compute_ratios(ticker, \
        lambda ic, bs, cf: bs['totalCurrentAsset'] / bs['totalCurrentLiability'], \
        lambda ic, bs, cf: sorted_periods(bs.keys()),
        interval)


def quick_ratio(ticker, interval='annual'):
    return compute_ratios(ticker, \
        lambda ic, bs, cf: ((bs['totalCurrentAsset'] - bs['inventory'])
                            / bs['totalCurrentLiability']), \
        lambda ic, bs, cf: sorted_periods(bs.keys()),
        interval)


def debt_to_equity(ticker, interval='annual'):
    return compute_ratios(ticker, \
        lambda ic, bs, cf: bs['totalLiabilities'] / bs['totalStockholderEquity'], \
        lambda ic, bs, cf: sorted_periods(bs.keys()),
        interval)


def gross_profit_margin(ticker, interval='annual'):
    return compute_ratios(ticker, \
        lambda ic, bs, cf: ic['grossProfit'] / ic['totalRevenue'], \
        lambda ic, bs, cf: sorted_periods(ic.keys()),
        interval)


def net_profit_margin(ticker, interval='annual'):
    def _ratio(ic, dict_bs, dict_cf):
        return ((ic['earningsBeforeInterestTaxes'] -
                ic['interestExpense'] - ic['incomeTaxExpense']) /
                ic['totalRevenue'])

    return compute_ratios(ticker, _ratio, \
        lambda ic, bs, cf: sorted_periods(ic.keys()),
        interval)


def operating_profit_margin(ticker, interval='annual'):
    return compute_ratios(ticker, \
        lambda ic, bs, cf: ic['operatingIncome'] / ic['totalRevenue'], \
        lambda ic, bs, cf: sorted_periods(ic.keys()),
        interval)


def interest_coverage_ratio(ticker, interval='annual'):
    return compute_ratios(ticker, \
        lambda ic, bs, cf: ic['operatingIncome'] / -ic['interestExpense'], \
        lambda ic, bs, cf: sorted_periods(ic.keys()),
        interval)


def roe(ticker, interval='annual'):
    def _ratio(ic, bs, dict_cf):
        revenue = ic['totalRevenue']
        equity = bs['totalStockholderEquity']
        # Asset Turnover = Revenue ÷ Assets
        # Equity Multiplier = Assets ÷ Shareholders’ Equity
        _net_profit_margin = ((ic['earningsBeforeInterestTaxes'] -
                ic['interestExpense'] - ic['incomeTaxExpense']) /
                ic['totalRevenue'])
        return _net_profit_margin * revenue / equity

    return compute_ratios(ticker, _ratio, \
        lambda ic, bs, cf: shared_periods(ic, bs),
        interval)


def cash_flow_ratio(ticker, interval='annual'):
    def _ratio(ic, bs, cf):
        return cf['totalCashFlowOperating'] / bs['totalCurrentLiability']

    return compute_ratios(ticker, _ratio, \
        lambda ic, bs, cf: shared_periods(cf, bs),
        interval)
