import logging
import os

import testset

"""Convert old format of testsets to a new one."""


def convert(from_dir, to_dir):
    logging.info(f"Converting {from_dir} to {to_dir}")

    if not os.path.exists(to_dir):
        os.makedirs(to_dir)

    assert os.path.isdir(from_dir)
    assert os.path.isdir(to_dir)

    testset.TestSet.convert(from_dir, to_dir)
