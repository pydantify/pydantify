import json

from pydantify.utility.model_generator import ModelGenerator
from pydantic import BaseModel, RootModel
from pydantify.models import ClassVarModel


def test_model_json_schema():
    result = MockRootModel.model_json_schema()
    assert result == json.load(open("tests/test_model_generator.json"))


def test_generate_pydantic():
    source = json.load(open("tests/test_model_generator.json"))
    result = ModelGenerator._generate_pydantic(source)
    assert result == open("tests/test_model_generator_result.py").read()


class MockModel(BaseModel):
    prefix: ClassVarModel = "if"


class MockRootModel(RootModel):
    root: MockModel
