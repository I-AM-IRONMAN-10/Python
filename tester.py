import json
import os
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import OneLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from datetime import datetime

class TaskManagerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.tasks = []
        self.selected_date = None
        self.dialog = None

        self.layout = MDBoxLayout(orientation='vertical', spacing=10, padding=10)

        # Live clock
        self.clock_label = MDLabel(halign='center', font_style='H4')
        Clock.schedule_interval(self.update_clock, 1)
        self.layout.add_widget(self.clock_label)

        # Task List
        self.task_list_label = MDLabel(text="Tasks:", halign='center', font_style='H6')
        self.layout.add_widget(self.task_list_label)

        self.task_container = MDBoxLayout(orientation='vertical', spacing=5)
        self.layout.add_widget(self.task_container)

        # Buttons
        self.add_task_btn = MDRaisedButton(text="Add Task", on_release=self.open_add_task_dialog)
        self.layout.add_widget(self.add_task_btn)

        # Load tasks if file exists
        self.load_tasks()

        return self.layout

    def update_clock(self, *args):
        self.clock_label.text = datetime.now().strftime("Time: %H:%M:%S")

    def open_add_task_dialog(self, *args):
        self.task_input = MDTextField(hint_text="Enter Task Name")
        self.date_btn = MDRaisedButton(text="Pick Date", on_release=self.show_date_picker)
        content = MDBoxLayout(orientation='vertical', spacing=10)
        content.add_widget(self.task_input)
        content.add_widget(self.date_btn)

        self.dialog = MDDialog(
            title="Add Task",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(text="Cancel", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Add", on_release=self.add_task)
            ]
        )
        self.dialog.open()

    def show_date_picker(self, *args):
        MDDatePicker(callback=self.on_date_selected).open()

    def on_date_selected(self, date_obj):
        self.selected_date = date_obj.strftime("%d-%m-%Y")
        self.date_btn.text = f"Date: {self.selected_date}"

    def add_task(self, *args):
        task_name = self.task_input.text.strip()
        if task_name and self.selected_date:
            task = {"name": task_name, "date": self.selected_date}
            self.tasks.append(task)
            self.save_tasks()
            self.update_task_list()
            self.dialog.dismiss()

    def update_task_list(self):
        self.task_container.clear_widgets()
        for task in self.tasks:
            item = OneLineListItem(
                text=f"{task['name']} - {task['date']}",
                on_release=lambda inst, t=task: self.remove_task(t)
            )
            self.task_container.add_widget(item)

    def remove_task(self, task):
        self.tasks.remove(task)
        self.save_tasks()
        self.update_task_list()

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
                self.update_task_list()

TaskManagerApp().run()