# -*- coding: utf-8 -*-
# vim:set et sts=4 sw=4:
#
# libpyzy - The Chinese PinYin and Bopomofo conversion library.
#
# Copyright (c) 2007-2008 Peng Huang <shawn.p.huang@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA

from pydict import *

class PinYinWord:
    correct_dict = {"nve" : "nue", "lve" : "lue"}
    def __init__ (self, pinyin):
        if pinyin in self.correct_dict:
            pinyin = self.correct_dict [pinyin]

        self._pinyin = pinyin
        self._is_completed = self.is_valid_pinyin ()
        if self._is_completed:
            sheng_mu, yun_mu = self.split ()
            self._pinyin_id = PINYIN_DICT [self._pinyin]
            self._sheng_mu_id = SHENGMU_DICT [sheng_mu]
        else:
            self._sheng_mu_id = SHENGMU_DICT [self._pinyin]

    def is_valid_pinyin (self):
        return self._pinyin in PINYIN_DICT

    def get_sheng_mu_id (self):
        return self._sheng_mu_id

    def get_shengmu (self):
        return ID_SHENGMU_DICT[self._sheng_mu_id]

    def get_pinyin_id (self):
        return self._pinyin_id

    def get_pinyin (self):
        return self._pinyin

    def get_pattern (self, mohu = False):
        if mohu == False:
            if self.is_valid_pinyin ():
                return self._pinyin
            else:
                return self._pinyin + "%"
        else:
            if not self.is_valid_pinyin ():
                if self._pinyin in ("zh", "ch", "sh"):
                    return self._pinyin[0] + "%"
                return self._pinyin + "%"
            else:
                shengmu = self.get_shengmu ()
                yunmu = self._pinyin [len (shengmu):]
                if shengmu in ("zh", "ch", "sh", "z", "c", "s"):
                    shengmu = shengmu[0] + "%"
                if yunmu in ("ing", "in", "en", "eng", "an", "ang"):
                    yunmu = yunmu[0:2] + "%"
                return shengmu + yunmu

    def split (self):
        if not self.is_valid_pinyin ():
            raise Exception ("Pinyin '%s' is not a valid pinyin!" % py)
        if self._pinyin[:2] in list(SHENGMU_DICT.keys ()):
            return self._pinyin[:2], self._pinyin[2:]
        elif self._pinyin[:1] in list(SHENGMU_DICT.keys ()):
            return self._pinyin[:1], self._pinyin[1:]
        else:
            return "", self._pinyin[:]

    def __str__ (self):
        return self._pinyin

class PinYinString:
    def __init__ (self, string):
        pass

def load_pinyin_table (_file):

    def pinyin_table_parser (f):
        for l in f:
            a = str (l, "utf-8").strip ().split ()
            hanzi, pinyin, freq = a
            yield (hanzi, pinyin, int (freq))
    # db.add_phrases (pinyin_table_parser (bzf))

    hanzi_dic = {}
    for hanzi, pinyin, freq in pinyin_table_parser (_file):
        if hanzi not in hanzi_dic:
            hanzi_dic[hanzi] = {}

        if pinyin in hanzi_dic[hanzi]:
            hanzi_dic[hanzi][pinyin] += freq
        else:
            hanzi_dic[hanzi][pinyin] = freq

    return hanzi_dic

def load_phrase_pinyin_freq (_file):
    def phrase_pinyin_parser (f):
        for l in f:
            phrase, pinyin, freq = str (l, "utf-8").strip ().split ()
            pinyin = pinyin.replace ("u:", "v")
            yield (phrase, pinyin, int (freq))
    phrases_dic = {}
    for phrase, pinyin, freq in phrase_pinyin_parser (_file):
        if phrase not in phrases_dic:
            phrases_dic[phrase] = []
        phrases_dic[phrase].append ((phrase, pinyin, freq))

    return phrases_dic

def load_phrase_pinyin (_file):
    def phrase_pinyin_parser (f):
        for l in f:
            phrase, pinyin = str (l, "utf-8").strip ().split ()
            pinyin = pinyin.replace ("u:", "v")
            yield (phrase, pinyin, 0)
    phrases_dic = {}
    for phrase, pinyin, freq in phrase_pinyin_parser (_file):
        if phrase not in phrases_dic:
            phrases_dic[phrase] = []
        phrases_dic[phrase].append ((phrase, pinyin, freq))

    return phrases_dic

def load_sogou_phrases (_file):
    import re
    dic = {}
    for l in _file:
        w = str (l, "utf8")
        w = re.split (r"\t+", w)
        dic [w[0]] = (w[0], int (w[1]))
    return dic
