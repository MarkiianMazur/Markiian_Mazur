from behave import given, when, then
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from time import sleep

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
driver: webdriver.Chrome = None


# Verify Homepage Title
@given('I am on the EPAM homepage')
def step_given_on_homepage(context):
    global driver
    if driver is None:
        driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
        driver.maximize_window()  # Maximize the browser window
    driver.get('https://www.epam.com/')  # Open EPAM homepage


@when('I retrieve the page title')
def step_when_retrieve_page_title(context):
    global driver
    context.title = driver.title


@then('the title should be "EPAM | Software Engineering & Product Development Services"')
def step_then_check_title(context):
    global driver
    assert context.title == 'EPAM | Software Engineering & Product Development Services'


# Search for Careers
@when('I click on the search icon')
def step_when_click_search_icon(context):
    global driver
    driver.find_element(By.CLASS_NAME, 'header-search__button').click()
    sleep(2)


@given('I enter "Careers" in the search bar')
def step_when_enter_careers(context):
    global driver
    driver.find_element(By.ID, 'new_form_search').send_keys('Careers')


@given('I click on the search submit')
def step_given_click_search(context):
    global driver
    driver.find_element(By.CLASS_NAME, 'header-search__submit').click()
    sleep(3)


@given('I click on the "Careers" link in the search results')
def step_given_click_careers_link(context):
    global driver
    search_results = driver.find_elements(By.CLASS_NAME, 'search-results__item')
    href = search_results[0].find_element(By.CLASS_NAME, 'search-results__title-link').get_property('href')
    driver.get(href)
    sleep(2)


@then('I should be redirected to the careers page')
def step_then_check_careers_page(context):
    global driver
    assert driver.title == 'Explore Professional Growth Opportunities | EPAM Careers'


# Verify Social Media Icons
@when('I check the social media section')
def step_given_check_social_media(context):
    global driver
    assert driver.find_element(By.CLASS_NAME, 'social')
    sleep(2)


@then('I should see icons for Facebook, Twitter, LinkedIn, and Instagram')
def step_then_check_social_media_icons(context):
    global driver
    social_elements = driver.find_elements(By.CLASS_NAME, 'social-link')
    for element in social_elements:
        assert element.is_displayed()


# Navigate to Services Page
@when('I click on the "Services" link in the navigation menu')
def step_when_click_services_link(context):
    global driver
    driver.find_element(By.CLASS_NAME, 'top-navigation__item-link').click()
    sleep(2)


@then('I should be redirected to the services page')
def step_then_check_services_page(context):
    global driver
    assert driver.title == 'Services | EPAM'


# Contact EPAM
@when('I click on the "Contact" link in the navigation menu')
def step_when_click_contact_link(context):
    global driver
    driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[1]/header/div/a[2]').click()
    sleep(2)


@then('I should see a contact form')
def step_then_check_contact_form(context):
    global driver
    print(driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div[2]/section/div[3]/div[1]/div/p/span/span').text)
    assert driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div[2]/section/div[3]/div[1]/div/p/span/span').text \
           == 'Contact Us'


# Verify Footer Links
@when('I scroll to the bottom of the page')
def step_when_scroll_to_bottom(context):
    global driver
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(10)


@then('I should see links for "About", "Services", "Industries", "Insights", "Careers", and "Contact" in the footer')
def step_then_check_footer_links(context):
    global driver
    footer_elements = driver.find_elements(By.CLASS_NAME, 'footer__link')
    footer_links = ['About', 'Services', 'Industries', 'Insights', 'Careers', 'Contact']
    for element in footer_elements:
        assert element.text in footer_links
        assert element.is_displayed()


# Verify Language Options
@when('I click on the language selector in the header')
def step_when_click_language_selector(context):
    global driver
    driver.find_element(By.CLASS_NAME, 'location-selector__button').click()
    sleep(2)


@then('I should see options to switch between English, SNG, and Ukrainian')
def step_then_check_language_options(context):
    global driver
    language_elements = driver.find_elements(By.CLASS_NAME, 'location-selector__link active')
    language_options = ['Global', 'СНГ', 'Україна']
    for element in language_elements:
        assert element.text in language_options
        assert element.is_displayed()


# Verify homepage slider
@then('I should see a slider with 3 images')
def step_then_check_slider(context):
    global driver
    assert driver.find_element(By.CLASS_NAME, 'slider__pagination--sum-page').text == '/ 03'
    slider_elements_active = driver.find_elements(By.CLASS_NAME, 'owl-item active')
    for element in slider_elements_active:
        assert element.is_displayed()


# Close the browser
@when('I close the browser')
def step_when_close_browser(context):
    global driver
    driver.close()
    driver.quit()


@then('The browser should close')
def step_then_check_browser_closed(context):
    global driver
    try:
        print(driver.current_url)
    except:
        assert True
        return
    assert False
