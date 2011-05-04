# -*- coding: utf-8 -*-

import os

from pojson import convert, po2dict
import polib

    
def test_po2dict():
    po = polib.POFile()
    po.metadata = {}
    entry = polib.POEntry(
        msgid=u'Hello world',
        msgstr=u'Hallo wereld')
    po.append(entry)
    
    result = po2dict(po)

    assert result == {'': {}, u'Hello world': u'Hallo wereld'}

def test_po2dict_with_metadata():
    po = polib.POFile()
    po.metadata = {'Project-Id-Version': '1.0'}
    entry = polib.POEntry(
        msgid=u'Hello world',
        msgstr=u'Hallo wereld')
    po.append(entry)
    
    result = po2dict(po)

    assert result == {'': {'Project-Id-Version': '1.0'},
                      u'Hello world': u'Hallo wereld'}

def test_convert(tmpdir):
    po = polib.POFile()
    po.metadata = {}
    entry = polib.POEntry(
        msgid=u'Hello world',
        msgstr=u'Hallo wereld')
    po.append(entry)

    path = tmpdir.join('test.po').strpath
    po.save(path)
    
    result = convert('foo', path)
    # XXX dependent on default key sorting of simplejson
    assert result == '{"foo": {"": {}, "Hello world": "Hallo wereld"}}'

def test_convert_detect_encoding(tmpdir):
    po = polib.POFile()
    po.metadata = {}
    entry = polib.POEntry(
        msgid=u'One',
        msgstr=u'Eén')
    po.append(entry)

    path = tmpdir.join('test.po').strpath
    po.save(path)

    result = convert('foo', path)
    # XXX dependent on default key sorting of simplejson
    assert result == u'{"foo": {"": {}, "One": "Eén"}}'

def test_convert_explicit_encoding(tmpdir):
    po = polib.POFile()
    po.metadata = {}
    entry = polib.POEntry(
        msgid=u'One',
        msgstr=u'Eén')
    po.append(entry)

    path = tmpdir.join('test.po').strpath
    po.save(path)

    result = convert('foo', path, encoding='utf-8')
    # XXX dependent on default key sorting of simplejson
    assert result == u'{"foo": {"": {}, "One": "Eén"}}'

def test_convert_pretty_print(tmpdir):
    po = polib.POFile()
    po.metadata = {}
    entry = polib.POEntry(
        msgid=u'One',
        msgstr=u'Een')
    po.append(entry)

    path = tmpdir.join('test.po').strpath
    po.save(path)

    result = convert('foo', path, pretty_print=True)
    # XXX dependent on default key sorting of simplejson
    assert result == u'''\
{
    "foo": {
        "": {}, 
        "One": "Een"
    }
}'''
    

def test_convert_javascript(tmpdir):
    po = polib.POFile()
    po.metadata = {}
    entry = polib.POEntry(
        msgid=u'One',
        msgstr=u'Een')
    po.append(entry)

    path = tmpdir.join('test.po').strpath
    po.save(path)

    result = convert('foo', path, encoding='utf-8',
                     js=True)
    assert result == u'var json_locale_data = {"foo": {"": {}, "One": "Een"}};'

def test_convert_javascript_prettyprint(tmpdir):
    po = polib.POFile()
    po.metadata = {}
    entry = polib.POEntry(
        msgid=u'One',
        msgstr=u'Een')
    po.append(entry)

    path = tmpdir.join('test.po').strpath
    po.save(path)

    result = convert('foo', path, encoding='utf-8',
                     js=True, pretty_print=True)

    assert result == u'''\
var json_locale_data = {
    "foo": {
        "": {}, 
        "One": "Een"
    }
};'''
    
def pytest_funcarg__nl_po(request):
    p = os.path.join(
        os.path.dirname(request.module.__file__), 'testdata', 'nl.po')
    return polib.pofile(p)

def test_po2dict_with_plural(nl_po):
    result = po2dict(nl_po)
    values = result["1 field did not validate"]
    assert values == [u'%1 fields did not validate',
                      u'1 veld kon niet gevalideerd worden',
                      u'%1 velden konden niet gevalideerd worden']

    