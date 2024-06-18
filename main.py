import numpy as np

class OptionPricing:
    def __init__(self, StockPrice, StrikePrice, Maturity, riskFree, volatility, iterations):
        self.StockPrice = StockPrice
        self.StrikePrice = StrikePrice
        self.Maturity = Maturity
        self.riskFree = riskFree
        self.volatility = volatility
        self.iterations = iterations

    def call_option_simulation(self):
        # we'll create two columns: first with 0s, the second will store the payoffs
        # we need the first column of 0s: payoff function is max(0, S-E) for call option
        options_data = np.zeros([self.iterations, 2])

        # Weiner Process / Brownian Motion to simulate the random values of the stock price
        rand = np.random.normal(0, 1, [1, self.iterations])

        # Equation to find stock price at maturity
        stock_price = self.StockPrice * np.exp(self.Maturity * (self.riskFree - 0.5 * self.volatility **2)
                                               + self.volatility * np.sqrt(self.Maturity) * rand)
        # we need S-E because we have to find the max where StockPrice - Expiration
        options_data[:, 1] = stock_price - self.StockPrice

        # find the average of the monte carlo sim
        # max() returns the max(0, S-E) according to the formula
        average = np.sum(np.amax(options_data, axis=1)) / float(self.iterations)

        # Use discount factor to find present cash flow
        return np.exp(-1.0*self.riskFree * self.volatility)* average

        # print(options_data)

    def put_option_simulation(self):
        # we'll create two columns: first with 0s, the second will store the payoffs
        # we need the first column of 0s: payoff function is max(0, S-E) for call option
        options_data = np.zeros([self.iterations, 2])

        # Weiner Process / Brownian Motion to simulate the random values of the stock price
        rand = np.random.normal(0, 1, [1, self.iterations])

        # Equation to find stock price at maturity
        stock_price = self.StockPrice * np.exp(self.Maturity * (self.riskFree - 0.5 * self.volatility **2)
                                               + self.volatility * np.sqrt(self.Maturity) * rand)
        # we need S-E because we have to find the max where StockPrice - Expiration
        options_data[:, 1] = self.StockPrice - stock_price

        # find the average of the monte carlo sim
        # max() returns the max(0, S-E) according to the formula
        average = np.sum(np.amax(options_data, axis=1)) / float(self.iterations)

        # Use discount factor to find present cash flow
        return np.exp(-1.0*self.riskFree * self.volatility)* average


def pullback_price(current_price, open_price):
    if (current_price / open_price) - 1 >= 0.05:
        print("Pullback, open long position")
        print(round((current_price / open_price)-1,4))
    else:
        print("No pullback")
        print(round((current_price / open_price)-1,4))



if __name__ == '__main__':
    call_prices = []
    put_prices = []
    option = OptionPricing(245.10, 250, 0.083, 0.042, 0.696, 1000000)
    for i in range(0,5):
        call_option_price = option.call_option_simulation()
        put_option_price = option.put_option_simulation()
        call_prices.append(call_option_price)
        put_prices.append(put_option_price)
        i += 1
    call_final_avg = sum(call_prices) / i
    put_final_avg = sum(put_prices) / i
    print(f"Call Option price: ", round(call_final_avg, 2))
    print(f"Call Price in dollars: ", round(call_final_avg*100, 2))
    print(f"Put option price: ", round(put_final_avg, 2))
    print(f"Put Price in dollars: ", round(put_final_avg*100, 2))

    pullback_price(18.59, 19)


