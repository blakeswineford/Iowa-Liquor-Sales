import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 12 
plt.rcParams['axes.labelcolor'] = 'black'
plt.rcParams['xtick.color'] = 'black'
plt.rcParams['ytick.color'] = 'black'
plt.rcParams['axes.titlecolor'] = 'black'


# ********************IOWA LIQUOR SALES DATA********************


# Load the datasets
iowa_liquor_sales = pd.read_csv('data/iowa_liquor_new.csv')
present_brands_df = pd.read_csv('data/present_brands_new.csv')

# Filter the iowa_liquor_sales data to retain only Diageo brands
diageo_sales_data = iowa_liquor_sales[iowa_liquor_sales['Item Description'].isin(present_brands_df['Diageo Brands in Iowa Liquor Data'])]

# Aggregate sales data by brand
diageo_sales_by_brand = diageo_sales_data.groupby('Item Description').agg({
    'Sale (Dollars)': 'sum',
    'Volume Sold (Liters)': 'sum'
}).reset_index()

# Sort the brands based on sales
diageo_sales_by_brand_sorted = diageo_sales_by_brand.sort_values(by='Sale (Dollars)', ascending=False)

# Filter the iowa_liquor_sales data to retain only the top Diageo brands
top_diageo_brands = ['CROWN ROYAL', 'CROWN ROYAL REGAL APPLE', 'CAPTAIN MORGAN ORIGINAL SPICED', 
                     'HENNESSY VS', 'CAPTAIN MORGAN SPICED RUM', 'SMIRNOFF 80PRF', 
                     'CAPTAIN MORGAN ORIGINAL SPICED BARREL', 'TANQUERAY GIN', 
                     'RUMPLE MINZE PEPPERMINT SCHNAPPS LIQUEUR', 'SMIRNOFF 80PRF PET']
top_diageo_sales_data = iowa_liquor_sales[iowa_liquor_sales['Item Description'].isin(top_diageo_brands)]

# Aggregate sales data by category for the top Diageo brands
top_diageo_sales_by_category = top_diageo_sales_data.groupby('Category Name').agg({
    'Sale (Dollars)': 'sum',
    'Volume Sold (Liters)': 'sum'
}).reset_index()

# Sort by sales
top_diageo_sales_by_category_sorted = top_diageo_sales_by_category.sort_values(by='Sale (Dollars)', ascending=False)

# Filter the iowa_liquor_sales data to exclude the top Diageo brands
non_diageo_sales_data = iowa_liquor_sales[~iowa_liquor_sales['Item Description'].isin(top_diageo_brands)]

# Aggregate sales data by category for non-Diageo brands
non_diageo_sales_by_category = non_diageo_sales_data.groupby('Category Name').agg({
    'Sale (Dollars)': 'sum',
    'Volume Sold (Liters)': 'sum'
}).reset_index()

# Filter to get sales data only for the top categories from the Diageo brands analysis
non_diageo_sales_top_categories = non_diageo_sales_by_category[non_diageo_sales_by_category['Category Name'].isin(top_diageo_sales_by_category_sorted['Category Name'])]

# Sort by sales
non_diageo_sales_top_categories_sorted = non_diageo_sales_top_categories.sort_values(by='Sale (Dollars)', ascending=False)

# Defining the categories based on the top categories for Diageo sales
categories = top_diageo_sales_by_category['Category Name'].tolist()

diageo_sales_in_iowa = iowa_liquor_sales[iowa_liquor_sales['Item Description'].isin(present_brands_df['Diageo Brands in Iowa Liquor Data'])]

# Extracting top 5 Diageo products by sales for each category
top_diageo_products_by_category = diageo_sales_in_iowa.groupby(['Category Name', 'Item Description']).agg({
    'Sale (Dollars)': 'sum'
}).reset_index()

# Filtering only the top categories
top_diageo_products_by_category = top_diageo_products_by_category[
    top_diageo_products_by_category['Category Name'].isin(categories)
]

# Sorting and picking top 5 products for each category
top_diageo_products_by_category = top_diageo_products_by_category.sort_values(['Category Name', 'Sale (Dollars)'], ascending=[True, False])
top_5_diageo_products_by_category = top_diageo_products_by_category.groupby('Category Name').head(5)

