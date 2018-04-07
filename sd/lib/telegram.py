import ujson as json
import requests

## https://github.com/eternnoir/pyTelegramBotAPI/blob/master/telebot/apihelper.py


class bot:    
    def __init__(self, token, chat_id=None, proxy=None):
        self.token = token
        self.chat_id = chat_id
        self.proxy = proxy
        self.base_url = 'https://api.telegram.org/bot{0}/{1}'
        self.CONNECT_TIMEOUT = 3.5
        self.READ_TIMEOUT = 9999
    
    def get_url(self, url):
        response = requests.request('GET', url)
        content = response.content.decode('utf8')
        return content
    
    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js
    
    def get_updates(self, timeout=30, offset=None):
        request_url = self.base_url.format(self.token, 'getUpdates?timeout={}'.format(timeout))
        if offset:
            request_url += '&offset={}'.format(offset)
        js = self.get_json_from_url(request_url)
        return js
    
    def get_last_chat_id(self, updates):
        num_updates = len(updates['result'])
        last_update = num_updates - 1
        chat_id = updates['result'][last_update]['message']['chat']['id']
        return chat_id
    
    def send(self, text):
        if not self.chat_id:
            self.chat_id = self.get_last_chat_id(self.get_updates())
        self.send_message(text, self.chat_id)
    
    def send_message(self, text, chat_id):
        text = requests.quote_plus(text)
        method = 'sendMessage?parse_mode=Markdown&chat_id={0}&text={1}'.format(chat_id, text)
        request_url = self.base_url.format(self.token, method)
        response = requests.request('GET', request_url)


class ApiException(Exception):
    """
    This class represents an Exception thrown when a call to the Telegram API fails.
    In addition to an informative message, it has a `function_name` and a `result` attribute, which respectively
    contain the name of the failed function and the returned result that made the function to be considered  as
    failed.
    """
    def __init__(self, msg, function_name, result):
        super(ApiException, self).__init__("A request to the Telegram API was unsuccessful. {0}".format(msg))
        self.function_name = function_name
        self.result = result


# EOF