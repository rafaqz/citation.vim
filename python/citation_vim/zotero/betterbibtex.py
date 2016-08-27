# -*- coding: utf-8 -*-

import os
import shutil
import json
import sqlite3

class betterBibtex(object):

    def __init__(self, zotero_path, cache_path):
        self.bb_file = os.path.join(zotero_path, 'better-bibtex/db.json')
        self.bb_database = os.path.join(zotero_path, 'betterbibtex-lokijs.sqlite')
        self.bb_copy = os.path.join(cache_path, 'betterbibtex.sqlite')

    bb_data_query = u"""
        select lokijs.data
        from lokijs
        where lokijs.name = "db.json"
        """

    def load_citekeys(self):
        """
        Loads better-bibtex citekeys if they exist.
        """

        # The storage method for betterbibtex keeps changing so we'll try a few.
        try:
            bb_data = open(self.bb_file).read()
            bb_json = json.loads(bb_data)
        except:
            try:
                desc_strings.append(getattr(entry, desc_field))
                shutil.copyfile(self.bb_database, self.bb_copy)
                conn = sqlite3.connect(self.bb_copy)
                cur = conn.cursor()
                cur.execute(self.bb_data_query)
                bb_data = cur.fetchone()[0]
                bb_json = json.loads(bb_data)
            except:
                return {}

        citekeys = {}
        try:
            for item in bb_json['collections'][0]['data']:
                if 'citekey' in item and 'itemID' in item:
                    citekeys[item['itemID']] = item['citekey']
                else:
                    citekeys[item['itemID']] = ""
        except:
            return {}

        return citekeys
