import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns


# Set the page configuration
st.set_page_config(
    page_title='Dashboard for PhonePe',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Read the "india_map" CSV file into a DataFrame
df1 = pd.read_csv('data/india_map.csv')

# Read the "Bar_chart" CSV file into a DataFrame
df2 = pd.read_csv('data/bar_chart.csv')

# Read the "Histogram_district" CSV file into a DataFrame :
df3 = pd.read_csv('data/histogram_district.csv')

# Read the "Histogram_state" CSV file into a DataFrame :
df4 = pd.read_csv('data/line_plot.csv')




# Create st.sidebar elements for the choropleth map , bar chart , histogram to select option
# Create the Streamlit app
# step :1 
def main():
    
    # Create sidebar with select options
    option = st.sidebar.radio('Select Visualization of transactions', ('Choropleth Map', 'Brand Wise', 'District Wise', 'top_10_states_by_count' ,'top_10_states_by_trans_amount'))

    if option == 'Choropleth Map':
         main_choropleth()
    elif option == 'Brand Wise':
         main_bar_chart()
    elif option == 'District Wise':
         main_histogram()
    elif option =='top_10_states_by_count':
         main_top_10_states()
    elif option =='top_10_states_by_trans_amount':
         main_top_10_states_trans_amount()
        
    # Create sidebar with select options
    option = st.sidebar.radio('Select Visualization of Users Analysis', ('Users Analysis', 'top_user_by_type'))

    if option == 'Users Analysis':  
        main_line_plot()
    elif option == 'top_user_by_type':
        main_histo_plot()
        


# Create the Streamlit app for the choropleth map
# Step 1 :

def main_choropleth():
    # Set the title of the app
    st.title('Phonepe Data Visualization Dashboard')
    st.subheader('Choropleth Map')

    # Filter options for choropleth map
    years_choropleth = df1['year'].unique()
    selected_year = st.selectbox('Select Year for Choropleth Map', years_choropleth)

    quarters_choropleth = df1['quarter'].unique()
    selected_quarter = st.selectbox('Select Quarter for Choropleth Map', quarters_choropleth)

    # Apply filters for choropleth map
    filtered_df = df1[(df1['year'] == selected_year) & (df1['quarter'] == selected_quarter)]

    # Geo plot
    # Calculate the range of transaction_amount for setting zmin and zmax
    zmin = 1e5  # Custom minimum value
    zmax = 1e9  # Custom maximum value

    fig_tra = px.choropleth(
        filtered_df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='transaction_amount',
        color_continuous_scale='Viridis',  # Change the color scale
        range_color=(zmin, zmax),  # Set custom range
        title='Transaction Analysis')

    fig_tra.update_geos(fitbounds="locations", visible=False)
    fig_tra.update_layout(title_font=dict(size=33), title_font_color='#6739b7', height=500)

    st.plotly_chart(fig_tra, use_container_width=True)


# Step : 2
def main_bar_chart():
    # Set the title of the app
    st.title('Data visualization on Brand wise transactions')   
    st.subheader('Bar chart Dashboard')

    # Filter options for histogram
    states_bar_chart = df2['state'].unique()
    selected_state_bar_chart = st.selectbox('Select State or UT for bar chart', states_bar_chart)

    years_bar_chart = df2['year'].unique()
    selected_year_bar_chart = st.selectbox('Select Year for bar chart', years_bar_chart)

    quarters_bar_chart = df2['quarter'].unique()
    selected_quarter_bar_chart = st.selectbox('Select Quarter for bar chart', quarters_bar_chart)

    # Apply filters for histogram
    filtered_data_bar_chart = df2[
        (df2['state'] == selected_state_bar_chart) &
        (df2['year'] == selected_year_bar_chart) &
        (df2['quarter'] == selected_quarter_bar_chart)
    ]

    # Sort the data in ascending order based on count
    filtered_data_bar_chart = filtered_data_bar_chart.sort_values('Count', ascending=True)

    # Create a simple histogram using Altair
    custom_color_scheme = alt.Scale(domain=filtered_data_bar_chart['Brands'].unique(),
                                   range=['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF'])
    chart = alt.Chart(filtered_data_bar_chart).mark_bar().encode(
        x=alt.X('Brands', sort='-y'),
        y='Count',
        color=alt.Color('Brands', scale=custom_color_scheme),
        tooltip=['Brands', 'Count']
    ).properties(
        width=600,
        height=400,
        title='Histogram of Count by Brand (Ascending Order)'
    )
    st.altair_chart(chart, use_container_width=True)


# Step 3:

# Create the Streamlit app for the histograms
def main_histogram():
    # Set the title of the app
    st.title('Data visualization on District wise transactions')
    st.subheader('Histogram Dashboard')

    # Filter options for histogram
    states_histogram = df3['state'].unique()
    selected_state_histogram = st.selectbox('Select State or Union Territory :', states_histogram)

    years_histogram = df3['year'].unique()
    selected_year_histogram = st.selectbox('Select Year :', years_histogram)

    quarters_histogram = df3['quarter'].unique()
    selected_quarter_histogram = st.selectbox('Select Quarter :', quarters_histogram)

    # Apply filters for histogram
    filtered_data_histogram = df3[
        (df3['state'] == selected_state_histogram) &
        (df3['year'] == selected_year_histogram) &
        (df3['quarter'] == selected_quarter_histogram)
    ]

    # Sort the data in ascending order based on 'Count' and 'Amount'
    filtered_data_histogram = filtered_data_histogram.sort_values(['Count', 'Amount'], ascending=[True, True])

    # Create a bar plot for Count
    plt.figure(figsize=(12, 6))
    sns.barplot(x='District', y='Count', data=filtered_data_histogram, palette='viridis')
    plt.xlabel('District')
    plt.ylabel('Count')
    plt.title('Transactions Counts by District (Ascending Order)')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Display the Count histogram using Streamlit
    st.pyplot(plt.gcf())
    
    # Create a bar plot for Amount
    plt.figure(figsize=(12, 6))
    sns.barplot(x='District', y='Amount', data=filtered_data_histogram, palette='tab20')
    plt.xlabel('District')
    plt.ylabel('Amount')
    plt.title('Transaction Amount by District (Ascending Order)')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Display the Amount histogram using Streamlit
    st.pyplot(plt.gcf())


# Top  10 states by transaction count :

# Function to create the Top 10 States visualization
def main_top_10_states():
    st.title("Top 10 States by Transaction Count")

    # Group the data by year and state and calculate the total transaction count for each state in each year
    grouped_data = df1.groupby(['year', 'state'])['transaction_count'].sum().reset_index()

    # Dropdown to select the year
    years = grouped_data['year'].unique()
    selected_year = st.selectbox("Select a year", years)

    # Display the top 10 states for the selected year
    top_10_states = grouped_data[grouped_data['year'] == selected_year].nlargest(10, 'transaction_count')
    st.write(f"Top 10 states in {selected_year}:")
    # ignore the index and add index to the top 10 states :
    top_10_states = top_10_states.reset_index()
    st.table(top_10_states)

    # Sort the data in descending order by transaction count for plotting
    top_10_states = top_10_states.sort_values(by='transaction_count', ascending=False )

    # Create a color palette for the bar chart
    num_states = len(top_10_states)
    colors = sns.color_palette('viridis', num_states)

    # Plot the transaction counts for the top 10 states
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_10_states['state'], top_10_states['transaction_count'], color=colors)
    ax.set_xticklabels(top_10_states['state'], rotation=90)
    ax.set_xlabel("State")
    ax.set_ylabel("Transaction Count")
    ax.set_title(f"Top 10 States by Transaction Count in {selected_year}")
    st.pyplot(fig)



