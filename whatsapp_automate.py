import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import qrcode
import streamlit as st
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to send WhatsApp messages


def send_whatsapp_messages(phone_numbers, image_paths, message, description):
    # Set up Chrome options to run headless (without opening a browser window)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com/")
    st.image('qr_code.png')
    st.text("Scan the QR Code from your WhatsApp app to log in and press Enter")
    input("Press Enter after logging in successfully...")

    # Wait for the web app to load properly
    time.sleep(15)

    for phone_number, image_path in zip(phone_numbers, image_paths):
        # Search for the contact using the search bar
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[title='Search or start new chat']"))
        )
        search_box.click()
        time.sleep(1)

        # Input the phone number
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div._2_1wd.copyable-text.selectable-text"))
        )
        search_input.send_keys(phone_number)
        time.sleep(2)

        # Find the chat element and click on it
        try:
            chat = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//span[@title='{phone_number}']"))
            )
            chat.click()
        except:
            st.warning(f"Chat with {phone_number} not found. Skipping...")
            continue

        time.sleep(2)

        # Find the input field for the message
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div._13mgZ"))
        )

        # Send the message description and content
        message_box.send_keys(f"{description}\n\n{message}")
        message_box.send_keys(Keys.ENTER)
        time.sleep(2)

        # If you want to send an image, you can use this code to attach it
        if image_path:
            attachment_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div._3e4VU"))
            )
            attachment_button.click()
            time.sleep(1)

            image_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@type='file']"))
            )
            image_input.send_keys(image_path)
            time.sleep(3)

    driver.quit()

# Create the Streamlit web interface


def main():
    st.title("Automated WhatsApp Messages with Images")
    st.text("Please upload an Excel file with mobile numbers and image paths")

    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)

        if "Mobile Number" not in df.columns or "Image Path" not in df.columns:
            st.error(
                "The Excel file must contain 'Mobile Number' and 'Image Path' columns.")
            return

        message_description = st.text_area(
            "Message Description", "Check out this image:")
        message = st.text_area("Enter the message you want to send", "")

        if st.button("Send Messages"):
            phone_numbers = df["Mobile Number"].tolist()
            image_paths = df["Image Path"].tolist()

            # Generate the QR code and save it as an image
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data("https://web.whatsapp.com")
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("qr_code.png", "PNG")

            # Display the QR code in the Streamlit interface
            st.image('qr_code.png')
            st.text(
                "Scan the QR Code from your WhatsApp app to log in and press Enter")
            input("Press Enter after logging in successfully...")

            with st.spinner("Sending messages..."):
                send_whatsapp_messages(
                    phone_numbers, image_paths, message, message_description)

            st.success("Messages sent successfully!")


if __name__ == "__main__":
    main()
