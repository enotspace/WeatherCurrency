from currency_converter import CurrencyConverter
c = CurrencyConverter()
money=input('Money')
currentc=c.convert(money, 'EUR', 'USD')
print(currentc)