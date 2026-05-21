import streamlit as st
import pandas as pd
import time

# Page Setup
st.set_page_config(page_title="Treat Your Skin", page_icon="🎀", layout="centered")

# Initialize session state so the form stays hidden on first load
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

# Custom CSS to give it a premium, boutique storefront feel
st.markdown("""
    <style>
    /* Make the titles look high-end and elegant */
    .main-title {
        font-size: 42px !important;
        font-weight: bold;
        color: #4A4A4A;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 20px !important;
        color: #D4A373;
        font-weight: 500;
        margin-bottom: 15px;
    }
    .desc-text {
        font-size: 15px !important;
        color: #707070;
        line-height: 1.6;
    }
    /* Style the steps to look clean and neat */
    .step-header {
        font-size: 20px !important;
        font-weight: bold;
        color: #4A4A4A;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def load_data():
    return pd.read_csv('my_products.csv')

df = load_data()

# --- STEP 1: HEADER LAYOUT ---
header_col1, header_col2 = st.columns([1.2, 1])

with header_col1:
    st.markdown('<p class="main-title">🎀 Treat Your Skin</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Your Personal Skincare Matchmaker</p>', unsafe_allow_html=True)
    st.markdown('<p class="desc-text">Welcome, gorgeous! Finding the right products shouldn\'t feel like guesswork. Tell us a bit about your skin goals, and we\'ll instantly scan our shelves to curate a routine tailored exactly to your needs and budget.</p>', unsafe_allow_html=True)

with header_col2:
    with st.container(border=True):
        st.image("skincare_teddy1.gif", use_container_width=True)

st.divider()

# --- STEP 2: PROFILE CONFIGURATION ---
st.markdown('<p class="step-header">Step 1: Tell us about you 💖</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    options = ['Oily', 'Dry', 'Sensitive', 'Combination']
    user_skin = st.selectbox("What is your skin type?", options)

with col2:
    budget_options = ["Under 500", "Under 1000", "1000 - 1500", "Any Budget"]
    user_budget = st.radio("What is your budget per item?", budget_options)

st.markdown('<p class="step-header">Step 2: Avoid Specific Ingredients (Optional) 🚫</p>', unsafe_allow_html=True)
red_flags = [
    "None - Show everything!",
    "Salicylic Acid (BHA)",
    "Niacinamide",
    "Glycolic Acid (AHA)",
    "Ceramides",
    "Hyaluronic Acid",
    "Centella"
]
avoid_ingredient = st.selectbox("Is there an ingredient you want to completely avoid?", red_flags)

st.divider()

# --- STEP 3: START BUTTON ---
if st.button("🔍 Scan Shelves for My Options", use_container_width=True):
    st.session_state.quiz_started = True

# --- STEP 4: INTERACTIVE MATCHMAKER FORM ---
if st.session_state.quiz_started:
    
    filtered_stock = df[df['Target_Skin'].str.strip().str.lower() == user_skin.lower()]

    if user_budget == "Under 500":
        filtered_stock = filtered_stock[filtered_stock['Price'] <= 500]
    elif user_budget == "Under 1000":
        filtered_stock = filtered_stock[filtered_stock['Price'] <= 1000]
    elif user_budget == "1000 - 1500":
        filtered_stock = filtered_stock[filtered_stock['Price'] <= 1500]
    elif user_budget == "Any Budget":
        pass

    if avoid_ingredient != "None - Show everything!":
        clean_search_term = avoid_ingredient.split(" (")[0]
        filtered_stock = filtered_stock[~filtered_stock['Ingredients'].str.contains(clean_search_term, case=False, na=False)]

    st.markdown(f"### 🌸 Build Your Custom {user_skin} Routine")
    st.write("Select one product from each category below to customize your bundle:")

    routine_steps = ['Cleanser', 'Toner', 'Serum', 'Moisturizer', 'Sunscreen']

    with st.form("routine_builder_form"):
        user_selections = {}
        
        for step in routine_steps:
            step_items = filtered_stock[filtered_stock['Category'].str.strip() == step]
            st.markdown(f"#### 🫧 {step}")
            
            if len(step_items) > 0:
                product_options = []
                product_mapping = {}
                
                for index, row in step_items.iterrows():
                    display_label = f"🌸 {row['Name']} — ৳{row['Price']}"
                    product_options.append(display_label)
                    product_mapping[display_label] = (row['Name'], row['Price'], row['Ingredients'])
                
                selected_radio = st.radio(
                    f"Choose your {step}:", 
                    options=product_options, 
                    label_visibility="collapsed",
                    key=f"radio_{step}"
                )
                user_selections[step] = product_mapping[selected_radio]
            else:
                st.info(f"Oops! We are out of {user_skin} {step}s that fit your budget or ingredient rules right now.")
                user_selections[step] = None

        submit_button = st.form_submit_button("✨ Calculate Bundle Total & Lock Routine ✨", use_container_width=True)

    # --- STEP 5: DISPLAY SELECTED RESULTS & TOTAL ---
    if submit_button:
        progress_text = "✨ Packaging your custom bundle... ✨"
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.005)
            my_bar.progress(percent_complete + 1, text=progress_text)
        my_bar.empty()

        st.success("### 🛍️ Your Locked Routine Bundle Summary")
        
        total_cost = 0
        tab1, tab2 = st.tabs(["📋 Selection Summary", "🧪 Complete Ingredient Breakdown"])
        
        with tab1:
            for step in routine_steps:
                selection = user_selections[step]
                if selection:
                    name, price, _ = selection
                    with st.container(border=True):
                        st.markdown(f"**{step}:** {name}")
                        st.markdown(f"💰 **Price:** ৳{price}")
                    total_cost += price
            st.divider()
            
            # --- NEW SIDE-BY-SIDE TOTAL COST & GIF LAYOUT ---
            #result_col1, result_col2 = st.columns([1.5, 1])
            
            st.metric(label="🛍️ Total Custom Bundle Cost", value=f"৳{total_cost}")
                
            st.image("moneyt.gif", use_container_width=True)
            
        with tab2:
            st.markdown("### 🧬 Ingredient Profiles")
            for step in routine_steps:
                selection = user_selections[step]
                if selection:
                    name, _, ingredients = selection
                    st.markdown(f"**{name} ({step}):**")
                    st.caption(f"✨ {ingredients}")
                    st.divider()

        st.toast('Your custom routine has been built successfully! 💖', icon='✨')