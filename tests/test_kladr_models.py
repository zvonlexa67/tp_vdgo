"""
Тесты для моделей KLADR: Altnames, Doma, Flat, Kladr, Street, SocrBase, NameMap.
Проверяют валидацию данных, генерацию DDL и корректность полей.
"""

import pytest
from pydantic import ValidationError

from tp_vdgo.models.kladr.altnames import Altnames
from tp_vdgo.models.kladr.doma import Doma
from tp_vdgo.models.kladr.flat import Flat
from tp_vdgo.models.kladr.kladr import Kladr
from tp_vdgo.models.kladr.street import Street
from tp_vdgo.models.kladr.socrbase import SocrBase
from tp_vdgo.models.kladr.namemap import NameMap


class TestAltnamesModel:
    """Тесты для модели Altnames."""

    def test_create_altnames_valid(self):
        """Создание валидной записи Altnames."""
        altnames = Altnames(oldcode="1234567890123456789", newcode="9876543210987654321", level="1")
        assert altnames.oldcode == "1234567890123456789"
        assert altnames.newcode == "9876543210987654321"
        assert altnames.level == "1"

    def test_altnames_missing_required_field(self):
        """Проверка отсутствия обязательного поля."""
        with pytest.raises(ValidationError):
            Altnames(oldcode="123", newcode="456")  # отсутствует level

    def test_altnames_get_pg_table_definition(self):
        """Проверка генерации DDL для таблицы altnames."""
        ddl = Altnames.get_pg_table_definition()
        assert "CREATE TABLE IF NOT EXISTS altnames" in ddl
        assert "oldcode CHAR(19) NOT NULL" in ddl
        assert "newcode CHAR(19) NOT NULL" in ddl
        assert "level CHAR(1) NOT NULL" in ddl
        assert "GRANT SELECT ON TABLE altnames TO admin_vdgo" in ddl
        assert "GRANT SELECT ON TABLE altnames TO user_vdgo" in ddl
        assert "GRANT SELECT ON TABLE altnames TO guest_vdgo" in ddl
        assert "GRANT SELECT ON TABLE altnames TO other_vdgo" in ddl

    def test_altnames_table_name_lowercase(self):
        """Проверка, что имя таблицы в нижнем регистре."""
        ddl = Altnames.get_pg_table_definition()
        assert "CREATE TABLE IF NOT EXISTS altnames" in ddl


class TestDomaModel:
    """Тесты для модели Doma."""

    def test_create_doma_valid(self):
        """Создание валидной записи Doma."""
        doma = Doma(
            name="Дом 1",
            socr="д",
            code="1234567890123456789",
            gninmb="1234",
            ocatd="12345678901",
        )
        assert doma.name == "Дом 1"
        assert doma.socr == "д"
        assert doma.code == "1234567890123456789"
        assert doma.korp is None
        assert doma.index is None
        assert doma.uno is None

    def test_create_doma_with_optional_fields(self):
        """Создание записи Doma с опциональными полями."""
        doma = Doma(
            name="Дом 2",
            korp="А",
            socr="д",
            code="9876543210987654321",
            index="123456",
            gninmb="5678",
            uno="9012",
            ocatd="11111111111",
        )
        assert doma.korp == "А"
        assert doma.index == "123456"
        assert doma.uno == "9012"

    def test_doma_missing_required_field(self):
        """Проверка отсутствия обязательного поля."""
        with pytest.raises(ValidationError):
            Doma(name="Дом", socr="д")  # отсутствует code

    def test_doma_get_pg_table_definition(self):
        """Проверка генерации DDL для таблицы doma."""
        ddl = Doma.get_pg_table_definition()
        assert "CREATE TABLE IF NOT EXISTS doma" in ddl
        assert "name CHAR(40) NOT NULL" in ddl
        assert "korp CHAR(10)" in ddl
        assert "socr CHAR(10) NOT NULL" in ddl
        assert "code CHAR(19) NOT NULL UNIQUE" in ddl
        assert "index CHAR(6)" in ddl
        assert "gninmb CHAR(4) NOT NULL" in ddl
        assert "uno CHAR(4)" in ddl
        assert "ocatd CHAR(11) NOT NULL" in ddl
        assert "CREATE INDEX idx_doma_code ON doma(code)" in ddl

    def test_doma_has_grants(self):
        """Проверка наличия GRANT в DDL."""
        ddl = Doma.get_pg_table_definition()
        for role in ["admin_vdgo", "user_vdgo", "guest_vdgo", "other_vdgo"]:
            assert f"GRANT SELECT ON TABLE doma TO {role}" in ddl


