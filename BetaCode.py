# coding=UTF-8

# Sublime-BetaCode, a plugin that allows typing polytonic Greek into ST.
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

import sublime, sublime_plugin
import sys, os

# cf. http://theo.im/blog/2012/10/25/workaround-failed-to-import-unicodedata-in-sublime-text-2-under-windows/
sys.path.append(os.path.dirname(sys.executable))

import re, unicodedata

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
  """BetaCode is a plugin that allows typing polytonic Greek into ST."""

  @staticmethod
  def diacritics_norm(match):
    """Reorders diacritics so that Unicode normalization will work."""

    aspr = ''; dial = ''; tone = ''; iota = ''; qunt = ''
    str = match.group(0)
    for i in xrange(0, len(str)):
      if str[i] in ('(', ')')       : aspr = str[i]
      if str[i] == '+'              : dial = str[i]
      if str[i] in ('/', '\\', '=') : tone = str[i]
      if str[i] == '|'              : iota = str[i]
      if str[i] in ('_', '^')       : qunt = str[i]
    return aspr + dial + tone + iota + qunt

  @staticmethod
  def betacode_transl(str):
    """Translate Beta-Code to Greek and then add accents"""

    latin = u'ABGDEVZHQIKLMNCOPRSJTUFXYW:abgdevzhqiklmncoprsjtufxyw'
    greek = u'ΑΒΓΔΕϜΖΗΘΙΚΛΜΝΞΟΠΡΣΣΤΥΦΧΨΩ·αβγδεϝζηθικλμνξοπρσςτυφχψω'
    accents = [
      ('(' , u'\u0314'), # Spiritus lenis
      (')' , u'\u0313'), # Spiritus asper
      ('\\', u'\u0300'), # Grave accent
      ('/' , u'\u0301'), # Acute accent
      ('=' , u'\u0342'), # Circumflex accent
      ('|' , u'\u0345'), # Iota subscript
      ('+' , u'\u0308'), # Diæresis
      ('_' , u'\u0304'), # Macron
      ('^' , u'\u0306')  # Breve
    ]
    # Initialize translation dictionary.
    transl_dict = dict(zip(latin, greek) + accents)
    # Convert ‘*a’ to ‘A’
    str = re.sub(r'\*([a-z])', lambda m: m.group(1).upper(), str)
    # Substitute sigma for sigma final when needed.
    str = re.sub(r's\b', 'j', str)
    # Normalize diacritics, i.e. reorder them and remove the superfluous ones.
    str = re.sub(r'[)(\\/=|_^+]+', BetaCode.diacritics_norm, str)
    # Translate using the transl_dict table.
    str = ''.join((transl_dict.has_key(x) and transl_dict[x] or x for x in str))
    # Unicode normalization, make chars precomposed whenever possible.
    str = unicodedata.normalize('NFKC', str)
    return str

  def run(self, edit):
    """Main function, apply betacode_transl() to each selected region."""
    for region in self.view.  sel():
      self.view.replace(edit, region, BetaCode.betacode_transl(self.view.substr(region)))
