# Smooth Tables

**A module to generate tables and panels with box drawing borders.**

## About

This module will accept a list (or tuple) of lists (or tuples) and generate a text table with box drawing borders and flexible alignment options, such as the following:

```
┌─────┬───────────────────────────────────────────────┬───────┐
│  #  │                  Lorem Ipsum                  │  Huh? │
╞═════╪═══════════════════════════════════════════════╪═══════╡
│     │ Lorem ipsum dolor sit amet, consectetur       │       │
│     │ adipiscing elit, sed do eiusmod tempor        │       │
│   1 │ incididunt ut labore et dolore magna aliqua.  │ Start │
│     │ Vel pharetra vel turpis nunc eget lorem dolor │       │
│     │ sed viverra.                                  │       │
├─────┼───────────────────────────────────────────────┼───────┤
│     │ In pellentesque massa placerat duis ultricies │       │
│     │ lacus sed turpis tincidunt. Ultricies         │       │
│   2 │ tristique nulla aliquet enim tortor at auctor │   ?   │
│     │ urna. Morbi tristique senectus et netus et    │       │
│     │ malesuada. Eget lorem dolor sed viverra.      │       │
├─────┼───────────────────────────────────────────────┼───────┤
│   3 │ Amet est placerat in egestas erat.            │  ?!!  │
├─────┼───────────────────────────────────────────────┼───────┤
│     │ Integer feugiat scelerisque varius morbi      │       │
│ 999 │ enim. Risus nullam eget felis eget nunc       │  End  │
│     │ lobortis. At elementum eu facilisis sed odio  │       │
│     │ morbi quis. Ut aliquam purus sit amet luctus. │       │
└─────┴───────────────────────────────────────────────┴───────┘
```

or:

```
┌───────────┬───────────┬───────────┬──────────┬───────┐
│  Column 1 │  Column 2 │  Column 3 │ Column 4 │ Colum │
╞═══════════╪═══════════╪═══════════╪══════════╪═══════╡
│ Value 1.1 │ Value 1.2 │ Value 1.3 │   Yes    │ True  │
│ Value 2.1 │ Value 2.2 │ Value 2.3 │    No    │ True  │
│ Value 3.1 │ Value 3.2 │ Value 3.3 │   Yes    │ False │
│ Value 4.1 │ Value 4.2 │ Value 4.3 │    No    │ False │
│ Value 5.1 │ Value 5.2 │ Value 5.3 │  Maybe   │ True? │
└───────────┴───────────┴───────────┴──────────┴───────┘
```

It can also take a list of two-item (key/value) lists or tuples and render it in tabular format as a `Panel`:

```
                      ╭────────────────────────────────╮
         Album Title: │ Moment                         │
                      ├────────────────────────────────┤
              Artist: │ Dark Tranquillity              │
                      ├────────────────────────────────┤
        Release Date: │ 20 November 2020               │
                      ├────────────────────────────────┤
               Label: │ Century Media                  │
                      ├────────────────────────────────┤
       Track Listing: │  1. Phantom Days               │
                      │  2. Transient                  │
                      │  3. Identical to None          │
                      │  4. The Dark Unbroken          │
                      │  5. Remain in the Unknown      │
                      │  6. Standstill                 │
                      │  7. Ego Deception              │
                      │  8. A Drawn Out Exit           │
                      │  9. Eyes of the World          │
                      │ 10. Failstate                  │
                      │ 11. Empires Lost to Time       │
                      │ 12. In Truth Divided           │
                      │ 13. Silence as a Force         │
                      │ 14. Time in Relativity         │
                      ├────────────────────────────────┤
Peak Chart Positions: │ SWE: 14                        │
                      │ AUT: 24                        │
                      │ FIN: 9                         │
                      │ FRA: 181                       │
                      │ GER: 17                        │
                      │ SWI: 16                        │
                      ╰────────────────────────────────╯
```

***NOTE:** Depending on the font used on your system, the box drawing characters may be displayed differently. For example, as rendered in GitHub by Google Chrome on a Windows 10 machine, the vertical lines in the examples above are not displayed as continuous, but the [Cascadia Code font](https://github.com/microsoft/cascadia-code) renders these lines as solid.*

The code to generate these examples can be found among the repository's [tests](https://github.com/lbaca/smoothtables/blob/main/tests/test_smoothtables.py).

## Installation

To install the module, run the following:

```
pip install smoothtables
```

## Usage

### Rendering Tables

To render a text table, we must first define our columns as a list of `Column` objects. The `Column` contructor accepts the following arguments:

| Argument | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `heading` | Positional | *N/A* | The column heading. |
| `width` | Keyword | `None` | The fixed width of the column. If `None`, the column width will be determined by the widest row value. |
| `fit_heading` | Positional | `True` | If `True`, the column width will be such that the heading will be guaranteed to fit. If `False` and the column's row data values are always shorter that the heading, the latter will be truncated. Ignored if `width` is provided. |
| `h_alignment` | Positional | `Alignment.LEFT` | The horizontal alignment of the column's row data values. One of `Alignment.LEFT`, `Alignment.CENTER` and `Alignment.RIGHT`. Note that column headings are always centered. |
| `v_alignment` | Positional | `Alignment.TOP` | The vertical alignment of the column's row data values. Pertinent in cases where different columns in the same row occupy a different number of lines of text. One of `Alignment.TOP`, `Alignment.MIDDLE` and `Alignment.BOTTOM`. |

Then we can create the `Table` object, whose contructor accepts the following arguments:

| Argument | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `columnns` | Positional | *N/A* | The list of `Column` objects. |
| `title` | Keyword | `None` | The title of the table, to be rendered above it. |
| `max_width` | Keyword | `None` | The maximum width of the table, in characters. If provided and the combination of `Column` definitions and row data is such that this width is not achieved, the last column will be stretched out to the `max_width`. |
| `include_headings` | Keyword | `True` | Whether the headings row should be rendered. |
| `use_row_separators` | Keyword | `True` | Whether separators should e rendered between subsequent data rows. |
| `column_margin` | Keyword | `1` | The number of blank spaces to render to the left and right of data cells, as spacing from column dividers. |

The data rows (a list of tuples or lists) can then be assigned to the `Table` object's `data` property, and the table printed by the `print_table` method.

### Rendering Panels

To render a text panel, we must first instantiate a `Panel` object, whose contructor accepts the following arguments:

| Argument | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `data` | Positional | *N/A* | A list of key/value tuples (or lists). If the value item is itself a list, the items of said list will be interpreted as individual lines in the same cell. If the value is a string containing newline characters, it will be split into a list of lines. |
| `use_colons` | Keyword | `True` | Whether the panel attribute labels will be suffixed by a colon (`:`). |
| `label_width` | Keyword | `None` | The width of the attribute label section, in characters. If `None`, the width will be determined dynamically based on the longest label. |
| `value_width` | Keyword | `None` | The width of the data value section, in characters. If `None`, the width will be determined dynamically based on the longest data value. If specified, and the data is too long, it will be automatically wrapped. |
| `margin` | Keyword | `1` | The number of blank spaces to render to the left and right of data value cells. |

The panel can then be printed by the `print_panel` method.
