from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
MAX_WAIT = 5

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):

        # Rapha decidiu utilizar o novo app TODO. Ele entra em sua pagina principal:
        self.browser.get(self.live_server_url)

        # Ele nota que o titulo da pagina menciona TODO
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ele eh convidado a entrar com um item TODO imediatamente
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Ele digita "Estudar testes funcionais" em uma caixa de texto
        inputbox.send_keys('Estudar testes funcionais')

        # Quando ele aperta enter, a pagina atualiza, e mostra a lista
        # "1: Estudar testes funcionais" como um item da lista # TODO
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Estudar testes funcionais')

        # Ainda existe uma caixa de texto convidado para adicionar outro item
        # Ele digita: "Estudar testes de unidade"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Estudar testes de unidade')
        inputbox.send_keys(Keys.ENTER)

        # A Pagina atualiza novamente, e agora mostra ambos os itens da sua lista
        self.wait_for_row_in_list_table('1: Estudar testes funcionais')
        self.wait_for_row_in_list_table('2: Estudar testes de unidade')

        # Rapha se pergunta se o site vai lembrar da sua lista. Entao, ele verifica que
        # o site gerou uma URL uni a para ele -- existe uma explicacao sobre essa feature

        # Ele visita a URL: a sua lista TODO ainda esta armazenada

        # Satisfeito, ele vai mimir

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Maria começa uma nova lista
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Estudar testes funcionais')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Estudar testes funcionais')

        # Ela nota que sua lista possui uma URL unica
        maria_list_url = self.browser.current_url
        self.assertRegex(maria_list_url, '/lists/.+')

        # Agora, um novo usuario, Joao, entra no site
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Joao visita a pagina inicial. Nao existe nenhum sinal da lista de Maria
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Estudar testes funcionais', page_text)
        self.assertNotIn('2: Estudar testes de unidade', page_text)

        # Joao inicia uma nova lista
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Comprar leite')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar leite')

        # Joao pega sua URL unica
        joao_list_url = self.browser.current_url
        self.assertRegex(joao_list_url, '/lists/.+')
        self.assertNotEqual(joao_list_url, maria_list_url)

        # Novamente, nao existe sinal da lista de Maria
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Estudar testes funcionais', page_text)
        self.assertIn('Comprar leite', page_text)

        # Satisfeitos, ambos vao dormir

class LayoutAndStylingTest(FunctionalTest):
    
    def test_layout_and_styling(self):
        # Rapha entra na home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Ele nota que o input box esta centralizado
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # Ele inicia uma nova lista e nota que o input
        # tambem esta centralizado
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
