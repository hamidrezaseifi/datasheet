# sales_prognosen_matrix/models_sqlalchemy.py
from abc import ABC
from datetime import datetime, date

from sqlalchemy import Column, BigInteger, Integer, String, Float, Date, ForeignKey, MetaData, Table, \
    PrimaryKeyConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapper

from sales_prognosen_matrix.forms import get_month_name
from shared_fields.data_provider import DataProviderBase, DatabaseConfig, ModelNavigationProvider
from shared_fields.model_navigation_provider import DummyModelNavigationProvider

Base = declarative_base()


class ZvmObjekte(Base):
    __tablename__ = 'zvm_objekte'
    __table_args__ = {'schema': 'ZVM_STAGING.stage'}
    Kuerzel = Column(String(255), primary_key=True)


class ZvmObjektProvider(DataProviderBase, ABC):
    def __init__(self):
        print("Initializing ZvmObjektProvider")
        super().__init__(DatabaseConfig('ZvmObjekt'),
                         'ZVM_STAGING.stage',
                         'zvm_objekte',
                         ['Kuerzel'],
                         ModelNavigationProvider('', '', '', None)
                         )
        # Kein create_table!
        metadata = MetaData()
        engine = self._engine  # von DataProviderBase bereitgestellt

        self._table = Table(
            self._table_name,
            metadata,
            autoload_with=engine,
            schema=self._schema_name
        )

    def _prepare_items_internal(self, data_item):
        # Nur wenn du später Transformation brauchst
        return data_item

    def get_data_model(self):
        return ZvmObjekte

    def get_django_instance(self, p_key, instance):
        django_instance = ZvmObjekte(Kuerzel=instance.Kuerzel)
        return django_instance


ZVM_OBJEKT_DATA_PROVIDER = ZvmObjektProvider()


class SalesObjekt(Base):
    __tablename__ = 'sales_objekt'
    __table_args__ = {'schema': 'test_evar.djange'}
    objekt = Column(String(100), nullable=False, primary_key=True, unique=False)
    sort_order = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    sales_date = relationship(
        "SalesPrognose",
        back_populates="sales_objekt",
        foreign_keys="SalesPrognose.objekt"
    )


class SalesObjektProvider(DataProviderBase, ABC):
    def __init__(self):
        print("Initializing SalesObjektProvider")
        super().__init__(DatabaseConfig('SalesObjekt'),
                         'test_evar.djange',
                         'sales_objekt',
                         ['objekt'],
                         ModelNavigationProvider("Objekte", "sales/objekte", "Sales", self))
        metadata = MetaData()

        self._table = Table(self._table_name, metadata,
                            Column('objekt', String(255), primary_key=True, nullable=False),
                            Column('sort_order', Integer, nullable=False),
                            Column('created_at', DateTime),
                            PrimaryKeyConstraint('objekt', name=self._table_name + '_PK', mssql_clustered=True),
                            schema=self._schema_name
                            )
        self._columns = [c[0] for c in self._table.columns.items()]
        self._create_table()

    def _prepare_items_internal(self, data_item):
        return data_item

    def get_data_model(self):
        return SalesObjekt

    def get_django_instance(self, p_key, instance):
        django_instance = SalesObjekt(objekt=instance.objekt,
                                      sort_order=instance.sort_order,
                                      created_at=instance.created_at)
        return django_instance

    def get_model_title(self) -> str:
        return "SalesObjekt"

    def get_base_url(self) -> str:
        return "sales_objekt"


SALES_OBJEKT_DATA_PROVIDER = SalesObjektProvider()


class SalesPrognose(Base):
    __tablename__ = 'sales_prognose'
    __table_args__ = {'schema': 'test_evar.djange'}

    objekt = Column(BigInteger, ForeignKey('test_evar.djange.sales_objekt.objekt'), primary_key=True, nullable=False)
    sortierreihen_folge = Column(BigInteger, ForeignKey('test_evar.djange.sales_objekt.sort_order'), primary_key=True, nullable=False)
    jahr = Column(Integer, primary_key=True, nullable=False)
    monat = Column(Integer, primary_key=True, nullable=False)
    datum = Column(Date, nullable=True)
    prognose = Column(Float, default=0.0, nullable=True)
    created_at = Column(Date, default=datetime.utcnow, nullable=True)

    sales_objekt = relationship(
        "SalesObjekt",
        back_populates="sales_date",
        foreign_keys=[objekt]
    )


class SalesPrognoseProvider(DataProviderBase, ABC):

    def __init__(self):
        super().__init__(DatabaseConfig('SalesPrognose'),
                         'test_evar.djange',
                         'sales_prognose',
                         ['objekt', 'sortierreihen_folge', 'jahr', 'monat'],
                         ModelNavigationProvider("Prognose", "sales/prognose", "Sales", self))
        metadata = MetaData()

        self._table = Table(self._table_name, metadata,
                            Column('objekt', String(255), primary_key=True,  nullable=False),
                            Column('sortierreihen_folge', Integer, primary_key=True, nullable=False),
                            Column('jahr', Integer, primary_key=True, nullable=False),
                            Column('monat', Integer, primary_key=True, nullable=False),
                            Column('datum', Date, nullable=True),
                            Column('prognose', Float, nullable=True),
                            Column('created_at', DateTime),
                            PrimaryKeyConstraint('objekt', 'sortierreihen_folge', 'jahr', 'monat',
                                                 name=self._table_name + '_PK', mssql_clustered=False),
                            schema=self._schema_name
                            )
        self._columns = [c[0] for c in self._table.columns.items()]

        self._create_table()

    def get_data_model(self):
        return SalesPrognose

    def get_django_instance(self, p_key, instance):
        jahr = instance.jahr
        monat = instance.mona
        datum = date(jahr, monat, 1) if jahr and monat else None
        django_instance = SalesPrognose(objekt=instance.objekt,
                                        sortierreihen_folge=instance.sortierreihen_folge,
                                        jahr=instance.jahr,
                                        monat=instance.monat,
                                        datum=datum,
                                        prognose=instance.prognose if instance else 0.0,
                                        created_at=instance.created_at if instance else datetime.utcnow().date()
                                        )
        return django_instance

    def _prepare_items_internal(self, data_item):
        data_item['monat'] = get_month_name(data_item['monat'])
        return data_item

    def get_model_title(self) -> str:
        return "SalesPrognose"

    def get_base_url(self) -> str:
        return "sales_objekt"


SALES_PROGNOSE_DATA_PROVIDER = SalesPrognoseProvider()
