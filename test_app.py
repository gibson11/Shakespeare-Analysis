import app
import unittest 
import urllib
import pathlib
import xml.etree.ElementTree as ET
import os
from flask import Flask, url_for, send_from_directory
from settings import APP_STATIC


class AppTests(unittest.TestCase): 

    def setUp(self):
        # creates a test client
        self.test_client = app.app.test_client()
        # propagate the exceptions to the test client
        self.test_client.testing = True 
        
 

    def openurl(self, url):
	    return self.test_client.post('/', data=dict(url=url), follow_redirects=True)

    """Check that the application gets and responds to HTTP GET request"""
    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.test_client.get('/') 
        # assert the status code of the response
        self.assertEqual(result.status_code, 200) 

    """Check that homepage works fine and has all components"""
    def test_home_page(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.test_client.get('/') 
        # assert the response data is on the URL page
        assert b'Shakespeare Play Analysis URL' in result.data
        #assert the presence of the URL input form
        assert b'form' in result.data
        #submit button
        assert b'Submit' in result.data

    """Check that the list of speakers is in descending order according to their respective
     number of lines"""
    def test_speaker_order(self):
        testfile = 'static/test01.xml'
        result = self.openurl(testfile)
        #check that label and data arrays are in order and have the correct values
        labels = 'labels : [\n   "Lafeu",\n   \n   "Bertram",\n   \n   "Countess",\n   ]' 
        data = 'data : [\n    5,\n    \n    3,\n    \n    1,\n    ]' 
        assert labels.encode('utf-8') in result.data
        assert data.encode('utf-8') in result.data

    """Good url but no speeches"""
    def test_zero_speakers(self):
        testfile = 'static/test02.xml'
        result = self.openurl(testfile)
        assert b'URL does not have any speakers' in result.data

    """Blank XML file"""
    def test_blank_file(self):
        testfile = 'static/test03.xml'
        result = self.openurl(testfile)
        assert b'The XML file has a bad format' in result.data 

    def test_zero_lines(self):
        testfile = 'static/test04.xml'
        result = self.openurl(testfile)
        assert b'data : [\n    5,\n    \n    3,\n    \n    0,\n    ]' in result.data
        assert b'"Countess",\n   ]' in result.data #countess has 0 lines


    """XML with bad format"""
    def test_XML_with_bad_format(self):
        testfile = 'static/test05.xml'
        result = self.openurl(testfile)
        assert b'The XML file has a bad format' in result.data


        

        
        



if __name__ == '__main__':
    unittest.main()



    