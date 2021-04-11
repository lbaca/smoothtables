"""Tests for the smoothtables module."""

import sys

import smoothtables as st


def _validate_output(expected_output, capfd):
    """Validate the captured output against the expected output."""
    captured = capfd.readouterr()
    assert captured.out == expected_output


def test_table_1(capfd):
    """Test a table with a fixed width."""
    expected_output = (
        'My Test Table\n'
        '┌───────────────┬───┬──────────────────────────────────────┐\n'
        '│    Column 1   │ C │               Column 3               │\n'
        '╞═══════════════╪═══╪══════════════════════════════════════╡\n'
        '│ First value 1 │ Y │ Third value 1                        │\n'
        '├───────────────┼───┼──────────────────────────────────────┤\n'
        '│               │   │                                      │\n'
        '├───────────────┼───┼──────────────────────────────────────┤\n'
        '│ First value 2 │ N │ Third value 2                        │\n'
        '├───────────────┼───┼──────────────────────────────────────┤\n'
        '│               │   │                                      │\n'
        '├───────────────┼───┼──────────────────────────────────────┤\n'
        '│ First value 3 │   │                                      │\n'
        '└───────────────┴───┴──────────────────────────────────────┘\n')
    columns = [
        st.Column('Column 1'),
        st.Column('Column 2', width=1, h_alignment=st.Alignment.CENTER),
        st.Column('Column 3'),
    ]
    data = [
        ('First value 1', 'Y', 'Third value 1'),
        (None, None, ' '),
        ('First value 2', 'N', 'Third value 2'),
        (None, None, None),
        ('First value 3', None, None),
    ]
    table = st.Table(columns, title='My Test Table', max_width=60)
    table.data = data
    table.print_table(file=sys.stdout)
    _validate_output(expected_output, capfd)


def test_table_2(capfd):
    """Test a table without a fixed width."""
    expected_output = (
        'My Test Table\n'
        '┌───────────────┬────┬───────────────┐\n'
        '│    Column 1   │ Co │    Column 3   │\n'
        '╞═══════════════╪════╪═══════════════╡\n'
        '│ First value 1 │ Y  │ Third value 1 │\n'
        '│               │    │               │\n'
        '│ First value 2 │ N  │ Third value 2 │\n'
        '│               │    │               │\n'
        '│ First value 3 │    │               │\n'
        '└───────────────┴────┴───────────────┘\n')
    columns = [
        st.Column('Column 1'),
        st.Column('Column 2', width=2, h_alignment=st.Alignment.CENTER),
        st.Column('Column 3'),
    ]
    data = [
        ('First value 1', 'Y', 'Third value 1'),
        (None, None, ' '),
        ('First value 2', 'N', 'Third value 2'),
        (None, None, None),
        ('First value 3', None, None),
    ]
    table = st.Table(columns, title='My Test Table', use_row_separators=False)
    table.data = data
    table.print_table(file=sys.stdout)
    _validate_output(expected_output, capfd)


def test_table_3(capfd):
    """Test a table where no columns have a fixed width."""
    expected_output = (
        'My Test Table\n'
        '┌───────────────┬──────────┬───────────────┐\n'
        '│    Column 1   │ Column 2 │    Column 3   │\n'
        '╞═══════════════╪══════════╪═══════════════╡\n'
        '│ First value 1 │    Y     │ Third value 1 │\n'
        '│               │          │               │\n'
        '│ First value 2 │    N     │ Third value 2 │\n'
        '│               │          │               │\n'
        '│ First value 3 │          │               │\n'
        '└───────────────┴──────────┴───────────────┘\n')
    columns = [
        st.Column('Column 1'),
        st.Column('Column 2', h_alignment=st.Alignment.CENTER),
        st.Column('Column 3'),
    ]
    data = [
        ['First value 1', 'Y', 'Third value 1'],
        (None, None, ' '),
        ('First value 2', 'N', 'Third value 2'),
        [None, None, None],
        ['First value 3', None, None],
    ]
    table = st.Table(columns, title='My Test Table', use_row_separators=False)
    table.data = data
    table.print_table(file=sys.stdout)
    _validate_output(expected_output, capfd)


