#!/usr/bin/env python

"""Tests for `testset_tool` package."""


import contextlib
import io
import unittest

from testset_tool import testset


class TestTestset_tool(unittest.TestCase):
    """Tests for `testset_tool` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_ok_load(self):
        """Test testset load."""
        ts = testset.TestSet("tests/fixtures/ok/")

    def test_ok_lazy_load(self):
        ts = testset.TestSet("tests/fixtures/ok/")

        self.assertEqual(len(ts.areas), 0)
        ts.areas['01_first'].load_meta()
        self.assertEqual(len(ts.areas), 1)
        keys = ts.areas.keys()
        self.assertEqual(list(keys), ['01_first', '02_second'])

        self.assertEqual(len(ts.areas['01_first'].questions), 0)
        ts.areas['01_first'].questions['1'].load_meta()
        self.assertEqual(len(ts.areas['01_first'].questions), 1)

    def test_ok_whoami(self):
        ts = testset.TestSet("tests/fixtures/ok/")
        self.assertEqual(ts.whoami, 'ok')
        self.assertEqual(ts.areas['01_first'].whoami, 'ok/01_first')
        self.assertEqual(ts.areas['01_first'].questions['1'].whoami, 'ok/01_first/1')

    def test_ok_show(self):
        """Test testset show."""
        ts = testset.TestSet("tests/fixtures/ok/")
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            ts.show()
        self.assertTrue("Description: Demo testset for SelfTest" in f.getvalue())
        self.assertTrue("Area: 01_first" in f.getvalue())
        self.assertTrue("Question: <p>From following possibilities choose <strong>first</strong> possibility.</p>" in f.getvalue())

    def test_ok_lint(self):
        """Test testset lint."""
        ts = testset.TestSet("tests/fixtures/ok/")
        ts.lint()
