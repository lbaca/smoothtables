"""Converts lists of lists into tables, or a single list into a panel.

The words "list" and "tuple" can be used interchangeably in this
context.
"""

import sys
import textwrap
from enum import Enum


class Alignment(Enum):
    """Enumeration of alignments."""

    # Horizontal alignment
    LEFT = 'L'
    CENTER = 'C'
    RIGHT = 'R'
    # Vertical alignment
    TOP = 'T'
    MIDDLE = 'M'
    BOTTOM = 'B'


class Column:
    """A text table column.

    If fit_heading is True, the column will be sized at a minimum to fit
    the heading text. If False and the column data is always shorter
    than the heading text, the latter will be truncated. If width is
    provided, fit_heading is ignored.
    """

    def __init__(self, heading, width=None, fit_heading=True,
                 h_alignment=Alignment.LEFT, v_alignment=Alignment.TOP):
        """Initialize a Column."""
        if width is int and width < 1:
            raise ValueError(f'invalid width for column "{heading}": {width}')
        self.heading = str(heading) if heading is not None else ''
        self.width = width
        self.fit_heading = fit_heading
        self.h_alignment = h_alignment
        self.v_alignment = v_alignment

    def __str__(self):
        """Return debug info for the column."""
        width = self.width if self.width else 'None'
        return (f'Column: "{self.heading}", width: {width}, horizontal '
                f'alignment: {self.h_alignment}, vertical alignment: '
                f'{self.v_alignment}')

    def get_header_cell(self):
        """Return the cell for the column header."""
        return self.heading.center(self.width)[:self.width]

    def get_cell(self, value):
        """Return a list representing the lines of a data cell."""
        cell = []
        lines = str(value).splitlines() if value is not None else ['']
        # Avoid printing empty lines at the end
        while len(lines) > 1 and not lines[-1]:
            del lines[-1]
        for line in lines:
            if len(line) <= self.width:
                # Entire line can fit in width
                cell.append(line)
            else:
                # Line length exceeds width; split as economically as
                # possible
                tokens = line.split(sep=' ')
                line = ''
                remaining_width = self.width
                for t in tokens:
                    # Ignore leading spaces
                    if t or line:
                        if len(t) <= remaining_width:
                            if line:
                                line += ' '
                            line += t
                            remaining_width -= len(t) + 1
                        else:
                            # Not enough space left on line for t
                            if line:
                                cell.append(line)
                                line = ''
                                remaining_width = self.width
                            while t:
                                if len(t) > self.width:
                                    cell.append(t[:self.width])
                                    t = t[self.width:]
                                else:
                                    line = t
                                    remaining_width -= len(t) + 1
                                    t = None
                if line:
                    cell.append(line)
        # Align and pad cell contents
        if self.h_alignment == Alignment.LEFT:
            cell = [text.ljust(self.width) for text in cell]
        elif self.h_alignment == Alignment.CENTER:
            cell = [text.center(self.width) for text in cell]
        elif self.h_alignment == Alignment.RIGHT:
            cell = [text.rjust(self.width) for text in cell]
        return cell

    def get_empty_cell(self):
        """Return an empty cell."""
        return ' ' * self.width


