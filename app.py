import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title = "Sales Dashboard",
    page_icon = ":bar_chart:",
    layout = "wide"
)

@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io = 'supermarkt_sales.xlsx',
        engine = 'openpyxl',
        sheet_name = 'Sales',
        skiprows = 3,
        usecols = 'B:R',
        nrows = 1000
    )
    # Add 'hour' column to dataframe
    df['hour'] = pd.to_datetime(df['Time'], format = "%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# -------- Sidebar ----

st.sidebar.header("Please Filter Here: ")
city = st.sidebar.multiselect(
    "Selct the City",
    options = df['City'].unique(),
    default = df['City'].unique(),

)

customer_type = st.sidebar.multiselect(
    "Selct the Customer Type: ",
    options = df['Customer_type'].unique(),
    default = df['Customer_type'].unique(),
)


gender = st.sidebar.multiselect(
    "Selct the Gender: ",
    options = df['Gender'].unique(),
    default = df['Gender'].unique(),
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# st.dataframe(df_selection)

# ------------ Main Page --------------
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI'S
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sales_by_transaction = round(df_selection['Total'].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sales_by_transaction}")
    
st.markdown("---")

# SALES BY PRODUCT LINE [ BAR CHART ]

sales_by_product_line = (
    df_selection.groupby(by = ['Product line']).sum()[['Total']].sort_values(by = "Total")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x = "Total",
    y = sales_by_product_line.index,
    orientation = "h",
    title = "Sales By Product Line",
    color_discrete_sequence= ["#0038BB"] * len(sales_by_product_line),
    template = "plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid = False))
)

# st.plotly_chart(fig_product_sales)
# ============================================
# SALES BY HOUR [ BAR CHART ]
# ============================================
sales_by_hour = df_selection.groupby(by = ["hour"]).sum()[["Total"]]

fig_hourly_sales = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y = "Total",
    orientation = "v",
    title = "Sales By Hour",
    color_discrete_sequence= ["#0038BB"] * len(sales_by_hour),
    template = "plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis = (dict(showgrid = False)),
)

# st.plotly_chart(fig_hourly_sales)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width = True)
right_column.plotly_chart(fig_product_sales, use_container_width = True)

# ------------- HIDE STREAMLIT STYLE ----------
style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""

st.markdown(style, unsafe_allow_html = True)