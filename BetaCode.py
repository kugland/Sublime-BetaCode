# coding=UTF-8

# Sublime-BetaCode, a plugin to help entering polytonic Greek into Sublime Text.
# Copyright (C) 2003  André von Kugland <kugland@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sublime, sublime_plugin, unicodedata, re

# Usage example (taken from Plato, Republic VI. 508d)
#
#   Ou(/tw toi/nun kai\ to\ th=s yuxh=s w(=de no/ei: o(/tan me\n ou(= katala/mpei
#   a)lh/qeia/ te kai\ to\ o)/n, ei)s tou=to a)perei/shtai, e)no/hse/n te kai\
#   e)/gnw au)to\ kai\ nou=n e)/xein fai/netai: o(/tan de\ ei)s to\ tw=| sko/tw|
#   kekrame/non, to\ gigno/meno/n te kai\ a)pollu/menon, doca/\zei te kai\
#   a)mbluw/ttei a)/nw kai\ ka/tw ta\s do/cas metaba/llon, kai\ e)/oiken au)=
#   nou=n ou)k e)/xonti.
#
# Becomes:
#
#   Οὕτω τοίνυν καὶ τὸ τῆς ψυχῆς ὧδε νόει· ὅταν μὲν οὗ καταλάμπει
#   ἀλήθειά τε καὶ τὸ ὄν, εἰς τοῦτο ἀπερείσηται, ἐνόησέν τε καὶ
#   ἔγνω αὐτὸ καὶ νοῦν ἔχειν φαίνεται· ὅταν δὲ εἰς τὸ τῷ σκότῳ
#   κεκραμένον, τὸ γιγνόμενόν τε καὶ ἀπολλύμενον, δοξάζει τε καὶ
#   ἀμβλυώττει ἄνω καὶ κάτω τὰς δόξας μεταβάλλον, καὶ ἔοικεν αὖ
#   νοῦν οὐκ ἔχοντι.

class BetaCode(sublime_plugin.TextCommand):
  # Reorders accents so that Unicode normalization will work.
  @staticmethod
  def norm_accents(match):
    aspr = ''; dial = ''; tone = ''; iota = ''; qunt = ''
    str = match.group(0)
    for i in xrange(0, len(str)):
      if str[i] in ('(', ')')       : aspr = str[i]
      if str[i] == '+'              : dial = str[i]
      if str[i] in ('/', '\\', '=') : tone = str[i]
      if str[i] == '|'              : iota = str[i]
      if str[i] in ('_', '^')       : qunt = str[i]
    return aspr + dial + tone + iota + qunt

  # Replace accents with combining diacritics and normalize the string.
  @staticmethod
  def betacode_accent(str):
    accents = {
      '(' : u'\u0314', # Spiritus lenis
      ')' : u'\u0313', # Spiritus asper
      '\\': u'\u0300', # Grave accent
      '/' : u'\u0301', # Acute accent
      '=' : u'\u0342', # Circumflex accent
      '|' : u'\u0345', # Iota subscript
      '_' : u'\u0304', # Macron
      '^' : u'\u0306', # Breve
      '+' : u'\u0308'  # Diæresis
    }
    str = re.sub(r'[)(\\/=|_^+]+', BetaCode.norm_accents, str)
    str = ''.join((accents.has_key(x) and accents[x] or x for x in str))
    str = unicodedata.normalize('NFKC', str)
    return str

  # Translate Beta-Code to Greek and then add accents
  @staticmethod
  def betacode_transl(str):
    latin = u'ABGDEVZHQIKLMNCOPRSJTUFXYW:abgdevzhqiklmncoprsjtufxyw'
    greek = u'ΑΒΓΔΕϜΖΗΘΙΚΛΜΝΞΟΠΡΣΣΤΥΦΧΨΩ·αβγδεϝζηθικλμνξοπρσςτυφχψω'
    transl_dict = dict(((latin[i], greek[i]) for i in xrange(0, len(latin))))
    str = re.sub(r'\*([abgdevzhqiklmncoprsjtufxyw])', lambda m: m.group(1).upper(), str) # *a → A
    str = re.sub(r's\b', 'j', str) # Substitute sigma for sigma final when needed.
    str = ''.join((transl_dict.has_key(x) and transl_dict[x] or x for x in str))
    return BetaCode.betacode_accent(str)

  def run(self, edit):
    for region in self.view.sel():
      substr = self.view.substr(region)
      substr_beta = BetaCode.betacode_transl(unicode(substr))
      self.view.replace(edit, region, substr_beta)
