from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRoundFlatIconButton
from kivy.lang import Builder
from kivymd.uix.snackbar import Snackbar
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
import numpy as np
from pyzbar.pyzbar import decode
from kivy.graphics.texture import Texture
import cv2
from kivy.uix.image import Image
import requests
from kivymd.toast import toast
from kivy.metrics import dp



helper_string = '''
<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#e7e4c0"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "#0c6c4d"


<DrawerLabelItem@MDNavigationDrawerItem>
    text_color: "#4a4939"
    icon_color: "#4a4939"
    focus_behavior: False
    selected_color: "#4a4939"
    _no_ripple_effect: True
ScreenManager:

    Login:
        size_hint_x: None
        width: "300dp"
        hint_text: "Password"
        pos_hint: {"center_x": .5, "center_y": .5}
    
    TakeAttendance:
    Details:
    SubAdmins:
<Login>:
    name: "login"
    id: log
    MDSmartTile:
        radius: 24
        box_radius: [0, 0, 24, 24]
        box_color: 1, 1, 1, .2
        source: "Ycce_CollegeLogo.jpg"
        pos_hint: {"center_x": .5, "center_y": .8}
        size_hint: None, None
        size: "100dp", "100dp"
    
    MDTextField:
        id: admin_id
        hint_text: "Admin ID"
        helper_text_mode: "on_focus"
        icon_left: "account-lock-open"
        pos_hint: {"center_x": .5, "center_y": .6}
        size_hint_x: .7

        
    MDTextField:
        id: text_field
        hint_text: "Password"
        password: True
        icon_left: "key-variant"
        pos_hint: {"center_x": .5, "center_y": .5}  # Adjust vertical position
        on_focus: text_field.hint_text = "" if self.focus else "Password"
        size_hint_x: .7
        
        
    MDIconButton:
        id: toggle_button
        icon: "eye-off"
        pos_hint: {"center_x": .9, "center_y": .5}
        theme_text_color: "Hint"
        on_release:
            text_field.password = not text_field.password
            toggle_button.icon = "eye" if text_field.password else "eye-off"
        
    MDRoundFlatIconButton:
        id:log
        text: "Login"
        icon: "login"
        pos_hint: {"center_x": .5, "center_y": .4}
        on_release:app.login()
        


        
<SubAdmins>
    name:"subadmins"
    orientation: "vertical"
    MDBottomNavigation:

        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Home'
            icon: 'home'
            on_tab_release:root.manager.current = "subadmins"

        MDBottomNavigationItem:
            name: 'home'
            text: 'Theme'
            icon: 'weather-night-partly-cloudy'
            on_tab_release:app.themeChange()

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:

                MDTopAppBar:
                    title: "Attendance QR"
                    elevation: 4
                    pos_hint: {"top": 1}
                    md_bg_color: "#e7e4c0"
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                MDFloatLayout:

                    MDRoundFlatIconButton:
                        text: "Take Attendance"
                        icon: "camera"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.camp()

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            MDNavigationDrawerMenu:

                MDNavigationDrawerHeader:
                    title: "Menu"
                    title_color: "#4a4939"
                    spacing: "4dp"
                    padding: "12dp", 0, 0, "56dp"

                MDNavigationDrawerLabel:
                    text: "Admin"

                DrawerClickableItem:
                    icon: "logout"
                    text: "Logout"
                    on_release:
                        root.manager.current = "login"
                


<TakeAttendance>
    name: "takeAttendance"

    MDRoundFlatIconButton:
        text: "Back"
        icon: "backburger"
        pos_hint: {"center_x": 0.08, "center_y": .95}
        on_release: root.manager.current = "details"


<Details>
    name:"details"
    MDBottomNavigation:

        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Home'
            icon: 'home'
            on_tab_release:app.h()

        MDBottomNavigationItem:
            name: 'home'
            text: 'Theme'
            icon: 'weather-night-partly-cloudy'
            on_tab_release:app.themeChange()

    MDLabel:
        id : cname
        text: "Campus Name"
        halign: "center"
        pos_hint: {"center_x": .5, "center_y": .6}
        theme_text_color:"Custom"
        text_color:1,0,0,1
        font_style : "H3"

    MDRoundFlatIconButton:
        text: "Take Attendance"
        icon: "camera"
        pos_hint: {"center_x":.5, "center_y": .5}
        on_release: app.takeAttendace()
       
'''



