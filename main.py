import requests
import pandas as pd
import streamlit as st
import base64


st.set_page_config(
    layout="wide",
    page_title="MTG Stuffs"
    )


# ========== Begin session state initialization ==========
# Initialize session states if they don't exist
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'page' not in st.session_state:
    st.session_state.page = 0


setList = ['']

sets = requests.get("https://api.scryfall.com/sets").json()['data']

for setName in sets:
    setList.append(setName['name']+' - '+setName['code'])

with st.sidebar:    
    set = st.selectbox('Select a set', setList, index=1)
    viewOption = st.selectbox('How would you like to view the set?', ['List', 'Images'], index=1)
    
# Initialize or reset page number based on the set selection
if 'previous_set' not in st.session_state or st.session_state.previous_set != set:
    st.session_state.current_page = 0
    st.session_state.previous_set = set

cardList = ['']

cards = requests.get("https://api.scryfall.com/cards/search?q=set%3A"+set.split(' - ')[1]).json()['data']

st.write('There are', len(cards), 'cards in this set')
df = pd.DataFrame(cards, columns=['image_uris', 'name', 'mana_cost', 'type_line', 'oracle_text', 'power', 'toughness', 'loyalty', 'colors', 'color_identity', 'rarity', 'set_name', 'collector_number',])


df.image_uris = df['image_uris'].apply(lambda x: x['large'])

if viewOption == 'List':
    st.dataframe(df,
                column_config={
                    "image_uris": st.column_config.ImageColumn(
                        "Card",
                        width='large', 
                        help="Streamlit app preview screenshots"
                        )
                    },
                hide_index=True,  
                )


# Number of cards per page
CARDS_PER_PAGE = 8

# Initialize session state for the page number
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0

# Function to split the list into chunks of n size.
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

# Extract cards for the current page
start_index = st.session_state.current_page * CARDS_PER_PAGE
end_index = start_index + CARDS_PER_PAGE
current_page_cards = df['image_uris'].tolist()[start_index:end_index]

if viewOption == 'Images':
    st.write('Cards Display:')
    
    # Display the cards for the current page
    for chunk in chunker(current_page_cards, 4):
        cols = st.columns(len(chunk))
        for i, image in enumerate(chunk):
            cols[i].image(image, width=350)
    
    # Define the callback for "Next" button
    def on_next():
        if len(df['image_uris']) > (st.session_state.current_page + 1) * CARDS_PER_PAGE:
            st.session_state.current_page += 1

    # Define the callback for "Previous" button
    def on_previous():
        if st.session_state.current_page > 0:
            st.session_state.current_page -= 1

    # Define the total number of pages
    total_pages = -(-len(df['image_uris']) // CARDS_PER_PAGE)  # Using ceiling division

   # Space for pushing pagination to the bottom
    st.write("\n" * 20)  # Adjust the number as needed

    # Create two columns: one as a spacer and one for the actual pagination
    spacer_col, pagination_col = st.columns([4, 1])

    # Inside the pagination column, create columns for the Previous button, page display, and Next button
    with pagination_col:

        prev_button_col, page_display_col, next_button_col = st.columns([.5, .33, .5])

        # "Previous" button
        with prev_button_col:
            if st.button('Previous', on_click=on_previous, disabled=st.session_state.current_page == 0):
                pass  # The action is handled in the on_click function

        # Display current page and total pages
        with page_display_col:
            st.write(f"{st.session_state.current_page + 1} / {total_pages}")

        # "Next" button
        with next_button_col:
            if st.button('Next', on_click=on_next, disabled=st.session_state.current_page == total_pages - 1):
                pass  # The action is handled in the on_click function