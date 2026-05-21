import streamlit as st
import pandas as pd

# Page Setup
st.set_page_config(page_title="Her Happy Skin", page_icon="🎀", layout="centered")

def load_data():
    return pd.read_csv('my_products.csv')

df = load_data()

# Website Header
st.title("🎀 Her Happy Skin")
st.subheader("Routine Matchmaker & Ingredient Scanner")
st.write("Find your perfect routine while automatically filtering out ingredients your skin dislikes!")
st.divider()

# User Inputs 
st.markdown("### Step 1: Your Skin Profile 💖")
col1, col2 = st.columns(2)

with col1:
    options = ['Oily', 'Dry', 'Sensitive', 'Combination']
    user_skin = st.selectbox("What is your skin type?", options)

with col2:
    budget_options = ["Under 500", "500 - 1000", "1000 - 1500", "Over 1500"]
    user_budget = st.radio("What is your budget per item?", budget_options)

# Ingredient Red Flag Dropdown
st.markdown("### Step 2: Avoid Specific Ingredients (Optional) 🚫")
# A list of common trigger ingredients
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

# Reveal Button
if st.button("✨ Reveal My Routine ✨", use_container_width=True):
    st.toast('Scanning ingredients and building your routine... 💖', icon='✨')
    
    st.markdown(f"### 🌸 Your Perfect {user_skin} Skin Routine")
    
    # 1. Base Filter: Skin Type
    filtered_stock = df[df['Target_Skin'].str.strip().str.lower() == user_skin.lower()]
    
    # 2. Filter: Budget
    if user_budget == "Under 500":
        filtered_stock = filtered_stock[filtered_stock['Price'] < 500]
    elif user_budget == "500 - 1000":
        filtered_stock = filtered_stock[(filtered_stock['Price'] >= 500) & (filtered_stock['Price'] <= 1000)]
    elif user_budget == "1000 - 1500":
        filtered_stock = filtered_stock[(filtered_stock['Price'] > 1000) & (filtered_stock['Price'] <= 1500)]
    elif user_budget == "Over 1500":
        filtered_stock = filtered_stock[filtered_stock['Price'] > 1500]
    
    # 3. Filter: Exclude Red Flag Ingredient
    if avoid_ingredient != "None - Show everything!":
        # Clean up the name to match what is inside the CSV (e.g., "Salicylic Acid (BHA)" -> "Salicylic Acid")
        clean_search_term = avoid_ingredient.split(" (")[0]
        
        # This line keeps only the rows where the ingredient column DOES NOT contain the red flag
        filtered_stock = filtered_stock[~filtered_stock['Ingredients'].str.contains(clean_search_term, case=False, na=False)]
    
    # 4. Print the Routine
    routine_steps = ['Cleanser', 'Toner', 'Serum', 'Moisturizer', 'Sunscreen']
    
    for step in routine_steps:
        step_items = filtered_stock[filtered_stock['Category'].str.strip() == step]
        
        st.markdown(f"#### 🫧 {step}")
        
        if len(step_items) > 0:
            first_item = step_items.iloc[0]
            
            # Display item nicely inside a pinkish success container
            with st.container(border=True):
                st.markdown(f"**{first_item['Name']}**")
                st.caption(f"🧪 Key Ingredients: {first_item['Ingredients']}")
                st.markdown(f"💰 Price: ৳{first_item['Price']}")
        else:
            st.info(f"Oops! We are out of {user_skin} {step}s in this price range that fit your ingredient rules right now.")
    st.toast('Your custom routine has been built successfully! 💖', icon='✨')