class TestFlatModel:
    """Тесты для модели Flat."""

    def test_create_flat_valid(self):
        """Создание валидной записи Flat."""
        flat = Flat(
            code="12345678901234567890123",
            np="1234",
            gninmb="5678",
            name="Квартира 1",
            uno="9012",
        )
        assert flat.code == "12345678901234567890123"
        assert flat.np == "1234"
        assert flat.gninmb == "5678"
        assert flat.name == "Квартира 1"
        assert flat.index is None
        assert flat.uno == "9012"

    def test_create_flat_with_optional_index(self):
        """Создание записи Flat с опциональным index."""
        flat = Flat(
            code="12345678901234567890123",
            np="1234",
            gninmb="5678",
            name="Квартира 2",
            index="123456",
            uno="9012",
        )
        assert flat.index == "123456"

    def test_flat_missing_required_field(self):
        """Проверка отсутствия обязательного поля."""
        with pytest.raises(ValidationError):
            Flat(code="123", np="123")  # отсутствуют обязательные поля

    def test_flat_get_pg_table_definition(self):
        """Проверка генерации DDL для таблицы flat."""
        ddl = Flat.get_pg_table_definition()
        assert "CREATE TABLE IF NOT EXISTS flat" in ddl
        assert "code CHAR(23) NOT NULL UNIQUE" in ddl
        assert "np CHAR(4) NOT NULL" in ddl
        assert "gninmb CHAR(4) NOT NULL" in ddl
        assert "name CHAR(40) NOT NULL" in ddl
        assert "index CHAR(6)" in ddl
        assert "uno CHAR(4) NOT NULL" in ddl
        assert "CREATE INDEX idx_flat_code ON flat(code)" in ddl


class TestKladrModel:
    """Тесты для модели Kladr."""

    def test_create_kladr_valid(self):
        """Создание валидной записи Kladr."""
        kladr = Kladr(
            name="Москва",
            socr="г",
            code="1234567890123",
            gninmb="1234",
            ocatd="12345678901",
        )
        assert kladr.name == "Москва"
        assert kladr.socr == "г"
        assert kladr.code == "1234567890123"
        assert kladr.index is None
        assert kladr.gninmb == "1234"
        assert kladr.uno is None
        assert kladr.ocatd == "12345678901"
        assert kladr.status is None

    def test_create_kladr_with_optional_fields(self):
        """Создание записи Kladr с опциональными полями."""
        kladr = Kladr(
            name="Санкт-Петербург",
            socr="г",
            code="9876543210987",
            index="123456",
            gninmb="5678",
            uno="9012",
            ocatd="11111111111",
            status="0",
        )
        assert kladr.index == "123456"
        assert kladr.uno == "9012"
        assert kladr.status == "0"

    def test_kladr_missing_required_field(self):
        """Проверка отсутствия обязательного поля."""
        with pytest.raises(ValidationError):
            Kladr(name="Город", socr="г")  # отсутствует code

    def test_kladr_get_pg_table_definition(self):
        """Проверка генерации DDL для таблицы kladr."""
        ddl = Kladr.get_pg_table_definition()
        assert "CREATE TABLE IF NOT EXISTS kladr" in ddl
        assert "name CHAR(40) NOT NULL" in ddl
        assert "socr CHAR(10) NOT NULL" in ddl
        assert "code CHAR(13) NOT NULL UNIQUE" in ddl
        assert "index CHAR(6)" in ddl
        assert "gninmb CHAR(4) NOT NULL" in ddl
        assert "uno CHAR(4)" in ddl
        assert "ocatd CHAR(11) NOT NULL" in ddl
        assert "status CHAR(1)" in ddl
        assert "CREATE INDEX idx_kladr_code ON kladr(code)" in ddl


class TestStreetModel:
    """Тесты для модели Street."""

    def test_create_street_valid(self):
        """Создание валидной записи Street."""
        street = Street(
            name="Ленина",
            socr="ул",
            code="12345678901234567",
            gninmb="1234",
            ocatd="12345678901",
        )
        assert street.name == "Ленина"
        assert street.socr == "ул"
        assert street.code == "12345678901234567"
        assert street.index is None
        assert street.gninmb == "1234"
        assert street.uno is None
        assert street.ocatd == "12345678901"

    def test_street_with_optional_fields(self):
        """Создание записи Street с опциональными полями."""
        street = Street(
            name="Мира",
            socr="пр-кт",
            code="98765432109876543",
            index="654321",
            gninmb="5678",
            uno="3456",
            ocatd="11111111111",
        )
        assert street.index == "654321"
        assert street.uno == "3456"

    def test_street_missing_required_field(self):
        """Проверка отсутствия обязательного поля."""
        with pytest.raises(ValidationError):
            Street(name="Улица", socr="ул")  # отсутствует code

    def test_street_get_pg_table_definition(self):
        """Проверка генерации DDL для таблицы street."""
        ddl = Street.get_pg_table_definition()
        assert "CREATE TABLE IF NOT EXISTS street" in ddl
        assert "name CHAR(40) NOT NULL" in ddl
        assert "socr CHAR(10) NOT NULL" in ddl
        assert "code CHAR(17) NOT NULL UNIQUE" in ddl
        assert "CREATE INDEX idx_street_code ON street(code)" in ddl


