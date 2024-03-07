import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
import datetime as dt
import urllib
from func import BrazilMapPlotter
import matplotlib.image as mpimg

url = "https://drive.google.com/file/d/1lRn4glI2iyxBa2jNJhPuKYViYppi0mwN/view?usp=sharing"
file_id=url.split('/')[-2]
dwn_url='https://drive.google.com/uc?id=' + file_id
df_all = pd.read_csv(dwn_url)

# ==========================
def df_create_by_product(df):
    product_id_counts = df.groupby('product_category_name_english')['product_id'].count().reset_index()
    df_sorted = product_id_counts.sort_values(by='product_id', ascending=False)
    return df_sorted

df_most_and_least_purchased_products=df_create_by_product(df_all)

# ==========================
datetime_columns = ["order_approved_at"]
for column in datetime_columns:
    df_all[column] = pd.to_datetime(df_all[column])

def number_order_per_month(df):
    df_monthly = df.resample(rule='M', on='order_approved_at').agg({
        "order_id": "size",
    })
    df_monthly.index = df_monthly.index.strftime('%B')
    df_monthly = df_monthly.reset_index()
    df_monthly.rename(columns={
        "order_id": "order_count",
    }, inplace=True)
    df_monthly = df_monthly.sort_values('order_count').drop_duplicates('order_approved_at', keep='last')
    month_mapping = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    df_monthly["month_numeric"] = df_monthly["order_approved_at"].map(month_mapping)
    df_monthly = df_monthly.sort_values("month_numeric")
    df_monthly = df_monthly.drop("month_numeric", axis=1)
    return df_monthly

daily_orders_df=number_order_per_month(df_all)

# ==========================
url = "https://drive.google.com/file/d/13qsmSQKJnpha03HGMay28vOAwHBAq8_y/view?usp=sharing"
file_id=url.split('/')[-2]
dwn_url='https://drive.google.com/uc?id=' + file_id
geolocation = pd.read_csv(dwn_url)

data = geolocation.drop_duplicates(subset='customer_unique_id')

map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)
st.set_option('deprecation.showPyplotGlobalUse', False)

# ==========================
def rating_cust_df(df):
    rating_by_customers = df['review_score'].value_counts().sort_values(ascending=False)
    maximal_score = rating_by_customers.idxmax()
    df_cust=df['review_score']
    return (rating_by_customers,maximal_score,df_cust)

rating_by_customers,maximal_score,df_rating_service=rating_cust_df(df_all)

# SideBar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/77/Streamlit-logo-primary-colormark-darktext.png")
    st.write('Proyek Analisis Data: E-Commerce Public Dataset')

# Header
st.header('Proyek Analisis Data: E-Commerce Public Dataset')

# Most and Least Purchased Products
st.subheader("Most and Least Purchased Products")
col1, col2 = st.columns(2)

with col1:
    highest_product_sold=df_most_and_least_purchased_products['product_id'].max()
    st.markdown(f"Higest Number Purchased Products : **{highest_product_sold}**")

with col2:
    lowest_product_sold=df_most_and_least_purchased_products['product_id'].min()
    st.markdown(f"Lowest Number Purchased Products: **{lowest_product_sold}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))

colors = ["#124076", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="product_id", 
    y="product_category_name_english", 
    data=df_most_and_least_purchased_products.head(5), 
    palette=colors, 
    ax=ax[0],
    )
ax[0].set_ylabel('')
ax[0].set_xlabel('')
ax[0].set_title("Most Purchased Products", loc="center", fontsize=20)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(
    x="product_id", 
    y="product_category_name_english", 
    data=df_most_and_least_purchased_products.sort_values(by="product_id", ascending=True).head(5), 
    palette=colors, 
    ax=ax[1],)
ax[1].set_ylabel('')
ax[1].set_xlabel('')
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Least Purchased Products", loc="center", fontsize=20)
ax[1].tick_params(axis='y', labelsize=15)

plt.suptitle("Most and Least Sold Products", fontsize=22)
st.pyplot(fig)

st.write('Berdasarkan grafik yang diperoleh, produk yang memiliki jumlah pembelian paling tinggi adalah **bed_bath_table** , sedangkan produk yang memiliki jumlah pembelian paling rendah adalah **security_and_services**.')

# Monthly Order Counts in 2018
st.subheader("Monthly Order Counts in 2018")

col1, col2 = st.columns(2)

with col1:
    high_order_num = daily_orders_df['order_count'].max()
    high_order_month=daily_orders_df[daily_orders_df['order_count'] == daily_orders_df['order_count'].max()]['order_approved_at'].values[0]
    st.markdown(f"Highest orders in {high_order_month} : **{high_order_num}**")

with col2:
    low_order = daily_orders_df['order_count'].min()
    low_order_month=daily_orders_df[daily_orders_df['order_count'] == daily_orders_df['order_count'].min()]['order_approved_at'].values[0]
    st.markdown(f"Lowest orders in {low_order_month} : **{low_order}**")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#124076",
)
plt.xticks(rotation=45)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.write('Berdasarkan grafik yang diperoleh, di tahun 2018, jumlah pembelian tertinggi terdapat di bulan **November** dan jumlah pembelian terendah terdapat di bulan **September**.')

# The region of Brazil with the highest customer concentration.
st.subheader("Customers Demographic")
map_plot.plot()
st.write('Berdasarkan grafik yang diperoleh, jumlah customers paling banyak terdapat di wilayah Brazil bagian **Tenggara** dan **Selatan**.')

# Customer Review Rating for Services
st.subheader("Customer Review Rating for Services")
    
plt.figure(figsize=(16, 8))
sns.barplot(x=rating_by_customers.index, 
            y=rating_by_customers.values, 
            order=rating_by_customers.index,
            palette=["#124076" if score == maximal_score else "#D3D3D3" for score in rating_by_customers.index],
            )

plt.title("Customer Review Rating for Services", fontsize=20)
plt.xlabel("Rating")
plt.ylabel("Customer")
plt.xticks(fontsize=15)
st.pyplot(plt)

st.write('Berdasarkan grafik yang diperoleh, total customer yang memberikan rating 5 lebih banyak daripada total customer yang memberikan rating dibawah 5, maka tingkat kepuasan customer terhadap services yang diberikan **sangat tinggi**.')

# Copyright
st.caption('Copyright (C) © 2024 by Reisa')
