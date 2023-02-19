import pytest
from time import sleep
from selenium import webdriver
from Test_Data import OHRM_Data
from Test_Locators import Locators
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class Test_OrangeHRM():

    @pytest.fixture
    def Web_Page_Booting(self):
        self.driver = webdriver.Firefox(service=Service (GeckoDriverManager().install()))
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 15)
        yield
        self.driver.close()
    
    # Test Case to Check whether the User is able to login Orange HRM with Valid Username and Password
    def test_TC_Login_01 (self, Web_Page_Booting):
        try:
            self.driver.get(OHRM_Data.OHRM_TEST_Data().url)
            cookie_before = self.driver.get_cookies()[0]['value']
            OHRM_USERNAME = self.wait.until(EC.presence_of_element_located((By.NAME, Locators.html_locators().username_locator)))
            OHRM_USERNAME.send_keys(OHRM_Data.OHRM_TEST_Data().username)
            self.driver.find_element(by=By.NAME, value= Locators.html_locators().password_locator).send_keys(OHRM_Data.OHRM_TEST_Data().password)
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().signin_locator).click()
            cookie_after = self.driver.get_cookies()[0]['value']
            assert cookie_before != cookie_after
            print('User Logged in successfully!')
        except NoSuchElementException:
            print('Element Missing')

    # Test Case to Check whether the User is not allowed to login Orange HRM with Invalid Password
    def test_TC_Login_02 (self, Web_Page_Booting):
        try:
            self.driver.get(OHRM_Data.OHRM_TEST_Data().url)
            cookie_before = self.driver.get_cookies()[0]['value']
            OHRM_USERNAME = self.wait.until(EC.presence_of_element_located((By.NAME, Locators.html_locators().username_locator)))
            OHRM_USERNAME.send_keys(OHRM_Data.OHRM_TEST_Data().username)
            self.driver.find_element(by=By.NAME, value= Locators.html_locators().password_locator).send_keys(OHRM_Data.OHRM_TEST_Data().invpassword)
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().signin_locator).click()
            cookie_after = self.driver.get_cookies()[0]['value']
            assert cookie_before == cookie_after
            print('Invalid Password, Login Unsuccessful!')
        except NoSuchElementException:
            print('Element Missing')

    # Test Case to Check whether the User is able to Add and Create Login for the New Employee
    def test_TC_PIM_01 (self, Web_Page_Booting):
        try:
            self.driver.get(OHRM_Data.OHRM_TEST_Data().url)
            OHRM_USERNAME = self.wait.until(EC.presence_of_element_located((By.NAME, Locators.html_locators().username_locator)))
            OHRM_USERNAME.send_keys(OHRM_Data.OHRM_TEST_Data().username)
            self.driver.find_element(by=By.NAME, value= Locators.html_locators().password_locator).send_keys(OHRM_Data.OHRM_TEST_Data().password)
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().signin_locator).click()

            # Navigating to PIM Tab
            PIM = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().PIM_locator)))
            self.action.move_to_element(PIM).click(PIM).perform()

            # Adding an Employee in PIM
            Add_Tab = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().AddEmp_locator)))
            self.action.move_to_element(Add_Tab).click(Add_Tab).perform()
            Add_Emp = self.wait.until(EC.presence_of_element_located((By.NAME, Locators.html_locators().Add_fn_locator)))
            Add_Emp.send_keys(OHRM_Data.OHRM_TEST_Data().FirstName)
            self.driver.find_element(by=By.NAME, value= Locators.html_locators().Add_mn_locator).send_keys(OHRM_Data.OHRM_TEST_Data().MiddleName)
            self.driver.find_element(by=By.NAME, value= Locators.html_locators().Add_ln_locator).send_keys(OHRM_Data.OHRM_TEST_Data().LastName)
            clear_input = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().Emp_ID_locator)))
            self.action.move_to_element(clear_input).double_click(clear_input).send_keys(Keys.DELETE).perform()
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().Emp_ID_locator).send_keys(OHRM_Data.OHRM_TEST_Data().Emp_ID)

            # Creating Login for the New Employee
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().Create_login_locator).click()
            Emp_Login = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().Login_id_locator)))
            Emp_Login.send_keys(OHRM_Data.OHRM_TEST_Data().Login_ID)
            C_Login_P = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().Login_pass_locator)))
            C_Login_P.send_keys(OHRM_Data.OHRM_TEST_Data().Login_password)
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().Login_confpass_locator).send_keys(OHRM_Data.OHRM_TEST_Data().Login_password)
            sleep(2)
            Submit = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().Add_Emp_Submit_locator)))
            Submit.click()
            print('New Employee Data and Login Created Successfully')
        except NoSuchElementException:
            print('Element Missing')

    # Test Case to Check whether the User is able to Edit the existing details of an Employee.
    def test__TC_PIM_02 (self, Web_Page_Booting):
        try:
            self.driver.get(OHRM_Data.OHRM_TEST_Data().url)
            OHRM_USERNAME = self.wait.until(EC.presence_of_element_located((By.NAME, Locators.html_locators().username_locator)))
            OHRM_USERNAME.send_keys(OHRM_Data.OHRM_TEST_Data().username)
            self.driver.find_element(by=By.NAME, value= Locators.html_locators().password_locator).send_keys(OHRM_Data.OHRM_TEST_Data().password)
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().signin_locator).click()

            # Navigating to PIM Tab
            PIM = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().PIM_locator)))
            self.action.move_to_element(PIM).click(PIM).perform()
            
            # Search the Existing Employee with Name and Employee ID
            Search_Name = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().Searchby_Name_locator)))
            Search_Name.send_keys(OHRM_Data.OHRM_TEST_Data().Search_Name)
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().Searchby_ID_locator).send_keys(OHRM_Data.OHRM_TEST_Data().Emp_ID)
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().Search_locator).click()
            sleep(2)

            # Edit and Save the Last Name of the Existing Employee 
            Edit_data = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().Edit_locator)))
            Edit_data.click()
            Edit_last_name = self.wait.until(EC.presence_of_element_located((By.NAME, Locators.html_locators().Add_ln_locator)))
            self.action.move_to_element(Edit_last_name).double_click(Edit_last_name).send_keys(Keys.DELETE).perform()
            Edit_last_name.send_keys(OHRM_Data.OHRM_TEST_Data().New_LastName)
            sleep(3)
            Save_Edit = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().Save_locator)))
            Save_Edit.click()
            print('Employee details Edited Successfully')
        except NoSuchElementException:
            print('Element Missing')
    
    # Test Case to Check whether the User is able to delete the Employee Details in Orange HRM PIM
    def test_TC_PIM_03 (self, Web_Page_Booting):
        try:
            self.driver.get(OHRM_Data.OHRM_TEST_Data().url)
            OHRM_USERNAME = self.wait.until(EC.presence_of_element_located((By.NAME, Locators.html_locators().username_locator)))
            OHRM_USERNAME.send_keys(OHRM_Data.OHRM_TEST_Data().username)
            self.driver.find_element(by=By.NAME, value= Locators.html_locators().password_locator).send_keys(OHRM_Data.OHRM_TEST_Data().password)
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().signin_locator).click()

            # Navigating to PIM Tab
            PIM = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().PIM_locator)))
            self.action.move_to_element(PIM).click(PIM).perform()
 
            # Search the Existing Employee with Name and Employee ID
            Search_Name = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().Searchby_Name_locator)))
            Search_Name.send_keys(OHRM_Data.OHRM_TEST_Data().Delete_Search_Name)
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().Searchby_ID_locator).send_keys(OHRM_Data.OHRM_TEST_Data().Emp_ID)
            self.driver.find_element(by=By.XPATH, value= Locators.html_locators().Search_locator).click()
            sleep(3)

            # Deleting the Existing Employee from PIM
            Delete_Emp = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().Delete_locator)))
            Delete_Emp.click()
            sleep(1)
            Delete_Confirm = self.wait.until(EC.presence_of_element_located((By.XPATH, Locators.html_locators().Delete_Confirm_locator)))
            Delete_Confirm.click()
            print('Employee details Deleted Successfully')
        except NoSuchElementException:
            print('Element Missing')