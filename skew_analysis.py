import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime
from scipy.stats import norm
from arch import arch_model
import plotly.graph_objs as go
import warnings

warnings.filterwarnings("ignore")

# Black-Scholes Functions 
def bs_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)

def bs_put(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def implied_vol(price, S, K, T, r, option_type="call"):
    sigma = 0.2
    for _ in range(100):
        if option_type == "call":
            price_est = bs_call(S, K, T, r, sigma)
        else:
            price_est = bs_put(S, K, T, r, sigma)
        vega = S * norm.pdf((np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))) * np.sqrt(T)
        diff = price_est - price
        if abs(diff) < 1e-5:
            return sigma
        sigma -= diff / (vega + 1e-10)
    return np.nan

# GARCH Estimation 
hist = yf.download("^SPX", start="2023-01-01", end="2024-01-01")
returns = 100 * hist["Adj Close"].pct_change().dropna()
model = arch_model(returns, vol='Garch', p=1, q=1)
res = model.fit(disp='off')
garch_vol = np.sqrt(res.forecast(horizon=1).variance.values[-1][0])
print(f"GARCH Forecast Volatility: {garch_vol:.2f}%")

# Implied Vol Surface + Skew
ticker = yf.Ticker("^SPX")
spot = hist["Adj Close"][-1]
rate = 0.045  # Fixed for now

iv_surface = []
skew_data = []

for expiry in ticker.options[:5]:  # First 5 expirations
    date_obj = datetime.strptime(expiry, "%Y-%m-%d")
    T = (date_obj - datetime.today()).days / 365
    if T <= 0:
        continue

    chain = ticker.option_chain(expiry)
    calls = chain.calls
    puts = chain.puts

    for _, row in calls.iterrows():
        K = row['strike']
        if row['lastPrice'] > 0 and abs(K - spot) < spot * 0.2:
            iv = implied_vol(row['lastPrice'], spot, K, T, rate, "call")
            if iv:
                iv_surface.append((K, T*365, iv * 100))

    # Skew: IV_put - IV_call at same strike
    for _, row in puts.iterrows():
        K = row['strike']
        put_price = row['lastPrice']
        matching_call = calls[calls['strike'] == K]
        if put_price > 0 and not matching_call.empty:
            call_price = matching_call['lastPrice'].values[0]
            iv_put = implied_vol(put_price, spot, K, T, rate, "put")
            iv_call = implied_vol(call_price, spot, K, T, rate, "call")
            if iv_put and iv_call:
                skew = iv_put - iv_call
                skew_data.append((K, T*365, skew * 100))

# Create DataFrames 
iv_df = pd.DataFrame(iv_surface, columns=["Strike", "DTE", "IV"])
skew_df = pd.DataFrame(skew_data, columns=["Strike", "DTE", "Put-Call Skew"])

# Plot 3D Implied Vol Surface 
fig = go.Figure(data=[go.Surface(
    z=iv_df.pivot_table(index="Strike", columns="DTE", values="IV").values,
    x=sorted(iv_df["Strike"].unique()),
    y=sorted(iv_df["DTE"].unique()),
    colorscale='Viridis'
)])
fig.update_layout(title="Implied Volatility Surface (Call Options)",
                  scene=dict(
                      xaxis_title="Strike",
                      yaxis_title="Days to Expiration (DTE)",
                      zaxis_title="IV (%)"))
fig.show()

# Plot Skew Surface 
fig2 = go.Figure(data=[go.Surface(
    z=skew_df.pivot_table(index="Strike", columns="DTE", values="Put-Call Skew").values,
    x=sorted(skew_df["Strike"].unique()),
    y=sorted(skew_df["DTE"].unique()),
    colorscale='RdBu',
    showscale=True
)])
fig2.update_layout(title="Put-Call IV Skew Surface",
                   scene=dict(
                       xaxis_title="Strike",
                       yaxis_title="Days to Expiration",
                       zaxis_title="Put - Call IV (%)"))
fig2.show()
