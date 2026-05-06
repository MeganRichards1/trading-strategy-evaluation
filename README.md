# Project: Algorithmic Trading
This project focuses on implementing and evaluating different trading strategies using Python. It utilizes simulated stock market data to test how various algorithms perform under different market conditions, modeled after research into financial time series.

## Project Structure

The project is organized as a Python package named `trading`. This package is structured into several modules, each responsible for a specific part of the algorithmic trading pipeline:

- `data.py`: Handles the generation and management of simulated stock price data.

- `process.py`: Contains utility functions for data processing, such as creating portfolios.

- `indicators.py`: Includes technical indicators used to analyze price movements.

- `strategy.py`: Defines the trading logic and decision-making algorithms.

- `performance.py`: Tools for evaluating the success and risk of the implemented strategies.

## Data Simulation Model

The core of the simulation relies on the **Random Walk Hypothesis**, with additional layers to simulate real-world market volatility and external events.

### 1. Price Evolution

The share price $p_t$ for a company on day t is calculated based on the previous day's price plus a random increment:

$$p_t = p_{t-1} + \Delta p_t$$
​	
where $\Delta p_t$ follows a normal distribution $N(0,\sigma^2)$, and σ represents the stock's volatility.

### 2. Company Closure

If a share price reaches zero or becomes negative, the company is considered closed. All subsequent prices for that company in the simulation are set to NaN.

### 3. Impact of "Important News"

To simulate market shocks (e.g., natural disasters or product launches), the model introduces random "drift" events:

 - **Probability**: Every day, there is a 1% chance of a news event occurring for a specific stock.

 - **Drift Magnitude**: The impact $d$ is proportional to the stock's volatility: $d = m \sigma$, with $m \sim N(0, 2^2)$ 

 - **Duration**: An event lasts for a random duration $t$. When an event occurs, its impact lasts for anywhere between 3 days and 2 weeks (Uniform distribution) -- i.e. the total duration is $t \sim U(3, 14)$.

 - **Cumulative Effect**: Multiple overlapping events sum their drifts: $$p_t = p_{t-1} + \Delta p_t + \sum_i d_i$$.
​
