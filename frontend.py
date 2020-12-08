from kivy.config import Config

from kivy.core.window import Window
from kivy.uix.actionbar import ActionButton
from kivy.uix.popup import Popup
from mybackend import Database
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivymd.uix.behaviors import HoverBehavior
from kivy.uix.label import Label


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
            self.raise_popup("Error", "Recommendations should be an integer positive number")
            flag = False

        # check that duration is a positive number (int or float)
        if not self.check_duration_type(duration):
            self.raise_popup("Error", "Duration should be a positive number")
            flag = False

        # check if location is string
        if not self.check_location_type(start_location):
            self.raise_popup("Error", "Location should be a string")
            flag = False
        else:
            # check if location is exist
            if not self.my_database.valid_start_location(start_location):
                self.raise_popup("Error", "Location is not exist")
                flag = False

        # if all values check pass
        if flag:
            result = self.get_recommendation(int(duration), start_location, int(num_of_result))
            # make one string of end locations names
            end_locations = ""
            for row in result:
                end_locations = end_locations + "\n" + row[1]
            if end_locations == "":
                end_locations = "Unfortanly we didn't find any recommendation that match your request :( \n You can try to change your preference"
                self.raise_popup(f"Sorry", end_locations, change_size=0)
            # pop up with names
            else:
                self.raise_popup(f"Here is your top recommendation", end_locations, change_size=len(result))

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

    def raise_popup(self, error_type, text, change_size=None):
        content = Button(text=text)
        if change_size is not None:
            high = 100 + 20 * change_size
            width = 400
            if change_size == 0:
                high = 200
                width = 600
            popup = Popup(title=error_type, content=content, auto_dismiss=False, size_hint=(None, None),
                          size=(width, high))
        else:
            popup = Popup(title=error_type, content=content, auto_dismiss=False, size_hint=(None, None),
                          size=(450, 200))

        # bind the on_press event of the button to the dismiss function
        content.bind(on_press=popup.dismiss)

        # open the popup
        popup.open()

    def get_recommendation(self, duration, start_location, num_of_result):
        result = self.my_database.select_end_stations(duration, start_location, num_of_result)
        # print(result)
        return result


class MyActionButton(HoverBehavior, ActionButton):
    pass


class MyButton(HoverBehavior, Button):
    pass


class MyApp(App):

    def build(self):
        return MyGrid()

    def MaxiMin_app_button(self):
        if Window.fullscreen == 'fake':
            Window.fullscreen = 'auto'
        else:
            Window.fullscreen = 'fake'


if __name__ == "__main__":
    Window.fullscreen = 'fake'
    Window.size = (600, 400)
    MyApp().run()
