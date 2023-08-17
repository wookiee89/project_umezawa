import requests
import pandas as pd
import streamlit as st

st.set_page_config(
    layout="wide"
    page_title="MTG Stuffs"
    )


setList = ['']

sets = requests.get("https://api.scryfall.com/sets").json()['data']

for setName in sets:
    setList.append(setName['name']+' - '+setName['code'])
    
set = st.selectbox('Select a set', setList, index=1)

st.write('You selected', set.split(' - ')[1])

cardList = ['']

cards = requests.get("https://api.scryfall.com/cards/search?q=set%3A"+set.split(' - ')[1]).json()['data']

st.write('There are', len(cards), 'cards in this set')
df = pd.DataFrame(cards, columns=['image_uris', 'name', 'mana_cost', 'type_line', 'oracle_text', 'power', 'toughness', 'loyalty', 'colors', 'color_identity', 'rarity', 'set_name', 'collector_number',])


df.image_uris = df['image_uris'].apply(lambda x: x['large'])


st.dataframe(df,
             column_config={
                "image_uris": st.column_config.ImageColumn(
                    "Card", help="Streamlit app preview screenshots"
                    )
                },
             hide_index=True,  
             )