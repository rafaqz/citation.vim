# -*- coding: utf-8 -*-

import os
import shutil
import json
import pprint
import sqlite3

class BetterBibtex(object):

    def __init__(self, zotero_path, cache_path):
        self.bb_database = os.path.join(zotero_path, 'better-bibtex.sqlite')
        self.bb_copy = os.path.join(cache_path, 'better-bibtex.sqlite')

    bb_data_query = u"""
        select data
        from "better-bibtex"
        where name = "better-bibtex.citekey"
        """

    def load_citekeys(self):
        """
        Loads better-bibtex citekeys if they exist.
        """

        # The storage method for betterbibtex citations is currently json in a sqlite database cell.
        try:
            shutil.copyfile(self.bb_database, self.bb_copy)
            conn = sqlite3.connect(self.bb_copy)
            cur = conn.cursor()
            cur.execute(self.bb_data_query)
            bb_data = cur.fetchone()[0]
            bb_json = json.loads(bb_data)
        except:
            return {}

        bb_citekeys = {}
        for item in bb_json['data']:
            # Check item contains required fields 
            if all (key in item for key in ("itemID", "citekey")):
                bb_citekeys[item['itemID']] = item['citekey']
            else:
                bb_citekeys[item['itemID']] = ""
        return bb_citekeys
