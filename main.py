import sanitize_input
import passover_map


def main(tables_filename, guests_filename, groups_filename):
    """Entry point of the passover map program"""
    # get the tables data
    tables = sanitize_input.sanitize_tables(tables_filename)

    # get the guests data
    guests = sanitize_input.sanitize_guests(guests_filename)

    # get the groups data
    groups = sanitize_input.sanitize_groups(groups_filename)

    # make the map
    passover_map.run(tables=tables, guests=guests, groups=groups)
    print("Finished successfully")

if __name__ == '__main__':
    # entry point of the program
    tables_file_name = "tables.csv"
    guests_file_name = "guests.csv"
    groups_filename = "groups.csv"
    main(tables_filename=tables_file_name, guests_filename=guests_file_name, groups_filename=groups_filename)