import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def claculate_current_balance(df):
    final_amount = df['Inflow'].sum() - df['Outflow'].sum()
    return final_amount

def update_excel_file(file_path, new_data):
    # Load the existing Excel file
    df = pd.read_excel(file_path)
    
    # Append new data to the DataFrame
    df = pd.concat([df, pd.DataFrame(new_data)], axis=0, ignore_index=True)
    
    # Calculate the final amount
    final_amount = df['Inflow'].sum() - df['Outflow'].sum()
    
    # Save the updated DataFrame to Excel
    df.to_excel(file_path, index=False)

    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df, final_amount


def main():
    st.set_page_config(layout="wide")
    st.title("Cash Flow Management System")

    # File upload section
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])


    tabs = ["Data Entry", "Data Analysis"]
    tab1, tab2 =  st.tabs(tabs)

    

    with tab1:

        if uploaded_file is not None:
            # Read the Excel file
            df = pd.read_excel(uploaded_file)

            opening_amount = df['Inflow'].sum() - df['Outflow'].sum()
            st.success(f"Current Available Amount: {opening_amount}")
            # Data entry section
            st.subheader("Enter New Transaction")
            num_entries = st.number_input("Number of Entries", step=1, min_value=1,max_value=100)

            for i in range(num_entries):
                col1, col2, col3, col4 = st.columns(4)

                i = str(i)
                with col1:
                    date = st.date_input("Date", key=f"date_{i}")

                with col2:
                    description = st.text_input("Description", key=f"desc_{i}")
                
                with col3:
                    inflow = st.number_input("Inflow Amount", min_value=0, key=f"inflow_{i}")

                with col4:
                    outflow = st.number_input("Outflow Amount", min_value=0, key=f"outflow_{i}")

            # Add transaction button
            if st.button("Add Transaction"):
                new_data = {'Date': [date], 'Description': [description], 'Inflow': [inflow], 'Outflow': [outflow]}
                updated_df, final_amount = update_excel_file(uploaded_file.name, new_data)

                # Show final amount
                st.success(f"Transaction added successfully! Final Amount: {final_amount}")

    with tab2:
        st.title("Data Analysis")
        
        if uploaded_file is not None:
            # Read the Excel file
            df = pd.read_excel(uploaded_file)
            df['Date'] = pd.to_datetime(df['Date'])
            min_date, max_date = min(df['Date']).date(),max(df['Date']).date()
            date_range = st.slider("Select a date range:", min_value=min_date, max_value=max_date, value=(min_date, max_date), format="YYYY-MM-DD")
            df = df[(df['Date']>=str(date_range[0]))&(df['Date']<=str(date_range[1]))]
            
            
            balance = claculate_current_balance(df)
            total_inflow, total_outflow = df['Inflow'].sum(), df['Outflow'].sum()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Balance")
                st.subheader(balance)


            with col2:
                st.subheader("Total Inflow")
                st.subheader(total_inflow)

            with col3:
                st.subheader("Total Outflow")
                st.subheader(total_outflow)
            
            # Plot inflow vs outflow
            df['Total Amount'] = df['Inflow'] - df['Outflow']
            date_wise_grped_data = df.groupby(by=['Date'], as_index=False)['Total Amount'].sum()
            fig = px.line(date_wise_grped_data, x='Date', y='Total Amount', title='Datewise Balance')
            st.plotly_chart(fig)

            # Plot inflow over time
            x = df['Date'].tolist()
            y1,y2  = df['Inflow'].tolist(), df['Outflow'].tolist()
            trace1 = go.Scatter(x=x, y=y1, mode='lines', name='Inflow Over Time')
            trace2 = go.Scatter(x=x, y=y2, mode='lines', name='Outflow Over Time')

            # Create layout
            layout = go.Layout(title='Inflow and Outflow Over Time',
                            xaxis=dict(title='X-axis Label'),
                            yaxis=dict(title='Y-axis Label'))
            fig = go.Figure(data=[trace1, trace2], layout=layout)

            # Display the figure
            st.plotly_chart(fig)


if __name__ == "__main__":
    main()