# Extracting top 5 non-Diageo products by sales for each category
non_diageo_sales_data = iowa_liquor_sales[~iowa_liquor_sales['Item Description'].isin(present_brands_df['Diageo Brands in Iowa Liquor Data'])]
top_non_diageo_products_by_category = non_diageo_sales_data.groupby(['Category Name', 'Item Description']).agg({
    'Sale (Dollars)': 'sum'
}).reset_index()

# Filtering only the top categories
top_non_diageo_products_by_category = top_non_diageo_products_by_category[
    top_non_diageo_products_by_category['Category Name'].isin(categories)
]

# Sorting and picking top 5 products for each category
top_non_diageo_products_by_category = top_non_diageo_products_by_category.sort_values(['Category Name', 'Sale (Dollars)'], ascending=[True, False])
top_5_non_diageo_products_by_category = top_non_diageo_products_by_category.groupby('Category Name').head(5)

# Extracting sales and volume values for both Diageo and non-Diageo brands
diageo_sales_values = top_diageo_sales_by_category['Sale (Dollars)'].tolist()
non_diageo_sales_values = non_diageo_sales_top_categories['Sale (Dollars)'].tolist()

diageo_volume_values = top_diageo_sales_by_category['Volume Sold (Liters)'].tolist()
non_diageo_volume_values = non_diageo_sales_top_categories['Volume Sold (Liters)'].tolist()

### NEW
# 1. Aggregate the total sales of Diageo products by city
total_diageo_sales_by_city = diageo_sales_data.groupby('City').agg({
    'Sale (Dollars)': 'sum'
}).reset_index().sort_values(by="Sale (Dollars)", ascending=False).head(10)  # Top 10 cities by sales

# 2. Identifying top 3 cities
top_3_cities = total_diageo_sales_by_city['City'].head(3).tolist()

# 3. Grouping by City and Category to get sales for Diageo brands
diageo_sales_by_city_category = diageo_sales_data[diageo_sales_data['City'].isin(top_3_cities)].groupby(['City', 'Category Name']).agg({
    'Sale (Dollars)': 'sum'
}).reset_index()

# 4. Extracting top 3 categories for each city for Diageo brands
top_3_categories_diageo_by_city = diageo_sales_by_city_category.groupby('City').apply(lambda x: x.nlargest(3, 'Sale (Dollars)')).reset_index(drop=True)

# 3. Grouping by City and Category to get sales for non-Diageo brands
non_diageo_sales_by_city_category = non_diageo_sales_data[non_diageo_sales_data['City'].isin(top_3_cities)].groupby(['City', 'Category Name']).agg({
    'Sale (Dollars)': 'sum'
}).reset_index()

# 4. Extracting top 3 categories for each city for non-Diageo brands
top_3_categories_non_diageo_by_city = non_diageo_sales_by_city_category.groupby('City').apply(lambda x: x.nlargest(3, 'Sale (Dollars)')).reset_index(drop=True)




# ********************STREAMLIT********************


# Title and headers
st.markdown("""
# Diageo Brands Analysis in Iowa Liquor Sales

This app analyzes Diageo brands sales and volume data in Iowa liquor sales.
""")

