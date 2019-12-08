import os

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


configuration = ConfigParser()
configuration.read('screenmanager.ini')


def merge_crosswalks(img_df, ques_df):
    return ques_df.merge(img_df, left_on=["problemid", "stepnumber"], right_on=["ProblemId", "StepNumber"])


def get_ques_text(df, idx):
    return df.iloc[idx]['clean_questiontext'] if idx < len(df) else "Reached end of file"


def get_img_url(df, idx):
    return df.iloc[idx]['PicUrl'] if idx < len(df) else None


def get_prob_id(df, idx):
    return int(df.iloc[idx]['problemid'] if idx < len(df) else 0)


def get_step_num(df, idx):
    return int(df.iloc[idx]['stepnumber'] if idx < len(df) else 0)


def get_replay_data(df, idx):
    ques_text = get_ques_text(df, idx)
    img_url = get_img_url(df, idx)
    prob_id = get_prob_id(df, idx)
    step_num = get_step_num(df, idx)

    return prob_id, step_num, ques_text, img_url



class ReplayScreen(Screen):
    pass


class MyScreenManager(ScreenManager):
    pass


class ScreenManagerApp(App):

    prob_id = NumericProperty(0)
    step_num = NumericProperty(0)
    ques_text = StringProperty("Please select dataset path from settings!")
    img_url = StringProperty(None)
    idx = NumericProperty(0)

    def build_config(self, config):
        config.setdefaults('replays', {
            'idx': 0,
            'img_df_path': os.getcwd(),
            'ques_df_path': os.getcwd()})

    def build_settings(self, settings):
        settings.add_json_panel('Configuration', self.config, "settings.json")

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False

        Window.bind(on_key_down=self._on_keyboard_down)

        self.idx = int(self.config.get('replays', 'idx'))

        try:
            img_df = pd.read_csv(self.config.get('replays', 'img_df_path'))
            ques_df = pd.read_csv(self.config.get('replays', 'ques_df_path'))
            self.df = merge_crosswalks(img_df, ques_df)
            self.prob_id, self.step_num, self.ques_text, self.img_url = get_replay_data(self.df, self.idx)
        except (FileNotFoundError, KeyError) as e:
            self.ques_text = "Please select the correct dataset path from settings"

        return self.root

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:  # 40 - Enter key pressed
            self.next_replay()

    def next_replay(self):
        try:
            self.idx += 1
            self.prob_id, self.step_num, self.ques_text, self.img_url = get_replay_data(self.df, self.idx)
            self.config.set('replays', 'idx', self.idx)
            self.config.write()
        except AttributeError:
            self.ques_text = "Please select dataset path from settings!"

    def prev_replay(self):
        if self.idx != 0:
            try:
                self.idx -= 1
                self.prob_id, self.step_num, self.ques_text, self.img_url = get_replay_data(self.df, self.idx)
                self.config.set('replays', 'idx', self.idx)
                self.config.write()
            except AttributeError:
                self.ques_text = "Please select dataset path from settings!"

    def on_config_change(self, config, section, key, value):

        self.idx = int(self.config.get('replays', 'idx'))

        try:
            img_df = pd.read_csv(config.get('replays', 'img_df_path'))
            ques_df = pd.read_csv(config.get('replays', 'ques_df_path'))
            self.df = merge_crosswalks(img_df, ques_df)
            self.prob_id, self.step_num, self.ques_text, self.img_url = get_replay_data(self.df, self.idx)
        except (FileNotFoundError, KeyError) as e:
            self.ques_text = "Please select the correct dataset path from settings"


if __name__ == "__main__":
    ScreenManagerApp().run()
