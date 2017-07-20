from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.webdriver import WebDriver

class Base:
    @classmethod
    def __init__(self, p_live_server_url):
        self.live_server_url = p_live_server_url
        self.driver = WebDriver()

    @classmethod
    def pause(self, p_seconds):
        try:
            WebDriverWait(self.driver, p_seconds).until(EC.title_is('pause'))
        except:
            pass

    @classmethod
    def grid_cell_doubleclick(self, p_element):
        ActionChains(self.driver).double_click(p_element).perform()

    @classmethod
    def grid_cell_input(self, p_element, p_text):
        self.grid_cell_doubleclick(p_element)
        for k in range(0, len(p_element.text)):
            p_element.send_keys(Keys.BACKSPACE)
        p_element.send_keys(p_text)

    @classmethod
    def action_login(self, p_username, p_password, p_expectsuccess=True):
        self.driver.get('{0}{1}'.format(self.live_server_url, '/login/'))
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        username_input = self.driver.find_element_by_id('txt_user')
        username_input.send_keys(p_username)
        password_input = self.driver.find_element_by_id('txt_pwd')
        password_input.send_keys(p_password)
        self.driver.find_element_by_xpath("//button[. = 'Sign in']").click()
        if p_expectsuccess:
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'header')))
            except:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'div_alert_text')))
        else:
            try:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'div_alert_text')))
            except:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'header')))

    @classmethod
    def action_create_user(self, p_username, p_password, p_superuser):
        self.driver.get('{0}{1}'.format(self.live_server_url, '/users/'))
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        assert 'OmniDB' in self.driver.title
        self.driver.find_element_by_xpath("//button[. = 'New User']").click()
        username_cell = self.driver.find_element_by_xpath("//tbody/tr[last()]/td[1]")
        self.grid_cell_input(username_cell, p_username)
        password_cell = self.driver.find_element_by_xpath("//tbody/tr[last()]/td[2]")
        self.grid_cell_input(password_cell, p_password)
        if p_superuser:
            superuser_cell = self.driver.find_element_by_xpath("//tbody/tr[last()]/td[3]")
            self.grid_cell_doubleclick(superuser_cell)
        self.driver.find_element_by_tag_name('body').click()
        self.driver.find_element_by_xpath("//button[. = 'Save Data']").click()

class Login(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(self):
        super(Login, self).setUpClass()
        self.base = Base(self.live_server_url)
        self.driver = self.base.driver

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super(Login, self).tearDownClass()

    def test_firstlogin_ok(self):
        self.base.action_login('admin', 'admin')
        assert '/workspace/' in self.driver.current_url

    def test_firstlogin_nok(self):
        self.base.action_login('admin', 'ad', False)
        assert '/login/' in self.driver.current_url


class Users(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(self):
        super(Users, self).setUpClass()
        self.base = Base(self.live_server_url)
        self.driver = self.base.driver

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super(Users, self).tearDownClass()

    def test_create_superuser(self):
        self.base.action_login('admin', 'admin')
        self.base.action_create_user('supertest', 'test', True)

    def test_create_normaluser(self):
        self.base.action_login('admin', 'admin')
        self.base.action_create_user('normaltest', 'test', False)
