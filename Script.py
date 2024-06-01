import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# Define the path to your chromedriver
chrome_driver_path = r"C:\Users\chatu\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"   # Update this path
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
# Initialize the webdriver
driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)

# Function to load contacts from CSV
def load_contacts_from_csv(file_path):
    contacts = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            contacts.append(row['mbn'])
    return contacts

# Function to open WhatsApp Web
def open_whatsapp():
    driver.get('https://web.whatsapp.com')
    print("Please scan the QR code to log in.")
    time.sleep(10)  # Wait time to scan the QR code

# Function to add contacts to a WhatsApp group
def add_contacts_to_group(contacts, group_name):
    # Search and open the group chat
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.clear()
    search_box.send_keys(group_name)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    # Click on the second menu button to open the dropdown menu
    menu_buttons = driver.find_elements(By.XPATH, '//div[@role="button"][@title="Menu"]')
    if len(menu_buttons) < 2:
        print("Could not find the second menu button.")
        return
    menu_buttons[1].click()
    time.sleep(2)

    # Click on the "Group info" option from the dropdown menu
    group_info_option = driver.find_element(By.XPATH, '//*[@id="app"]/div/span[5]/div/ul/div/div/li[1]/div')
    group_info_option.click()
    time.sleep(3)

    # Click on Add Participant button
    add_participant_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[5]/span/div/span/div/div/div/section/div[7]/div[2]/div[1]/div[1]/div')
    add_participant_button.click()
    time.sleep(3)

    for contact in contacts:
        # Enter the contact number in the participant search field
        participant_search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        participant_search_box.click()
        
        # Clear the search box using backspace key
        participant_search_box.send_keys(Keys.CONTROL + "a")
        participant_search_box.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        
        participant_search_box.send_keys(contact)
        time.sleep(2)

        try:
            # Select the contact from the search results
            contact_result = driver.find_element(By.XPATH, f'//span[contains(@title, "{contact}")]')
            contact_result.click()
            time.sleep(1)
        except Exception as e:
            print(f"Could not find or add contact {contact}: {e}")
            continue  # Move to the next contact if there's an issue

    # Confirm adding participants
    confirm_button = driver.find_element(By.XPATH, '//div[@role="button"][@data-testid="add-participant-approve"]')
    confirm_button.click()
    time.sleep(20)


# Main execution
if __name__ == "__main__":
    # Load contacts from CSV
    contacts = load_contacts_from_csv('contacts.csv')
    print(f"Loaded {len(contacts)} contacts from CSV.")

    # Open WhatsApp Web
    open_whatsapp()

    # Specify the name of the group you want to add contacts to
    group_name = 'Hire me internship interview'  # Update with your actual group name

    # Add contacts to the specified WhatsApp group
    add_contacts_to_group(contacts, group_name)

    # Close the webdriver
    driver.quit()
