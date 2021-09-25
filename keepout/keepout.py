from datetime import datetime
import time

import PySimpleGUI as sg
from screeninfo import get_monitors

import config

class Mask(object):

    def __init__(self, conf:dict) -> None:
        self.password = conf["password"]
        self.soft = conf["soft"]
        self.hard = conf["hard"]

        self.width = self.height = 0
        for m in get_monitors():
            self.width += m.width
            self.height += m.height

    def start(self) -> None:
        text = sg.Text('', font=('Arial', 128, 'bold'),
                       text_color = 'white', background_color = 'black', )
        layout = [[text]]
        self.window = sg.Window('keepout', layout = layout,
                                size = (self.width, self.height),
                                location = (0, 0),
                                keep_on_top = True, no_titlebar = True,
                                return_keyboard_events = True,
                                transparent_color = 'black',
                                background_color = 'black',
                               )
        self.window.finalize()
        self.window.set_alpha(0.5)
        self.window.hide()

        soft_timer = Timer(self.soft["start"], self.soft["end"])
        hard_timer = Timer(self.hard["start"], self.hard["end"])

        while True:
            event, values = self.window.read(timeout = 1000)
            print(f"event:{event}, values:{values}")
            print(datetime.now())

            if event == 'Escape:27' or event == sg.WIN_CLOSED:
                print("escaped")
                password = None
                if(hard_timer.is_time()):
                    password = sg.popup_get_text('Input password',
                                                 password_char = "*",
                                                 keep_on_top = True
                                                )

                if(self.password == password):
                    self.window.close()
                    break

            if event == '__TIMEOUT__':
                if(hard_timer.is_time()):
                    text.update(value = self.hard["message"])
                    self.window.un_hide()
                    self.window.set_transparent_color('blue')
                elif(soft_timer.is_time()):
                    text.update(value = self.soft["message"])
                    self.window.un_hide()
                    self.window.set_transparent_color('black')
                else:
                    time.sleep(30)

        self.window.close()

class Timer(object):
    TIME_FORMAT = "%H:%M"

    def __init__(self, start:str, end:str) -> None:
      self._start = datetime.strptime(start, self.TIME_FORMAT).time()
      self._end = datetime.strptime(end, self.TIME_FORMAT).time()

    def is_time(self, now:str = None) -> bool:
      now = datetime.strptime(now, self.TIME_FORMAT) if now else datetime.now().time()
      if  self._start <= self._end:
        return self._start <= now <= self._end
      else:
        return self._start <= now or now <= self._end


if __name__ == '__main__':
    conf = config.get_config()
    mask = Mask(conf)
    mask.start()
