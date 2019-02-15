# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import datetime

from django.db import transaction
from django.utils.text import slugify

from ncdr import models

TABLE_NAME = "Table"
DATABASE = "Database"
CREATED_DATE = "Created_Date"

# the name of the column as it comes in from the csv
DATA_DICTIONARY_NAME = "Data Dictionary Name"
DATA_DICTIONARY_LINKS = "Data Dictionary Links"
IS_DERIVED_ITEM = "Is_Derived_Item"
COLUMN_NAME = "Item_Name"
DATA_DICTIONARY_DESCRIPTION = "Description"
DERIVATION_METHODOLOGY = "NCDR_Derivation_Methodology"
DATA_TYPE = "Data_Type"
DEFINITION_ID = "Definition ID"
TECHNICAL_CHECK = "Technical check"
BUSINESS_CHECK = "Business check"
RK_2 = "RK 2"
SCHEMA = "Schema"
CHECKED = "Checked"
PRESENT_IN_TABLES = "Present_In_Tables"
LINK = "Link"
LINK_TYPE = "Link Type"
DATA_ELEMENT = "Mapping"

# unused
GROUPING = "Grouping"
LAST_UPDATE_DATE = "Last_Update_Date"
LAST_UPDATE_BY = "Last_Update_By"

# we skip these columns as requested
TO_SKIP = ["DB_Col_Group", "DB_Col_Name", DATA_ELEMENT, CREATED_DATE]


# These are the minimum expected csv columns, if they're missing, blow up
EXPECTED_COLUMN_NAMES = set(
    [
        COLUMN_NAME,
        DATA_DICTIONARY_DESCRIPTION,
        DATA_TYPE,
        IS_DERIVED_ITEM,
        DERIVATION_METHODOLOGY,
        PRESENT_IN_TABLES,
        LINK,
        DATA_ELEMENT,
    ]
)

CSV_FIELD_TO_COLUMN_FIELD = {
    DEFINITION_ID: "definition_id",
    DATA_DICTIONARY_DESCRIPTION: "description",
    DATA_TYPE: "data_type",
    IS_DERIVED_ITEM: "is_derived_item",
    DERIVATION_METHODOLOGY: "derivation",
    LINK: "link",
    TECHNICAL_CHECK: "technical_check",
    "Author": "author",
    "Created_Date": "created_date_ext",
}

IGNORED_FIELDS = set(
    [
        PRESENT_IN_TABLES,
        BUSINESS_CHECK,
        RK_2,
        SCHEMA,
        CHECKED,
        GROUPING,
        LAST_UPDATE_DATE,
        LAST_UPDATE_BY,
        COLUMN_NAME,
        LINK_TYPE,
    ]
)


def process_is_derived(value):
    if not value:
        # don't try and save an empty string
        value = None
    elif value.lower() not in ["yes - external", "yes - ncdr", "no"]:
        raise ValueError(f"Unable to recognise is derived item {value}")
    else:
        value = not value.lower() == "no"

    return value


def process_created_date(value):
    if not value:
        return None
    else:
        return datetime.datetime.strptime(value, "%m/%d/%y").date()


def get_tables(csv_row):
    # table names are split with ; and there are a lot of empty rows
    full_table_names = [i for i in csv_row[PRESENT_IN_TABLES].split(";") if i]
    result = []
    for full_table_name in full_table_names:
        splitted = full_table_name.split(".dbo.")
        if len(splitted) == 3:
            if splitted[0].strip() == splitted[1].strip():
                # sometimes the database name is put in twice...
                db_name = splitted[0].strip()
                table_name = splitted[2].strip()
            else:
                raise ValueError(
                    f"unable to process db_name and table name for {full_table_name}"
                )
        else:
            db_name, table_name = full_table_name.split(".dbo.")
        db, _ = models.Database.objects.get_or_create(name=db_name.strip())
        table, _ = models.Table.objects.get_or_create(
            name=table_name.strip(), database=db
        )
        result.append(table)
    return result


def process_row(csv_row, file_name):
    if not any(i for i in csv_row.values() if i.strip()):
        # if its an empty row, skip it
        return

    tables = get_tables(csv_row)
    if not csv_row[DATA_ELEMENT].strip():
        raise ValueError(f"{DATA_ELEMENT} expected")
    mapping, _ = models.DataElement.objects.get_or_create(
        name=csv_row[DATA_ELEMENT].strip()
    )

    for idx, table in enumerate(tables):
        slug = slugify(csv_row[COLUMN_NAME])
        column = models.Column(
            name=csv_row[COLUMN_NAME], table=table, slug=f"{slug}{idx}"
        )
        # auto publish anything coming in via the csv api
        column.published = True
        field_names = csv_row.keys()

        known_fields = EXPECTED_COLUMN_NAMES.union(CSV_FIELD_TO_COLUMN_FIELD.keys())
        for field_name in field_names:
            value = csv_row[field_name].strip()
            field_name = field_name.strip()

            if field_name in TO_SKIP:
                continue

            if (
                field_name == TABLE_NAME
                or field_name == DATABASE
                or field_name == DATA_ELEMENT
            ):
                # these fields are the Foreign keys handled above.
                continue

            if isinstance(value, str):
                value = value.strip()

            if field_name in IGNORED_FIELDS or not field_name.strip():
                continue

            if field_name.startswith("Table "):
                # csv schemas have titles Table n, skip this, its all in present in
                # tables
                continue

            if value and field_name not in known_fields:
                raise ValueError(
                    f"We are not saving a value for {field_name} in {file_name}, should we be?"
                )
            elif not value and field_name not in CSV_FIELD_TO_COLUMN_FIELD:
                continue

            # these are compounded into a foreign key, so we
            # deal with these later
            if field_name in [DATA_DICTIONARY_NAME, DATA_DICTIONARY_LINKS]:
                continue

            db_column_name = CSV_FIELD_TO_COLUMN_FIELD[field_name]
            if field_name == IS_DERIVED_ITEM:
                value = process_is_derived(value)

            if field_name == CREATED_DATE:
                value = process_created_date(value)

            # don't accidentally put an empty space where a None should be
            if field_name == DEFINITION_ID:
                if value == "":
                    value = None

            setattr(column, db_column_name, value)
        column.save()
        mapping.column_set.add(column)


def validate_csv_structure(reader, file_name):
    field_names = reader.fieldnames
    field_names = set([i.strip() for i in field_names if i.strip()])
    missing = EXPECTED_COLUMN_NAMES - field_names

    if missing:
        raise ValueError("missing fields %s in %s" % (", ".join(missing), file_name))


@transaction.atomic
def load_file(file_name):
    """ loads in a file. At present the columns are a bit in flux so our
        methodolgy is:

        1. if there's a column that's populated but not in our database model
           blow up

        2. if there's a column that's not in our database model, but also
           not populated, ignore it
    """
    with open(file_name) as csv_file:
        reader = csv.DictReader(csv_file)
        validate_csv_structure(reader, file_name)

        for csv_row in reader:
            process_row(csv_row, file_name)
