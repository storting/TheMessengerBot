
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from AppModul import SendMessage as SM

SM.DriverHandler.open()
SM.MessageSend.send_whatsapp_message("+79137898373", "Иван", "Кирилл")
SM.DriverHandler.close()