def test_table_4(capfd):
    """Test a table where data rows have too many/too few values."""
    expected_output = (
        '┌───────────────┬──────────┬───────────────┐\n'
        '│    Column 1   │ Column 2 │    Column 3   │\n'
        '╞═══════════════╪══════════╪═══════════════╡\n'
        '│ First value 1 │    Y     │ Third value 1 │\n'
        '│               │          │               │\n'
        '│ First value 2 │    N     │ Third value 2 │\n'
        '│               │          │               │\n'
        '│ First value 3 │          │               │\n'
        '└───────────────┴──────────┴───────────────┘\n')
    columns = [
        st.Column('Column 1'),
        st.Column('Column 2', h_alignment=st.Alignment.CENTER),
        st.Column('Column 3'),
    ]
    data = [
        ['First value 1', 'Y', 'Third value 1'],
        (None,),
        ('First value 2', 'N', 'Third value 2', 'What is this?!'),
        [],
        ['First value 3', None],
    ]
    table = st.Table(columns, use_row_separators=False)
    table.data = data
    table.print_table(file=sys.stdout)
    _validate_output(expected_output, capfd)


def test_table_5(capfd):
    """Test a table with complex rendering."""
    expected_output = (
        '┌─────┬───────────────────────────────────────────────┬───────┐\n'
        '│  #  │                  Lorem Ipsum                  │  Huh? │\n'
        '╞═════╪═══════════════════════════════════════════════╪═══════╡\n'
        '│     │ Lorem ipsum dolor sit amet, consectetur       │       │\n'
        '│     │ adipiscing elit, sed do eiusmod tempor        │       │\n'
        '│   1 │ incididunt ut labore et dolore magna aliqua.  │ Start │\n'
        '│     │ Vel pharetra vel turpis nunc eget lorem dolor │       │\n'
        '│     │ sed viverra.                                  │       │\n'
        '├─────┼───────────────────────────────────────────────┼───────┤\n'
        '│     │ In pellentesque massa placerat duis ultricies │       │\n'
        '│     │ lacus sed turpis tincidunt. Ultricies         │       │\n'
        '│   2 │ tristique nulla aliquet enim tortor at auctor │   ?   │\n'
        '│     │ urna. Morbi tristique senectus et netus et    │       │\n'
        '│     │ malesuada. Eget lorem dolor sed viverra.      │       │\n'
        '├─────┼───────────────────────────────────────────────┼───────┤\n'
        '│   3 │ Amet est placerat in egestas erat.            │  ?!!  │\n'
        '├─────┼───────────────────────────────────────────────┼───────┤\n'
        '│     │ Integer feugiat scelerisque varius morbi      │       │\n'
        '│ 999 │ enim. Risus nullam eget felis eget nunc       │  End  │\n'
        '│     │ lobortis. At elementum eu facilisis sed odio  │       │\n'
        '│     │ morbi quis. Ut aliquam purus sit amet luctus. │       │\n'
        '└─────┴───────────────────────────────────────────────┴───────┘\n')
    columns = [
        st.Column('#', h_alignment=st.Alignment.RIGHT,
                  v_alignment=st.Alignment.MIDDLE),
        st.Column('Lorem Ipsum', width=45),
        st.Column('Huh?', h_alignment=st.Alignment.CENTER,
                  v_alignment=st.Alignment.MIDDLE),
    ]
    data = [
        (
            1,
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '
            'eiusmod tempor incididunt ut labore et dolore magna aliqua. Vel '
            'pharetra vel turpis nunc eget lorem dolor sed viverra.',
            'Start'
        ),
        (
            2,
            'In pellentesque massa placerat duis ultricies lacus sed turpis '
            'tincidunt. Ultricies tristique nulla aliquet enim tortor at '
            'auctor urna. Morbi tristique senectus et netus et malesuada. '
            'Eget lorem dolor sed viverra.',
            '?'
        ),
        (
            3,
            'Amet est placerat in egestas erat.',
            '?!!'
        ),
        (
            999,
            'Integer feugiat scelerisque varius morbi enim. Risus nullam eget '
            'felis eget nunc lobortis. At elementum eu facilisis sed odio '
            'morbi quis. Ut aliquam purus sit amet luctus.',
            'End'
        ),
    ]
    table = st.Table(columns)
    table.data = data
    table.print_table(file=sys.stdout)
    _validate_output(expected_output, capfd)


