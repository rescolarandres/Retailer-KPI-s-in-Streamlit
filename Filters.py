import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import numpy as np

class Filters():
    def __init__(self, ):
        self.sidebar = st.sidebar
        self.sidebar.image("static\img\hm_logo.png", width=100)
        self.sidebar.write('Filters')
        self.checkbox = st.sidebar.checkbox('Group Ages by Decades',value=True)

        self.df_transactions = self.load_data('https://api-dot-nth-canyon-378812.oa.r.appspot.com', '/api/v1/transactions',headers={"Authorization": "Bearer xxxxxx"})
        self.df_articles = self.load_data('https://api-dot-nth-canyon-378812.oa.r.appspot.com', '/api/v1/articles',headers={"Authorization": "Bearer xxxxxx"})
        self.df_customers = self.load_data('https://api-dot-nth-canyon-378812.oa.r.appspot.com', '/api/v1/customers',headers={"Authorization": "Bearer xxxxxx"})

        # Apply users filters
        self.status_filter()
        self.age_filter()
        self.sales_channel_filter()
        self.date_filter()
        self.price_filter()

    def load_json_to_dataframe(self, response_json):
        target_json = response_json["result"]
        try:
            df = pd.json_normalize(target_json)
        except Exception as e:
            print(e)
        return df 

    @st.experimental_memo
    def load_data(_self, main_url, service_URL, headers):
        response_json = _self.make_request(main_url, service_URL, headers)
        df = _self.load_json_to_dataframe(response_json)
        return df

    def make_request(self, main_url, service_url, headers):
        response = requests.get(f"{main_url}{service_url}", headers = headers)
        response_json = response.json()
        return response_json

    def status_filter(self):
        ## Filter made by club member status, the output of this filter will be the updated df with new status only
        status_df = self.df_customers['club_member_status'].unique()
        # Drop None and turn it to list
        status_df = status_df[status_df != np.array(None)]
        status_lst = status_df.tolist()

        # Add the number of status to the sidebar filter
        status_filtered_lst = self.sidebar.multiselect(
            label = "Status",
            options = status_lst,
            default = status_lst,
            key = "multiselect_status"
        )   

        self.df_customers = self.df_customers[self.df_customers['club_member_status'].isin(status_filtered_lst)]

    def age_filter(self):
        ## This filters by age of the customers. The output of this function will be the df updated by age
        age_filtered_lst = self.sidebar.slider(
            'Select a range of ages',
            0, 100, (20, 80))
        
        self.df_customers = self.df_customers[(self.df_customers['age']>=age_filtered_lst[0]) & (self.df_customers['age']<=age_filtered_lst[1])]

    def sales_channel_filter(self):
        ## This function sets filters by sales channel in transactions. 

        channel_lst = self.df_transactions["sales_channel_id"].unique().tolist()

        channel_filtered_lst = self.sidebar.multiselect(
            label = "Sales channel",
            options = channel_lst,
            default = channel_lst,
            key = "multiselect_channel"
        )   

        self.df_transactions = self.df_transactions[self.df_transactions['sales_channel_id'].isin(channel_filtered_lst)]

    def date_filter(self):
        ## This function obtains the dataframe with the dates specified by the user.

        # Obtaining the date range from the user
        min_date = self.sidebar.date_input('Initial Date',value=datetime.strptime(self.df_transactions['t_dat'].min(), '%Y-%m-%d'))
        max_date = self.sidebar.date_input('Final Date',value=datetime.strptime(self.df_transactions['t_dat'].max(), '%Y-%m-%d'))

        self.df_transactions['t_dat'] = pd.to_datetime(self.df_transactions['t_dat'])
        self.df_transactions = self.df_transactions[(self.df_transactions.t_dat >= datetime.combine(min_date, datetime.min.time())) & 
                                                    (self.df_transactions.t_dat <= datetime.combine(max_date, datetime.max.time()))]
        
    def price_filter(self):
        # This function filters by the price of the transactions
        price_lst = self.sidebar.slider(
            'Select a range of price',
            float(0), float(1), (float(0), float(1)),
            step = 0.00001)
        
        self.df_transactions = self.df_transactions[(self.df_transactions['price']>=price_lst[0]) & (self.df_transactions['price']<=price_lst[1])]
