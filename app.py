import streamlit as st
import pandas as pd

# Page Setup
st.set_page_config(page_title="Treat Your Skin", page_icon="🎀", layout="centered")

def load_data():
    return pd.read_csv('my_products.csv')

df = load_data()

# Website Header
st.title("🎀 Treat Your Skin")
st.subheader("Your Personal Skincare Matchmaker")
st.write("Let's build a glowing routine from our shelves, just for you!")
# Your teddy bear GIF is safe right here!
st.image("skincare_teddy1.gif", use_container_width=True)
st.divider()

# User Inputs 
st.markdown("### Step 1: Tell us about you 💖")
col1, col2 = st.columns(2)

with col1:
    options = ['Oily', 'Dry', 'Sensitive', 'Combination']
    user_skin = st.selectbox("What is your skin type?", options)

with col2:
    budget_options = ["Under 500", "Under 1000", "1000 - 1500", "Over 1500"]
    user_budget = st.radio("What is your budget per item?", budget_options)

# Step 2: Ingredient Red Flag Scanner
st.markdown("### Step 2: Avoid Specific Ingredients (Optional) 🚫")
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
        
    # 3. Filter out Red Flag Ingredient (New Code Block)
    if avoid_ingredient != "None - Show everything!":
        # Extracts just the plain name before the parentheses (e.g. "Niacinamide")
        clean_search_term = avoid_ingredient.split(" (")[0]
        # Drop rows where the ingredient text contains our red flag
        filtered_stock = filtered_stock[~filtered_stock['Ingredients'].str.contains(clean_search_term, case=False, na=False)]
    
    routine_steps = ['Cleanser', 'Toner', 'Serum', 'Moisturizer', 'Sunscreen']
    total_cost = 0
    
    for step in routine_steps:
        step_items = filtered_stock[filtered_stock['Category'].str.strip() == step]
        st.markdown(f"#### 🫧 {step}")
        
        if len(step_items) > 0:
            for index, row in step_items.iterrows():
                st.success(f"**{row['Name']}** — ৳{row['Price']}\n\n*Star Ingredients:* {row['Ingredients']}")
                total_cost += row['Price']
                break # Just show the top 1 item per step to keep it clean!
        else:
            st.info(f"Oops! We are out of {user_skin} {step}s in this price range that fit your ingredient rules right now.")
            
    st.divider()
    st.metric(label="🛍️ Estimated Routine Total", value=f"৳{total_cost}")
  
    # Displays your clean, self-disappearing pop-up in the corner!
    st.toast('Your custom routine has been built successfully! 💖', icon='✨')