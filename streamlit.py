import pandas as pd
import streamlit as st
import plotly.express as px
from Filters import Filters


# Create Streamlit and add filters
df_filtered = Filters()

# Streamlit features
st.title('H&M KPIs')
pd.options.plotting.backend = "plotly"

# KPI'S
## 1. Average purchuase value from clubmembers and not clubmembers along time
def avg_ear_status(df_customers, df_transactions):
    aux_df = pd.merge(df_customers,df_transactions,how='inner',on='customer_id')
    original_df = aux_df
    # Compute average purchuase value (to be used in another function)
    apv = original_df['price'].sum()/len(original_df)
    # Date to datetime
    aux_df['t_dat'] = pd.to_datetime(aux_df['t_dat'])
    # Goupby Club member and t_dat to obtaining the mean
    aux_df = aux_df.groupby(['t_dat','club_member_status'])['price'].mean().reset_index()
    aux_df = aux_df.set_index('t_dat')
    aux_df = aux_df.pivot_table('price',index=['t_dat'], columns='club_member_status').reset_index()
    aux_df = aux_df.set_index('t_dat')

    st.subheader('1. Average purchuase value per date and status')
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(
    label = "Maximum average earnings",
    value = round(aux_df.max().max(),5) )
    kpi2.metric(
        label= "Date",
        value = str(aux_df.reset_index().max().t_dat)[:10]
    )
    kpi3.metric(
        label = "Status",
        value = aux_df.max().idxmax()
    )
    
    kpi4, kpi5 = st.columns(2)
    kpi4.metric(
        label = "Average purchuase value  (APV)" ,
        value = round(apv,5)
    )
    st.plotly_chart(px.line(aux_df))
    with st.expander("See explanation"):
        st.write("""Average earnings per purchuase along time. The data is grouped by the club status of the customers, and the mean quantity of each status is computed.
                 This sales indicator offers an important insight, as if the whole dataset was displayed, a large peak in the Left-Club line would have been observed,
                meaning that those members spend larger quantities in purchuases that the club members and pre club members.""")
        st.image("static/img/avgdate.png")
    
    return apv

apv = avg_ear_status(df_filtered.df_customers, df_filtered.df_transactions)

## 2. Return Rate/ mean number of sales per customer
def return_rate(df_transactions,df_customers):
    # Groupby customer_id counting how many times each customer has done a purchuase
    df_transactions = df_transactions.rename(columns={'article_id':'Number_of_purchuases'})
    aux_df = df_transactions.groupby(['customer_id']).aggregate({'price':'count', 'Number_of_purchuases':'count'})
    # Group by number of purchuases and sum
    aux_df = aux_df.groupby(['Number_of_purchuases'])['price'].agg(['count'])
    #  Obtain percentages
    aux_df['percentage'] = aux_df['count']/aux_df.sum()[0]*100

    # Compute the mean of sales per customer
    aux2_df = pd.merge(df_customers,df_transactions,how='inner',on='customer_id')
    apf = len(aux2_df)/len(aux2_df['customer_id'].unique())

    st.subheader('2.Return rate of customers ')
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(
    label = "Most common number of sales per customer",
    value = aux_df.index[aux_df.reset_index()['percentage'].idxmax()])
    kpi2.metric(
        label= "Percentage",
        value =  round(aux_df.reset_index()['percentage'].max(),5))
    
    kpi3, kpi4 = st.columns(2)
    kpi3.metric(
        label = "Mean number of sales per customer (APF)",
        value = round(apf,5) 
    )
    
    fig6 = px.pie(aux_df.reset_index(), values='percentage', names='Number_of_purchuases')
    fig6.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig6, use_container_width=True)

    with st.expander("See explanation"):
        st.write("""Return rate. One of the most important KPI's, as it measures the return of customers. It was obtained by means
        of counting the number of transactions per customer, then grouping by those number of transactions, and computing the percentage of 
        this number with respect to the total. It can be seen that the Return rate is around 70%, since at least 7/10 customers repeat buying at H&M. 
        The average number of sales made to the customers was also computed, so that the Customer Lifetime Value can be later computed """)

    return apf

apf = return_rate(df_filtered.df_transactions, df_filtered.df_customers)

##3. Customer Lifespan
def lifespan(df_transactions, df_customers):
    st.subheader('3. Customer Lifespan ')
    # Customer Lifespan
    aux_df = pd.merge(df_customers,df_transactions,how='inner',on='customer_id')
    # Date to datetime
    aux_df['t_dat'] = pd.to_datetime(aux_df['t_dat'])
    # Get max/min and total spent t_dat per customer
    new_df = aux_df.groupby(['customer_id']).aggregate({'t_dat':'min','price':'sum'}).rename(columns={'t_dat':'min_dat'})
    new_df['max_dat'] =  aux_df.groupby(['customer_id']).aggregate({'t_dat':'max'})
    new_df['lifespan'] = new_df['max_dat']-new_df['min_dat']
    lifespan = new_df.groupby(['lifespan'])['price'].count()[1:]
    # Compute the average customer lifespan
    acl = new_df['lifespan'].mean().days*24 + new_df['lifespan'].mean().seconds/(3600)

    fig = px.bar(lifespan, x=lifespan.index.days, y=lifespan, text_auto='.2s',
        labels={'x':'Lifespan [days]', 'y':'Number of customers'})
    
    kp1, kpi2 = st.columns(2)
    kp1.metric(
        label = "Average customer lifespan (ACL)",
        value = str(acl)[:4] + ' hours'
    )
    st.plotly_chart(fig)
    with st.expander("See explanation"):
        st.write("""Customer lifespan. It measures the time between the last and first sale of each customer. It was computed grouping by customers
        and computing the maximum date and minimu date of each customer, then taking the difference. This calculations do only consider the customers
        that repeat at least one time. """)
    return acl

