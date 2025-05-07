import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from arch import arch_model
import plotly.graph_objects as go

# 1. Download historical price data
symbol = "^SPX"  # S&P 500 Index
data = yf.download(symbol, start="2022-01-01", end="2024-01-01")
returns = 100 * data['Adj Close'].pct_change().dropna()

# 2. Estimate Realized Volatility via GARCH(1,1)
garch_model = arch_model(returns, vol='Garch', p=1, q=1)
garch_fit = garch_model.fit(disp="off")
forecast = garch_fit.forecast(horizon=1)
garch_vol = np.sqrt(forecast.variance.values[-1][0])

print(f"GARCH-forecasted volatility: {garch_vol:.2f}%")

# 3. Simulated Option Implied Volatility Surface (for illustration only)
# In real cases, pull from a data provider like ORATS, IVolatility, or OptionMetrics
strikes = np.arange(3800, 4300, 50)
days = np.array([7, 14, 30, 60, 90])
iv_surface = np.array([
    [0.22, 0.21, 0.19, 0.18, 0.17],
    [0.20, 0.19, 0.18, 0.17, 0.16],
    [0.18, 0.17, 0.16, 0.15, 0.15],
    [0.17, 0.16, 0.15, 0.145, 0.14],
    [0.16, 0.15, 0.145, 0.14, 0.135],
    [0.155, 0.145, 0.14, 0.135, 0.13],
    [0.15, 0.14, 0.135, 0.13, 0.125],
    [0.145, 0.135, 0.13, 0.125, 0.12],
    [0.14, 0.13, 0.125, 0.12, 0.115],
    [0.135, 0.125, 0.12, 0.115, 0.11]
])

# 4. Plot Volatility Surface
fig = go.Figure(data=[go.Surface(z=iv_surface.T, x=strikes, y=days)])
fig.update_layout(
    title='Implied Volatility Surface',
    scene=dict(
        xaxis_title='Strike',
        yaxis_title='Days to Expiry',
        zaxis_title='Implied Volatility'
    )
)
fig.show()

# 5. Find Mispricing: Compare GARCH vol to IV at ATM 30-day
atm_index = np.argmin(np.abs(strikes - data['Adj Close'][-1]))
iv_atm_30d = iv_surface[atm_index][2] * 100  # 30-day column

print(f"Implied Volatility (ATM, 30D): {iv_atm_30d:.2f}%")

# Compare IV to GARCH forecast
if iv_atm_30d > garch_vol + 2:
    print("Options are potentially OVERPRICED → consider premium selling strategies.")
elif iv_atm_30d < garch_vol - 2:
    print("Options are potentially UNDERPRICED → consider premium buying strategies.")
else:
    print("Options are fairly priced based on current volatility expectations.")
