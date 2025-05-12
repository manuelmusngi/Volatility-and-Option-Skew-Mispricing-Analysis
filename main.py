from src.fetch_data import fetch_historical_data, fetch_option_chain
from src.bs_model import black_scholes
from src.garch_model import garch_volatility
from src.surface_builder import build_volatility_surface
from src.plot_surface import plot_volatility_surface

def main():
    # Fetch data
    ticker = '^SPX'
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    data = fetch_historical_data(ticker, start_date, end_date)

    # Fetch options chain
    expiration_date = '2023-06-16'
    calls, puts = fetch_option_chain(ticker, expiration_date)

    # Calculate Black-Scholes prices
    S = data['Close'].iloc[-1]
    K = calls['strike'].values
    T = 0.5  # 6 months in years
    r = 0.05  # Risk-free rate
    sigma = 0.2
    bs_prices = [black_scholes(S, k, T, r, sigma, 'call') for k in K]

    # Build volatility surface
    strikes = calls['strike'].values
    expirations = [T] * len(strikes)
    volatilities = sigma * np.ones(len(strikes))  # Example data
    grid_x, grid_y, surface = build_volatility_surface(strikes, expirations, volatilities)

    # Plot surface
    plot_volatility_surface(grid_x, grid_y, surface)

if __name__ == '__main__':
    main()
