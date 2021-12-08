# sharpe ratio formula
import numpy as np
import pandas as pd
df_price = pd.read_csv(
    '/home/krishna/Music/stock_market/stock_analysis/todayshareprice.csv')
df_price.rename(columns={'Max Price': 'high',
                         'Min Price': 'low',
                         'Closing Price': 'close',
                'Amount': 'volume',
                          'Traded Shares': 'traded_shares'}, inplace=True)


class STATSFINDER:
    def __init__(self, price_df, risk_free__yr_return=8):
        """
        args:
        price_df : the pandas dataframe constaining price of stock over the period
        """
        self.price_df = price_df
        self.risk_free__yr_return = risk_free__yr_return

    def real_returns_calculator(self, periods=1):
        risk_free__yr_return = self.risk_free__yr_return
        daily_return = risk_free__yr_return**(1/365)
        req_return = daily_return**periods
        return req_return

    def returns_calculator(self, periods=1, real=True):
        """
        args
        periods = no of periods that we want to calculate returns for
        """
        if real:
            risk_free_return = self.real_returns_calculator(periods=periods)
        else:
            risk_free_return = 0
        returns = self.price_df[['close', 'high', 'low']].pct_change(
            periods=periods)-risk_free_return-1
        returns.replace([np.inf, -np.inf], np.nan, inplace=True)
        returns.fillna(returns.mean(), inplace=True)
        return returns

    def mean_return_calculator(self, periods=1, real=True):
        df_returns = self.returns_calculator(periods=1, real=True)
        return df_returns.mean().to_dict()

    def std_return_calculator(self,periods=1, real=True):
        df_returns = self.returns_calculator(periods=1, real=True)
        return df_returns.std().to_dict()

class MathematicalFormulae:
    def sharpe_ratio(self,mean_of_risk_free_return,std_of_risk_free_return):
        # information ratio or sharpe ratio
        sharpe_ratio = mean_of_risk_free_return/std_of_risk_free_return
        return sharpe_ratio


if __name__ == '__main__':
    stats_values = STATSFINDER(df_price)
    std_of_return = stats_values.std_return_calculator(periods=30).get('close')
    mean_of_return = stats_values.mean_return_calculator(periods=30).get('close')
    sharpe_ratio = MathematicalFormulae().sharpe_ratio(mean_of_return,std_of_return)
    print(sharpe_ratio)
