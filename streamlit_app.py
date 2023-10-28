import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

# Initialize Snowflake connection
def get_snowflake_connection():
    return snowflake.connector.connect(**streamlit.secrets["snowflake"])

# function to get fruityvice data from API
def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized

# function to get fruit load list from Snowflake database
def get_fruit_load_list():
        try:
           with get_snowflake_connection().cursor() as my_cur:
                my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
           return my_cur.fetchall()
        except snowflake.connector.errors.ProgrammingError as e:
                return None
# 
def insert_row_snowflake(new_fruit):
    try:
        with get_snowflake_connection().cursor() as my_cur:
            my_cur.execute(f"INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('{new_fruit}')")
        return f"Thanks for adding {new_fruit}"
    except snowflake.connector.errors.ProgrammingError as e:
        return None

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

        #streamlit.dataframe(my_fruit_list)
        # Let's put a pick list here so they can pick the fruit they want to include
        #streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
                #streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected] if fruits_selected else my_fruit_list
            #display the table on the page
            #streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)
            #new sction to display fruityvice api response
            ##fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
            ##fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "Kiwi")
            ##streamlit.text(fruityvice_reponse)
            ##streamlit.header("Fruityvice Fruit Advice")
            ##streamlit.text(fruityvice_response.json()) # just writes the data to the screen

#New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice")
            ##fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
            streamlit.error("Please select a fruit to get information.")
    else:
            #10/27        streamlit.write('The user entered', fruit_choice) #output what the user entered
            ###fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
            # write your own comment - put the data from fruityvice.com/api into new variable named below but formats it.
            ###fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
            # write your own comment - what does this do?
            ###streamlit.dataframe(fruityvice_normalized)
            # 10/27 if fruit_choice:  # Check if the input is not empty
            # 10/27        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
            # 10/27        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
            # 10/27        streamlit.dataframe(fruityvice_normalized)
        
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()

# we don't want to run anything past here while we toubleshoot - lab 12
############streamlit.stop()  #this stops any code below from running in the app
####### move below to function lab....
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
                ##my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
                ##my_data_row = my_cur.fetchone()
#my_data_row = my_cur.fetchall()
                ##streamlit.text("Hello from Snowflake:")
#streamlit.header("The Fruit Load List Contains:")
                ##streamlit.text("The fruit load list contains:")
#streamlit.text(my_data_row)

streamlit.header("The Fruit Load List Contains:")
# Add a button to load the fruit
#if streamlit.button('Get Fruit Load List'):
#        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#        my_data_row = get_fruit_load_list()
#            ##########streamlit.dataframe(my_data_row)
#        streamlit.text(my_data_row)
if streamlit.button('Get Fruit Load List'):
    fruit_load_list = get_fruit_load_list()
    if fruit_load_list is not None:
        streamlit.dataframe(fruit_load_list)
    else:
        streamlit.error("Failed to retrieve data from Snowflake database.")

# lab 12
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List '):
    if add_my_fruit:
            result = insert_row_snowflake(add_my_fruit)
            streamlit.text(result)
        else:
            streamlit.error("Please enter a fruit to add to the list.")
   
        #######streamlit.write('Thanks for entering ', add_my_fruit) #output what the user entered
        #########my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from Streamlit')") 
#10/28    back_from_function = insert_row_snowflake(new_fruit)
#10/28    streamlit.text(back_from_function)

##streamlit.stop()  #this stops any code below from running in the app
