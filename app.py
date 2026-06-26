import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Sales Perfomance Analytics ", layout="wide")

@st.cache_data
def load_live_data():
    try:
        # Pulls data strictly from the tab named "Dashboard"
        df = pd.read_excel("Sale-Perfomative-Analysis(1).xlsx", sheet_name="Dashboard")
        return df
    except Exception as e:
        # Safe catch-all to prevent app crashes during live viewing
        return None

df_live = load_live_data()



st.title("Sales Perfomance Analysis: From Data to Strategy")
st.markdown("---")

col_prob, col_imp = st.columns(2)

with col_prob:
    st.error("###  The Problem")
    st.write(
        "Most businesses cannot see corporate health clearly because critical "
        "sales data remains trapped inside giant, messy spreadsheets."
    )

with col_imp:
    st.warning("### The Impact")
    st.write(
        "Without an interactive visual tool, leadership cannot easily identify which regions "
        "are losing money, who their target customers are, or why buyers are leaving."
    )

st.markdown("---")


st.sidebar.header(" CONTROL PANEL")

# --- CUSTOM CSS TO MAKE SIDEBAR SLICERS MATCH YOUR GREEN THEME ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #2e5621 !important; /* Matches your dark green background */
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #ffffff !important; /* Turns filter label text white for high contrast */
    }
    div.stMultiSelect, div.stSelectbox {
        background-color: #ffffff !important;
        border-radius: 4px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Generate unique dropdown lists from your live data (or fallback defaults)
if df_live is not None:
    try:
        available_regions = sorted(df_live['Region'].unique().tolist())
        available_categories = sorted(df_live['Product Category'].unique().tolist())
        available_ratings = sorted(df_live['Rating'].unique().tolist())
    except:
        available_regions = ["East", "North", "South", "West"]
        available_categories = ["Beauty", "Clothing", "Electronics", "Home"]
        available_ratings = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
else:
    available_regions = ["East", "North", "South", "West"]
    available_categories = ["Beauty", "Clothing", "Electronics", "Home"]
    available_ratings = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7]

# 1. Region Filter Slicer
selected_regions = st.sidebar.multiselect(
    "Select Region", 
    options=available_regions, 
    default=available_regions
)

# 2. Product Category Filter Slicer
selected_categories = st.sidebar.multiselect(
    "Select Product Category", 
    options=available_categories, 
    default=available_categories
)

# 3. Customer Rating Filter Slicer
selected_ratings = st.sidebar.multiselect(
    "Select Customer Rating", 
    options=available_ratings, 
    default=available_ratings
)

if df_live is not None:
    try:
        df_filtered = df_live[
            (df_live['Region'].isin(selected_regions)) & 
            (df_live['Product Category'].isin(selected_categories)) & 
            (df_live['Rating'].isin(selected_ratings))
        ]
    except:
        df_filtered = df_live
else:
    df_filtered = None




st.header("Project Overview")
col_about, col_sol = st.columns(2)

with col_about:
    st.info("#### About the Project\n"
            "This project analyzes over 100,000 sales rows to find where the business makes money "
            "and see what customers think about our platform.")

with col_sol:
    st.success("#### The Solution\n"
              "Instead of looking at massive spreadsheets, this app gives managers "
              "**fast, interactive data tools** to make smart decisions instantly.")

st.markdown("---")



st.header("Sales Perfomance Analysis")


st.markdown("""
    <style>
    /* 1. This turns the cards into your leaf-green shape with a dark blue border */
    div[data-testid="metric-container"] {
        background-color: #a1d183 !important;      /* Leaf-green fill color */
        border: 2px solid #0a2d54 !important;         /* Dark-blue sharp border */
        border-radius: 15px 4px 4px 15px !important;  /* Rounds only the left side */
        padding: 12px 15px !important;               /* Creates space inside the shape */
        text-align: center !important;                /* Centers all text inside the shape */
    }
    
    /* 2. This styles the big number text inside the shape */
    [data-testid="stMetricValue"] { 
        color: #0c1a2f !important;                    /* Dark blue text color */
        font-weight: bold !important; 
        font-family: 'Georgia', serif !important; 
    }
    
    /* 3. This styles the small label text at the top of the shape */
    [data-testid="stMetricLabel"] { 
        color: #333333 !important;                    /* Soft dark grey text */
        text-transform: uppercase !important;         /* Makes label ALL CAPS */
        font-family: 'Georgia', serif !important; 
    }
    </style>
""", unsafe_allow_code_html=True) 


kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)


with kpi_col1:
    st.metric(label="Total Revenue", value="$5,109,775.7")

with kpi_col2:
    st.metric(label="Total Customers", value="5,000")

with kpi_col3:
    st.metric(label="Average Order Value", value="1,021.96")

with kpi_col4:
    st.metric(label="Average Rating", value="2.97")

st.markdown("###  Product Revenue Analysis")

chart_data = pd.DataFrame({
    "Category": ["Beauty", "Clothing", "Electronics", "Home"],
    "Revenue ($)": [760000, 1530000, 1830000, 980000] 
})


