# -*- coding: utf-8 -*-
import unittest
import sys
from unihandecode import Unihandecoder

class TestUnidecode(unittest.TestCase):
	def test_ascii(self):
		u = Unihandecoder(lang="zh")
		for n in xrange(0,128):
			t = chr(n)
			self.failUnlessEqual(u.decode(t), t)

	def test_bmp(self):
		u = Unihandecoder(lang="zh")
		for n in xrange(0,0x10000):
			# Just check that it doesn't throw an exception
			try:
				t = unichr(n)
				u.decode(t)
			except:
				print "catch error at %02x"%n


	def test_mathematical_latin(self):
		# 13 consecutive sequences of A-Z, a-z with some codepoints
		# undefined. We just count the undefined ones and don't check
		# positions.
		if sys.maxunicode < 0x1d6a4:
			print "skip test because of Narrow Python"
			return

		empty = 0
		u = Unihandecoder(lang="zh")
		for n in xrange(0x1d400, 0x1d6a4):
			if n % 52 < 26:
				a = chr(ord('A') + n % 26)
			else:
				a = chr(ord('a') + n % 26)
			b = u.decode(unichr(n))

			if not b:
				empty += 1
			else:
				self.failUnlessEqual(b, a)

		self.failUnlessEqual(empty, 24)

	def test_mathematical_digits(self):
		if sys.maxunicode < 0x1d800:
			print "skip test because of Narrow Python"
			return

		u = Unihandecoder(lang="zh")
		# 5 consecutive sequences of 0-9
		for n in xrange(0x1d7ce, 0x1d800):
			a = chr(ord('0') + (n-0x1d7ce) % 10)
			b = u.decode(unichr(n))

			self.failUnlessEqual(b, a)

	def test_specific_bmp(self):

		TESTS = [
				(u"Hello, World!", 
				"Hello, World!"),

				(u"'\"\r\n",
				 "'\"\r\n"),

				(u"ČŽŠčžš",
				 "CZSczs"),

				(u"ア",
				 "a"),

				(u"α",
				"a"),

				(u"а",
				"a"),

				(u'ch\xe2teau',
				"chateau"),

				(u'vi\xf1edos',
				"vinedos"),
				
				(u"\u5317\u4EB0",
				"Bei Jing "),

				(u"Efﬁcient",
				"Efficient"),

				# Table that doesn't exist
				(u'\ua500',
				''),
				
				# Table that has less than 256 entriees
				(u'\u1eff',
				''),
			]

		u = Unihandecoder(lang="zh")
		for input, output in TESTS:
			self.failUnlessEqual(u.decode(input), output)

	def test_specific_ext(self):
		if sys.maxunicode < 0x1d6a4:
			print "skip test because of Narrow Python"
			return

		TESTS = [
				# Non-BMP character
				(u'\U0001d5a0',
				'A'),

				# Mathematical
				(u'\U0001d5c4\U0001d5c6/\U0001d5c1',
				'km/h'),
		]
		u = Unihandecoder(lang="zh")
		for input, output in TESTS:
			self.failUnlessEqual(u.decode(input), output)

	def test_ja(self):
		JATESTS = [
			(u'\u660e\u65e5\u306f\u660e\u65e5\u306e\u98a8\u304c\u5439\u304f',
			'Ashita ha Ashita no Kaze ga Fuku'),
			(u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
            'Mei Ten Mei Ten Teki Feng Sui ')
			]
		u = Unihandecoder(lang="ja")
		for input, output in JATESTS:
			self.failUnlessEqual(u.decode(input), output)

	def test_kr(self):
		KRTESTS = [
			(u'\ub0b4\uc77c\uc740 \ub0b4\uc77c \ubc14\ub78c\uc774 \ubd84\ub2e4',
        		'naeileun naeil barami bunda'),
			(u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
             'Myeng Chen Myeng Chen Cek Feng Chwi ')
			]
		u = Unihandecoder(lang="kr")
		for input, output in KRTESTS:
			self.failUnlessEqual(u.decode(input), output)

	def test_zh(self):
		ZHTESTS = [
			(u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
			 'Ming Tian Ming Tian De Feng Chui ')
			]
		u = Unihandecoder(lang="zh")
		for input, output in ZHTESTS:
			self.failUnlessEqual(u.decode(input), output)

	def test_vn(self):
		VNTESTS = [
			(u'Ng\xe0y mai gi\xf3 th\u1ed5i v\xe0o ng\xe0y mai',
			'Ngay mai gio thoi vao ngay mai'),
			(u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
            'Minh Tian Minh Tian De Feng Xuy ')
			]
		u = Unihandecoder(lang="vn")
		for input, output in VNTESTS:
			self.failUnlessEqual(u.decode(input), output)

if __name__ == "__main__":
    unittest.main()