st.markdown(""" <hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

# Custom font
st.markdown(
        f"""
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap">
<style>
    body {{
        font-family: 'Roboto', sans-serif;
    }}
</style>
""",
        unsafe_allow_html=True)

# Sidebar formatting 
st.markdown(
    """
     <style>
    [data-testid="stSidebar"] {
        background-color: #f9f9f9;
        padding: 1rem; 
        box-shadow: 1px 1px 1px 1px rgba(0, 0, 0, 0.1);
    }
    [data-testid="stSidebar"] > div {
        padding: 0rem 1rem 1rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Content width
st.markdown(
    """
    <style>
        .reportview-container .main .block-container {
            max-width: 1000px;
        }
    </style>    
    """,
    unsafe_allow_html=True,
)


def plot_sales_volume_comparison():
    fig, axs = plt.subplots(2, 1, figsize=(20, 15))

    # Sales bar plot
    bar_width = 0.35
    index = np.arange(len(categories))
    bar1 = axs[0].bar(index, diageo_sales_values, bar_width, label='Diageo Brands', color='b', alpha=0.7)
    bar2 = axs[0].bar(index + bar_width, non_diageo_sales_values, bar_width, label='Non-Diageo Brands', color='r', alpha=0.7)

    axs[0].set_xlabel('Category')
    axs[0].set_ylabel('Sales ($)')
    axs[0].set_title('Sales Comparison by Category')
    axs[0].set_xticks(index + bar_width / 2)
    axs[0].set_xticklabels(categories, rotation=45)
    axs[0].legend()

    # Volume bar plot
    bar1 = axs[1].bar(index, diageo_volume_values, bar_width, label='Diageo Brands', color='b', alpha=0.7)
    bar2 = axs[1].bar(index + bar_width, non_diageo_volume_values, bar_width, label='Non-Diageo Brands', color='r', alpha=0.7)

    axs[1].set_xlabel('Category')
    axs[1].set_ylabel('Volume Sold (Liters)')
    axs[1].set_title('Volume Sold Comparison by Category')
    axs[1].set_xticks(index + bar_width / 2)
    axs[1].set_xticklabels(categories, rotation=45)
    axs[1].legend()

    plt.tight_layout()
    st.pyplot(fig)


def plot_top_products_comparison():
    fig, axs = plt.subplots(len(categories), 2, figsize=(20, 15))

    for index, category in enumerate(categories, 1):
        ax = axs[index-1, 0]
        data = top_5_diageo_products_by_category[top_5_diageo_products_by_category['Category Name'] == category]
        sns.barplot(data=data, y='Item Description', x='Sale (Dollars)', palette='viridis', ax=ax)
        ax.set_title(f'Top 5 Diageo Products in {category}')
        ax.set_xlabel('Sales ($)')
        ax.set_ylabel('Product Name')

    for index, category in enumerate(categories, 1):
        ax = axs[index-1, 1]
        data = top_5_non_diageo_products_by_category[top_5_non_diageo_products_by_category['Category Name'] == category]
        sns.barplot(data=data, y='Item Description', x='Sale (Dollars)', palette='viridis', ax=ax)
        ax.set_title(f'Top 5 Non-Diageo Products in {category}')
        ax.set_xlabel('Sales ($)')
        ax.set_ylabel('Product Name')

    plt.tight_layout()
    st.pyplot(fig)
    
    ### NEW
def plot_city_sales_comparison():
    # Diageo Brands Sales by City
    st.title("Diageo Brands Sales in Top 3 Cities")
    fig, axs = plt.subplots(3, 1, figsize=(15, 15))
    for idx, city in enumerate(top_3_cities):
        city_data = top_3_categories_diageo_by_city[top_3_categories_diageo_by_city['City'] == city]
        sns.barplot(x="Sale (Dollars)", y="Category Name", data=city_data, palette="viridis", ax=axs[idx])
        axs[idx].set_title(f"Top 3 Diageo Categories in {city}")
        axs[idx].set_xlabel('Sales ($)')
        axs[idx].set_ylabel('Category')
    plt.tight_layout()
    st.pyplot(fig)

    # Non-Diageo Brands Sales by City
    st.title("Non-Diageo Brands Sales in Top 3 Cities")
    fig, axs = plt.subplots(3, 1, figsize=(15, 15))
    for idx, city in enumerate(top_3_cities):
        city_data = top_3_categories_non_diageo_by_city[top_3_categories_non_diageo_by_city['City'] == city]
        sns.barplot(x="Sale (Dollars)", y="Category Name", data=city_data, palette="viridis", ax=axs[idx])
        axs[idx].set_title(f"Top 3 Non-Diageo Categories in {city}")
        axs[idx].set_xlabel('Sales ($)')
        axs[idx].set_ylabel('Category')
    plt.tight_layout()
    st.pyplot(fig)


# Dropdown to select the visualization
option = st.selectbox(
    'Which visualization would you like to see?',
    ('Sales and Volume Comparison', 'Top 5 Products Comparison', 'Sales in Top 3 Cities'))

if option == 'Sales and Volume Comparison':
    plot_sales_volume_comparison()
elif option == 'Top 5 Products Comparison':
    plot_top_products_comparison()
else:
    plot_city_sales_comparison()
    


# Adjusting the main block width
st.markdown(
    """
<style>
    .reportview-container .main .block-container {
        max-width: 1200px; 
        padding-top: 5rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
</style>
""",
    unsafe_allow_html=True,
)