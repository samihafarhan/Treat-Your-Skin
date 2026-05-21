# 🎀 Treat Your Skin: Personal Skincare Matchmaker

An interactive, data-driven web app built with Python that helps users build a custom 5-step skincare routine based on skin profile, budget caps, and ingredient exclusions.

---

## ✨ Features

* **Skin Profile Matching:** Automatically filters by Oily, Dry, Sensitive, or Combination skin types.
* **Smart Budget Ceiling:** Displays all budget-friendly options up to the selected price maximum.
* **Ingredient Filter:** Excludes specific user-selected "red flag" ingredients (e.g., BHA, Niacinamide) live.
* **Custom Routine Builder:** Interactive radio inputs inside a secure `st.form` block to select products per tier.
* **Live Calculations:** Tabular UI sections that show individual selection metrics, group ingredient lists, and dynamic total price sums.
* **Elegantly Styled:** Infused with custom HTML/CSS font controls, smooth loading modules, and asset-mapped brand animations.

---

## 🛠️ Tech Stack

* **Core Backend:** Python
* **Data Core:** Pandas (Dataframe parsing, masking, string matching)
* **Frontend UI Engine:** Streamlit Framework
* **Environment Pipeline:** Git, GitHub, Streamlit Cloud

---

## 📁 Project Structure

```text
├── app.py                 # Core application logic and UI layouts
├── my_products.csv        # Product catalog dataset
├── requirements.txt       # App software dependencies 
├── skincare_teddy1.gif    # Animated header layout media
└── moneyt.gif             # Checkout validation success media

```
---
## 🚀 How to Run Locally
# 1. Clone the repository
git clone [https://github.com/samihafarhan/Treat-Your-Skin.git](https://github.com/samihafarhan/Treat-Your-Skin.git)

cd Treat-Your-Skin

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch host server
streamlit run app.py

