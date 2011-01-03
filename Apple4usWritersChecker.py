#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Apple4us Writer's Checker
A class to check basic errors for apple4.us articles using
regular expression.

The class added several default replace patterns.
'''

__version__ = '0.1'

import re

def _removeCommaInNumber(m):
	'''Remove commas in a number.'''
	return m.group(0).replace(',','')

def _convertToChinesePunctuation(m):
	'''Replace Latin punctuations with Chinese's '''
	convert = {
		',' : u'，',
		'.' : u'。',
		'!' : u'！',
		'(' : u'（',
		')' : u'）',
		':': u'：',
		';' : u'；',
		'?' : u'？',
		'\[' : u'【',
		'\]' : u'】',
		'~' : u'～'
	}
	
	if m.group('char1') is not None:
		return u'%s%s' % (m.group('char1'), convert.get(m.group('punc1')))
	else:
		return u'%s%s' % (convert.get(m.group('punc2')), m.group('char2'))

class Apple4usWritersChecker:
	'''Checker class, check() method take textToCheck as arugment and returns a result dictionary.'''
	
	RE_LATIN_SP = u' !-~'
	RE_LATIN = u'!-~'
	RE_LATIN_LETTER_NUMBER = u'a-zA-Z0-9'
	RE_LATIN_LETTER = u'a-zA-Z'
	RE_LATIN_PUNCTUATION = u',.!():;?\[\]~'
	RE_CJK = u'一-龥、-〟！-～。，「」、'
	RE_CJK_CHARACTER = u'一-龥'
	RE_CJK_PUNCTUATION = u'、-〟！-～。，「」、'
	
	RE_DEFAULT_PATTERN = {
	  # Default regular expression patterns
	  # Format: 'name' : ('regex_obj_to_call_sub, repl_pattern/function, description)
	  # UseODE and unicode string
		'REPLACE_CHINESE_QUOTES' 			: [(re.compile(u'(\'|‘)(.*[%s]+.*)(\'|’)' % RE_CJK, re.UNICODE), ur'『\2』', "Use Chinese quotes for Chinese."), 
												(re.compile(u'("|“)(.*[%s]+.*)("|”)' % RE_CJK, re.UNICODE), ur'「\2」', "Use Chinese quotes for Chinese.")],
		'REPLACE_CHINESE_APPLE'				: [(re.compile(u'Apple', re.UNICODE), ur'苹果', "Use translated name for \"Apple\"."),
												(re.compile(u'苹果 TV', re.UNICODE), ur'Apple TV', "Correct the wrongly replaced product name."),
												(re.compile(u'( 苹果 )|( 苹果)|(苹果 )', re.UNICODE), ur'苹果', "Clean the space around 苹果.")],
		'REMOVE_COMMA_IN_NUMBER' 			: [(re.compile(u'((\d+)((,\d+)+))', re.UNICODE), _removeCommaInNumber, "Remove comma in numbers.")],
		'REPLACE_CHINESE_PUNCTUATION'		: [(re.compile(u'((?P<char1>[%s]{1})(?P<punc1>[%s]))|((<?P<punc2>[%s])(<?P<char2>[%s]{1}))' % (RE_CJK_CHARACTER, RE_LATIN_PUNCTUATION, RE_LATIN_PUNCTUATION, RE_CJK_CHARACTER), re.UNICODE), _convertToChinesePunctuation, "Use Chinese punctuation.")],
		'ADD_SPACE_CHINESE_LATIN'			: [(re.compile(u'([%s]+)([%s]+)' % (RE_CJK, RE_LATIN), re.UNICODE), ur'\1 \2', "Space between a Chinese character and an Latin character."),
												(re.compile(u'([%s]+)([%s]+)' % (RE_LATIN, RE_CJK), re.UNICODE), ur'\1 \2', "Space between an Latin character and a Chinese character.")],
		'REMOVE_SPACE_BEFORE_LATIN_PUNCTUATION'	: [(re.compile(u'([%s]) ([%s])' % (RE_LATIN, RE_LATIN_PUNCTUATION), re.UNICODE), ur'\1\2', "Remove whitespace before latin punctuation.")],
		'ADD_SPACE_AFTER_LATIN_PUNCTUATION'	: [(re.compile(u'([%s])([%s])([^%s \n]{1})' % (RE_LATIN, RE_LATIN_PUNCTUATION, RE_LATIN_PUNCTUATION), re.UNICODE), ur'\1\2 \3', "Space after a Latin punctuation.")]
	}
	# Default regular expression key names, ORDERED
	RE_DEFAULT = ('REPLACE_CHINESE_QUOTES', 'REPLACE_CHINESE_APPLE', 'REMOVE_COMMA_IN_NUMBER', 'REPLACE_CHINESE_PUNCTUATION', 'ADD_SPACE_CHINESE_LATIN', 'REMOVE_SPACE_BEFORE_LATIN_PUNCTUATION', 'ADD_SPACE_AFTER_LATIN_PUNCTUATION')
	
	VOCABULARY_REPLACE = {
		u'802.11 n' : u'802.11n',
		u'Apple Store' : u'苹果专卖店',
		u'AppStore' : u'App Store',
		u'BlackBerry' : u'黑莓',
		u'Engadget' : u'瘾科技',
		u'Genius Bar' : u'天才吧',
		u'Human Interface Guidelines' : u'人机介面规约',
		u'Intel' : u'英特尔',
		u'iPod Classic' : u'iPod classic',
		u'iPod Nano' : u'iPod nano',
		u'iPod Touch' : u'iPod touch',
		u'iTunes Store' : u'iTunes 商店',
		u'Keynote' : u'主题演讲',
		u'Logo' : u'标志',
		u'Mac Mini' : u'Mac mini',
		u'MacWorld' : u'Macworld',
		u'Multi-Touch' : u'多点触控',
		u'Native' : u'原生',
		u'Sun Microsystem' : u'升阳',
		u'SSH tunnel' : u'SSH 隧道',
		u'Time Machine' : u'「时间机器」',
		u'Time Capsule' : u'「时间胶囊」',
		u'Quick Look' : u'「快速查看」',
		u'Quicktime' : u'QuickTime',
		u'Web app' : u'线上软件',
		u'Web application' : u'线上软件',
		u'WiFi' : u'Wi-Fi',
		u'Wi-fi' : u'Wi-Fi',
		u'Wifi' : u'Wi-Fi',
		u'Widget' : u'挂件',
		u'WIMAX' : u'WiMAX',
		u'Wimax' : u'WiMAX',
		u'Fake Steve Jobs' : u'假乔布斯',
		u'John Gruber' : u'约翰·格鲁伯',
		u'Jonathan Ive' : u'约翰森·艾弗',
		u'Jonny Ive' : u'约翰森·艾弗',
		u'Steve Jobs' : u'乔布斯',
		u'John Markoff' : u'约翰·马可夫',
		u'Phil Schiller' : u'菲尔·席勒',
		u'Eric Schmidt' : u'埃里克·施密特'
	} 
	
	def __init__(self):
		pass
	
	def check(self, text, disabledDefaultRE = set([]), disabledWord = set([])):
		'''Check the text. Return a result dictionary.
		
			Result dictionary has one keys:
				'result' for the correct text (or the exception info).
		'''
		result = {}
		originalText = text
		
		#try:
		spellingCheck = self._spellingCheck(text, disabledWord)
		text = spellingCheck['text']
		description = spellingCheck['description']
		
		regexCheck = self._regexCheck(text, disabledDefaultRE)
		text = regexCheck['text']
		description += regexCheck['description']
		
		result['text'] = text
		result['description'] = description
		#except Exception, e:
		#	result['text'] = u'ERROR: %s' % e
		
		return result
	
	def _regexCheck(self, text, disabledDefaultRE = set([])):
		for REGroup in self.RE_DEFAULT:
			if not (REGroup in disabledDefaultRE):
				for re in self.RE_DEFAULT_PATTERN[REGroup]:
					text = re[0].sub(re[1], text)
		
		result = {
			'text' : text
		}

		return result
	
	def _spellingCheck(self, text, disabledVocabulary = set([])):
		#Vocabulary replacement
		for vocabulary in self.VOCABULARY_REPLACE:
			if not (vocabulary in disabledVocabulary):
	 			text = text.replace(vocabulary, self.VOCABULARY_REPLACE[vocabulary])
		
		result = {
			'text' : text
		}
		
	 	return result
  