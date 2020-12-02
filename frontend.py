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
        result = mybackend.select_top_duration(1)
        print(result)


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
