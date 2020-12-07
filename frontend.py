from kivy.uix.popup import Popup

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
    my_database = Database()
    location = ObjectProperty(None)
    time = ObjectProperty(None)
    recommendations = ObjectProperty(None)

    def btn(self):
        duration = self.time.text
        start_location = self.location.text
        num_of_result = self.recommendations.text
        flag = True

        # check that num of result is a positive number (int)
        if not self.check_recommendions_type(num_of_result):
            # create content and add to the popup
            self.raise_popup("recommendations should be an integer positive number")
            flag = False

        # check that duration is a positive number (int or float)
        if not self.check_duration_type(duration):
            self.raise_popup("duration should be a positive number")
            flag = False

        # check if location is string
        if not self.check_location_type(start_location):
            self.raise_popup("location should be a string")
            flag = False
        else:
            # check if location is exist
            if not self.my_database.valid_start_location(start_location):
                self.raise_popup("location is not exist")
                flag = False

        # if all values check pass
        if flag:
            result = self.get_recommendation(float(duration), start_location, int(num_of_result))
            # make one string of end locations names
            end_locations = ""
            for row in result:
                end_locations = end_locations + "\n" + row[1]
            # pop up with names
            self.raise_popup(end_locations)

    def clear_inputs(self, text_inputs):
        for text_input in text_inputs:
            text_input.text = ""

    def check_location_type(self, user_input):
        try:
            val = int(user_input)
            return False
        except ValueError:
            try:
                val = float(user_input)
                return False
            except ValueError:
                # check this name in list locations by query
                return True

    def check_recommendions_type(self, user_input):
        try:
            val = int(user_input)
            if val > 0:
                return True
            else:
                return False
        except ValueError:
            return False

    def check_duration_type(self, user_input):
        try:
            val = int(user_input)
            if val > 0:
                return True
            else:
                return False
        except ValueError:
            return False

    def raise_popup(self, text):
        content = Button(text=text)
        popup = Popup(title='Error', content=content, auto_dismiss=False, size_hint=(None, None), size=(400, 400))

        # bind the on_press event of the button to the dismiss function
        content.bind(on_press=popup.dismiss)

        # open the popup
        popup.open()

    def get_recommendation(self, duration, start_location, num_of_result):
        result = self.my_database.select_end_stations(duration, start_location, num_of_result)
        # print(result)
        return result




class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