class Table:
    """A text table.

    Expects an iterable of Column objects on initialization, and the
    row data to be provided later.
    """

    def __init__(self, columns, title=None, max_width=None,
                 include_headings=True, use_row_separators=True,
                 column_margin=1):
        """Initialize a Table with a list of Column objects.

        If max_width is provided and the combination of Column
        definitions and row data is such that this width is not
        achieved, the last Column will be stretched out to the
        max_width.
        """
        if type(max_width) is int:
            if max_width <= 0:
                raise ValueError(f'invalid maximum table width: {max_width}')
            min_width = sum((col.width for col in columns if col.width),
                            len(columns) * (2 * column_margin + 2) + 1)
            if max_width < min_width:
                raise ValueError(
                    f'maximum table width is too narrow: {max_width}')
        self.columns = columns
        self.title = title
        self.use_row_separators = use_row_separators
        self.max_width = max_width
        self.include_headings = include_headings
        self.column_margin = column_margin
        self._text_lines = []
        self.data = []

    def _determine_column_widths(self):
        """Calculate the width of columns that don't specify it."""
        total_width = sum((col.width for col in self.columns if col.width),
                          len(self.columns) * (2 * self.column_margin + 1) + 1)
        if self.max_width is not None and total_width > self.max_width:
            raise ValueError(
                f'maximum table width is too narrow: {self.max_width}')
        unbounded_columns = [(i, col) for i, col in enumerate(self.columns)
                             if col.width is None]
        for n, (i, col) in zip(range(len(unbounded_columns), 0, -1),
                               unbounded_columns):
            data = [row[i] for row in self.data if i < len(row)]
            if self.include_headings and col.fit_heading:
                data.append(col.heading)
            width = max((len(str(cell)) if cell is not None else 0)
                        for cell in data)
            if n == 1 and self.max_width is not None:
                remaining_width = self.max_width - total_width
                if remaining_width > 0:
                    width = remaining_width
                else:
                    raise ValueError(f'not enough width to fit column {i + 1}')
            col.width = width
            total_width += width
            if self.max_width is not None and total_width > self.max_width:
                raise ValueError(
                    f'maximum table width is too narrow: {self.max_width}')

    def _generate_header(self):
        """Generate the table header."""
        margin_str = ' ' * self.column_margin
        top = '┌'
        headings = '│'
        heading_sep = '╞'
        row_sep = '├'
        self._bottom = '└'
        for i, col in enumerate(self.columns, start=1):
            top += ('─' * (col.width + 2 * self.column_margin)
                    + ('┐' if i == len(self.columns) else '┬'))
            headings += margin_str + col.get_header_cell() + margin_str + '│'
            heading_sep += ('═' * (col.width + 2 * self.column_margin)
                            + ('╡' if i == len(self.columns) else '╪'))
            row_sep += ('─' * (col.width + 2 * self.column_margin)
                        + ('┤' if i == len(self.columns) else '┼'))
            self._bottom += ('─' * (col.width + 2 * self.column_margin)
                             + ('┘' if i == len(self.columns) else '┴'))
        if self.title:
            self._text_lines.append(self.title)
        self._text_lines.append(top)
        if self.include_headings:
            self._text_lines.append(headings)
            self._text_lines.append(heading_sep)
        self._row_separator = row_sep if self.use_row_separators else None

    def _generate_rows(self):
        """Generate the table rows."""
        margin_str = ' ' * self.column_margin
        # Loop over each data row
        for n, data_row in enumerate(self.data):
            if self.use_row_separators and n > 0:
                # Add row separator before every row except the first
                self._text_lines.append(self._row_separator)
            # Create a list where each element is a cell, represented by
            # a list of lines with its contents
            cells = [
                col.get_cell(data_row[i]) for i, col in enumerate(self.columns)
                if i < len(data_row)
            ]
            # The size of the tallest cell
            max_lines = max(len(cell) for cell in cells) if cells else 1
            # Loop over the columns to do vertical alignment
            for i, col in enumerate(self.columns):
                # Calculate how many lines are "missing" from each cell
                # with respect to the tallest
                delta = max_lines - (len(cells[i]) if i < len(cells) else 0)
                if delta > 0:
                    if col.v_alignment == Alignment.MIDDLE:
                        # Insert half as many missing lines at the top
                        cells[i][0:0] = [col.get_empty_cell()] * (delta // 2)
                    elif col.v_alignment == Alignment.BOTTOM:
                        # Insert all missing lines at the top
                        cells[i][0:0] = [col.get_empty_cell()] * delta
            for m in range(max_lines):
                row = '│'
                for i, col in enumerate(self.columns):
                    row += margin_str
                    if i >= len(cells) or m >= len(cells[i]):
                        row += col.get_empty_cell()
                    else:
                        row += cells[i][m]
                    row += margin_str + '│'
                self._text_lines.append(row)
        self._text_lines.append(self._bottom)

    def render(self):
        """Render the table from the columns and data."""
        self._text_lines = []
        if self.columns and self.data:
            self._determine_column_widths()
            self._generate_header()
            self._generate_rows()

    def print_table(self, end='\n', file=sys.stdout, flush=False):
        """Print the table."""
        if not self._text_lines:
            self.render()
        print(*self._text_lines, sep='\n', end=end, file=file, flush=flush)


class Panel:
    """A panel to display a single row of information in tabular format.

    The data input must be an iterable of key/value tuples or lists. If
    the value item is itself a list, the items of said list will be
    interpreted as individual lines in the same cell. If the value is a
    string containing newline characters, it will be split into a list.
    """

    def __init__(self, data, use_colons=True, label_width=None,
                 value_width=None, margin=1):
        """Initialize a Panel with the given data."""
        self.use_colons = use_colons
        self.label_width = label_width
        self.value_width = value_width
        self.margin = margin
        self.data = []
        for item in data:
            value = self._split_value(item[1])
            self.data.append((item[0], value))
        self._text_lines = []

    def _split_value(self, value):
        """Split the value if it exceeds the allotted width."""
        if value:
            if type(value) is str:
                if self.value_width:
                    value = textwrap.wrap(value, width=self.value_width)
                else:
                    value = value.splitlines()
                if len(value) == 0:
                    value = None
            elif self.value_width and type(value) is list:
                lines = []
                for line in value:
                    lines += textwrap.wrap(line, width=self.value_width)
                value = lines
        else:
            value = None
        return value

    def _determine_cell_width(self, cell):
        """Calculate the width of a given cell, accounting for type."""
        width = 0
        if cell:
            if type(cell) is str:
                width = len(cell)
            elif type(cell) is list:
                width = max(self._determine_cell_width(line) for line in cell)
        return width

    def _determine_column_widths(self):
        """Calculate the width of the labels and panel."""
        max_width = max((len(item[0]) if item[0] is not None else 0)
                        for item in self.data)
        if self.label_width is None:
            self.label_width = max_width
        elif self.label_width < max_width:
            raise ValueError(f'label width is too narrow: {self.label_width}, '
                             f'need at least {max_width}')
        max_width = max(
            self._determine_cell_width(item[1]) for item in self.data)
        if self.value_width is None:
            self.value_width = max_width
        elif self.value_width < max_width:
            raise ValueError(f'value width is too narrow: {self.value_width}, '
                             f'need at least {max_width}')

    def _generate_separator(
            self, left_char='├', middle_char='─', right_char='┤'):
        """Generate the separator."""
        self._text_lines.append(
            ' ' * (self.label_width
                   + (1 if self.use_colons else 0)
                   + self.margin)
            + left_char
            + middle_char * (self.value_width + 2 * self.margin)
            + right_char)

    def _generate_top_border(self):
        """Generate the top border."""
        self._generate_separator(left_char='╭', right_char='╮')

    def _generate_bottom_border(self):
        """Generate the bottom border."""
        self._generate_separator(left_char='╰', right_char='╯')

    def _generate_attribute_line(self, label, value):
        """Generate an attribute line."""
        label_str = str(label) if label is not None else ''
        value_str = str(value) if value is not None else ''
        label_fmt = label_str.rjust(self.label_width)
        if self.use_colons:
            label_fmt += ':' if label is not None else ' '
        margin_str = ' ' * self.margin
        self._text_lines.append(
            label_fmt
            + margin_str
            + '│'
            + margin_str
            + value_str.ljust(self.value_width)
            + margin_str
            + '│')

    def _generate_attribute(self, label, value):
        """Generate an attribute row."""
        if type(value) is list:
            for i, v in enumerate(value):
                self._generate_attribute_line(label if i == 0 else None, v)
        else:
            self._generate_attribute_line(label, value)

    def render(self):
        """Render the table from the data."""
        self._text_lines = []
        if self.data:
            self._determine_column_widths()
            self._generate_top_border()
            for i, item in enumerate(self.data, start=1):
                if i > 1:
                    self._generate_separator()
                self._generate_attribute(item[0], item[1])
            self._generate_bottom_border()

    def print_panel(self, end='\n', file=sys.stdout, flush=False):
        """Print the panel."""
        if not self._text_lines:
            self.render()
        print(*self._text_lines, sep='\n', end=end, file=file, flush=flush)
