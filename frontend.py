from mybackend import Database
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
# from kivy.core.window import Window
# Window.size = (600, 300)
from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '300')

class MyGrid(Widget):
    location = ObjectProperty(None)
    time = ObjectProperty(None)
    recommendations = ObjectProperty(None)


    def btn(self):
        y = self.size
        x = 3

    def get_recommendation(self, duration, start_location, num_of_result):
        result = Database.select_end_stations(duration, start_location, num_of_result)
        print(result)
        return result




class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