class Login(Screen):
    pass



class TakeAttendance(Screen):
    pass





class Details(Screen):
    pass



class SubAdmins(Screen):
    pass
sm = ScreenManager()
sm.add_widget(Login(name="login"))
sm.add_widget(Login(name="subadmis"))


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snackbar = None
        self._interval = 0
        self.campus = None
        self.admin_id = None
        
        
       

    def build(self):
        s = Screen()
        self.theme_cls.theme_style = "Light"
        self.help_str = Builder.load_string(helper_string)
        s.add_widget(self.help_str)
        self.cap = None  # Webcam capture object
        self.scanning = False
        return s
    
    def themeChange(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else :
            self.theme_cls.theme_style = "Light"

    def create_round_flat_icon_button(self,text, icon_name, pos_hint, on_release):
        button = MDRoundFlatIconButton()
        button.text = text
        button.icon = icon_name
        button.pos_hint = pos_hint
        button.on_release = on_release
        return button

    def wait_interval(self, interval):
        self._interval += interval
        if self._interval > self.snackbar.duration + 0.5:
            anim = Animation(y=dp(10), d=.2)
            anim.start(self.help_str.get_screen("login"))
            Clock.unschedule(self.wait_interval)
            self._interval = 0
            self.snackbar = None

    def h(self):
        self.help_str.current = "subadmins"

    def login(self):
        self.admin_id = self.help_str.get_screen("login").ids.admin_id.text
        password1 = self.help_str.get_screen("login").ids.text_field.text
        data = {
            "id":self.admin_id,
            "password":password1
        }
        response = requests.post('http://127.0.0.1:5000/cologin', json=data)
        
        
        if response.status_code == 200:
            response_data = response.json()
            message = response_data.get("message")
            self.campus = response_data.get("campus")
            if message == "True":
                self.help_str.current = "subadmins"
                self.help_str.transition.direction = "left"

                
            else:
                self.snackbar = Snackbar(text="Invalid credentials contact Admin")
                self.snackbar.open()
                anim = Animation(y=dp(72), d=.2)
                anim.bind(on_complete=lambda *args: Clock.schedule_interval(
                    self.wait_interval, 0))
                anim.start(self.help_str.get_screen("login"))
        else:
            self.snackbar = Snackbar(text="Server Error")
            self.snackbar.open()
            anim = Animation(y=dp(72), d=.2)
            anim.bind(on_complete=lambda *args:Clock.schedule_interval(
                    self.wait_interval, 0))
            anim.start(self.help_str.get_screen("login"))

            
        
    def camp(self):
        self.help_str.get_screen("details").ids.cname.text = self.campus
        self.help_str.current = "details"


    def takeAttendace(self):
        self.image = Image()
        self.campus = self.help_str.get_screen("details").ids.cname.text
        self.help_str.get_screen("takeAttendance").add_widget(self.image)
        self.start_scanner()
        self.help_str.current = "takeAttendance"
        self.help_str.transition.direction = "left"

    def start_scanner(self):
        if not self.scanning:
            self.cap = cv2.VideoCapture(0)
            Clock.schedule_interval(self.update, 1.0 / 30.0)
            self.scanning = True 

    def update(self, dt):
        ret, frame = self.cap.read()

        if not ret:
            return

        decoded_objects = decode(frame)

        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            qr_type = obj.type

            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                cv2.polylines(frame, [hull], True, (0, 255, 0), 2)
            else:
                for j in range(4):
                    cv2.line(frame, points[j], points[(j + 1) % 4], (0, 255, 0), 2)


            try:
                response = requests.put(f"http://127.0.0.1:5000/updateAttendance/{self.campus}/{qr_data}")
                if response.status_code==200:
                    data = response.json()
                    message = data.get("message")
                    if message == "True":
                        name = data.get("Name")
                        toast(f"{name} Present")
                    else:
                        toast(message)
                else:
                    toast(f"Error occued with code {response.status_code}")

            except :
                print("Error Occured")
                
            print("QR Code Type:", qr_type)
            print("QR Code Data:", qr_data)

        buf = cv2.flip(frame, 0).tobytes()
        texture = self.image.texture
        if not texture:
            self.image.texture = texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image.canvas.ask_update()

    def on_stop(self):
        if self.cap:
            self.cap.release()     
		    
    
			    



        

if __name__ == "__main__":
    MyApp().run()
