from time import sleep

import chromedriver_autoinstaller
import selenium
from behave import *
from selenium.webdriver.common.by import By

chromedriver_autoinstaller.install()
driver: selenium.webdriver


# Login to the application
@given('I am on the login page')
def step_login_page(context):
    global driver
    driver = selenium.webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://opensource-demo.orangehrmlive.com/')
    sleep(3)
    assert driver.find_element(By.CLASS_NAME, 'orangehrm-login-form')


@when('I enter username and password')
def step_enter_username_password(context):
    global driver
    username = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/div/div/p[1]')
    username = username.text.split('Username : ')[1]
    password = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/div/div/p[2]')
    password = password.text.split('Password : ')[1]
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)


@when('I click on login button')
def step_click_login_button(context):
    global driver
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[3]/button').click()
    sleep(3)


@then('I should see the Dashboard page')
def step_dashboard_page(context):
    global driver
    assert driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[1]/div[1]/span/h6').text \
           == 'Dashboard'


# Add new job
@given('I am on the admin page')
def step_admin_page(context):
    global driver
    try:
        driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers')
    except:
        step_login_page(context)
        step_enter_username_password(context)
        step_click_login_button(context)
        driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers')
    sleep(3)
    assert driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[1]/div[1]/span/h6[2]').text \
           == 'User Management'


@when('I go to the jobs page')
def step_jobs_page(context):
    global driver
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[2]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[2]/ul/li[1]/a').click()
    sleep(3)
    assert driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[1]/div[1]/span/h6[2]').text == 'Job'


@when('I click on add new job button')
def step_add_new_job_button(context):
    global driver
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div[1]/div/button').click()
    sleep(3)
    assert driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/h6').text == 'Add Job Title'


@when('I enter job details')
def step_enter_job_details(context):
    global driver
    import os
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div/div[2]/input') \
        .send_keys('QA Engineer KPI')
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[2]/div/div[2]/textarea') \
        .send_keys('QA Engineer is responsible for testing the software')
    driver.find_element(By.XPATH, "//input[@type='file']") \
        .send_keys(f'{os.getcwd()}\\job.txt')
    sleep(10)


@then('I click on save button')
def step_click_save_button(context):
    global driver
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[5]/button[2]').click()
    sleep(3)


# Delete my job
@when('I should find and delete my job')
def step_see_my_job(context):
    global driver
    quantity = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div[2]/div/span').text
    quantity = int(quantity.split('(')[1].split(')')[0])
    for i in range(quantity):
        card_element = driver.find_element(By.XPATH, f'//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div[3]/div/div['
                                                     f'2]/div[{i + 1}]/div/div[2]/div')
        if card_element.text == 'QA Engineer KPI':
            driver.find_element(By.XPATH,
                                f'//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div[3]/div/div[2]/div[{i + 1}]/div/div['
                                f'4]/div/button[1]').click()
            sleep(1)
            driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div/div/div[3]/button[2]').click()
            sleep(1)
            assert True
            break
    else:
        assert False


@then('I should not see my job in the list')
def step_not_see_my_job(context):
    global driver
    step_jobs_page(context)
    quantity = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div[2]/div/span').text
    quantity = int(quantity.split('(')[1].split(')')[0])
    for i in range(quantity):
        card_element = driver.find_element(By.XPATH, f'//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div[3]/div/div['
                                                     f'2]/div[{i + 1}]/div/div[2]/div')
        if card_element.text == 'QA Engineer KPI':
            assert False
    else:
        assert True


# Logout from the application and close the browser
@when('I click on logout button')
def step_logout_button(context):
    global driver
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[1]/div[2]/ul/li/span').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[1]/div[2]/ul/li/ul/li[4]/a').click()
    sleep(3)


@when('I should see the login page')
def step_login_page(context):
    global driver
    assert driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/h5').text == 'Login'


@then('I close the browser')
def step_close_browser(context):
    global driver
    driver.close()
    driver.quit()
    try:
        print(driver.current_url)
    except:
        assert True
        return
    assert False
