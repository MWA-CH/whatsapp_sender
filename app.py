import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def send_message(driver, mobile_number):
    message = "Hello, this is an automated message sent using Python!"

    # Construct the WhatsApp URL with the phone number and message
    url = f"https://web.whatsapp.com/send?phone={mobile_number}&text={message}"

    # Open the WhatsApp URL
    driver.get(url)

    # Wait for the WhatsApp chat window to load
    time.sleep(5)

    # Find the input field and send the message
    input_field = driver.find_element_by_xpath(
        '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    input_field.send_keys(Keys.ENTER)
    return


def main():
    st.title("Automated WhatsApp Message Sender")

    st.write("Upload an Excel file with a column named 'Mobile' containing the phone numbers to send messages to.")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write(df)

        # Initialize Chrome WebDriver
        driver = webdriver.Chrome()

        # Open WhatsApp Web
        driver.get("https://web.whatsapp.com/")
        st.write("Scan the QR code on WhatsApp Web to continue...")

        # Wait for the user to scan the QR code manually
        while True:
            try:
                driver.find_element_by_xpath(
                    '//*[@id="side"]/div[1]/div/label/input')
                st.write("QR code scanned successfully!")
                break
            except:
                time.sleep(2)

        st.write("Sending messages...")
        # Loop through the phone numbers in the DataFrame and send messages
        for index, row in df.iterrows():
            mobile_number = str(row["Mobile"])
            send_message(driver, mobile_number)
            st.write(f"Message sent to {mobile_number}")
            # Add a delay between messages to avoid rate-limiting issues
            time.sleep(2)

        st.write("All messages sent!")
        driver.quit()


if __name__ == "__main__":
    main()
