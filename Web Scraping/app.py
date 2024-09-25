import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

#Reading data from CSV
df = pd.read_csv("ProductData.csv")

st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem}</style>', unsafe_allow_html=True)
image = Image.open('img.jpg')

col1, col2 = st.columns([0.1,0.9])
with col1:
    st.write("")
    st.image(image,width=100)
html_title = """
    <style>
    .title-test{
    font-weight:bold;
    padding:10px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Interactive Flipkart Shoe Data Dashboard</h1></center>
    """
with col2:
    st.write("")
    st.markdown(html_title, unsafe_allow_html = True)

col3, col4, col5 =st.columns([0.1, 0.45, 0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by: \n {box_date}")

brand_counts = df['Brand'].value_counts().reset_index()
brand_counts.columns = ['Brand', 'Frequency']

with col4:
    fig = px.bar(brand_counts, x='Frequency', y='Brand', orientation='h',
             title='Frequency of Brands',
             labels={'Frequency': 'Count', 'Brand': 'Brand Name'})
    st.plotly_chart(fig, use_container_width=True)

grouped_data = df.groupby(['Brand', 'Gender']).size().reset_index(name='count')
color_sequence = ['#1f77b4', '#ff7f0e'] 

with col5:
    fig = px.bar(grouped_data, x='Brand', y='count', color='Gender',  # Use 'count' here
                     title='Product Count by Brand and Gender',
                     labels={'count': 'Number of Products', 'Brand': 'Brand'},
                     barmode='stack', color_discrete_sequence=color_sequence)
    st.plotly_chart(fig, use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])

with view1:
    expander = st.expander("Brand Wise Products")
    product_counts = df.groupby('Brand')['ProductName'].count()
    expander.write(product_counts)

with dwn1:
    st.download_button("Get Data", data=product_counts.to_csv().encode("utf-8"),
                       file_name="flipkarProductCount.csv", mime="text/csv")

with view2:
    expander_gender = st.expander("Products by Gender")  
    gender_counts = df.groupby(['Brand', 'Gender']).size().unstack(fill_value=0)
    gender_counts.columns.name = None
    expander_gender.dataframe(gender_counts)

with dwn2:
    st.download_button("Get Data", data=gender_counts.to_csv().encode("utf-8"),
                       file_name="flipkartGenderCount.csv", mime="text/csv")

st.divider()

col6, col7, col8 = st.columns([0.33, 0.33, 0.33])

average_prices = df.groupby('Brand')['ProductPrice'].mean().reset_index()
custom_colors1 = ['#C154C1']
with col6:
    fig = px.line(average_prices, x='Brand', y='ProductPrice', 
                  title='Average Product Prices Comparison by Brand',
                  labels={'ProductPrice': 'Average Price', 'Brand': 'Brand'},
                  markers=True, color_discrete_sequence=custom_colors1)  
    st.plotly_chart(fig, use_container_width=True)

average_discounts = df.groupby('Brand')['ProductDiscount'].mean().reset_index()
custom_colors2 = ['#E75480']
with col7:
    fig = px.line(average_discounts, x='Brand', y='ProductDiscount', 
              title='Average Product Discounts Comparison by Brand',
              labels={'ProductDiscount': 'Average Discount', 'Brand': 'Brand'},
              markers=True, color_discrete_sequence=custom_colors2)
    st.plotly_chart(fig, use_container_width=True)

df['Discounted'] = df['ProductDiscount'] != df['ProductPrice']
discounted_counts = df.groupby('Brand')['Discounted'].value_counts().unstack(fill_value=0).reset_index()
discounted_counts.columns.name = None

with col8:
    fig = px.bar(discounted_counts, x='Brand', y=[True, False], 
                 title='Brand-wise Count: Discounted vs Non-Discounted',
                 labels={'value': 'Number of Products', 'variable': 'Discounted'},
                 barmode='group',
                 color_discrete_sequence=['#0B6623', '#4B0082'])  
    st.plotly_chart(fig, use_container_width=True)

_, view3, dwn3, view4, dwn4, view5, dwn5 = st.columns([0.05, 0.18, 0.15, 0.17, 0.15, 0.15, 0.15])

with view3:
    expander_avgprice = st.expander("Average Prices")
    expander_avgprice.dataframe(average_prices.reset_index(drop=True))

with dwn3:
    st.download_button("Get Data", data=average_prices.to_csv().encode("utf-8"),
                       file_name="flipkartAvgPrices.csv", mime="text/csv")

with view4:
    expander_avgdiscount = st.expander("Average Discounts")
    expander_avgdiscount.dataframe(average_discounts.reset_index(drop=True))

with dwn4:
    st.download_button("Get Data", data=average_discounts.to_csv().encode("utf-8"),
                       file_name="flipkartAvgDiscounts.csv", mime="text/csv")

with view5:
    expander_privsdis = st.expander("Discounted")
    expander_privsdis.dataframe(discounted_counts.reset_index(drop=True))

with dwn5:
    st.download_button("Get Data", data=discounted_counts.to_csv().encode("utf-8"),
                       file_name="flipkartDiscountedCounts.csv", mime="text/csv")

st.divider()