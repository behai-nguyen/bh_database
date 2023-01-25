"""
Provide mechanisms to implement a custom paginating SQLAlchemy Query.

For usage example, see the following test modules:

    * ``./tests/test_11_paginator_postgresql.py``
    * ``./tests/test_12_paginator_mysql.py``
"""
from sqlalchemy.orm import Query

class Paginator:
    """Provides mechanisms to implement a custom paginating SQLAlchemy Query.

    It receives three (3) main inputs: a fully loaded SQLAlchemy Query, a page number
    and a number of records per page, it calculates and prepares paginated data. And
    returns its own instance. Callers can then access instance properties to prepare
    final data.

    :param query: `sqlalchemy.orm.Query <https://docs.sqlalchemy.org/en/14/orm/query.html>`_,\
        which is opened, and data are ready to be fetched.

    :param int page: the page number to retrieve data for.

    :param int per_page: how many records to retrieve for each page.
    """

    def __init__(self, query: Query, page: int, per_page: int ):
        self._query = query
        self._page = page
        self._per_page = per_page
        self._total_records = query.count()
        self._total_pages = 0
        self._offset = 0
        self._limit = 0
        self._items = []

    def __calc_total_pages(self):
        total_pages = (self._total_records // self._per_page)
        return total_pages + 1 if (self._total_records % self._per_page) > 0 else total_pages

    def __adjust_page(self):
        return self._page if (self._page <= self._total_pages) else self._total_pages

    def __calc_offset(self):
        if (self._total_pages == 0): return 0

        """
        page = 1, per_page = 5 -- offset = 1 - 1  =  0 = (page - 1) * per_page
        page = 2, per_page = 5 -- offset = 6 - 1  =  5 = (page - 1) * per_page
        page = 3, per_page = 5 -- offset = 11 - 1 = 10 = (page - 1) * per_page
        """

        return (self._page - 1) * self._per_page

    def __calc_limit(self):
        if (self._total_pages == 0): return 0
        return self._per_page

    def execute(self):
        """Carry out the paginating operation.

        Calculating values for properties, retrieve target data rows.
        """
        try:
            self._total_pages = self.__calc_total_pages()
            self._page = self.__adjust_page()
            self._offset = self.__calc_offset()
            self._limit = self.__calc_limit()

            if (self._limit == 0): return

            resultset = self._query.offset(self._offset).limit(self._limit)
            for r in resultset:
                self._items.append( r )

        finally:
            return self

    @property
    def page(self) -> int: 
        """Read only property. The requested page number.

        If the originally requested page number is greater than the calculated 
        :attr:`~.Paginator.total_pages`, then the value of this property is
        set to :attr:`~.Paginator.total_pages`.
        """
        return self._page

    @property
    def per_page(self) -> int: 
        """Read only property. The requested number of records per page.
        """
        return self._per_page

    @property
    def total_records(self) -> int: 
        """Read only property. The total number of records retrieved.
        """
        return self._total_records

    @property
    def total_pages(self) -> int: 
        """Read only property. The total number of pages. 

        Its value is calculated page on :attr:`~.Paginator.total_records` and 
        :attr:`~.Paginator.per_page` properties.
        """
        return self._total_pages

    @property
    def offset(self) -> int: 
        """Read only property. It is 0-based.

        From which row number to retrieve data for the requested :attr:`~.Paginator.page`.
        """
        return self._offset

    @property
    def limit(self) -> int: 
        """Read only property. The requested number of records per page.

        Its value is basically :attr:`~.Paginator.per_page`, but if :attr:`~.Paginator.total_pages`
        is 0, then it is set to 0 also.
        """
        return self._limit

    @property
    def items(self) -> list: 
        """Read only property. 

        This is essentially the paginated data for the requested :attr:`~.Paginator.page`.
        It is a list of rows from :attr:`~.Paginator.offset` to :attr:`~.Paginator.limit`,
        inclusively.

        Rows are copied or rather referenced from Query directly, there is no additional
        process performed on the rows when copied to this list.
        """
        return self._items

    @property
    def has_next(self) -> bool:
        """Read only property. 

        ``True`` if there is a next page. ``False`` otherwise.
        """
        return (self._page < self._total_pages)

    @property
    def has_prev(self) -> bool:
        """Read only property. 

        ``True`` if there is a previous page. ``False`` otherwise.
        """
        return (self._page > 1)