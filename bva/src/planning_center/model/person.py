import typing


class Person:
    def __init__(self, data, **kwargs):
        self._data = data
        self._kwargs = kwargs

    @property
    def _attributes(self):
        return self._data["attributes"]

    @property
    def name(self):
        return self._attributes["name"]

    @property
    def id(self):
        return self._data["id"]

    @property
    def phone_number(self) -> typing.Optional[str]:
        return self._kwargs.get("phone_number", None)