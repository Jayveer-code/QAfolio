import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def main_function(driver, action, link_text):
    try:
        element = driver.find_element(By.LINK_TEXT, link_text)
        action.move_to_element(element).perform()  
        time.sleep(3)  
        element.click() 
    except Exception as e:
        print(f"Error Occuring with {link_text}: {e}")
        return False
    return True

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://jayveerportfolio.netlify.app/")
    yield driver
    driver.quit()

def test_navigation_links(driver):
    actions = ActionChains(driver)
    menu_items = ["About", "Services", "Portfolio", "Contact"]  
    for item in menu_items:
        assert main_function(driver, actions, item), f"Failed tomove {item}"
    assert main_function(driver, actions, "Home"), "Failed to move Home"

def test_social_links(driver):
    social_links = {
        "Twitter": "//div[@class='social-media']/a[contains(@href, 'twitter.com') or contains(@href, 'x.com')]",
        "LinkedIn": "//div[@class='social-media']/a[contains(@href, 'linkedin.com')]",
        # "Instagram": "//div[@class='social-media']/a[contains(@href, 'instagram.com')]"
    }

    for name, xpath in social_links.items():
        time.sleep(2)
        links = driver.find_elements(By.XPATH, xpath)  
        if links: 
            link = links[0]
            href = link.get_attribute("href")
            print(f"Clicking on {name}: {href}")
            ActionChains(driver).move_to_element(link).click().perform()
            time.sleep(3)
            driver.back()
            time.sleep(1)
        else:
            print(f"{name} link not found, skipping...")

def test_portfolio_hover(driver):
    actions = ActionChains(driver)
    assert main_function(driver, actions, "Portfolio"), "Failed to click Portfolio"
    time.sleep(2)

    portfolio_boxes = driver.find_elements(By.CLASS_NAME, "portfolio-box")
    for idx, box in enumerate(portfolio_boxes, start=1):
        ActionChains(driver).move_to_element(box).perform()
        print(f"Hovered over element {idx} successfully")
        time.sleep(3)

def test_contact_form(driver):
    actions = ActionChains(driver)
    assert main_function(driver, actions, "Contact"), "Failed to click Contact"
    time.sleep(3)

    form_data = {
        '//input[@type="text" and @placeholder="Full Name"]': "John Doe",
        '//input[@type="email" and @placeholder="Email Address"]': "johndoe@example.com",
        '//input[@type="number" and @placeholder="Mobile Number"]': "9876543210",
        '//input[@type="text" and @placeholder="Email Subject"]': "9876543210",
        '//textarea[@placeholder="Your Message"]': "This is a test message."
    }
    for xpath, value in form_data.items():
        driver.find_element(By.XPATH, xpath).send_keys(value)
        print(f"Entered: {value}")
    
    print("Form filled successfully!")
    driver.find_element(By.XPATH, "//*[@type='submit']").click()
    print("Send Message button clicked successfully")
    time.sleep(4)

def test_popup_window(driver):
    success_popup = driver.switch_to.alert
    print("Message Sent Successfully Popup Appeared")
    success_popup.accept()
    time.sleep(4)
    print("Popup OK clicked")
    
def test_responsive_design(driver):
    devices = [
        (1920, 1080, "Full HD"),
        (768, 1024, "iPad Pro portrait"),
        (375, 667, "iPhone 8")
    ]
    for width, height, device in devices:
        driver.set_window_size(width, height)
        print(f"Testing on {device} successfully.")
        driver.get("https://jayveerportfolio.netlify.app/")
        time.sleep(10)
    time.sleep(1)
