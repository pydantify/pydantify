from lxml import etree
from pydantic import BaseModel
from typing import Any


def model_dump_xml_string(model: BaseModel, pretty_print: bool = False) -> str:
    element = model_dump_xml(model)
    return etree.tostring(element, encoding=str, pretty_print=pretty_print)


def model_dump_xml(model: BaseModel) -> etree.Element:
    dump = model.model_dump(exclude_defaults=True)
    return dict_to_elements(dump, model.namespace, model.prefix)[0]


def dict_to_elements(
    model: dict[str, Any], namespace: str, prefix: str
) -> list[etree.Element]:
    result: list[etree.Element] = []
    for name, value in model.items():
        element = etree.Element(f"{{{namespace}}}{name}", nsmap={prefix: namespace})
        if isinstance(value, dict):
            for child in dict_to_elements(value, namespace, prefix):
                element.append(child)
        else:
            element.text = str(value)
        result.append(element)
    return result


def model_validate_xml(
    model_class: type[BaseModel], element: etree.Element
) -> BaseModel:
    model_dict = element_to_dict(element)
    return model_class.model_validate(model_dict)


def element_to_dict(element: etree.Element) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for child in element:
        if len(child):
            result[child.tag.split("}", 1)[1]] = element_to_dict(child)
        else:
            result[child.tag.split("}", 1)[1]] = child.text
    return result
