import requests

token = '7764910871:AAEImdb2IGshCOPtFXLzshPn6PqHSkSdLAU'

def sendMessage(chat_id: str , message : str) -> dict:

    """
    :param chat_id:

    :param message:
    :return:
    ex. chat_id = '@notify_test_for_fun'
    ex. text = 'text="<strong>WTF</strong>"'
    """

    url = 'https://api.telegram.org/bot' + token + '/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    r = requests.post(url, data=payload)
    return r.json()

def sendPic(chat_id: str , image_url : str , caption : str) -> dict:

    """
    :param chat_id: 
    :param image_url: 
    :param caption: 
    :return: 
    ex. chat_id = '@notify_test_for_fun'
    ex. image_url = 'https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg'
    ex. cation = 'message = "<strong>Name : Data</strong>\n"'
    """

    url = 'https://api.telegram.org/bot' + token + '/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': image_url,
        'caption': caption,
        'parse_mode': 'HTML'
    }
    r = requests.post(url, data=payload)
    return r.json()

def sendVideo(chat_id: str , video_url: str , caption : str) -> dict:

    """
    :param chat_id:
    :param video_url:
    :param caption:
    :return:
    ex. chat_id = '@notify_test_for_fun'
    ex. video-url = 'https://example.com/sample.mp4'
    ex. cation = 'message = "<strong>Name : Data</strong>\n"'
    """

    url = 'https://api.telegram.org/bot' + token + '/sendVideo'
    payload = {
        'chat_id': chat_id,
        'video': video_url,
        'caption': caption,
        'parse_mode': 'HTML'
    }
    r = requests.post(url, data=payload)
    return r.json()

def sendDocument(chat_id: str , document_url: str , caption : str) -> dict:

    """
    :param chat_id:
    :param document_url:
    :param caption:
    :return:
    ex. chat_id = '@notify_test_for_fun'
    ex. document_url = 'https://www.w3.org/TR/PNG/iso_8859-1.txt'
    ex. cation = 'message = "<strong>Name : Data</strong>\n"'
    """
    url = 'https://api.telegram.org/bot' + token + '/sendDocument'

    # with open(document_url, 'rb') as f:
    #     files = {'document': f}
    payload = {
        'chat_id': chat_id,
        'document': document_url,
        'caption': caption,
        'parse_mode': 'HTML'
    }
    r = requests.post(url, data=payload)
    return r.json()

