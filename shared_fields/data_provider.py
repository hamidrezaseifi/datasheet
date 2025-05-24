import base64
import configparser
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

from sqlalchemy import Table, text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared_fields.model_navigation_provider import ModelNavigationProvider


class DatabaseConfig:
    _user: str = None
    _password: str = None
    _host: str = None
    _port: int = None
    _database: str = None
    _database_type: str = None
    _url_additional: str = None

    def __init__(self, segment: str):
        config = configparser.ConfigParser()
        parent_path = Path(__file__).resolve().parent.parent
        init_path = os.path.join(parent_path, 'meinprojekt', 'database.ini')

        if not os.path.exists(init_path):
            raise FileNotFoundError(f"database.ini not found at {init_path}")

        config.read(init_path)

        self._user = config[segment]['user']
        self._password = config[segment]['password']
        self._host = config[segment]['host']
        try:
            self._port = int(config[segment]['port'])
        except ValueError:
            self._port = 0
        self._database = config[segment]['database']
        self._database_type = config[segment]['database_type']
        self._url_additional = config[segment]['url_additional']

    def get_url(self) -> str:
        _server = self._host
        if self._port and self._port > 0:
            _server = f"{self._host}:{self._port}"
        additional = ''
        if self._url_additional and len(self._url_additional) > 0:
            additional = f'?{self._url_additional}'
        return f"{self._database_type}://{self._user}:{self._password}@{_server}/{self._database}{additional}"


