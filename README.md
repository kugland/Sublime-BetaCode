Sublime-BetaCode
================

A plugin to help entering polytonic Greek into Sublime Text.

To use it, just drop the file BetaCode.py inside your Packages/User directory,
and add the following lines (or something similar) to your Keybindings — User file:

```
{"keys": ["ctrl+b"], "command": "beta_code"}
```

Usage example taken from Plato, Republic VI. 508d:

```
Ou(/tw toi/nun kai\ to\ th=s yuxh=s w(=de no/ei: o(/tan me\n ou(= katala/mpei
a)lh/qeia/ te kai\ to\ o)/n, ei)s tou=to a)perei/shtai, e)no/hse/n te kai\
e)/gnw au)to\ kai\ nou=n e)/xein fai/netai: o(/tan de\ ei)s to\ tw=| sko/tw|
kekrame/non, to\ gigno/meno/n te kai\ a)pollu/menon, doca/\ei te kai\
a)mbluw/ttei a)/nw kai\ ka/tw ta\s do/cas metaba/llon, kai\ e)oiken au)=
nou=n ou)k e)/xonti.
```

Becomes:

```
Οὕτω τοίνυν καὶ τὸ τῆς ψυχῆς ὧδε νόει· ὅταν μὲν οὗ καταλάμπει
ἀλήθειά τε καὶ τὸ ὄν, εἰς τοῦτο ἀπερείσηται, ἐνόησέν τε καὶ
ἔγνω αὐτὸ καὶ νοῦν ἔχειν φαίνεται· ὅταν δὲ εἰς τὸ τῷ σκότῳ
κεκραμένον, τὸ γιγνόμενόν τε καὶ ἀπολλύμενον, δοξάζει τε καὶ
ἀμβλυώττει ἄνω καὶ κάτω τὰς δόξας μεταβάλλον, καὶ ἔοικεν αὖ
νοῦν οὐκ ἔχοντι.
```
