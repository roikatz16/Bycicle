import mybackend
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class MyGrid(Widget):
    location = ObjectProperty(None)
    time = ObjectProperty(None)
    recommendations = ObjectProperty(None)

    def btn(self):
        duration = self.time.text
        start_location = self.location.text
        num_of_result = self.recommendations.text

    def get_recommendation(self, duration, start_location, num_of_result):
        result = mybackend.select_end_stations(duration, start_location, num_of_result)
        print(result)
        return result




class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