def test_table_6(capfd):
    """Test a table with many columns."""
    expected_output = (
        '┌───────────┬───────────┬───────────┬──────────┬───────┐\n'
        '│  Column 1 │  Column 2 │  Column 3 │ Column 4 │ Colum │\n'
        '╞═══════════╪═══════════╪═══════════╪══════════╪═══════╡\n'
        '│ Value 1.1 │ Value 1.2 │ Value 1.3 │   Yes    │ True  │\n'
        '│ Value 2.1 │ Value 2.2 │ Value 2.3 │    No    │ True  │\n'
        '│ Value 3.1 │ Value 3.2 │ Value 3.3 │   Yes    │ False │\n'
        '│ Value 4.1 │ Value 4.2 │ Value 4.3 │    No    │ False │\n'
        '│ Value 5.1 │ Value 5.2 │ Value 5.3 │  Maybe   │ True? │\n'
        '└───────────┴───────────┴───────────┴──────────┴───────┘\n')
    columns = [
        st.Column('Column 1'),
        st.Column('Column 2'),
        st.Column('Column 3'),
        st.Column('Column 4', h_alignment=st.Alignment.CENTER),
        st.Column('Column 5', fit_heading=False),
    ]
    data = [
        ('Value 1.1', 'Value 1.2', 'Value 1.3', 'Yes', True),
        ('Value 2.1', 'Value 2.2', 'Value 2.3', 'No', True),
        ('Value 3.1', 'Value 3.2', 'Value 3.3', 'Yes', False),
        ('Value 4.1', 'Value 4.2', 'Value 4.3', 'No', False),
        ('Value 5.1', 'Value 5.2', 'Value 5.3', 'Maybe', 'True?'),
    ]
    table = st.Table(columns, use_row_separators=False)
    table.data = data
    table.print_table(file=sys.stdout)
    _validate_output(expected_output, capfd)


def test_table_7(capfd):
    """Test a table with many columns and no headings."""
    expected_output = (
        '┌───────────┬───────────┬───────────┬───────┬───────┐\n'
        '│ Value 1.1 │ Value 1.2 │ Value 1.3 │  Yes  │ True  │\n'
        '│ Value 2.1 │ Value 2.2 │ Value 2.3 │   No  │ True  │\n'
        '│ Value 3.1 │ Value 3.2 │ Value 3.3 │  Yes  │ False │\n'
        '│ Value 4.1 │ Value 4.2 │ Value 4.3 │   No  │ False │\n'
        '│ Value 5.1 │ Value 5.2 │ Value 5.3 │ Maybe │ True? │\n'
        '└───────────┴───────────┴───────────┴───────┴───────┘\n')
    columns = [
        st.Column('Column 1'),
        st.Column('Column 2'),
        st.Column('Column 3'),
        st.Column('Column 4', h_alignment=st.Alignment.CENTER),
        st.Column('Column 5', fit_heading=False),
    ]
    data = [
        ('Value 1.1', 'Value 1.2', 'Value 1.3', 'Yes', True),
        ('Value 2.1', 'Value 2.2', 'Value 2.3', 'No', True),
        ('Value 3.1', 'Value 3.2', 'Value 3.3', 'Yes', False),
        ('Value 4.1', 'Value 4.2', 'Value 4.3', 'No', False),
        ('Value 5.1', 'Value 5.2', 'Value 5.3', 'Maybe', 'True?'),
    ]
    table = st.Table(columns, include_headings=False, use_row_separators=False)
    table.data = data
    table.print_table(file=sys.stdout)
    _validate_output(expected_output, capfd)


def test_panel_1(capfd):
    """Test a panel."""
    expected_output = (
        '             ╭──────────────────╮\n'
        'Attribute 1: │ Value 1          │\n'
        '             ├──────────────────┤\n'
        'Attribute 2: │ Longer value 2   │\n'
        '             │ on multiple rows │\n'
        '             ├──────────────────┤\n'
        'Attribute 3: │                  │\n'
        '             ├──────────────────┤\n'
        '             │ Value 4          │\n'
        '             ╰──────────────────╯\n')
    data = [
        ('Attribute 1', 'Value 1'),
        ('Attribute 2', ['Longer value 2', 'on multiple rows']),
        ('Attribute 3', None),
        (None, 'Value 4'),
    ]
    panel = st.Panel(data)
    panel.print_panel(file=sys.stdout)
    _validate_output(expected_output, capfd)


