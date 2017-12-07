# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction
import datetime
import csv
from csv_schema import models

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

# unused
GROUPING = "Grouping"
LAST_UPDATE_DATE = "Last_Update_Date"
LAST_UPDATE_BY = "Last_Update_By"


# These are the minimum expected csv columns, if they're missing, blow up
EXPECTED_COLUMN_NAMES = set([
    COLUMN_NAME,
    DATA_DICTIONARY_DESCRIPTION,
    DATA_TYPE,
    IS_DERIVED_ITEM,
    DERIVATION_METHODOLOGY,
    PRESENT_IN_TABLES,
    LINK
])

CSV_FIELD_TO_COLUMN_FIELD = {
    DEFINITION_ID: "definition_id",
    COLUMN_NAME: "data_item",
    DATA_DICTIONARY_DESCRIPTION: "description",
    DATA_TYPE: "data_type",
    IS_DERIVED_ITEM: "is_derived_item",
    DERIVATION_METHODOLOGY: "derivation",
    LINK: "link",
    TECHNICAL_CHECK: "technical_check",
    "Author": "author",
    "Created_Date": "created_date_ext"
}

IGNORED_FIELDS = set([
    PRESENT_IN_TABLES,
    BUSINESS_CHECK,
    RK_2,
    SCHEMA,
    CHECKED,
    GROUPING,
    LAST_UPDATE_DATE,
    LAST_UPDATE_BY
])


def process_is_derived(value):
    if not value:
        # don't try and save an empty string
        value = None
    elif value.lower() not in ["yes - external", "yes - ncdr", "no"]:
        raise ValueError(
            "Unable to recognise is derived item {}".format(
                value
            )
        )
    else:
        value = not value.lower() == "no"

    return value


def process_created_date(value):
    if not value:
        return None
    else:
        return datetime.datetime.strptime(value, "%m/%d/%y").date()


def get_database_to_table(csv_row):
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
                err = "unable to process db_name and table name for {}"
                raise ValueError(err.format(full_table_name))
        else:
            db_name, table_name = full_table_name.split(".dbo.")
        db, _ = models.Database.objects.get_or_create(
            name=db_name.strip()
        )
        table, _ = models.Table.objects.get_or_create(
            name=table_name.strip(), database=db
        )
        result.append((db, table,),)

    return result


def process_data_dictionary_reference(db_column, csv_row):
    """ we store data dictionary links and names as a seperate foreign key table
        we want there to be one link to one name after being split by new lines

        this is not always the case.

        work arounds.

        (i) if there is only a single link and lots of names, apply that link
            to all the names

        (ii) if there are no links, just save a name
    """
    names_str = csv_row[DATA_DICTIONARY_NAME]
    if names_str == "N//A" or names_str == "N/A":
        db_column.datadictionaryreference_set.all().delete()
        return

    links_str = csv_row[DATA_DICTIONARY_LINKS]
    names = [i.strip() for i in names_str.split("\n") if i.strip()]
    links = [i.strip() for i in links_str.split("\n") if i.strip()]
    if not len(names) == len(links):
        if not names:
            raise ValueError(
                'found links but no names for {}.{}.{}'.format(
                    db_column.table.database.name,
                    db_column.table.name,
                    db_column.data_item
                )
            )
        elif len(links) == 1:
            links = [links[0] for i in range(len(names))]
        elif not links:
            links = [None for i in range(len(names))]
        else:
            raise ValueError(
                'for {}.{}.{} the number of links is different'.format(
                    db_column.table.database.name,
                    db_column.table.name,
                    db_column.data_item
                )
            )

    obj_args = [dict(name=i[0], link=i[1]) for i in zip(names, links)]

    existing = []
    new_db_refs = []
    for obj_arg in obj_args:
        existing_column = db_column.datadictionaryreference_set.filter(
            **obj_arg
        ).first()

        if existing_column:
            existing.append(existing_column)
        else:
            new_db_refs.append(obj_arg)

    db_column.datadictionaryreference_set.exclude(
        id__in=[i.id for i in existing]
    ).delete()

    for new_db_ref in new_db_refs:
        db_column.datadictionaryreference_set.create(**new_db_ref)


def process_row(csv_row, file_name):
    if not any(i for i in csv_row.values() if i.strip()):
        # if its an empty row, skip it
        return

    column, _ = models.Column.objects.get_or_create(
        name=csv_row[COLUMN_NAME]
    )
    field_names = csv_row.keys()

    known_fields = EXPECTED_COLUMN_NAMES.union(
        CSV_FIELD_TO_COLUMN_FIELD.keys()
    )
    for field_name in field_names:
        value = csv_row[field_name].strip()
        field_name = field_name.strip()

        if field_name == TABLE_NAME or field_name == DATABASE:
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
            e = "We are not saving a value for {} in {}, should we be?"
            raise ValueError(
                e.format(field_name, file_name)
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
            if value == '':
                value = None

        setattr(column, db_column_name, value)
    column.save()

    db_to_tables = get_database_to_table(csv_row)
    column.tables.set(i[1] for i in db_to_tables)


def validate_csv_structure(reader, file_name):
    field_names = reader.fieldnames
    field_names = set([i.strip() for i in field_names if i.strip()])
    missing = EXPECTED_COLUMN_NAMES - field_names

    if missing:
        raise ValueError(
            'missing fields %s in %s' % (", ".join(missing), file_name)
        )


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