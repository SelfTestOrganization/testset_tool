import logging
import os

import yaml

"""Load a testset."""


class Question(object):
    """Represent testset area question as an object."""

    def __init__(self, filename):
        logging.info(f"Creating question from {filename}")
        self.filename = filename

        with open(filename, 'r') as fp:
            metadata = yaml.load(fp, Loader=yaml.Loader)
            self.type = metadata['type']
            self.timeout = int(metadata['timeout'])
            self.question = metadata['question']
            self.answers = metadata['answers']
            self.correct = metadata['correct']

    def __repr__(self):
        return f"<Question({self.filename}, {self.type}, {self.timeout})>"

    def lint(self):
        logging.debug(f"Linting question from {self.filename}")
        assert self.type == 'abc'
        assert self.timeout > 0
        assert isinstance(self.answers, dict)
        assert self.correct in self.answers

    def show(self):
        print(f"      - Type: {self.type}")
        print(f"        Timeout: {self.timeout}")
        print(f"        Question: {self.question}")
        print(f"        Correct: {self.correct}")
        print("        Answers:")
        for answer, value in self.answers.items():
            print(f"            {answer}) {value}")


class Area(object):
    """Represent testset area as an object."""

    def __init__(self, dirname, questions_to_ask):
        logging.info(f"Creating area from {dirname}")
        self.dirname = dirname
        self.name = os.path.basename(dirname)
        self.questions_to_ask = int(questions_to_ask)

        self.questions = []
        for item in os.listdir(dirname):
            if os.path.isfile(os.path.join(dirname, item)) \
               and (item.endswith('.yaml') or item.endswith('.yml')):
                question = Question(os.path.join(dirname, item))
                self.questions.append(question)

    def __gt__(self, other):
        return self.dirname > other.dirname

    def __repr__(self):
        return f"<Area({self.basename}, {self.questions_to_ask})>"

    def lint(self):
        logging.debug(f"Linting area from {self.dirname}")
        assert len(self.name) > 0
        assert self.questions_to_ask > 0
        assert self.questions_to_ask <= len(self.questions)

        for question in self.questions:
            question.lint()

    def show(self):
        print(f"  - Area: {self.name}")
        print(f"    Questions to ask: {self.questions_to_ask}")
        print("    Questions:")
        for question in self.questions:
            question.show()


class TestSet(object):
    """Represent testset as an object."""

    def __init__(self, dirname):
        logging.info(f"Creating testset from {dirname}")
        self.dirname = dirname

        with open(os.path.join(dirname, 'metadata.yaml'), 'r') as fp:
            metadata = yaml.load(fp, Loader=yaml.Loader)
            self.name = metadata['name']
            self.version = int(metadata['version'])
            self.questions_to_ask = metadata['questions_to_ask']

        self.areas = []
        for item in os.listdir(dirname):
            if os.path.isdir(os.path.join(dirname, item)) and item in self.questions_to_ask:
                area = Area(os.path.join(dirname, item), self.questions_to_ask[item])
                self.areas.append(area)
        self.areas.sort()

    def __repr__(self):
        return f"<TestSet({self.dirname}, {self.version})>"

    def lint(self):
        logging.debug(f"Linting testset from {self.dirname}")
        assert self.version > 0
        assert len(self.questions_to_ask) > 0
        assert len(self.questions_to_ask) == len(self.areas)

        for area in self.areas:
            area.lint()

    def show(self):
        print(f"Name: {self.name}")
        print(f"Version: {self.version}")
        print("Areas:")
        for area in self.areas:
            area.show()
