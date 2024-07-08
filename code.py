import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from datetime import datetime
from docx import Document

# Load data
df = pd.read_csv('C:\\Users\\\deeks\\Downloads\\hda1\\hda\\finaldata.csv')

# Initialize session state for login
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Function to check credentials
def check_credentials(username, password):
    return username == "rahul" and password == "rahul"  # Simplified for demo purposes

# Login and Signup
if not st.session_state['authenticated']:
    st.title('Hospital Data Analytics Login')
    
    # Login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if check_credentials(username, password):
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Invalid username or password")
else:
    st.title('Hospital Data Analysis')
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Data Entry", "Data Analytics", "Generate Report"])

    # Tab 1: Data Entry
    with tab1:
        st.header('Data Entry')
        input_data = {}

        # Create input fields for each column
        for column in df.columns:
            if 'Date' in column or column in ['In date', 'Out date']:
                input_data[column] = st.date_input(f'Select {column}')
            else:
                input_data[column] = st.text_input(f'Enter {column}')
        
        if st.button('Submit Data'):
            if all(input_data.values()):
                # Convert dates to string format
                for column in df.columns:
                    if 'Date' in column or column in ['In date', 'Out date']:
                        input_data[column] = input_data[column].strftime('%Y-%m-%d')
                
                new_data = {col: [input_data[col]] for col in df.columns}
                new_df = pd.DataFrame(new_data)
                df = pd.concat([df, new_df], ignore_index=True)
                df.to_csv('finaldata.csv', index=False)
                st.success('Data submitted successfully')
                st.write(df.tail())
                
                # Clear input fields by resetting the state
                st.experimental_rerun()
            else:
                st.error('Please fill in all fields before submitting')

    # Tab 2: Data Analytics
    with tab2:
        st.header('Data Analytics')

        if df.empty:
            st.error("The dataset is empty. Please add data in the 'Data Entry' tab.")
        else:
            # Chart 1: Age distribution
            if st.button('Show Age Distribution'):
                try:
                    fig, ax = plt.subplots()
                    sns.histplot(df['PatientAge'], bins=20, ax=ax)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error displaying chart: {e}")
            
            # Chart 2: Gender distribution
            if st.button('Show Gender Distribution'):
                try:
                    fig, ax = plt.subplots()
                    sns.countplot(x='PatientGender', data=df, ax=ax)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error displaying chart: {e}")
            
            # Chart 3: Severity distribution
            if st.button('Show Severity Distribution'):
                try:
                    fig, ax = plt.subplots()
                    sns.countplot(x='Severity', data=df, ax=ax)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error displaying chart: {e}")
            
            # Chart 4: Final bill distribution
            if st.button('Show Final Bill Distribution'):
                try:
                    fig, ax = plt.subplots()
                    sns.histplot(df['Final bill'], bins=20, ax=ax)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error displaying chart: {e}")
            
            # Chart 5: Combination of Age and Severity
            if st.button('Show Age vs Severity'):
                try:
                    fig, ax = plt.subplots()
                    sns.boxplot(x='Severity', y='PatientAge', data=df, ax=ax)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error displaying chart: {e}")
            
            # Chart 6: Pie chart for Severity distribution
            if st.button('Show Severity Distribution Pie Chart'):
                try:
                    fig, ax = plt.subplots()
                    df['Severity'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
                    ax.set_ylabel('')
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error displaying chart: {e}")
            
            # Chart 7: Pie chart for Patient region distribution
            if st.button('Show PatientRegion Pie Chart'):
                try:
                    fig, ax = plt.subplots()
                    df['PatientRegion'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
                    ax.set_ylabel('')
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error displaying chart: {e}")

    # Tab 3: Generate Report
    with tab3:
        st.header('Generate Report')
        
        # Date input
        start_date = st.date_input('Start Date')
        end_date = st.date_input('End Date')

        def generate_report(start_date, end_date):
            try:
                # Ensure start_date and end_date are strings
                start_date = start_date.strftime('%Y-%m-%d')
                end_date = end_date.strftime('%Y-%m-%d')

                filtered_df = df[(df['In date'] >= start_date) & (df['Out date'] <= end_date)]
                
                # Calculations for the report
                total_patients = filtered_df.shape[0]
                avg_age = filtered_df['PatientAge'].mean()
                gender_distribution = filtered_df['PatientGender'].value_counts()
                total_final_bill = filtered_df['Final bill'].sum()
                severity = filtered_df['Severity'].value_counts()
                most_severe = severity.idxmax() if not severity.empty else 'N/A'
                most_severe_count = severity.max() if not severity.empty else 0
                patient_region = filtered_df['PatientRegion'].value_counts()
                most_common_region = patient_region.idxmax() if not patient_region.empty else 'N/A'
                most_common_region_count = patient_region.max() if not patient_region.empty else 0

                # Generate the report document
                doc = Document()
                doc.add_heading('HOSPITAL ANALYTICS REPORT', 0)
                doc.add_heading(f'Date Range: {start_date} to {end_date}', level=1)

                doc.add_heading('CONCLUSIONS:', level=1)
                doc.add_paragraph(f'Total patients: {total_patients}')
                doc.add_paragraph(f'Average age: {avg_age:.2f}')
                doc.add_paragraph(f'Gender distribution: {gender_distribution.to_dict()}')
                doc.add_paragraph(f'Total final bill: {total_final_bill:.2f}')
                doc.add_paragraph(f'Most common severity: {most_severe} with {most_severe_count} cases')

                # Add conclusion statements
                doc.add_heading('Detailed Analysis and Conclusions', level=1)
                doc.add_paragraph(f'The hospital admitted a total of {total_patients} patients between {start_date} and {end_date}.')
                doc.add_paragraph(f'The average age of the patients was {avg_age:.2f} years.')
                doc.add_paragraph(f'The gender distribution among the patients was as follows: {gender_distribution.to_dict()}.')
                doc.add_paragraph(f'The most common severity level observed was "{most_severe}" with {most_severe_count} cases.')

                # Adding more detailed conclusions
                if most_common_region_count >5:  # Example threshold
                    doc.add_paragraph(f"Consider opening a new branch in {most_common_region} due to high patient inflow.")
                if most_severe_count > 2:  # Example threshold
                    doc.add_paragraph(f"Additional resources may be needed to handle the high number of {most_severe} cases.")

                doc_file = 'monthly_Report.docx'
                doc.save(doc_file)
                st.success(f'Report generated and saved as {doc_file}')
            except Exception as e:
                st.error(f"Error generating report: {e}")

        if st.button('Generate Report'):
            if start_date and end_date:
                generate_report(start_date, end_date)
            else:
                st.error("Please select both start and end dates")