class DataProviderBase(ABC):
    _db_config: DatabaseConfig = None
    _columns: List[str] = []
    _table: Table = None
    _schema_name = ''
    _table_name = ''
    _table_created: bool = False
    _primary_key_list: List[str] = []
    _engine = None
    _session_maker = None
    _session = None
    _nav_provider: ModelNavigationProvider = None

    def __init__(self,
                 db_config: DatabaseConfig,
                 schema_name: str,
                 table_name: str,
                 primary_key_list: List[str],
                 nav_provider: ModelNavigationProvider):
        self._db_config = db_config
        self._schema_name = schema_name
        self._table_name = table_name
        self._primary_key_list = primary_key_list
        self._primary_key_list = primary_key_list
        self._nav_provider = nav_provider

        self._engine = create_engine(self._db_config.get_url(), echo=True, future=True)
        self._session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)


    def _create_table(self) -> [Table, Dict]:
        if self._table_created:
            return
        try:
            with self._engine.connect() as connection:
                if not self._engine.dialect.has_table(connection, self._table_name, schema=self._schema_name):
                    self._table.create(self._engine)
                    print(f"tabelle {self._schema_name}.{self._table_name} erstellt")
                else:
                    print(f"tabelle {self._schema_name}.{self._table_name} existiert")
                self._table_created = True
        except Exception as e:
            print(f"fehler bei tabellenerstellung: {e}")
            raise

    def _get_session(self):
        if self._session is None:
            self._session = self._session_maker()
        return self._session

    def _close_session(self):
        if self._session:
            self._session.close()
            self._session = None

    def _commit_session(self):
        if self._session:
            self._session.commit()

    def _rollback_session(self):
        if self._session:
            self._session.rollback()

    @abstractmethod
    def get_data_model(self):
        pass

    # alt
    def get_instance(self, p_key: dict, close_session: bool = True):
        try:
            qr = self._get_session().query(self.get_data_model())
            for attr, value in p_key.items():
                qr = qr.filter(getattr(self.get_data_model(), attr) == value)

            instance = qr.first()
            return instance

        except Exception as e:
            print(f"Exception in getting instance: {e}")
            self._rollback_session()
            raise
        finally:
            if close_session:
                self._close_session()

    @abstractmethod
    def get_django_instance(self, p_key, instance):
        pass

    # alt
    def delete(self, p_key, instance):
        try:
            if instance is None:
                instance = self.get_instance(p_key)
            self._get_session().delete(instance)
            self._commit_session()

        except Exception as e:
            print(f"Exception in deleting item: {e}")
            self._rollback_session()
            raise
        finally:
            self._close_session()

    def update(self, p_key, post_data):
        try:
            instance = self.get_instance(p_key, False)
            for field_name, value in post_data.items():
                if hasattr(instance, field_name):
                    if field_name not in self._primary_key_list:
                        setattr(instance, field_name, value)

            self._commit_session()

        except Exception as e:
            print(f"Exception in updating item: {e}")
            self._rollback_session()
            raise
        finally:
            self._close_session()

    def add(self, post_data):

        instance = self._create_new_instance(post_data)
        try:
            self._get_session().add(instance)
            self._commit_session()

        except Exception as e:
            print(f"Exception in adding item: {e}")
            self._rollback_session()
            raise
        finally:
            self._close_session()

    def _create_new_instance(self, post_data):
        instance = self.get_data_model()()
        for field_name, value in post_data.items():
            if hasattr(instance, field_name):
                setattr(instance, field_name, value)

        return instance

    def get_columns(self) -> List[str]:
        return self._columns

    def get_items(self, item_count: int = 15,
                  page: int = 0,
                  sort_col: str = None,
                  sort_type: str = None,
                  search_col: str = None,
                  search_value: str = None) -> [int, int, List[object]]:

        try:

            qr = self._get_session().query(self.get_data_model())
            if search_col and len(search_col) > 0 and search_value and len(search_value) > 0:
                qr = qr.filter(getattr(self.get_data_model(), search_col).like("%{}%".format(search_value)))

            total = qr.count()

            page_count = int(total / item_count)
            if page_count * item_count < total:
                page_count += 1
            if page > page_count:
                page = page_count

            qr = self._get_session().query(self.get_data_model())
            if search_col and len(search_col) > 0 and search_value and len(search_value) > 0:
                qr = qr.filter(getattr(self.get_data_model(), search_col).like("%{}%".format(search_value)))

            if sort_col:
                if sort_type is None:
                    sort_type = "asc"
                qr = qr.order_by(text(sort_col + " " + sort_type))
            if item_count:
                qr = qr.limit(item_count)
            if page:
                qr = qr.offset(item_count * (page - 1))

            items = qr.all()

            data_items = []
            for item in items:
                attrs = {key: value for key, value in item.__dict__.items() if not key.startswith('_')}
                data_item = {key: attrs[key] for key in self._columns}
                data_item = self._prepare_items_internal(data_item)
                pk_data_item = {key: attrs[key] for key in self.get_primary_key()}
                base64_string = self.convert_dic_to_base64(pk_data_item)
                data_item['_dj_pk'] = base64_string
                data_items.append(data_item)

                # print(f"{self.get_model_title()} -> pk-64: {base64_string}")

                t1 = self.convert_base64_to_dic(base64_string)

                # print(f"{self.get_model_title()} -> pk-dict: {t1}")

            return total, page_count, data_items

        except Exception as e:
            print(f"Exception in reading items: {e}")
            self._rollback_session()
            raise
        finally:
            self._close_session()

    def convert_dic_to_base64(self, dict_item):
        pk_as_str = json.dumps(dict_item)
        pk_as_str_bytes = pk_as_str.encode("utf8")
        base64_bytes = base64.b64encode(pk_as_str_bytes)
        base64_string = base64_bytes.decode("utf8")

        return base64_string

    def convert_base64_to_dic(self, base64_string):
        base64_bytes = base64_string.encode("ascii")

        string_bytes = base64.b64decode(base64_bytes)
        json_string = string_bytes.decode("ascii")

        json_dict = json.loads(json_string)

        return json_dict

    @abstractmethod
    def _prepare_items_internal(self, data_item):
        pass

    def get_nav_provider(self) -> ModelNavigationProvider:
        return self._nav_provider

    def get_primary_key(self) -> List[str]:
        return self._primary_key_list