acl = lifespan(df_filtered.df_transactions, df_filtered.df_customers)

## 4. Customer Lifetime Value
def customer_lifetime_value(apv,apf,acl):
    st.subheader('4.Customer Lifetime Value')
    clv = (apv- apf)*acl
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(
        label = "Customer lifetime value",
        value = round(clv,5)
    )
    with st.expander("See explanation"):
        st.write("""Customer Lifetime Value: it’s a way to measure the value that your customers bring to your business over
          their lifetimes and not just on their initial sale. It is computed as the difference between APV and APF, multiplied by
          the ACL. The result obtained for this dataset is extremely poor due to the low average purchuase value as the prices in the 
          dataset are not real, but this KPI is one of the most important in a business, an optimizing it is crutial""")
    
customer_lifetime_value(apv, apf, acl)    

## 5. Distribution of sales channels and customer age
def channel_age(df_customers, df_transactions, checkbox):
    aux_df = pd.merge(df_customers,df_transactions,how='inner',on='customer_id')
    # First, the ages are rounded to the nearest decen to be more easily tracked
    if checkbox:
        aux_df['age'] = round(aux_df['age'],-1)
    aux_df = aux_df.groupby(['age','sales_channel_id']).agg({'customer_id':'count'})
    aux_df = aux_df.pivot_table('customer_id',index=['age'], columns='sales_channel_id')
    fig = aux_df.plot.bar()
    st.subheader("5. Distribution of sales channels and customer age")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("See explanation"):
        st.write("""Count of customers by age group and sales channel. This KPI offers a couple of interesting insights: """)
        st.write("1. Sales channel 2, which presumably is the online channel, is the backbone of the sales.") 
        st.write("2. The sales are more abundant in people ranging from 20-50, with a higher percentage of this sales being made online") 

channel_age(df_filtered.df_customers, df_filtered.df_transactions, df_filtered.checkbox)

## 6 Gender distribution from clothes bought
def gender(df_articles, df_transactions, df_customers):
    # Double merge to merge all datasets and link articles with customers
    aux_df = pd.merge(df_articles,df_transactions,how='inner',on='article_id')
    aux_df = pd.merge(aux_df,df_customers,how='inner',on='customer_id')
    # Now that we know there is 4 groups, we will filter by ladies and men
    aux_df = aux_df[(aux_df.index_group_name == 'Menswear') | (aux_df.index_group_name == 'Ladieswear')]
    aux_df = aux_df.groupby(['index_group_name'])['article_id'].count().reset_index()
    fig = px.pie(aux_df, values='article_id', names='index_group_name')
    st.subheader('6. Gender distribution')
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("See explanation"):
        st.write("""Percentages sales made to women/men. There was no gender information included in the original dataset,
         thus what was done, was: using the transactions, obtain the articles of this transactions, and get the index group of those articles
          (Ladies or Men) and from that, obtaining an estimation of the gender distribution in our sales. It can be clearly seen that H&M is highly 
          oriented to women, no matter the age/sales channel/price. """)

gender(df_filtered.df_articles, df_filtered.df_transactions, df_filtered.df_customers)

## 7 Total earnings per color
def earnings_color(df_articles, df_transactions):
    aux_df = pd.merge(df_articles,df_transactions,on='article_id',how='inner')
    fig4 = px.pie(aux_df.groupby(['colour_group_name'])['price'].sum().to_frame().reset_index(), values='price', names='colour_group_name')
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    st.subheader('7. Earnings per color')
    st.plotly_chart(fig4, use_container_width=True)
    with st.expander("See explanation"):
        st.write("""Sum of earnings per color. What is the color trend right now? What was done in this KPI was to obtain all the articles purchuased
         and with the color of the article obtain the percentage of sales that that color represents. Black is unmatched """)

earnings_color(df_filtered.df_articles, df_filtered.df_transactions)

## 8. Product Type per Age Group
def type_age(df_articles, df_transactions, df_customers, checkbox):
    # Double merge to merge all datasets and link articles with customers
    aux_df = pd.merge(df_articles,df_transactions,how='inner',on='article_id')
    aux_df = pd.merge(aux_df,df_customers,how='inner',on='customer_id')

    # Group by ages group of decades (easier to see)
    if checkbox:
        aux_df['age'] = round(aux_df['age'],-1)

    # Group by product type and age
    aux_df = aux_df.groupby(['age','product_type_name']).count()
    # change NAN with 0
    aux_df = aux_df.fillna(value=0)
    aux_df = aux_df.rename(columns={'article_id':'Number of articles'})

    st.subheader('8. Sales per product and age')
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(
    label = "Maximum products sold",
    value = aux_df.max().max()
    )
    kpi2.metric(
        label= "Age",
        value = aux_df.idxmax()[0][0]
    )
    kpi3.metric(
        label = "Product",
        value = aux_df.idxmax()[0][1]
    )

    fig5 = px.bar(aux_df.reset_index(), x='age', y='Number of articles', color='product_type_name')
    st.plotly_chart(fig5)

    with st.expander("See explanation"):
        st.write("""Product type. In this KPI, the products sold are grouped with the customer information such as the age of the customer,
        and then grouped by the type of product. If a more detailed insight is required in terms of the age, the Group Ages by Decade checkbox offers a 
        very nice feature, that decomposes the ages group, changing the results quite a bit. From this KPI, it can be seen that trousers are the most sold 
        product across all ages, followed by underwear. Another interesting feature is the sales of Cardigans to people 49 years old (don't ask me why).""")

type_age(df_filtered.df_articles, df_filtered.df_transactions,df_filtered.df_customers, df_filtered.checkbox)
    

