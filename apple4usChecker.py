#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from Apple4usWritersChecker import Apple4usWritersChecker
import wsgiref.handlers
import os
from difflib import HtmlDiff
from diff_match_patch import diff_match_patch

class A4uCheckerHandler(webapp.RequestHandler):
	def _sortVocabulary(self, v):
		for key in sorted(v.iterkeys()):
			sorted['before'] += key
			sorted['after'] += v[key]
			
		return sorted
	def post(self):
		text = self.request.get('text')
		
		allOptions = ('chinese_quotes', 'chinese_apple', 'remove_comma', 'chinese_punctuation', 'space_latin_chinese')
		options = {
			'chinese_quotes'		: ['REPLACE_CHINESE_SINGLE_QUOTES', 'REPLACE_CHINESE_DOUBLE_QUOTES'],
			'chinese_apple'			: ['REPLACE_CHINESE_APPLE', 'RECOVER_CHINESE_APPLE_PRODUCT_NAME', 'RECOVER_CHINESE_APPLE_REMOVE_SPACE'],
			'remove_comma'			: ['REMOVE_COMMA_IN_NUMBER'],
			'chinese_punctuation'	: ['REPLACE_CHINESE_PUNCTUATION'],
			'space_latin_chinese'	: ['ADD_CHINESE_SPACE_LATIN', 'ADD_LATIN_SPACE_CHINESE'],
			'space_after_latin_punctuation'	: ['SPACE_AFTER_LATIN_PUNCTUATION'],
			'remove_space_before_latin_punctuation'	: ['REMOVE_SPACE_BEFORE_LATIN_PUNCTUATION'],
			'add_space_after_latin_punctuation'	: ['ADD_SPACE_AFTER_LATIN_PUNCTUATION']
		}
		disabledDefault = []
		
		for option in options:
			if self.request.get(option) is '':
				disabledDefault += options[option]
		
		disabledDefault = set(disabledDefault)
		checker = Apple4usWritersChecker()

		newText = checker.check(text, disabledDefault)['result']
		diff = diff_match_patch()
		
# 		vocabulary = _sortVocabulary(checker.VOCABULRY_REPLACE)
		template_values = {
			'oldText' : text,
			'newText' : newText.replace('\n','<br />'),
			'vocabulary_key' : sorted(checker.VOCABULARY_REPLACE.iterkeys()),
			'vocabulary' : checker.VOCABULARY_REPLACE,
			'diff_table' : diff.diff_prettyHtml(diff.diff_main(text,newText))
		}
		
		path = os.path.join(os.path.dirname(__file__), 'apple4usChecker.html')
		self.response.out.write(template.render(path, template_values))
		
	def get(self):
		checker = Apple4usWritersChecker()
			
		template_values = {
			'oldText' : "",
			'newText' : "",
			'vocabulary_key' : sorted(checker.VOCABULARY_REPLACE.iterkeys()),
			'vocabulary' : checker.VOCABULARY_REPLACE
		}
		
		path = os.path.join(os.path.dirname(__file__), 'apple4usChecker.html')
		self.response.out.write(template.render(path, template_values))
		
def main():
	application = webapp.WSGIApplication([('/a4uchecker', A4uCheckerHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()