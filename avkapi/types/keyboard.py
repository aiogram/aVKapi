import json
import typing

from . import base
from . import fields
from .base import VKObject
from ..utils.helper import Item, HelperMode


class Colours:
    mode = HelperMode.lowercase
    PRIMARY = Item()
    DEFAULT = Item()
    NEGATIVE = Item()
    POSITIVE = Item()

    BLUE = PRIMARY
    WHITE = DEFAULT
    RED = NEGATIVE
    GREEN = POSITIVE


class Keyboard(VKObject):
    buttons: 'typing.List[typing.List[KeyboardButton]]' = fields.ListOfLists(base='KeyboardButton', default=[])
    one_time: base.Boolean

    def __init__(self, buttons: 'typing.List[typing.List[KeyboardButton]]' = None,
                 one_time: base.Boolean = False,
                 row_width: base.Integer = 3):
        super(Keyboard, self).__init__(one_time=one_time,
                                       buttons=buttons,
                                       conf={'row_width': row_width})

    @property
    def row_width(self):
        return self.conf.get('row_width', 3)

    @row_width.setter
    def row_width(self, value):
        self.conf['row_width'] = value

    def add(self, *args):
        """
        Add buttons

        :param args:
        :return: self
        :rtype: :obj:`types.Keyboard`
        """
        row = []
        for index, button in enumerate(args, start=1):
            row.append(button)
            if index % self.row_width == 0:
                self.buttons.append(row)
                row = []
        if len(row) > 0:
            self.buttons.append(row)
        return self

    def row(self, *args):
        """
        Add row

        :param args:
        :return: self
        :rtype: :obj:`types.Keyboard`
        """
        btn_array = []
        for button in args:
            btn_array.append(button)
        self.buttons.append(btn_array)
        return self

    def insert(self, button):
        """
        Insert button to last row

        :param button:
        :return: self
        :rtype: :obj:`types.Keyboard`
        """
        if self.buttons and len(self.buttons[-1]) < self.row_width:
            self.buttons[-1].append(button)
        else:
            self.add(button)
        return self


class KeyboardButton(VKObject):
    action: typing.Dict
    color: base.String = fields.Field()

    def __init__(self, label: base.String,
                 payload: base.String = None,
                 color: base.String = Colours.DEFAULT):
        self.label = label
        self.color = color
        self.action = {"type": "text", "label": self.label}

        if payload:
            self.payload = payload
            self.action["payload"] = json.dumps({"button": self.payload})
        super(KeyboardButton, self).__init__(action=self.action,
                                             color=self.color)


class EmptyKeyboard(Keyboard):
    def __init__(self):
        super().__init__(buttons=[])
