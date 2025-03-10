#!/bin/env python3.4
__author__ = 'Ostico <ostico@gmail.com>'
# -*- coding: utf-8 -*-
import unittest
import os

os.environ['DEBUG'] = "0"
os.environ['DEBUG_VERBOSE'] = "0"

import pyorient


class CommandTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CommandTestCase, self).__init__(*args, **kwargs)
        self.client = None

    def setUp(self):

        self.client = pyorient.OrientDB("localhost", 2424)
        self.client.connect("admin", "admin")

        db_name = "test_tr"
        try:
            self.client.db_drop(db_name)
        except pyorient.PyOrientCommandException as e:
            print(e.message)
        finally:
            db = self.client.db_create(db_name, pyorient.DB_TYPE_GRAPH,
                                       pyorient.STORAGE_TYPE_MEMORY)

        cluster_info = self.client.db_open(
            db_name, "admin", "admin", pyorient.DB_TYPE_GRAPH, ""
        )

    def test_reserved_words(self):

        class_id1 = self.client.command("create class my_v_class extends V")[0]
        class_id2 = self.client.command("create class str extends E")[0]
        rec1 = {'@my_v_class': {'accommodation': 'house', 'work': 'office',
                                'holiday': 'sea'}}
        rec2 = {'@my_v_class': {'accommodation': 'house', 'work2': 'office',
                                'holiday': 'sea3'}}
        rec_position1 = self.client.record_create(class_id1, rec1)
        rec_position2 = self.client.record_create(class_id1, rec2)

        sql_edge = "create edge from " + rec_position1.rid + " to " + \
                   rec_position2.rid
        res = self.client.command(sql_edge)

        # print (res[0].__getattribute__('in'))
        assert isinstance(res[0].__getattribute__('in'),
                          pyorient.OrientRecordLink)
        assert res[0].__getattribute__('in').get_hash() == rec_position2.rid

        # print (res[0].out)
        assert isinstance(res[0].out, pyorient.OrientRecordLink)
        assert res[0].out.get_hash() == rec_position1.rid

        result = self.client.query(
            "select @rid, @version, holiday from my_v_class")
        # for x in result:
        # print ( "%r" % x.rid.get() )
        # print ( "%r" % x.rid.get_hash() )
        # print ( "%r" % x.holiday )
        # print ( "%r" % x.version )

        assert result[0].rid.get() == '11:0'
        assert result[0].rid.get_hash() == rec_position1.rid
        assert result[0].holiday == rec1['@my_v_class']['holiday']
        assert result[0].version == 2

        assert result[1].rid.get() == '11:1'
        assert result[1].rid.get_hash() == rec_position2.rid
        assert result[1].holiday == rec2['@my_v_class']['holiday']
        assert result[1].version == 2

        x = self.client.command(
            "insert into V ( 'rid', 'version', 'model', 'ciao')" +
            " values ('test_rid', 'V1', '1123', 1234)")

        # print (x[0].rid)
        # print (x[0].model)
        assert x[0].ciao == 1234

        x = self.client.command("select rid, @rid, model, ciao from V")
        # print (x[0].rid)
        # print (x[0].rid2)
        # print (x[0].model)
        assert x[0].model == '1123'
        assert x[0].ciao == 1234

    def test_sql_batch(self):
        cmd = "begin;" + \
              "let a = create vertex set script = true;" + \
              "let b = select from v limit 1;" + \
              "let e = create edge from $a to $b;" + \
              "commit retry 100;"

        edge_result = self.client.batch(cmd)

        # print( cluster_id[0] )
        # print (cluster_id[0].__getattribute__('in'))
        assert isinstance(edge_result[0].__getattribute__('in'),
                          pyorient.OrientRecordLink)
        assert edge_result[0].__getattribute__('in').get_hash() == "#9:0", \
            "in is not equal to '#9:0': %r" % edge_result[0].__getattribute__(
                'in').get_hash()

        # print (cluster_id[0].out)
        assert isinstance(edge_result[0].out, pyorient.OrientRecordLink)
        assert edge_result[0].out.get_hash() == "#9:100", \
            "out is not equal to '#9:101': %r" % edge_result[0].out.get_hash()


# x = CommandTestCase('test_reserved_words').run()