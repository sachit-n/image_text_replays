import os
import json

import pandas as pd

from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.settings import SettingsWithSidebar
from kivy.config import ConfigParser
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from configuration import *


def merge_crosswalks(img_df, ques_df, config):
    primary_keys = config.get('replays', 'PRIMARY_KEY').split(',')
    foreign_keys = config.get('replays', 'FOREIGN_KEY').split(',')
    return ques_df.merge(img_df, left_on=primary_keys, right_on=foreign_keys)


def get_ques_text(df, idx, col):
    return df.iloc[idx][col] if idx < len(df) else COMPLETED_MESSAGE


def get_img_url(df, idx, col):
    return df.iloc[idx][col] if idx < len(df) else 'unk'


def get_prob_id(df, idx, col):
    return int(df.iloc[idx][col] if idx < len(df) else 0)


def get_step_num(df, idx, col):
    return int(df.iloc[idx][col] if idx < len(df) else 0)


def get_replay_data(df, config):
    idx = int(config.get('replays', 'IDX'))
    ques_text = get_ques_text(df, idx, config.get("replays", "QUESTION_TEXT"))
    img_url = get_img_url(df, idx, config.get("replays", "PIC_URL"))
    prob_id = get_prob_id(df, idx, config.get("replays", 'PROBLEM_ID'))
    step_num = get_step_num(df, idx, config.get("replays", "STEP_NUM"))

    return [prob_id, step_num, ques_text, img_url]


class ReplayScreen(BoxLayout):

    prob_id = NumericProperty(0)
    step_num = NumericProperty(0)
    ques_text = StringProperty(INITIAL_MESSAGE)
    img_url = StringProperty(None)
    curr_idx = NumericProperty(0)

    ques1opt1 = ObjectProperty(None)
    ques1opt2 = ObjectProperty(None)
    ques2opt1 = ObjectProperty(None)
    ques2opt2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ReplayScreen, self).__init__(**kwargs)
        self.config = App.get_running_app().config

        Window.bind(on_key_down=self._on_keyboard_down)

        self.popup = Popup(title=INC_POPUP_TITLE, content=Label(text=INC_POPUP_MSG),
                           auto_dismiss=True, size_hint=(0.4, 0.2), pos=(self.x, self.y))

        self.output_path = os.path.join(self.config.get("replays", "OUTPUT_DF_PATH"),
                                        self.config.get("replays", "USER")+"_enc.csv")

        try:
            self.output_df = pd.read_csv(self.output_path).iloc[:, 1:]
        except FileNotFoundError:
            self.output_df = pd.DataFrame()

        self.curr_idx = int(self.config.get('replays', 'IDX'))
        self.start_replay()

    def check_if_answered(self):
        if self.ques1opt1.active + self.ques1opt2.active == 1 and self.ques2opt1.active + self.ques2opt2.active == 1:
            return True
        else:
            return False

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == KEYCODE_NEXT:
            self.next_replay() if self.check_if_answered() else self.show_incomplete_popup()

    def start_replay(self):
        self.config = App.get_running_app().config
        try:
            img_df = pd.read_csv(self.config.get('replays', 'IMG_DF_PATH'))
            ques_df = pd.read_csv(self.config.get('replays', 'QUES_DF_PATH'))
            self.df = merge_crosswalks(img_df, ques_df, self.config)
            self.prob_id, self.step_num, self.ques_text, self.img_url = get_replay_data(self.df, self.config)
        except:
            self.ques_text = UNABLE_TO_LOAD_MESSAGE

    def next_replay(self):
        self.save_encodings()
        try:
            self.curr_idx += 1
            self.config.set('replays', 'IDX', self.curr_idx)
            self.config.write()
            self.prob_id, self.step_num, self.ques_text, self.img_url = get_replay_data(self.df, self.config)
        except:
            self.ques_text = UNABLE_TO_LOAD_MESSAGE

    def show_incomplete_popup(self):
        self.popup.open()

    def prev_replay(self):
        if self.curr_idx != 0:
            try:
                self.curr_idx -= 1
                self.config.set('replays', 'IDX', self.curr_idx)
                self.config.write()
                self.prob_id, self.step_num, self.ques_text, self.img_url = get_replay_data(self.df, self.config)
            except:
                self.ques_text = UNABLE_TO_LOAD_MESSAGE

    def save_encodings(self):
        try:
            curr_encoding = [self.curr_idx] + get_replay_data(self.df, self.config) + [self.ques1opt1.active,
                                                                                       self.ques1opt2.active,
                                                                                       self.ques2opt1.active,
                                                                                       self.ques2opt2.active]

            curr_df = pd.DataFrame([curr_encoding], columns=['idx',
                                                             self.config.get("replays", "PROBLEM_ID"),
                                                             self.config.get("replays", "STEP_NUM"),
                                                             self.config.get("replays", "QUESTION_TEXT"),
                                                             self.config.get("replays", "PIC_URL"),
                                                             "ques1opt1", "ques1opt2",
                                                             "ques2opt1", "ques2opt2"])

            self.output_df = self.output_df.append(curr_df, ignore_index=True)
            self.output_df.to_csv(self.output_path)
        except:
            self.ques_text = UNABLE_TO_LOAD_MESSAGE


class ScreenManagerApp(App):

    def build_config(self, config):
        config.setdefaults('replays', {
            'IDX': DEFAULT_IDX,
            'IMG_DF_PATH': DEFAULT_DF_PATH,
            'FOREIGN_KEY': DEFAULT_FOR_KEY,
            'QUES_DF_PATH': DEFAULT_DF_PATH,
            'PRIMARY_KEY': DEFAULT_PRIMARY_KEY,
            'PIC_URL': DEFAULT_PIC_URL,
            'QUESTION_TEXT': DEFAULT_QUES_TEXT,
            'PROBLEM_ID': DEFAULT_PROB_ID,
            'STEP_NUM': DEFAULT_STEP_NUM,
            'OUTPUT_DF_PATH': DEFAULT_DF_PATH,
            'USER': DEFAULT_USER_NAME})

    def build_settings(self, settings):
        settings.add_json_panel(PRESET_NAME, self.config, "/Users/sachitnagpal/upenn/clean2/settings.json")

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False

        return ReplayScreen()

    def on_config_change(self, config, section, key, value):
        App.get_running_app().root.curr_idx = int(self.config.get('replays', 'IDX'))
        self.output_path = os.path.join(self.config.get("replays", "OUTPUT_DF_PATH"),
                                        self.config.get("replays", "USER")+"_enc.csv")
        App.get_running_app().root.start_replay()


if __name__ == "__main__":
    ScreenManagerApp().run()
