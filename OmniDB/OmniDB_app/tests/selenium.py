from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Get geckodriver from https://github.com/mozilla/geckodriver/releases and put in your $PATH
from selenium.webdriver.firefox.webdriver import WebDriver

class Base:
    @classmethod
    def __init__(self, p_live_server_url):
        self.live_server_url = p_live_server_url
        self.driver = WebDriver()

    @classmethod
    def action_login(self, p_username, p_password):
        self.driver.get('{0}{1}'.format(self.live_server_url, '/login/'))
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        assert 'OmniDB' in self.driver.title
        username_input = self.driver.find_element_by_id('txt_user')
        username_input.send_keys(p_username)
        password_input = self.driver.find_element_by_id('txt_pwd')
        password_input.send_keys(p_password)
        self.driver.find_element_by_xpath("//button[. = 'Sign in']").click()


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
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'header')))
        assert '/connections/' in self.driver.current_url

    def test_firstlogin_nok(self):
        self.base.action_login('admin', 'ad')
        alert = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'div_alert_text')))
        assert 'Invalid username or password.' in alert.text
