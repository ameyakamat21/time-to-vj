# Internal imports
from effect.culeidoscope.vertical_culeidoscope import (
	VerticalCuleidoscope,
	WideningVerticalCuleidoscope,
	MultiplyingVerticalCuleidoscope
)
from effect.culeidoscope.random_culeidoscope import RandomCuleidoscope
from effect.zoom_and_translate import ZoomAndTranslateRelativeRectangular
from effect.pass_through import PassThrough

character_effect_map = {
	"v": VerticalCuleidoscope,
	"w": WideningVerticalCuleidoscope,
	"m": MultiplyingVerticalCuleidoscope,
	"r": RandomCuleidoscope,
	"z": ZoomAndTranslateRelativeRectangular,
	"t": PassThrough
}

character_action_map = {
	"n": "next_effect",
	"1": "kick_drum_effect",
	"0": "snare_drum_effect",
	"4": "hihat_drum_effect"
}