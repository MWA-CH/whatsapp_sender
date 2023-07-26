# CAN: Import the necessary libraries
import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# CAN: Define the Streamlit web app


def main():
    # CAN: Set the page title and description
    st.title("WhatsApp Message Sender")
    st.subheader("Send WhatsApp messages with images and text")

    # CAN: Add file upload options for Excel sheet and image
    st.sidebar.title("Upload Options")
    excel_file = st.sidebar.file_uploader(
        "Upload Excel File", type=["xls", "xlsx"])
    image_file = st.sidebar.file_uploader(
        "Upload Image (Optional)", type=["jpg", "png", "jpeg"])

    # CAN: Add input field for text message
    text_message = st.text_area("Enter the text message to send")

    # CAN: Add a button to trigger the message sending process
    if st.button("Send Messages"):
        # CAN: Validate that the user has provided the Excel sheet
        if excel_file is not None:
            # CAN: Read the Excel sheet into a pandas DataFrame
            df = pd.read_excel(excel_file)

            # CAN: Display the DataFrame on the web page (optional, for user verification)
            st.dataframe(df)

            # CAN: Get the phone numbers from the Excel sheet
            phone_numbers = df["Phone Number"].tolist()

            # CAN: Set up the Selenium WebDriver for Chrome
            driver = webdriver.Chrome()
            driver.get("https://web.whatsapp.com")
            st.info("Please scan the QR code on WhatsApp Web to continue...")

            # CAN: Wait for the user to scan the QR code and log in
            while "WhatsApp" not in driver.title:
                time.sleep(1)

            # CAN: Iterate through each phone number and send the WhatsApp message
            for phone_number in phone_numbers:
                try:
                    # CAN: Open a new chat with the phone number
                    driver.get(
                        f"https://web.whatsapp.com/send?phone={phone_number}")
                    # CAN: Wait until the chat is opened successfully
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@contenteditable='true']")))

                    # CAN: Check if the chat is opened successfully
                    chat_title = driver.find_element_by_xpath(
                        f"//span[@title='{phone_number}']")
                    if chat_title:
                        # CAN: Upload the image if provided
                        if image_file is not None:
                            attachment_icon = driver.find_element_by_xpath(
                                "//div[@title='Attach']")
                            attachment_icon.click()
                            time.sleep(2)

                            image_input = driver.find_element_by_xpath(
                                "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
                            image_input.send_keys(image_file.name)
                            time.sleep(2)

                        # CAN: Enter the text message
                        message_box = driver.find_element_by_xpath(
                            "//div[@contenteditable='true']")
                        message_box.send_keys(text_message)

                        # CAN: Send the message
                        send_button = driver.find_element_by_xpath(
                            "//span[@data-icon='send']")
                        send_button.click()

                        # CAN: Wait for a few seconds before proceeding to the next number
                        time.sleep(5)

                except Exception as e:
                    # CAN: Display any errors or exceptions on the web page
                    st.error(
                        f"Error sending message to {phone_number}: {str(e)}")

            # CAN: Close the browser after sending messages to all numbers
            driver.quit()

            # CAN: Display a success message after sending messages
            st.success("WhatsApp messages sent successfully to all numbers!")

        else:
            st.warning("Please upload the Excel file before sending messages.")


# CAN: Run the Streamlit web app
if __name__ == "__main__":
    main()
