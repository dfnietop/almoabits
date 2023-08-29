from app.almoabits.almoabits_country.country_code import ConcreteCountryCode


class Country:

    def __init__(self):
        self.handler = self.__get_country_code_handler()

    def __get_country_code_handler(self):
        try:
            return ConcreteCountryCode()
        except Exception as e:
            print('Error on __get_country_code_handler method')

    def get_country_code(self, string) -> str:
        try:
            return self.handler.get_country(string)
        except Exception as e:
            print('Error on __get_country_code method')

    def get_currency_code(self, string) -> str:
        try:
            return self.handler.get_currency_code(string)
        except Exception as e:
            print('Error on __get_country_code method')

    def get_country_by_currency_code(self, currency_code, country_code) -> str:
        try:
            return self.handler.get_country_by_currency_code(currency_code, country_code)
        except Exception as e:
            print('Error on __get_country_code method')