fig_revenue = px.bar(
    chart_data, 
    x="Category", 
    y="Revenue ($)", 
    title="Electronics Drive 35% More Revenue Than Any Category",
    labels={"Revenue ($)": "Revenue in Dollars", "Category": "Product Category"},
    color_discrete_sequence=["#62ad43"] 
)


fig_revenue.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',   
    font_family="Georgia",          
    title_font_color="#2e5621",     
    title_font_size=20,
    title_x=0.15                    
)


st.plotly_chart(fig_revenue, use_container_width=True)

st.markdown("---")


st.markdown("###  Regional Revenue Analysis")

regional_data = pd.DataFrame({
    "Region": ["East", "North", "South", "West"],
    "Revenue ($)": [1235000, 1280000, 1245000, 1345000] 
})

fig_regional = px.bar(
    regional_data,
    x="Revenue ($)",
    y="Region",
    orientation="h", 
    title="The West Region Contributes more Revenue by<br>26.33%",
    labels={"Revenue ($)": "Revenue in Dollars", "Region": ""},
    color_discrete_sequence=["#70ad47"] 
)


fig_regional.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_family="Georgia",
    title_font_color="#375623", 
    title_font_size=20,
    title_x=0.5,                
    xaxis=dict(
        showgrid=False,          
        linecolor="#d9d9d9"     
    ),
    yaxis=dict(
        linecolor="#d9d9d9"      
    )
)

st.plotly_chart(fig_regional, use_container_width=True)

st.markdown("---")


st.markdown("### 👥 Customer Satisfaction Breakdown")

satisfaction_data = pd.DataFrame({
    "Segment": ["Dissatisfied", "Highly Satisfied", "Satisfied but Neutral"],
    "Percentage": [50, 25, 25]
})

fig_satisfaction = px.pie(
    satisfaction_data,
    values="Percentage",
    names="Segment",
    hole=0.6, 
    title="Customer Segmentation by Satisfaction",
    
    color_discrete_sequence=["#a9d18e", "#70ad47", "#375623"] 
)

fig_satisfaction.update_traces(
    textposition="inside",
    textinfo="percent", 
    insidetextfont=dict(fontfamily="Georgia", size=14, color="#333333")
)

fig_satisfaction.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    font_family="Georgia",
    title_font_color="#444444", 
    title_font_size=22,
    title_x=0.22,               
    legend=dict(
        font=dict(size=12),
        yanchor="center",
        y=0.5,
        xanchor="left",
        x=1.05                
    )
)


st.plotly_chart(fig_satisfaction, use_container_width=True)

st.markdown("---")



st.markdown("###  Customer Operational Matrix")

if df_filtered is not None:
    try:
        summary_df = df_filtered.groupby('Satisfaction').mean()[['Discount', 'Delivery Days', 'Quantity']].reset_index()
        summary_df.columns = ["Customer Segment", "Avg. Discount Given", "Avg. Shipping Speed (Days)", "Avg. Items per Order"]
        
        summary_df["Avg. Discount Given"] = summary_df["Avg. Discount Given"].apply(lambda x: f"{x*100:.0f}%" if x < 1 else f"{x:.0f}%")
        summary_df["Avg. Shipping Speed (Days)"] = summary_df["Avg. Shipping Speed (Days)"].round(1).astype(str) + " Days"
        summary_df["Avg. Items per Order"] = summary_df["Avg. Items per Order"].round(0).astype(int).astype(str) + " Units"
        
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
    except Exception as e:

        st.warning("Could not calculate dynamic matrix averages. Showing backup data.")



matrix_data = pd.DataFrame({
    "Customer Segment": ["Dissatisfied (50%)", "Satisfied but Neutral (25%)", "Highly Satisfied (25%)"],
    "Number of Customers":[2477,1254,1269],
    "Average Discount": ["0.18", "0.18", "0.18"],
    "Average Delivery Days": [6.2, 6.1, 6.0],
    "Average Quantity": [4, 4, 4]
})


st.markdown("""
    <style>
    /* Styles the container grid to look exactly like your card outline */
    .stDataFrame {
        border: 2px solid #a1d183 !important; 
        border-radius: 8px !important;
        background-color: #ffffff !important;
        padding: 5px !important;
    }
    </style>
""", unsafe_allow_code_html=True)


st.dataframe(
    matrix_data, 
    use_container_width=True, 
    hide_index=True 
)

st.markdown("---")

st.header(" Real-World Business Value Delivered")
val1, val2, val3 = st.columns(3)

with val1:
    st.subheader("Direct Cost Savings")
    st.write("Stops wasteful spending on deep discounts, since data proves discounts do not improve customer satisfaction.")

with val2:
    st.subheader(" Strategic Capital Reallocation")
    st.write("Enables leadership to reallocate budgets from the strong West region to fix operations in the failing East region.")

with val3:
    st.subheader(" Process Automation")
    st.write("Saves hours spent manually building reports. Interactive layouts allow instant access to regional metrics.")