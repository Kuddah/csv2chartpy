import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set page title
st.set_page_config(page_title='Multiple Line Charts From CSV')

# Define function to read CSV file and return a DataFrame
def load_data(file):
    df = pd.read_csv(file)
    return df

# Create file uploader
uploaded_file = st.file_uploader('Choose a CSV file', type='csv')

# If a file was uploaded, load it into a DataFrame
if uploaded_file is not None:
    df = load_data(uploaded_file)

    # Display the DataFrame in a table
    st.write('DataFrame:')
    st.write(df)

    # Check if DataFrame is not empty
    if not df.empty:
        # Choose between different pages
        page = st.sidebar.radio("Choose a page", ["Single Y-axis", "Multiple Y-axes"])

        # Create a selectbox for the number of charts to be created
        num_charts = st.sidebar.selectbox('Select the number of charts:', list(range(1, 11)))

        x_column = None
        for i in range(num_charts):
            st.subheader(f'Chart {i+1}')
            cols = st.beta_columns(4)

            # Create an input field for the chart name
            with cols[0]:
                chart_name = st.text_input(f'Chart Name {i+1}:', value=f'Line Chart {i+1}')

            # Create a selectbox for the X column
            with cols[1]:
                x_column = st.selectbox(f'Select column for X axis for Chart {i+1}:', df.columns, index=0 if x_column is None else df.columns.get_loc(x_column))

            # Create a selectbox or multiselect for the Y column(s)
            with cols[2]:
                if page == "Single Y-axis":
                    y_column = st.selectbox(f'Select column for Y axis for Chart {i+1}:', df.columns)

                    # Allow user to choose chart color
                    color_palette = px.colors.qualitative.Alphabet
                    color = st.selectbox(f'Select chart color for Chart {i+1}:', color_palette)
                    
                    # Create line chart using Plotly Graph Objects
                    fig = go.Figure(go.Scatter(x=df[x_column], y=df[y_column], mode='lines', name=y_column, line=dict(color=color)))
                
                else:  # "Multiple Y-axes"
                    y_columns = st.multiselect(f'Select column(s) for Y axis for Chart {i+1}:', df.columns)

                    # Create line chart using Plotly Graph Objects
                    fig = go.Figure()
                    color_palette = px.colors.qualitative.Alphabet
                    for j, y_column in enumerate(y_columns):
                        color = color_palette[j % len(color_palette)]
                        fig.add_trace(go.Scatter(x=df[x_column], y=df[y_column], mode='lines', name=y_column, yaxis=f'y{j+1}', line=dict(color=color)))

            # Update layout for multiple Y-axes
            if len(y_columns) > 1:
                fig.update_layout(
                    yaxis=dict(title=y_columns[0]),
                    yaxis2=dict(title=y_columns[1], overlaying='y', side='right')
                )

            # Allow user to customize chart name
            fig.update_layout(title=chart_name)

            st.plotly_chart(fig, use_container_width=True)
