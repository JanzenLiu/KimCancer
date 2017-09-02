#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

unicodes = {
	r"\u2013":"-",
	r"\u2212":"?",
	r"\u03bc":"mu",
	r"\u2009":"?",
	r"\u00d7":"times",
	r"\u03b1":"alpha", # lowercase
	r"\u00b1":"plusminus",
	r"\u03b2":"beta",
	r"\u0394":"delta", # capital
	r"\u2019":"\'",
	r"\u21d3":"?",
	r"\u200b":"?",
	r"\u200a":"?",
	r"\u2032":"\'",
	r"\u00b7":".",
	r"\u201d":"\"",
	r"\u223c":"?",
	r"\u201c":"\"",
	r"\u00b0":"degree",
	r"\u00b5":"?",
	r"\u2265":"greaterequal",
	r"\u2192":"rightarrow",
	r"\u00c5":"?",
	r"\u2014":"--",
	r"\u03b3":"gamma",
	r"\u2264":"lessequal",
	r"\u00bc":"?",
	r"\u2022":"?",
	r"\u2018":"\'",
	r"\u00ae":"?",
	r"\u2010":"-",
	r"\u03ba":"kappa", # lowercase
	r"\u03c7":"chi",
	r"\u2217":"?",
	r"\u2a7e":"?",
	r"\u00c3":"?",
	r"\u00e9":"e", # latin letter
	r"\u20ac":"eurosign",
	r"\u00e2":"?",
	r"\u25b6":"?",
	r"\u0178":"?",
	r"\u2248":"approximatelyequal",
	r"\u03b4":"delta", # lowercase
	r"\u2020":"?",
	r"\u00b4":"?",
	r"\u2122":"?",
	r"\u00f6":"?",
	r"\u2236":":",
	r"\u03c6":"phi", # lowercase
	r"\u00fc":"u", # latin letter
	r"\u02da":"?",
	r"\u00fe":"?",
	r"\u03bb":"lambda",
	r"\u2005":"?",
	r"\u03c1":"rho",
	r"\u03c3":"sigma", # lowercase
	r"\u03c0":"pi", # lowercase
	r"\u2002":"?",
	r"\u25b5":"?",
	r"\u00ad":"?",
	r"\u00a9":"?",
	r"\u03b8":"theta", # lowercase
	r"\u03a6":"phi", # capital
	r"\u25a1":"whitesquare",
	r"\u2011":"?",
	r"\u03b5":"epsilon",
	r"\u25aa":"?",
	r"\u266f":"?",
	r"\u204e":"?",
	r"\u25cb":"whitecircle",
	r"\u00bd":"?",
	r"\u00a7":"sectionsign",
	r"\u226a":"?",
	r"\u03b6":"zeta",
	r"\u2021":"?",
	r"\u00df":"?",
	r"\u25b4":"?",
	r"\u02c6":"?",
	r"\u03c8":"psi", # lowercase
	r"\u2206":"?",
	r"\u22c5":"?",
	r"\u21d1":"?",
	r"\u03f5":"?",
	r"\u00c2":"?",
	r"\u03b9":"iota",
	r"\u00ef":"?",
	r"\u00e4":"?",
	r"\u00a2":"?",
	r"\u25a0":"blacksquare",
	r"\u00a1":"?",
	r"\u00e1":"a", # latin letter
	r"\u2202":"?",
	r"\u00f8":"?",
	r"\u2a7d":"?",
	r"\u00e8":"e", # latin letter
	r"\u2666":"?",
	r"\u00ed":"i", # latin letter
	r"\u00b6":"?",
	r"\u212b":"?",
	r"\u0080":"controlsign",
	r"\u2033":"\"",
	r"\u025b":"?",
	r"\u00a8":"diaeresis",
	r"\u00f3":"o", # latin letter
	r"\u00a3":"?", 
	r"\u2026":"ellipsis",
	r"\u2237":"proportionsign",
	r"\u02dc":"?",
	r"\u03a8":"psi", # capital
	r"\u2194":"?",
	r"\u00b2":"?",
	r"\u2245":"?",
	r"\u00ac":"?",
	r"\u03d5":"?",
	r"\u25ca":"?",
	r"\u25b2":"blackuptriangle",
	r"\u22ef":"?",
	r"\u00e7":"?",
	r"\u2215":"dividedby", # division slash
	r"\u2191":"uparrow",
	r"\u03a0":"pi", # capital
	r"\u221e":"infinity", # or infinitysign?
	r"\u0152":"?",
	r"\u00e5":"?",
	r"\u25bc":"blackdowntriangle",
	r"\u25be":"?",
	r"\u00f4":"?",
	r"\u221a":"squareroot",
	r"\u226b":"?",
	r"\u2709":"?",
	r"\u00e3":"?",
	r"\u03a9":"omega", # capital
	r"\u00ea":"e", # latin letter
	r"\u2260":"notequalto",
	r"\u00ab":"?",
	r"\u00bb":"?",
	r"\u00f1":"?",
	r"\u25cf":"blackcircle",
	r"\u00af":"?",
	r"\u2193":"downarrow",
	r"\u2302":"?",
	r"\u03c4":"tau",
	r"\u201a":"?",
	r"\u0131":"?",
	r"\u03b7":"eta",
	r"\u00ba":"?",
	r"\u3008":"leftanglebracket", # merge with one kind of the brackets/parenthesis?
	r"\u3009":"rightanglebracket", # merge with one kind of the brackets/parenthesis?
	r"\u25c7":"whitediamond",
	r"\u25bf":"?",
	r"\u00d8":"?",
	r"\u25c6":"blackdiamond",
	r"\u03c9":"omega", # lowercase
	r"\u2133":"?",
	r"\u0301":"?",
	r"\u00e6":"?",
	r"\u00b3":"?",
	r"\u2008":"?",
	r"\u039a":"kappa", # capital
	r"\u0398":"theta", # capital
	r"\u00f7":"dividedby", # division sign
	r"\u2211":"sigma", # uppercase / or sumup
	r"\ue001":" ", # don't know the usage of this character
	r"\u2227":"logicaland",
	r"\u00bf":"?",
	r"\u2016":"doubleverticalline",
	r"\u2223":"divides",
	r"\ue003":" ", # don't know the usage of this character
	r"\u03bd":"nu",
	r"\u0160":"?",
	r"\u02b9":"?",
	r"\u2461":"circledigit2",
	r"\u2462":"circledigit3",
	r"\u2463":"circledigit4",
	r"\u00f2":"o", # latin letter
	r"\u030a":"?",
	r"\u0454":"?",
	r"\u2012":"?",
	r"\u2460":"circledigit1",
	r"\u0391":"alpha", # capital
	r"\u00d4":"?",
	r"\u0308":"?",
	r"\u05f3":"?",
	r"\u2606":"whitestar",
	r"\u2298":"?",
	r"\u2003":"?",
	r"\u0007":"bellcode",
	r"\u2190":"leftarrow",
	r"\u00fa":"u", # latin letter
	r"\u011b":"e", # latin letter
	r"\u2662":"?",
	r"\udbc0":"?",
	r"\u0161":"?",
	r"\u00e0":"a", # latin letter
	r"\udc42":"?"
}