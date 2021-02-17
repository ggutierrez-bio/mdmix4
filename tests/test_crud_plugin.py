import os
from argparse import ArgumentParser
from sqlalchemy.schema import Sequence
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pymdmix_core.plugin.crud import CRUDPlugin

from .conftest import FPATH


class FixtureClass(declarative_base()):
    __tablename__ = "fixture_class"
    id = Column(Integer, Sequence('fixture_ids', start=1, increment=1), primary_key=True)
    test_field1 = Column(Integer)
    test_field2 = Column(String(32))

    def __repr__(self) -> str:
        return f"FixtureModel. id={self.id} TF1 = {self.test_field1}, TF2 = {self.test_field2}"


class CRUDTestPlugin(CRUDPlugin):
    NAME = "test"
    CLASS = FixtureClass


def test_crud_plugin_loading(tmpdir):
    engine = create_engine(f"sqlite:///{tmpdir}/sqlite.db")
    parser = ArgumentParser()
    crud_plugin = CRUDTestPlugin(parser, engine)
    assert crud_plugin is not None
    "/data/UB/repositories/mdmix4/mdmix-core/tests/fixture_crud_plugin/input.yml"
    config_file = os.path.join(FPATH, "fixture_crud_plugin", "input.yml")
    args = parser.parse_args(["test", "create", "-y", config_file])
    crud_plugin.run(args)
    session = sessionmaker(bind=engine)()
    assert len(session.query(FixtureClass).all()) == 1
    model: FixtureClass = session.query(FixtureClass).first()
    assert model.test_field1 == 42
    assert model.test_field2 == "foo"

    config_file = os.path.join(FPATH, "fixture_crud_plugin", "input.json")
    args = parser.parse_args(["test", "create", "-j", config_file])
    crud_plugin.run(args)
    assert len(session.query(FixtureClass).all()) == 2
    model: FixtureClass = session.query(FixtureClass).all()[1]
    assert model.test_field1 == 35
    assert model.test_field2 == "bar"

    args = parser.parse_args(["test", "list"])
    crud_plugin.run(args)
    # assert there are 2 lines in output

    args = parser.parse_args(["test", "info", "2"])
    crud_plugin.run(args)
    # assert the stdout is the str representation of model with 35 and bar

    args = parser.parse_args(["test", "info", "2", "1"])
    crud_plugin.run(args)
    # assert there are 2 lines in stdout

    args = parser.parse_args(["test", "delete", "1", "2"])
    crud_plugin.run(args)
    assert len(session.query(FixtureClass).all()) == 0
