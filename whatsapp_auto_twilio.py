# Complete code for sending automated WhatsApp messages using Streamlit and Twilio

# Importing required libraries
import streamlit as st
import openpyxl
from twilio.rest import Client

# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC4a8ae20a1465d1db3b4c7496a571263b'
TWILIO_AUTH_TOKEN = '3503c258da01f9f205bb1fbcfe69bd8f'
TWILIO_PHONE_NUMBER = '+923016636557'

# Function to send WhatsApp message using Twilio


def send_whatsapp_message(to_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(from_=f'whatsapp:{TWILIO_PHONE_NUMBER}',
                           to=f'whatsapp:{to_number}',
                           body=message)

# Streamlit interface


def main():
    st.title('WhatsApp Automation')

    # File upload
    uploaded_file = st.file_uploader('Upload Excel file', type=['xlsx'])

    if uploaded_file is not None:
        # Read the Excel file
        wb = openpyxl.load_workbook(uploaded_file)
        sheet = wb.active

        # Get mobile numbers and messages
        mobile_numbers = [str(cell.value) for cell in sheet['A'] if cell.value]
        messages = [cell.value for cell in sheet['B'] if cell.value]

        # Input message
        message = st.text_area('Enter your message:', '')

        if st.button('Send Messages'):
            if not message:
                st.error('Please enter a message!')
                return

            # Sending messages
            for i, number in enumerate(mobile_numbers):
                send_whatsapp_message(number, message)
                st.success(
                    f'Message {i+1}/{len(mobile_numbers)} sent to {number}')


if __name__ == '__main__':
    main()