def test_panel_2(capfd):
    """Test a panel with word wrapping."""
    expected_output = (
        '             ╭────────╮\n'
        'Attribute 1: │ Value  │\n'
        '             │ 1      │\n'
        '             ├────────┤\n'
        'Attribute 2: │ Longer │\n'
        '             │ value  │\n'
        '             │ 2      │\n'
        '             │ on mul │\n'
        '             │ tiple  │\n'
        '             │ rows   │\n'
        '             ├────────┤\n'
        'Attribute 3: │        │\n'
        '             ├────────┤\n'
        '             │ Value  │\n'
        '             │ 4      │\n'
        '             ╰────────╯\n')
    data = [
        ('Attribute 1', 'Value 1'),
        ('Attribute 2', ['Longer value 2', 'on multiple rows']),
        ('Attribute 3', None),
        (None, 'Value 4'),
    ]
    panel = st.Panel(data, value_width=6)
    panel.print_panel(file=sys.stdout)
    _validate_output(expected_output, capfd)


def test_panel_3(capfd):
    """Test a panel with real data."""
    expected_output = (
        '                      ╭────────────────────────────────╮\n'
        '         Album Title: │ Moment                         │\n'
        '                      ├────────────────────────────────┤\n'
        '              Artist: │ Dark Tranquillity              │\n'
        '                      ├────────────────────────────────┤\n'
        '        Release Date: │ 20 November 2020               │\n'
        '                      ├────────────────────────────────┤\n'
        '               Label: │ Century Media                  │\n'
        '                      ├────────────────────────────────┤\n'
        '       Track Listing: │  1. Phantom Days               │\n'
        '                      │  2. Transient                  │\n'
        '                      │  3. Identical to None          │\n'
        '                      │  4. The Dark Unbroken          │\n'
        '                      │  5. Remain in the Unknown      │\n'
        '                      │  6. Standstill                 │\n'
        '                      │  7. Ego Deception              │\n'
        '                      │  8. A Drawn Out Exit           │\n'
        '                      │  9. Eyes of the World          │\n'
        '                      │ 10. Failstate                  │\n'
        '                      │ 11. Empires Lost to Time       │\n'
        '                      │ 12. In Truth Divided           │\n'
        '                      │ 13. Silence as a Force         │\n'
        '                      │ 14. Time in Relativity         │\n'
        '                      ├────────────────────────────────┤\n'
        'Peak Chart Positions: │ SWE: 14                        │\n'
        '                      │ AUT: 24                        │\n'
        '                      │ FIN: 9                         │\n'
        '                      │ FRA: 181                       │\n'
        '                      │ GER: 17                        │\n'
        '                      │ SWI: 16                        │\n'
        '                      ╰────────────────────────────────╯\n')
    data = [
        ('Album Title', 'Moment'),
        ('Artist', 'Dark Tranquillity'),
        ('Release Date', '20 November 2020'),
        ('Label', 'Century Media'),
        (
            'Track Listing',
            [
                ' 1. Phantom Days',
                ' 2. Transient',
                ' 3. Identical to None',
                ' 4. The Dark Unbroken',
                ' 5. Remain in the Unknown',
                ' 6. Standstill',
                ' 7. Ego Deception',
                ' 8. A Drawn Out Exit',
                ' 9. Eyes of the World',
                '10. Failstate',
                '11. Empires Lost to Time',
                '12. In Truth Divided',
                '13. Silence as a Force',
                '14. Time in Relativity',
            ]
        ),
        (
            'Peak Chart Positions',
            [
                'SWE: 14',
                'AUT: 24',
                'FIN: 9',
                'FRA: 181',
                'GER: 17',
                'SWI: 16',
            ]
        )
    ]
    panel = st.Panel(data, value_width=30)
    panel.print_panel(file=sys.stdout)
    _validate_output(expected_output, capfd)
