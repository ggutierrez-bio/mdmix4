import os
from argparse import ArgumentParser
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pymdmix_core.plugin.crud import CRUDPlugin

from .conftest import FPATH


class FixtureClass(declarative_base()):
    __tablename__ = "fixture_class"
    test_field1 = Column(Integer, primary_key=True)
    test_field2 = Column(String(32))

    def __repr__(self) -> str:
        return f"FixtureModel. TF1 = {self.test_field1}, TF2 = {self.test_field2}"


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
    args = parser.parse_args(["test", "list"])
    crud_plugin.run(args)
    # assert the stdout
