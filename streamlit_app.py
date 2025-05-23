import streamlit as st
import snowflake.connector

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

conn = snowflake.connector.connect(
    user="triciaradovan",
    password="TestingSnow123!",
    account="AVLTGMM-GMB10007",
    role="SYSADMIN",
    warehouse="COMPUTE_WH",
    database="SMOOTHIES",
    schema="PUBLIC"
)

cur = conn.cursor()
cur.execute("SELECT FRUIT_NAME FROM smoothies.public.fruit_options")
fruit_rows = cur.fetchall()
cur.close()

fruit_names = [row[0] for row in fruit_rows]

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names, max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    insert_stmt = "INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (%s, %s)"

    if st.button('Submit Order'):
        cur = conn.cursor()
        cur.execute(insert_stmt, (ingredients_string, name_on_order))
        conn.commit()
        cur.close()
        st.success(f"Your Smoothie is ordered, **{name_on_order}**!", icon="✅")

conn.close()