# Top 10 States by transaction count :
def main_top_10_states_trans_amount():
    st.title("Top 10 States by Transaction amount")
    
    # Group the data by year and state and calculate the total transaction count for each state in each year
    grouped_data = df1.groupby(['year', 'state'])['transaction_amount'].sum().reset_index()

    # Dropdown to select the year
    years = grouped_data['year'].unique()
    selected_year = st.selectbox("Select a year", years)

    # Display the top 10 states for the selected year
    top_10_states = grouped_data[grouped_data['year'] == selected_year].nlargest(10, 'transaction_amount')
    st.write(f"Top 10 states in {selected_year}:")
    # ignore the index and add index to the top 10 states :
    top_10_states = top_10_states.reset_index()
    st.table(top_10_states)

    # Sort the data in descending order by transaction count for plotting
    top_10_states = top_10_states.sort_values(by='transaction_amount', ascending=False )

    # Create a color palette for the bar chart
    num_states = len(top_10_states)
    colors = sns.color_palette('viridis', num_states)

    # Plot the transaction counts for the top 10 states
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_10_states['state'], top_10_states['transaction_amount'], color=colors)
    ax.set_xticklabels(top_10_states['state'], rotation=90)
    ax.set_xlabel("State")
    ax.set_ylabel("Transaction Amount")
    ax.set_title(f"Top 10 States by Transaction Amount in {selected_year}")
    st.pyplot(fig)
   


