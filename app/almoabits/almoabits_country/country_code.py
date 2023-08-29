import pycountry as country


class ConcreteCountryCode:

    def __init__(self):
        print('inicio ConcreteCountryCode')

    def get_country(self, string):
        try:
            string = string.capitalize()
            code = country.countries.get(name=string)
            return code.alpha_2
        except Exception as e:
            print(f'Error get_country: {string}')

    def get_currency_code(self, alpha2):
        try:
            country_code = country.currencies.get(numeric=alpha2)
            return country_code.alpha_3
        except Exception as e:
            print(f'Error get_currency_code: {alpha2}', e)

    def get_country_by_currency_code(self, currency_code, country_code):
        try:
            currency = country.currencies.get(alpha_3=currency_code)
            country_ = country.countries.lookup(currency.alpha_3[:-1]).alpha_2
            if country is None:
                return country_code
            else:
                return country_
        except Exception as e:
            print(f'Error get_currency_code: {currency_code}')
