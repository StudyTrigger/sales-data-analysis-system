import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Sales Analysis System", layout="wide")

# ---------------- GLOBAL CLEAN CSS ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1rem;
}

/* Reduce vertical gaps */
div[data-testid="stVerticalBlock"] > div {
    gap: 0.4rem;
}

/* Style horizontal radio like navigation */
div[role="radiogroup"] {
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 6px;
}

div[role="radiogroup"] label {
    font-size: 15px !important;
    font-weight: 500;
    margin-right: 30px !important;
}

/* Hide radio circle */
div[role="radiogroup"] input[type="radio"] {
    display: none;
}

/* Active tab underline */
div[role="radiogroup"] input[type="radio"]:checked + div {
    border-bottom: 2px solid black;
    padding-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h2 style="margin-bottom:0;">📊 Sales Analysis System</h2>
<p style="color:gray; margin-top:0; margin-bottom:10px;">
Powered by Study Trigger
</p>
""", unsafe_allow_html=True)

# ---------------- CONTROL ROW ----------------
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("Upload Sales CSV File", type=["csv"])

with col2:
    if uploaded_file is None:
        st.markdown(
            "<div style='margin-top:28px; color:gray;'>Please upload a CSV file to begin.</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='margin-top:28px;'>Uploaded: <b>{uploaded_file.name}</b></div>",
            unsafe_allow_html=True
        )

# ---------------- NAVIGATION (CLEAN RADIO) ----------------
menu = st.radio(
    "",
    ["Home", "City-wise Sales", "Category Revenue", "Best Product", "Filters"],
    horizontal=True,
    label_visibility="collapsed"
)

# ---------------- MAIN CONTENT ----------------
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    df["Revenue"] = df["Quantity"] * df["Price"]

    if menu == "Home":

        total_revenue = df["Revenue"].sum()
        best_product = df.groupby("Product")["Quantity"].sum().idxmax()
        highest_revenue_product = df.groupby("Product")["Revenue"].sum().idxmax()

        k1, k2, k3 = st.columns(3)

        card_style = """
            background-color:white;
            border:1px solid #e0e0e0;
            padding:12px;
            border-radius:6px;
            text-align:center;
        """

        k1.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:14px; color:gray;">Total Revenue</div>
            <div style="font-size:22px; font-weight:600;">₹ {total_revenue}</div>
        </div>
        """, unsafe_allow_html=True)

        k2.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:14px; color:gray;">Best Selling Product</div>
            <div style="font-size:20px; font-weight:600;">{best_product}</div>
        </div>
        """, unsafe_allow_html=True)

        k3.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:14px; color:gray;">Highest Revenue Product</div>
            <div style="font-size:20px; font-weight:600;">{highest_revenue_product}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

    elif menu == "City-wise Sales":
        city_sales = df.groupby("City")["Revenue"].sum().reset_index()
        st.dataframe(city_sales, use_container_width=True)

    elif menu == "Category Revenue":
        category_revenue = df.pivot_table(
            values="Revenue",
            index="Category",
            aggfunc="sum"
        )
        st.dataframe(category_revenue, use_container_width=True)

    elif menu == "Best Product":

        product_sales = df.groupby("Product")[["Quantity", "Revenue"]].sum().reset_index()

        colA, colB = st.columns(2)

        basis = colA.selectbox(
            "Select Basis",
            ["Sales (Quantity)", "Revenue"]
        )

        top_n = colB.slider(
            "Select Number of Top Products",
            min_value=1,
            max_value=len(product_sales),
            value=3
        )

        if basis == "Sales (Quantity)":
            top_products = product_sales.sort_values(by="Quantity", ascending=False).head(top_n)
        else:
            top_products = product_sales.sort_values(by="Revenue", ascending=False).head(top_n)

        st.dataframe(top_products, use_container_width=True)

    elif menu == "Filters":

        colX, colY = st.columns(2)

        selected_category = colX.selectbox(
            "Select Category",
            df["Category"].unique()
        )

        min_revenue = colY.number_input(
            "Minimum Revenue",
            min_value=0,
            value=10000
        )

        filtered_df = df[
            (df["Category"] == selected_category) &
            (df["Revenue"] >= min_revenue)
        ]

        st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("Upload a CSV file to view insights.")