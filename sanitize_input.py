def sanitize_tables(tables_filename):
    """Input: csv file containing tables data
    Output: a list which each element is a dictionary with the table's data"""
    # column numbers for each field in the csv file
    TABLE_NUMBER = 0
    SEATS_NUMBER = 1
    LOCATION = 2
    WHEEL_CHAIR = 3
    CART1 = 4
    CART2 = 5
    EDGE = 6

    # sanitize input
    with open(tables_filename, "r", encoding="utf-8") as tables_file:
        i = 0
        tables = []  # each element of the list will eventually be in the data base
        for line in tables_file:
            document = {}
            if i == 0:  # get rid of header line
                i += 1
                continue
            # get the table's data
            split_line = line.rstrip().split(',')
            document["table_number"] = split_line[TABLE_NUMBER].strip()
            document["seats_number"] = int(split_line[SEATS_NUMBER].strip())
            document["location"] = split_line[LOCATION].strip()
            document["wheel_chair"] = split_line[WHEEL_CHAIR].strip()
            document["cart1"] = split_line[CART1].strip()
            document["cart2"] = split_line[CART2].strip()
            document["edge"] = split_line[EDGE].strip()
            if document["edge"]:
                document["edge"] = int(document["edge"].strip())
            else:
                document["edge"] = 0

            # save the table's data
            tables.append(document)

    return tables


def sanitize_guests(guests_filename):
    """Input: csv file containing guests data
    Output: a list which each element is a dictionary with the each guest's data"""
    # column numbers for each field in the csv file
    LAST_NAME = 0
    FIRST_NAME = 1
    GUESTS_NUMBER = 2
    WHEEL_CHAIR = 3
    CART = 4
    LOCATION = 5
    TABLE = 6

    # sanitize input
    with open(guests_filename, "r", encoding="utf-8") as guests_file:
        i = 0
        guests = []  # each element of the list will eventually be in the data base
        for line in guests_file:
            document = {}
            if i == 0:  # get rid of header line
                i += 1
                continue
            # get the table's data
            split_line = line.rstrip().split(',')
            document["last_name"] = split_line[LAST_NAME].strip()
            document["first_name"] = split_line[FIRST_NAME].strip()
            document["guests_number"] = int(split_line[GUESTS_NUMBER].strip())
            document["wheel_chair"] = split_line[WHEEL_CHAIR].strip()
            document["cart"] = split_line[CART].strip()
            document["location"] = split_line[LOCATION].strip()
            document["table"] = split_line[TABLE].strip()

            # save the table's data
            guests.append(document)

    return guests

def sanitize_groups(groups_filename):
    """Input: csv file containing groups data
    Output: a list which each element is a dictionary with the group's data"""
    # column numbers for each field in the csv file
    GROUP_NUMBER = 0
    LAST_NAME = 1
    FIRST_NAME = 2
    GUESTS_NUMBER = 3

    # sanitize input
    with open(groups_filename, "r", encoding="utf-8") as groups_file:
        i = 0
        groups = []  # each element of the list will eventually be in the data base
        for line in groups_file:
            document = {}
            if i == 0:  # get rid of header line
                i += 1
                continue
            # get the table's data
            split_line = line.rstrip().split(',')
            document["group_number"] = int(split_line[GROUP_NUMBER].strip())
            document["last_name"] = split_line[LAST_NAME].strip()
            document["first_name"] = split_line[FIRST_NAME].strip()
            document["guests_number"] = int(split_line[GUESTS_NUMBER].strip())

            # save the group's data
            groups.append(document)

    return groups
