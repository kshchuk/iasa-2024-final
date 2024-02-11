import xml.etree.ElementTree as ET
from typing import List
from controller.controller import Controller
from uuid import uuid4


class RSSFeed:

    def __init__(self, title='WEB ANALYZER RSS FEED',
                 link='https://www.example.com',
                 description='Recently collected data'):
        self.title = title
        self.link = link
        self.desc = description

    def create_rss_feed_from_dict(self, values: dict, filename: str):
        controller = Controller()
        df = controller.analyze_event(values)
        self.create_rss_feed_from_and_save(df, filename)

    def create_rss_feed(self, keywords: List[str], period: str, sources: List[str], filename: str):
        options = {
            'tags': keywords,
            'services': sources,
            'timeperiod': period
        }
        self.create_rss_feed_from_dict(options, filename)

    def create_rss_feed_from_and_save(self, df, filename):
        rss_str = self.create_rss_feed_from(df)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write(rss_str)

    def create_rss_feed_from(self, df):
        rss = ET.Element('rss', version='2.0')
        channel = ET.SubElement(rss, 'channel')

        ET.SubElement(channel, 'title').text = self.title
        ET.SubElement(channel, 'link').text = self.link
        ET.SubElement(channel, 'description').text = self.desc

        for index, row in df.iterrows():
            item = ET.SubElement(channel, 'item')
            ET.SubElement(item, 'title').text = row['Title']
            ET.SubElement(item, 'description').text = row['Summary']
            ET.SubElement(item, 'pubDate').text = row['Date'].strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, 'guid').text = str(uuid4())
            ET.SubElement(item, 'link').text = row['Link']
            ET.SubElement(item, 'category').text = row['Sentiment']

        rss_str = ET.tostring(rss, encoding='unicode')
        return rss_str
