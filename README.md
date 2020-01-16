In order to make stock investment decision, it's very helpful if we could automate the process
of selecting stocks based on their past financial performance (e.g., profit margin ratio, 
debt-to-equity ratio, etc.).
All of these ratios could be computed quickly from financial reports: the income statement, the 
balance sheet, and the cash flow statement.
Companies usually release these reports under PDF format which aren't quite suitable for an automatic
data extraction task.

This project aims to perform the above-mentioned task by leveraging the free [UniBit
API](https://unibit.ai/docs/V2.0/introduction) (currently as of January 2020 they allow a free user to consume 500K
[credits](https://unibit.ai/docs/V2.0/credit_system)).
You need to register an UniBit account and supply your access key in the file `api_key.config`.
The following features are implemented:
+ Given a stock symbol (e.g., GOOGL), retrieve its all financial reports and compute financial ratios.
Some implemented ratios are Current ratio, Quick ratio, Debt to equity, Gross profit margin, Net profit margin,
Operating profit margin, Interest coverage ratio, ROE, Cash flow ratio.
It's very easy to implement your own custom metric.
Please take a detailed look in `fundamental_analysis.py`.
+ [Plot financial ratio of a group of stocks](StockScreener.ipynb) in order to compare their performance visually.
+ Filter stocks from an exchange by their sector/industry. [This notebook](CompanyFilter.ipynb) gives an example of filtering all stocks in
real estate industry from EuroNext Paris exchange.