# Step 4 :
# Create the Streamlit app for Registered Users and App Opens:
def main_line_plot():
    # Set the title of the app
    st.title('Data visualization on Users Data by District wise')
    st.subheader('Line Plot based on Selected Filters')

    # Filter options for line plot
    states_line_plot = df4['State'].unique()
    selected_state_line_plot = st.selectbox('Select State or UT', states_line_plot)

    years_line_plot = df4['Year'].unique()
    selected_year_line_plot = st.selectbox('Select Year', years_line_plot)

    # make filter options for District based on selected state and provide a scrollable select box:
    districts_line_plot = df4[df4['State'] == selected_state_line_plot]['District'].unique()
    selected_districts_line_plot = st.selectbox('Select District(s)', districts_line_plot, index=0)

    # Apply filters for line plots
    filtered_data_line_plot = df4[
        (df4['State'] == selected_state_line_plot) &
        (df4['Year'] == selected_year_line_plot) &
        (df4['District'] == selected_districts_line_plot)]

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot RegisteredUser data
    ax.plot(filtered_data_line_plot['Quarter'], filtered_data_line_plot['RegisteredUser'], label='Registered Users', marker='o', linestyle='-')

    # Plot AppOpens data
    ax.plot(filtered_data_line_plot['Quarter'], filtered_data_line_plot['AppOpens'], label='App Opens', marker='x', linestyle='--')

    # Add labels and title
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Count')
    ax.set_title('Registered Users and App Opens in {} ({})'.format(selected_districts_line_plot, selected_year_line_plot))

    # Add gridlines
    ax.grid(True)

    # Add a legend to distinguish the lines
    ax.legend()

    # Display the plot using Streamlit
    st.pyplot(fig)

# create histo plot for transcation_type by state wise :
# Function to create the histo Plot for Transaction Type by State-Wise data
def main_histo_plot():
    # Set the title of the app
    st.title('Data visualization on Transaction Type by State-Wise')
    st.subheader('Histogram Dashboard')

    # Filter options for histogram
    states_histogram = df1['state'].unique()
    selected_state_histogram = st.selectbox('Select State or UT', states_histogram)

    years_histogram = df1['year'].unique()
    selected_year_histogram = st.selectbox('Select Year', years_histogram)

    quarters_histogram = df1['quarter'].unique()
    selected_quarter_histogram = st.selectbox('Select Quarter', quarters_histogram)

    # Apply filters for histogram
    filtered_data_histogram = df1[
        (df1['state'] == selected_state_histogram) &
        (df1['year'] == selected_year_histogram) &
        (df1['quarter'] == selected_quarter_histogram)
    ]

    # Group the data by transaction_type and sum the transaction counts
    grouped_data = filtered_data_histogram.groupby('transaction_type')['transaction_count'].sum().reset_index()

    # Sort the data in descending order based on transaction_count
    grouped_data = grouped_data.sort_values(by='transaction_count', ascending=False)

    # Create a histogram using Seaborn and Matplotlib
    plt.figure(figsize=(12, 6))
    sns.barplot(data=grouped_data, x='transaction_type', y='transaction_count', palette='viridis')
    plt.xlabel('Transaction Type')
    plt.ylabel('Transaction Count')
    plt.title(f'Histogram of Transaction Count by Transaction Type\nState: {selected_state_histogram}, Year: {selected_year_histogram}, Quarter: {selected_quarter_histogram}')
    plt.xticks(rotation=90)
    plt.tight_layout()

    st.pyplot(plt)


# Run the app
if __name__ == '__main__':
    main()
