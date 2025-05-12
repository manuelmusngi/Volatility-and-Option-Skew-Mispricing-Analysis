#### volatility-and-Option-Skew-Mispricings
Volatility and Option Skew Mispricings refer to situations where options are priced in a way that doesn't align with the underlying asset's actual or expected volatility, especially when comparing across different strikes or expirations. These mispricings can provide trading opportunities for sophisticated traders.

#### Project Structure
vol_skew_analysis/\
│
├── data/                        
│\
├── notebooks/                  
│\
├── src/                       
│   ├── [__init__.py](https://github.com/manuelmusngi/Volatility-and-Option-Skew-Mispricing-Analysis/blob/main/src/init.py)\
│   ├── [fetch_data.py](https://github.com/manuelmusngi/Volatility-and-Option-Skew-Mispricing-Analysis/blob/main/src/fetch_data.py)            
│   ├── [bs_model.py](https://github.com/manuelmusngi/Volatility-and-Option-Skew-Mispricing-Analysis/blob/main/src/bs_model.py)              
│   ├── garch_model.py          
│   ├── surface_builder.py       
│   ├── plot_surface.py          
│\
├── [main.py](https://github.com/manuelmusngi/Volatility-and-Option-Skew-Mispricing-Analysis/blob/main/main.py)                     
│\
├── [requirements.txt](https://github.com/manuelmusngi/Volatility-and-Option-Skew-Mispricing-Analysis/blob/main/requirements.txt)            
│\
└── README.md                   
