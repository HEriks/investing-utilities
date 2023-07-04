import yfinance as yf
import pandas as pd


def get_historical_difference(df : pd.DataFrame, ticker_a : str, ticker_b : str):


    history = df[[ticker_a, ticker_b]].copy()
    history['ab_diff'] = history[ticker_a] - history[ticker_b]
    history['ab_quota'] = history[ticker_a] / history[ticker_b]
    history['ab_quota_mean'] = history['ab_quota'].mean()
    history['ab_quota_stdev'] = history['ab_quota'].std()
    results = {"date" : history.last_valid_index(),
               "ab_diff" : history['ab_diff'].iloc[-1],
               "ab_quota" : history['ab_quota'].iloc[-1],
               "ab_quota_mean" : history['ab_quota_mean'].iloc[-1],
               "ab_quota_stdev" : history['ab_quota_stdev'].iloc[-1]}
    return results

def pretty_print_results(res : dict, company : str, time_period : str):
    stdev = "less" if (1-res['ab_quota_mean']) < res['ab_quota_stdev'] else "more"
    
    print(f"Stats for {company} in time period {time_period}:" )
    print(f"Data from {res['date']}")
    print(f"A-B price difference: {res['ab_diff'].round(3)}")
    print(f"A/B price quota: {res['ab_quota'].round(3)}")
    print(f"Historical price quota: {res['ab_quota_mean'].round(3)}")
    # print(f"Curently {stdev} than one stdev from normal quota")

def do_stuff(data : yf.Tickers, time_period : str, company : str, ticker_a : str, ticker_b : str):
    prefix_a = ticker_a.split('-')[0]
    prefix_b = ticker_b.split('-')[0]
    assert(prefix_a == prefix_b) # Assert both tickers are same company
    assert(time_period in ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo", "max"])

    tickers_close = data.history(time_period)['Close']
    res_company = get_historical_difference(tickers_close, ticker_a, ticker_b)
    pretty_print_results(res_company, company, time_period)

def main():
    tickers = yf.Tickers("INVE-A.ST INVE-B.ST SVOL-A.ST SVOL-B.ST INDU-A.ST INDU-C.ST")

    do_stuff(tickers, "3mo", "Investor", "INVE-A.ST", "INVE-B.ST")
    do_stuff(tickers, "max", "Svolder", "SVOL-A.ST", "SVOL-B.ST")
    do_stuff(tickers, "max", "Industrivärden", "INDU-A.ST", "INDU-C.ST")

if __name__ == "__main__":
    main()