import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

class OptionsBot(webdriver.Chrome):
    '''Scrapes stock options data from Yahoo Finance'''
    def __init__(self, options):
        super().__init__(options=options)
        self.implicitly_wait(60)

    def fetch_stock(self, ticker):
        '''Loads the individual stock webpage page based on the given ticker'''
        stock_search = self.find_element(By.ID, 'yfin-usr-qry')
        search_btn = self.find_element(By.ID, 'header-desktop-search-button')

        stock_search.send_keys(ticker)
        search_btn.click()

    def load_options_page(self):
        '''Navigates to the inital options webpage for the given stock'''
        options_btn = self.find_element(By.XPATH, '//a/descendant::span[contains(text(), "Options")]') #TODO
        options_btn.click()

    def get_expiry_dates(self):
        '''Gets the possible expiry dates for every option associated with a stock
        Returns:
            List<str> of dates in Month(text), DD, YYYY format 
        '''
        try:
            #If we can't find this, it means that there's no option data for this stock, so return None and handle the exception in the UI
            date_select = Select(self.find_element(By.CSS_SELECTOR, 'select[class="Fz(s) H(25px) Bd Bdc($seperatorColor)"]'))
            dates = [date.text for date in date_select.options] 
        except:
            return None
        return dates

    def load_options_on_date(self, date):
        '''Navigates to the specific options contracts based on the given expiry date.'''
        date_select = Select(self.find_element(By.CSS_SELECTOR, 'select[class="Fz(s) H(25px) Bd Bdc($seperatorColor)"]'))
        date_select.select_by_visible_text(date)
    
    def get_options_df(self):
        '''Returns a dataframe of all call options for a ticker on a particular expiry date.'''
        options_table = self.find_element(By.CSS_SELECTOR, 'table[class="calls W(100%) Pos(r) Bd(0) Pt(0) list-options"]')
        df_options = pd.read_html(options_table.get_attribute('outerHTML'))[0]
        df_options = df_options.filter(items=['Contract Name', 'Strike', 'Implied Volatility'])

        return df_options
    
    



class BotManager():
    '''Directs bot instances and groups navigation into coherent chunks.'''
    def __init__(self):
        options = webdriver.ChromeOptions() 
        #options.add_argument('--headless')
        self.options = options
        self.base_url = r'https://finance.yahoo.com/'
        
        self.bot = OptionsBot(options) #FIXME- violates Dependency inversion but idrc lowkey (hard to integrade)

    def load_bot_instance(self):
        self.bot.get(r'https://finance.yahoo.com/')

    def get_dates(self, ticker):
        self.bot.fetch_stock(ticker) #TODO: get ticker from UI
        self.bot.load_options_page()
        date_list = self.bot.get_expiry_dates()
        return date_list

    def get_options_df(self, date):
        self.bot.load_options_on_date(date)
        df = self.bot.get_options_df()
        return df

    def options_df_to_list(self, df: pd.DataFrame):
        '''Takes in a DataFrame of the selected options and returns a list of lists<str> each
        of the form ['strike-price', 'implied-volatility']'''
        options_strings_list = df[['Strike', 'Implied Volatility']].iloc[df.index].to_numpy().tolist()

        options = []
        for option in options_strings_list:
            strike = option[0]
            iv = float(option[1][:len(option[1])-1]) #Dont include the percentage sign

            options.append([strike, iv])

        return options
    
    def get_options_strings(self, strike_and_iv):

        options_strings = []
        for i in range(len(strike_and_iv)):

            strike = strike_and_iv[i][0]
            iv = strike_and_iv[i][1]
            options_strings.append(f'Strike: {strike} Implied Volatility:{iv}')
        return options_strings