import streamlit as st
import pandas as pd
#from streamlit_extras.let_it_rain import rain
# Page Setup
st.set_page_config(page_title="Treat Your Skin", page_icon="🎀", layout="centered")

def load_data():
    return pd.read_csv('my_products.csv')

df = load_data()

# Website Header
st.title("🎀 Treat Your Skin")
st.subheader("Your Personal Skincare Matchmaker")
st.write("Let's build a glowing routine from our shelves, just for you!")
# The use_container_width=True makes it perfectly stretch to fit the screen!
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

# The Magic Button
if st.button("✨ Reveal My Routine ✨", use_container_width=True):
    st.divider()
    st.markdown(f"### 🌸 Your Perfect {user_skin} Skin Routine")
    
    # Filter by Skin Type
    # Added .str.strip() to make sure hidden spaces don't break the skin type filter
    filtered_stock = df[df['Target_Skin'].str.strip().str.lower() == user_skin.lower()]
    
    # Filter by Budget
    if user_budget == "Under 500":
        filtered_stock = filtered_stock[filtered_stock['Price'] < 500]
    elif user_budget == "Under 1000":
        filtered_stock = filtered_stock[filtered_stock['Price'] < 1000]
    elif user_budget == "1000 - 1500":
        filtered_stock = filtered_stock[(filtered_stock['Price'] >= 1000) & (filtered_stock['Price'] <= 1500)]
    elif user_budget == "Over 1500":
        filtered_stock = filtered_stock[filtered_stock['Price'] > 1500]
    
    routine_steps = ['Cleanser', 'Toner', 'Serum', 'Moisturizer', 'Sunscreen']
    total_cost = 0
    
    for step in routine_steps:
        # Added .str.strip() here too!
        step_items = filtered_stock[filtered_stock['Category'].str.strip() == step]
        st.markdown(f"#### 🫧 {step}")
        
        if len(step_items) > 0:
            for index, row in step_items.iterrows():
                st.success(f"**{row['Name']}** — ৳{row['Price']}\n\n*Star Ingredients:* {row['Ingredients']}")
                total_cost += row['Price']
                break # Just show the top 1 item per step to keep it clean!
        else:
            st.info(f"Oops! We are out of {user_skin} {step}s in this price range right now.")
            
    st.divider()
    st.metric(label="🛍️ Estimated Routine Total", value=f"৳{total_cost}")
  
# Displays a gorgeous, self-disappearing pop-up in the corner!
    st.toast('Your custom routine has been built successfully! 💖', icon='✨')