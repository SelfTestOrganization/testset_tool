============
TestSet tool
============


.. image:: https://img.shields.io/pypi/v/testset_tool.svg
        :target: https://pypi.python.org/pypi/testset_tool

.. image:: https://img.shields.io/travis/jhutar/testset_tool.svg
        :target: https://travis-ci.com/jhutar/testset_tool

.. image:: https://readthedocs.org/projects/testset-tool/badge/?version=latest
        :target: https://testset-tool.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Library to read and check SelfTest test set files

Example of the testset to read: https://github.com/SelfTestOrganization/testset_example_bash

Intentin is to use this only in: https://github.com/SelfTestOrganization/SelfTest-server


Usage
-----

To use TestSet tool in a project::

    import testset_tool.testset
    ts = testset.TestSet('path/to/your/testset/')
    print(ts)
    for area in ts.areas:
        print(area)
        for question in area.questions:
            print(question)

To use command line tool to check if your testset is syntactically correct::

    testset_tool --lint path/to/your/testset/

(it will traceback if issue is found).


And to use command line tool to quickly check content of your testset::

    testset_tool --show path/to/your/testset/

Credits
-------

This project is based on previous work of Ivana Vařeková, Pavel Moravec and Izidor Matušov (hope I'm not missing somebody).

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
