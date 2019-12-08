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

from configuration import *


def merge_crosswalks(img_df, ques_df, config):
    primary_keys = config.get('replays', 'PRIMARY_KEY').split(',')
    foreign_keys = config.get('replays', 'FOREIGN_KEY').split(',')
    return ques_df.merge(img_df, left_on=primary_keys, right_on=foreign_keys)


def get_ques_text(df, idx, col):
    return df.iloc[idx][col] if idx < len(df) else COMPLETED_MESSAGE


def get_img_url(df, idx, col):
    return df.iloc[idx][col] if idx < len(df) else None


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

    return prob_id, step_num, ques_text, img_url


class ReplayScreen(BoxLayout):
    pass


class ScreenManagerApp(App):

    prob_id = NumericProperty(0)
    step_num = NumericProperty(0)
    ques_text = StringProperty(INITIAL_MESSAGE)
    img_url = StringProperty(None)
    curr_idx = NumericProperty(0)

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
            'STEP_NUM': DEFAULT_STEP_NUM})

    def build_settings(self, settings):
        settings.add_json_panel(PRESET_NAME, self.config, JSON_SETTINGS_PATH)

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False

        Window.bind(on_key_down=self._on_keyboard_down)

        self.curr_idx = int(self.config.get('replays', 'IDX'))
        self.start_replay()

        return ReplayScreen()

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == KEYCODE_NEXT:
            self.next_replay()

    def start_replay(self):
        try:
            img_df = pd.read_csv(self.config.get('replays', 'IMG_DF_PATH'))
            ques_df = pd.read_csv(self.config.get('replays', 'QUES_DF_PATH'))
            self.df = merge_crosswalks(img_df, ques_df, self.config)
            self.prob_id, self.step_num, self.ques_text, self.img_url = get_replay_data(self.df, self.config)
        except:
            self.ques_text = UNABLE_TO_LOAD_MESSAGE

    def next_replay(self):
        try:
            self.curr_idx += 1
            self.config.set('replays', 'IDX', self.curr_idx)
            self.config.write()
            self.prob_id, self.step_num, self.ques_text, self.img_url = get_replay_data(self.df, self.config)
        except:
            self.ques_text = UNABLE_TO_LOAD_MESSAGE

    def prev_replay(self):
        if self.curr_idx != 0:
            try:
                self.curr_idx -= 1
                self.config.set('replays', 'IDX', self.curr_idx)
                self.config.write()
                self.prob_id, self.step_num, self.ques_text, self.img_url = get_replay_data(self.df, self.config)
            except:
                self.ques_text = UNABLE_TO_LOAD_MESSAGE

    def on_config_change(self, config, section, key, value):

        self.curr_idx = int(self.config.get('replays', 'IDX'))
        self.start_replay()


if __name__ == "__main__":
    ScreenManagerApp().run()
