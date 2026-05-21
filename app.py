import streamlit as st
import pandas as pd
import time

# Page Setup
st.set_page_config(page_title="Treat Your Skin", page_icon="🎀", layout="centered")

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

# --- STEP 1: UPGRADED HEADER LAYOUT (Two Columns to fill the empty space) ---
header_col1, header_col2 = st.columns([1.2, 1])

with header_col1:
    st.markdown('<p class="main-title">🎀 Treat Your Skin</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Your Personal Skincare Matchmaker</p>', unsafe_allow_html=True)
    st.markdown('<p class="desc-text">Welcome, gorgeous! Finding the right products shouldn\'t feel like guesswork. Tell us a bit about your skin goals, and we\'ll instantly scan our shelves to curate a routine tailored exactly to your needs and budget.</p>', unsafe_allow_html=True)

with header_col2:
    # Giving the image a clean border container so it sits beautifully next to the text
    with st.container(border=True):
        st.image("skincare_teddy1.gif", use_container_width=True)

st.divider()

# User Inputs 
st.markdown('<p class="step-header">Step 1: Tell us about you 💖</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    options = ['Oily', 'Dry', 'Sensitive', 'Combination']
    user_skin = st.selectbox("What is your skin type?", options)

with col2:
    budget_options = ["Under 500", "Under 1000", "1000 - 1500", "Over 1500"]
    user_budget = st.radio("What is your budget per item?", budget_options)

# Step 2: Ingredient Red Flag Scanner
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

# The Magic Button
if st.button("✨ Reveal My Routine ✨", use_container_width=True):
    st.divider()
    
    # Aesthetic Loading Animation
    progress_text = "✨ Scanning shelf stock and analyzing ingredients... ✨"
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(0.3)
    my_bar.empty()

    st.markdown(f"### 🌸 Your Perfect {user_skin} Skin Routine")
    
    # 1. Filter by Skin Type
    filtered_stock = df[df['Target_Skin'].str.strip().str.lower() == user_skin.lower()]
    
    # 2. Filter by Budget
    if user_budget == "Under 500":
        filtered_stock = filtered_stock[filtered_stock['Price'] < 500]
    elif user_budget == "Under 1000":
        filtered_stock = filtered_stock[filtered_stock['Price'] < 1000]
    elif user_budget == "1000 - 1500":
        filtered_stock = filtered_stock[(filtered_stock['Price'] >= 1000) & (filtered_stock['Price'] <= 1500)]
    elif user_budget == "Over 1500":
        filtered_stock = filtered_stock[filtered_stock['Price'] > 1500]
        
    # 3. Filter out Red Flag Ingredient
    if avoid_ingredient != "None - Show everything!":
        clean_search_term = avoid_ingredient.split(" (")[0]
        filtered_stock = filtered_stock[~filtered_stock['Ingredients'].str.contains(clean_search_term, case=False, na=False)]
    
    routine_steps = ['Cleanser', 'Toner', 'Serum', 'Moisturizer', 'Sunscreen']
    total_cost = 0
    
    # Create beautiful tabs for the results
    tab1, tab2 = st.tabs(["📋 Recommended Routine", "🧪 Detailed View"])
    
    with tab1:
        for step in routine_steps:
            step_items = filtered_stock[filtered_stock['Category'].str.strip() == step]
            st.markdown(f"#### 🫧 {step}")
            
            if len(step_items) > 0:
                first_item = step_items.iloc[0]
                with st.container(border=True):
                    st.markdown(f"🌸 **{first_item['Name']}**")
                    st.markdown(f"🧴 **Price:** ৳{first_item['Price']}")
                total_cost += first_item['Price']
            else:
                st.info(f"Oops! We are out of {user_skin} {step}s in this price range right now.")
                
        st.divider()
        st.metric(label="🛍️ Estimated Routine Total", value=f"৳{total_cost}")
    
    with tab2:
        st.markdown("### 🧬 Ingredient Breakdown")
        st.write("Here are the star ingredients in your recommended products:")
        for step in routine_steps:
            step_items = filtered_stock[filtered_stock['Category'].str.strip() == step]
            if len(step_items) > 0:
                first_item = step_items.iloc[0]
                st.markdown(f"**{first_item['Name']}:**")
                st.caption(f"✨ {first_item['Ingredients']}")
                st.divider()

    st.toast('Your custom routine has been built successfully! 💖', icon='✨')