class TestSocrBaseModel:
    """Тесты для модели SocrBase."""

    def test_create_socrbase_valid(self):
        """Создание валидной записи SocrBase."""
        socrbase = SocrBase(
            level="1",
            scname="г",
            socrname="город",
            kod_t_st="001",
        )
        assert socrbase.level == "1"
        assert socrbase.scname == "г"
        assert socrbase.socrname == "город"
        assert socrbase.kod_t_st == "001"

    def test_socrbase_missing_required_field(self):
        """Проверка отсутствия обязательного поля."""
        with pytest.raises(ValidationError):
            SocrBase(level="1", scname="г")  # отсутствуют обязательные поля

    def test_socrbase_get_pg_table_definition(self):
        """Проверка генерации DDL для таблицы socrbase."""
        ddl = SocrBase.get_pg_table_definition()
        assert "CREATE TABLE IF NOT EXISTS socrbase" in ddl
        assert "level CHAR(5) NOT NULL" in ddl
        assert "scname CHAR(10) NOT NULL" in ddl
        assert "socrname CHAR(29) NOT NULL" in ddl
        assert "kod_t_st CHAR(3) NOT NULL" in ddl


class TestNameMapModel:
    """Тесты для модели NameMap."""

    def test_create_namemap_valid(self):
        """Создание валидной записи NameMap."""
        namemap = NameMap(
            code="12345678901234567",
            name="Москва",
            shname="МСК",
            scname="Москва",
        )
        assert namemap.code == "12345678901234567"
        assert namemap.name == "Москва"
        assert namemap.shname == "МСК"
        assert namemap.scname == "Москва"

    def test_namemap_missing_required_field(self):
        """Проверка отсутствия обязательного поля."""
        with pytest.raises(ValidationError):
            NameMap(code="123", name="Город")  # отсутствуют обязательные поля

    def test_namemap_get_pg_table_definition(self):
        """Проверка генерации DDL для таблицы namemap."""
        ddl = NameMap.get_pg_table_definition()
        assert "CREATE TABLE IF NOT EXISTS namemap" in ddl
        assert "code CHAR(17) NOT NULL UNIQUE" in ddl
        assert "name CHAR(250) NOT NULL" in ddl
        assert "shname CHAR(40) NOT NULL" in ddl
        assert "scname CHAR(10) NOT NULL" in ddl
        assert "CREATE INDEX idx_namemap_code ON namemap(code)" in ddl


class TestKladrModelsInheritance:
    """Тесты для проверки наследования всех KLADR моделей от BaseModel."""

    def test_altnames_inherits_from_basemodel(self):
        """Проверка, что Altnames наследуется от BaseModel."""
        from pydantic import BaseModel
        assert issubclass(Altnames, BaseModel)

    def test_doma_inherits_from_basemodel(self):
        """Проверка, что Doma наследуется от BaseModel."""
        from pydantic import BaseModel
        assert issubclass(Doma, BaseModel)

    def test_flat_inherits_from_basemodel(self):
        """Проверка, что Flat наследуется от BaseModel."""
        from pydantic import BaseModel
        assert issubclass(Flat, BaseModel)

    def test_kladr_inherits_from_basemodel(self):
        """Проверка, что Kladr наследуется от BaseModel."""
        from pydantic import BaseModel
        assert issubclass(Kladr, BaseModel)

    def test_street_inherits_from_basemodel(self):
        """Проверка, что Street наследуется от BaseModel."""
        from pydantic import BaseModel
        assert issubclass(Street, BaseModel)

    def test_socrbase_inherits_from_basemodel(self):
        """Проверка, что SocrBase наследуется от BaseModel."""
        from pydantic import BaseModel
        assert issubclass(SocrBase, BaseModel)

    def test_namemap_inherits_from_basemodel(self):
        """Проверка, что NameMap наследуется от BaseModel."""
        from pydantic import BaseModel
        assert issubclass(NameMap, BaseModel)
