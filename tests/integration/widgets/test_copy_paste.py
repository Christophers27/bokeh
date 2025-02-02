#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2023, Anaconda, Inc. All rights reserved.
#
# Powered by the Bokeh Development Team.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations # isort:skip

import pytest ; pytest

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from time import sleep

# Bokeh imports
from bokeh.layouts import column
from bokeh.models import (
    ColumnDataSource,
    DataTable,
    Div,
    TableColumn,
)
from tests.support.plugins.project import BokehModelPage
from tests.support.util.selenium import (
    copy_table_rows,
    enter_text_with_click_enter,
    find_element_for,
    paste_values,
)

#-----------------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------------

pytest_plugins = (
    "tests.support.plugins.project",
)


@pytest.mark.selenium
class Test_CopyPaste:
    def test_copy_paste_to_textarea(self, bokeh_model_page: BokehModelPage) -> None:
        source = ColumnDataSource(dict(x=[1, 2], y=[1, 1]))
        columns = [TableColumn(field='x', title='x'), TableColumn(field='y', title='y')]
        table = DataTable(source=source, columns=columns, editable=False, width=600)
        text_area = Div(text='<textarea></textarea>')

        page = bokeh_model_page(column(table, text_area))

        # Use reversed order to get the correct order
        copy_table_rows(page.driver, table, [2, 1])

        # Copy is a little slow
        sleep(0.1)

        element = find_element_for(page.driver, text_area, "textarea")

        # Selenium doesn't paste until we write something to the element first
        # textarea works like a cell
        enter_text_with_click_enter(page.driver, element, 'PASTED:')

        paste_values(page.driver, element)

        result = element.get_attribute('value')

        # The textarea now contains the content in the datatable
        assert result == '\nPASTED:\n0\t1\t1\n1\t2\t1\n'

        assert page.has_no_console_errors()
