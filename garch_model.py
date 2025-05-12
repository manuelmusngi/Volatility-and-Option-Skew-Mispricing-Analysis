from arch import arch_model

def garch_volatility(data, p=1, q=1):
    """Fit a GARCH model to historical data and forecast volatility."""
    model = arch_model(data, vol='Garch', p=p, q=q)
    fitted_model = model.fit(disp="off")
    forecast = fitted_model.forecast(horizon=1)
    return forecast.variance.values[-1, :]
