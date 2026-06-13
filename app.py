import serpapi
from serpapi import GoogleSearch
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def compare(med_name):
    results = GoogleSearch({
        "engine": "google_shopping",
        "q": med_name,
        "gl": "in",
        "api_key": "3d9c7b8b3457b29cd7ca67ce38d1dbf1bfac41d44b48ca9b54b30e63d82b5875"
    }).get_dict()

    shopping_res = results.get("shopping_results", [])
    return shopping_res


col1 , col2 = st.columns(2)
col1.image('e_pharmacy.jpeg' , width=200)
col2.header('E Pharmacy Price Comparison System')

st.sidebar.title('Enter Name Of Medicine')
med_name = st.sidebar.text_input('Enter Name Here 👇')
numbers = st.sidebar.text_input('Enter Number Of Options 👇')

medicine_company = []
medicine_price = []

if med_name:
    if st.sidebar.button('Show Compare'):
        shopping_res = compare(med_name)

        numbers = int(numbers) if numbers.isdigit() else len(shopping_res)

        lowest_price = float((shopping_res[0].get('price'))[1:].replace(',',''))
        lowest_price_index = 0

        side_img = st.sidebar.image(shopping_res[0].get('thumbnail'))

        for i in range(min(numbers, len(shopping_res))):
            current_price = float((shopping_res[i].get('price'))[1:].replace(',',''))

            # For Bar Graph
            medicine_company.append(shopping_res[i].get('source'))
            medicine_price.append(current_price)

            st.title(f"Options {i+1}")
            col1 , col2 = st.columns(2)

            col1.write('Company')
            col2.write(shopping_res[i].get('source'))

            col1.write('Title')
            col2.write(' '.join(shopping_res[i].get('title').split()[:5]))

            col1.write('Price')
            col2.write(shopping_res[i].get('price'))

            url = shopping_res[i].get('product_link')
            col1.write('Buying Link')
            col2.write("[Link](%s)"%url)

            if current_price < lowest_price:
                lowest_price = current_price
                lowest_price_index = i

        st.title('Best Option')
        col1, col2 = st.columns(2)

        col1.write('Company')
        col2.write(shopping_res[lowest_price_index].get('source'))

        col1.write('Title')
        col2.write(' '.join(shopping_res[lowest_price_index].get('title').split()[:5]))

        col1.write('Price')
        col2.write(shopping_res[lowest_price_index].get('price'))

        url = shopping_res[lowest_price_index].get('product_link')
        col1.write('Buying Link')
        col2.write("[Link](%s)" % url)


        # Graphs
        df = pd.DataFrame({
            "Company": medicine_company,
            "Price": medicine_price
        }).set_index("Company")

        st.title('Chart Comparison')
        st.bar_chart(df)

        fig, ax = plt.subplots()
        ax.pie(medicine_price, labels=medicine_company, rotatelabels=True, shadow=True)
        ax.axis('equal')
        st.pyplot(fig)