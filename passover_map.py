import numpy as np
import random
import copy

close_to_stage = "קרוב לבמה"
north = "צפון"
center = "מרכז"
dish_washer = "מכונת כלים"

class Table(object):
    def __init__(self, table_dict):
        self.number = table_dict["table_number"]
        self.seats_number = table_dict["seats_number"]
        self.location = table_dict["location"]
        self.wheel_chair = table_dict["wheel_chair"]
        self.cart1 = table_dict["cart1"]
        self.cart2 = table_dict["cart2"]
        self.edge = table_dict["edge"]
        self.total_seats = self.seats_number + self.edge
        self.available_seats = self.total_seats
        self.full = False
        self.who_sits_here = []
        self.max_amount_of_wheel_chairs = 3


class Guest(object):
    def __init__(self, guest_dict):
        self.last_name = guest_dict.get("last_name", "")
        self.first_name = guest_dict.get("first_name", "")
        self.guests_number = guest_dict.get("guests_number", "")
        self.wheel_chair = guest_dict.get("wheel_chair", "")
        self.cart = guest_dict.get("cart", "")
        self.location = guest_dict.get("location", "")
        self.table = guest_dict.get("table", "")
        self.specific_table = self.table  # Assuming this is only ran once, so the specific table is only filled once when we get the input and not after we place everyone in their tables
        self.group_number = guest_dict.get("group_number", "")
        if self.last_name == "קבוצה":
            self.group_number = int(self.first_name)
        self.already_sitting = False

class PassoverMap(object):
    def __init__(self, tables, guests, groups):
        self.tables = tables  # list of Table
        self.guests = guests  # list of Guest
        self.groups = groups  # list of Guest, each guest has a group
        self.locations = [close_to_stage, dish_washer, center, north]

    def get_amount_of_total_seats_per_location(self):
        output = {close_to_stage: 0, north: 0, center: 0, dish_washer: 0}  # the output looks like this but with correct values
        for table in self.tables:
            output[table.location] += table.total_seats

        return output

    def get_amount_of_available_seats_per_location(self):
        output = {close_to_stage: 0, north: 0, center: 0, dish_washer: 0}  # the output looks like this but with correct values
        for table in self.tables:
            output[table.location] += table.available_seats

        return output

    def place_guest_in_table(self, table, guest):
        if guest.guests_number > table.available_seats:
            raise ValueError("Not enough room in this table")  # shouldn't get here but just in case
        table.who_sits_here.append(guest)  # place the guest in the table
        guest.table = table.number  # flag that the guest sits in that table also in the Guest object
        table.available_seats -= guest.guests_number
        guest.already_sitting = True  # mark that this guest has a seat
        if table.available_seats == 0:
            table.full = True

    def find_table_by_number(self, number):
        for table in self.tables:
            if table.number == number:
                return table

    def get_tables_by_location(self, location):
        """Returns a list of tables from a specific location"""
        return [table for table in self.tables if table.location == location]

    def place_guests_in_mandatory_table(self):
        """Some guests must sit in a specific table. This function places those guests in their tables.
        This will be ran only once in the beginning"""
        for guest in self.guests:
            if guest.table:
                table = self.find_table_by_number(guest.table)
                self.place_guest_in_table(table=table, guest=guest)

    def print_map_by_tables(self):
        tables = sorted(self.tables,
                        key=lambda _table: int(_table.number) if all([c.isdigit() for c in _table.number]) else 0)  # sort by table number
        for table in tables:
            print("Table Number: {}, Total Seats: {}, Available Seats: {}\nWho sits here: {}\n"
                  .format(table.number, table.total_seats, table.available_seats, [guest.first_name + ' ' + guest.last_name for guest in table.who_sits_here]))

    def print_map_by_guests(self):
        guests = sorted(self.guests, key=lambda _guest: _guest.last_name)  # sort by last name
        for guest in guests:
            print("Last Name: {}, First Name: {}\nGuests Number: {}, Table Number: {}\n".
                  format(guest.last_name, guest.first_name, guest.guests_number, guest.table))

    def save_map_by_tables_to_csv(self, filename="map_by_tables.csv"):
        tables = sorted(self.tables,
                        key=lambda _table: int(_table.number) if all([c.isdigit() for c in _table.number]) else 0)
        write_data = 'מספר שולחן,שם משפחה,שם פרטי,מספר סועדים,כסא גלגלים,מספר עגלות,מיקום,שולחן ספציפי,מספר קבוצה,סה"כ לשולחן\n'
        for table in tables:
            guests = sorted(table.who_sits_here, key=lambda _guest: _guest.last_name)  # sort by last name
            for guest in guests:
                data = "{},{},{},{},{},{},{},{},{},{}\n".format(table.number, guest.last_name, guest.first_name,
                                                       guest.guests_number, guest.wheel_chair, guest.cart,
                                                       guest.location, guest.specific_table,guest.group_number,
                                                       table.total_seats - table.available_seats)
                write_data += data

        with open(filename, 'w') as map_file:
            map_file.write(write_data)

    def save_map_by_guests_to_csv(self, filename="map_by_guests.csv"):
        guests = sorted(self.guests, key=lambda _guest: _guest.last_name)  # sort by last name
        write_data = "שם משפחה, שם פרטי, מספר סועדים, מספר שולחן\n"
        for guest in guests:
            data = "{},{},{},{}\n".format(guest.last_name, guest.first_name, guest.guests_number, guest.table)
            write_data += data

        with open(filename, 'w') as map_file:
                map_file.write(write_data)

    def save_last_names(self, filename="last_names.csv", columns_number=4):
        """Saves a file with each guest's last name in the amount of the guests number
        columns_number is the amount of names per row in the file"""
        guests = sorted(self.guests, key=lambda _guest: _guest.last_name)  # sort by last name
        last_names_list_of_lists = [[" ".join([guest.last_name, '(' + guest.table + ')'])] * guest.guests_number for guest in guests]
        last_names_list_of_strings = [last_name for sublist in last_names_list_of_lists for last_name in sublist]
        for i in range(columns_number - 1, len(last_names_list_of_strings), columns_number):
            last_names_list_of_strings[i] += '\n'  # add \n every in the desired columns number

        write_data = ','.join(last_names_list_of_strings)  # make a string separated by commas
        write_data = write_data.replace("\n,", "\n")

        with open(filename, 'w') as last_names_file:
                last_names_file.write(write_data)

    def is_possible_to_place_everyone_where_they_want(self):
        """Returns True if possible to place everyone where they want to be"""
        desired_seats_per_location = {close_to_stage: 0, north: 0, center: 0, dish_washer: 0}
        for guest in self.guests:
            if guest.location:
                desired_seats_per_location[guest.location] += guest.guests_number

        available_seats = self.get_amount_of_available_seats_per_location()

        return desired_seats_per_location[close_to_stage] <= available_seats[close_to_stage] \
               and desired_seats_per_location[north] <= available_seats[north] \
               and desired_seats_per_location[center] <= available_seats[center] \
               and desired_seats_per_location[dish_washer] <= available_seats[dish_washer]

    def is_valid_input(self):
        """Checks if the input is valid.
        If not: raises an error"""
        if not self.is_possible_to_place_everyone_where_they_want():
            raise Exception("Too many people want to sit in the same location. This is unsupported for now.")

        amount_of_guests_with_2_carts = len([guest for guest in self.guests if guest.cart == '2'])
        amount_of_tables_with_2_carts = len([table for table in self.tables if table.cart1 == '2'])
        if amount_of_guests_with_2_carts > amount_of_tables_with_2_carts:
            raise Exception("Too many people with 2 baby strolls. This is unsupported for now.")

        max_amount_of_wheel_chairs_per_table = self.tables[0].max_amount_of_wheel_chairs  # all the tables have this attribute and all are equal
        amount_of_guests_with_wheel_chair = len([guest for guest in self.guests if guest.wheel_chair])
        amount_of_wheel_chair_available = len([table for table in self.tables if table.wheel_chair]) * max_amount_of_wheel_chairs_per_table
        if amount_of_guests_with_wheel_chair > amount_of_wheel_chair_available:
            raise Exception("Too many people with wheel chairs. This is unsupported for now.")

        amount_of_guests_per_group_in_groups_file = {}
        for guest in self.groups:
            amount_of_guests_per_group_in_groups_file[guest.group_number] = amount_of_guests_per_group_in_groups_file.get(guest.group_number, 0) + guest.guests_number
        amount_of_guests_per_group_in_guests_file = {int(guest.first_name): guest.guests_number for guest in self.guests if guest.last_name == "קבוצה"}
        for group in amount_of_guests_per_group_in_groups_file:
            try:
                if amount_of_guests_per_group_in_groups_file[group] != amount_of_guests_per_group_in_guests_file[group]:
                    raise Exception("Group number {} in the groups file doesn't match the guests file. Fix the amount of people in the groups file.".format(group))
            except KeyError:
                raise Exception("There is a group in the groups file that doesn't exists in the guests file.")

        if len(amount_of_guests_per_group_in_groups_file) != len(amount_of_guests_per_group_in_guests_file):
            raise Exception("Amount of groups does not match in guests file and groups file.")

    def replace_group_number_with_guest_name(self):
        """Replaces the groups into the group content, namely the guests who make the group"""

        # replace the guests who sits in table
        for table in self.tables:  # go through all tables
            groups_in_table = [guest for guest in table.who_sits_here if guest.last_name == "קבוצה"]
            for group in groups_in_table:  # go through each group (in each table)
                group_number = group.group_number
                table.who_sits_here.remove(group)  # remove the group from the table
                for guest in self.groups:
                    if guest.group_number == group_number:
                        guest.table = table.number
                        table.who_sits_here.append(guest)

        # replace self.guests
        guests = [guest for guest in self.guests if guest.last_name == "קבוצה"]
        for guest in guests:
            if guest.last_name == "קבוצה":  # if it is a group
                group_number = guest.group_number
                table_number = guest.table
                wheel_chair = guest.wheel_chair
                cart = guest.cart
                self.guests.remove(guest)  # remove the group from the table
                for _guest in self.groups:
                    if _guest.group_number == group_number:
                        _guest.table = table_number
                        if wheel_chair:  # we don't have the information to who in he group has a wheel chair
                            _guest.wheel_chair = '*'  # so we just put astrix
                        if cart:  # we don't have the information to who in he group has a cart
                            _guest.cart = '*'  # so we just put astrix
                        _guest.location = guest.location
                        _guest.specific_table = guest.specific_table
                        self.guests.append(_guest)

    def can_guest_sit_in_this_table(self, table, guest, cart_availability=None, guests_in_table=None, wheel_chairs_in_table=None,j=None):
        """Some guests have constraints (for example wheel chair).
        This functions returns whether or not a specific guest can sit in a specific table given those constraints"""

        if guest.specific_table:  # if the guest has a specific table
            if guest.specific_table != table.number:  # if the specific table is not this table
                return False
        if guest.location and table.location != guest.location:  # guest's request for location fits the table location
            return False
        if guest.wheel_chair and not table.wheel_chair:  # if guests needs a wheel chair but the table doesn't have ot
            return False
        if guest.cart:  # if the guest needs a cart
            if not table.cart1 and not table.cart2:  # if guest needs a cart but no cart in table
                return False
            if int(guest.cart) == 1:  # if guest needs 1 cart but no carts in table
                if not table.cart1 and not table.cart2:
                    return False
            if int(guest.cart) == 2:  # if guest needs 2 cart but no 2 carts (in edge 1) in table
                if not table.cart1:
                    return False
                if int(table.cart1) != 2:
                    return False
        if guest.guests_number > table.available_seats:  # not enough room in table
            return False

        if guests_in_table is not None:
            if j is None:
                raise IndexError(" the index j must be given")
            available_seats_in_table = table.available_seats - guests_in_table[j]
            if available_seats_in_table < guest.guests_number:  # if there's enough room
                return False

        if cart_availability is not None:
            if j is None:
                raise IndexError(" the index j must be given")
            if guest.cart:  # if the guest needs a cart
                cart1_available, cart2_available = cart_availability[j]
                if int(guest.cart) == 2 and not cart1_available:  # if the guest needs 2 carts but no 2 carts are available (someone is already sitting there)
                    return False
                if int(guest.cart) == 1:
                    if not cart1_available and not cart2_available:
                        return False

        if wheel_chairs_in_table is not None:
            if j is None:
                raise IndexError(" the index j must be given")
            if guest.wheel_chair:  # if the guest needs a wheel chair
                number_of_wheel_chairs_already_in_table = wheel_chairs_in_table[j]
                if number_of_wheel_chairs_already_in_table >= table.max_amount_of_wheel_chairs:  # if the table already has max capacity of wheel chairs
                    return False

        return True

    def get_unseated_guests(self):
        """Returns a list of guests that don't have a table yet"""
        # return [guest for guest in self.guests if not guest.table]
        return [guest for guest in self.guests if not guest.already_sitting]

    def guest_must_sit_in_location(self, guest, location):
        """Returns True of guest must sit in specified location, False otherwise"""
        return guest.location == location

    def get_guests_that_must_sit_in_location(self, location, guests=None):
        """Returns a list of all guests that must sit in a specified location"""
        if guests is None:
            guests = self.guests

        return [guest for guest in guests if self.guest_must_sit_in_location(guest=guest, location=location)]

    def update_cart_availability(self, table, guest, cart_availability, j):
        """Update the cart availability after placing a guest in a table"""
        cart1_available, cart2_available = cart_availability[j]
        if guest.cart:  # if the guest needs a cart
            if int(guest.cart) == 1:  # if the guest needs 1 cart
                if table.cart1 and int(table.cart1) == 1 and cart1_available:  # if the cart is available
                    cart1_available = False  # then now it's not available anymore

                # and if it didn't update cart1 so it's cart2 which needs to be updated
                elif table.cart2 and int(table.cart2) == 1 and cart2_available:
                    cart2_available = False

            if int(guest.cart) == 2:  # if the guest needs 2 carts
                if table.cart1 and int(table.cart1) == 2 and cart1_available:
                    cart1_available = False

        cart_availability_in_table = (cart1_available, cart2_available)
        cart_availability.pop(j)
        cart_availability.insert(j, cart_availability_in_table)
        return cart_availability

    def update_wheel_chairs_per_table(self, table, guest, wheel_chairs_per_table, j):
        """Update the number of wheel chairs per table after placing a guest in a table"""
        if guest.wheel_chair and table.wheel_chair:
                wheel_chairs_per_table[j] += 1

        return wheel_chairs_per_table

    def place_everybody(self, order_of_locations_to_place=None):
        """Places guests in tables
        order_of_locations_to_place: a list containing all 4 locations (north, center, dish_washer, close_to_stage)
                                    ordered with the order you want to place the guests.
                                    For example: [close_to_stage, dish_washer, center, north]
                                    will first place guests close to the stage, afterwards in the dish washer location etc."""

        if order_of_locations_to_place is None:
            order_of_locations_to_place = self.locations

        unseated_guests = self.get_unseated_guests()  # get all the guests that don't have a seat yet
        self.fill_location(tables=self.tables, guests=unseated_guests)
        """
        for location in order_of_locations_to_place:
            tables = self.get_tables_by_location(location=location)  # get the tables in current location
            unseated_guests = self.get_unseated_guests()  # get all the guests that don't have a seat yet
            must_sit_in_location = self.get_guests_that_must_sit_in_location(location=location, guests=unseated_guests)  # guests that requested to be in current location

            # Since the algorithm relies somewhat on the order of the guests list
            # We put the guests that requested to be in the current location before the others
            # This helps the algorithm to converge faster
            for guest in must_sit_in_location:
                unseated_guests.remove(guest)

            must_sit_in_location.extend(unseated_guests)
            optional_guests = must_sit_in_location[:]

            # place guests in tables
            # changes self.tables and self.guests
            # uses dynamic programming
            self.fill_location(tables=tables, guests=optional_guests)"""

    def dp(self, tables, guests):
        """Uses dynamic programming and returns a matrix corresponding to the following logic:
        rows (index i) are guests, columns (index j) are tables.
        In mat[i][j] there is the amount of guests that can sit (capacity) if we had guests[:i] guests and tables[:j] tables.
        It's dividing it to a sub problem.
        That is the heart of the program"""

        # initialize the matrix to zeros
        mat = np.zeros(shape=(len(guests) + 1, len(tables) + 1))  # The matrix is of this shape to include 0 guests and tables

        # keeping count of how many guests ae sitting in each table
        number_of_guests_in_table = np.zeros(shape=(len(tables) + 1, ))  # in shape of len(tables) + 1 for convenience, the +1 is not necessary

        # keeping count of how many carts are in each table
        cart_data = []
        for table in tables:
            cart1_availability = True if table.cart1.isdigit() else False  # initialize to True (available)
            cart2_availability = True if table.cart2.isdigit() else False  # initialize to True (available)
            cart_data.append((cart1_availability, cart2_availability))

        cart_availability_per_table = [0] + cart_data  # the [0] in the beginning is for convenience

        # keeping count of how many wheel chairs are in each table
        number_of_wheel_chairs_per_table = np.zeros(shape=(len(tables) + 1,))  # in shape of len(tables) + 1 for convenience, the +1 is not necessary

        # bottom up approach
        for i in range(1, mat.shape[0]):
            cur_guest = guests[i - 1]  # current guest
            already_sitting = False  # flag to indicate if the guest is already sitting so we don't include twice
            already_counted_in_table_seats = False  # flag
            for j in range(1, mat.shape[1]):
                cur_table = tables[j - 1]  # current table
                capacity_without_guest = mat[i-1][j]  # if we don't include the guest in the solution, then it's like the row above
                capacity_with_guest = -1  # initialize to -1

                # available_seats_in_table = cur_table.available_seats - number_of_guests_in_table[j]
                # if available_seats_in_table >= cur_guest.guests_number or already_sitting:  # if there's enough room
                if self.can_guest_sit_in_this_table(table=cur_table, guest=cur_guest, cart_availability=cart_availability_per_table, guests_in_table=number_of_guests_in_table, wheel_chairs_in_table=number_of_wheel_chairs_per_table, j=j) or already_sitting:  # if the constraints of the guest match to the table
                    if not already_sitting:
                        capacity_with_guest = capacity_without_guest + cur_guest.guests_number
                        already_sitting = True

                    else:  # if already seating, don't count twice
                        # capacity_with_guest = mat[i][j - 1]
                        capacity_with_guest = capacity_without_guest + cur_guest.guests_number

                elif already_sitting:  # if it can't sit in this table but already sitting in another one
                    capacity_with_guest = mat[i][j - 1]

                # take the maximum between including the guest and not including it
                max_value = max(capacity_with_guest, capacity_without_guest)
                mat[i][j] = max_value
                if max_value == capacity_with_guest and max_value != mat[i][j-1] and not already_counted_in_table_seats:
                    number_of_guests_in_table[j] += cur_guest.guests_number
                    cart_availability_per_table = self.update_cart_availability(table=cur_table, guest=cur_guest, cart_availability=cart_availability_per_table, j=j)
                    number_of_wheel_chairs_per_table = self.update_wheel_chairs_per_table(table=cur_table, guest=cur_guest, wheel_chairs_per_table=number_of_wheel_chairs_per_table, j=j)
                    already_counted_in_table_seats = True

        return mat

    def get_who_sits_where_from_dp_matrix(self, matrix, tables, guests):
        """Input: matrix from the dynamic programming.
        Output: a dictionary with keys as tables and values as list containing guests who sits in the table"""

        # initialize a dict with instead of tables, their indices as keys (it's easier to work with that with the matrix)
        # values are what guests sits in this table
        tables_dict_by_index = {i: [] for i, _ in enumerate(tables, start=1)}
        for i in reversed(range(1, matrix.shape[0])):  # go through the matrix from bottom up
            for j in range(1, matrix.shape[1]):  # go through the matrix from left to right
                if matrix[i][j] > matrix[i-1][j]:  # if there is a change between the current row to the one above it
                        tables_dict_by_index[j].append(guests[i-1])  # the guest sits in this table (column j)
                        break  # and only in this table

        # instead of indices, the keys are now the tables themselves
        tables_dict = {tables[i - 1]: tables_dict_by_index[i] for i, _ in enumerate(tables, start=1)}
        return tables_dict

    def place_guests_after_dp(self, tables_dict):
        """places the guests in their table"""
        for table in tables_dict:
            for guest in tables_dict[table]:
                self.place_guest_in_table(table=table, guest=guest)

    def fill_location(self, tables, guests):
        """Fill a certain location with guests in an (almost) optimal way"""
        matrix = self.dp(tables=tables, guests=guests)  # matrix as returned from self.dp
        tables_dict = self.get_who_sits_where_from_dp_matrix(matrix=matrix, tables=tables, guests=guests)  # decode the matrix
        self.place_guests_after_dp(tables_dict)  # place the guests (change self.guests and self.tables)

    def is_map_legal(self):
        """Map validation
        This is ran in the end, after placing everyone.
        This should always return True, it's just to make sure"""
        for guest in self.guests:
            if not guest.table:  # if the guest is not sitting anywhere
                return False
            table = self.find_table_by_number(guest.table)
            if guest.location:  # if the guest has a specified location
                if guest.location != table.location:  # and is not sitting in this location
                    return False

        return True

    def run(self):
        """Makes the map
        Changes self.tables and self.guests"""
        # self.place_guests_in_mandatory_table()  # place guests that have specific tables
        self.is_valid_input()  # raises an error if the input is not valid
        while True:
            tables_temp = copy.deepcopy(self.tables)  # save the current state of the tables
            guests_temp = copy.deepcopy(self.guests)  # save the current state of the guests
            self.place_everybody()  # place guests in tables
            unseated_guests = self.get_unseated_guests()
            if unseated_guests:  # if some guests don't have room yet
                self.tables = copy.deepcopy(tables_temp)  # restore tables
                self.guests = copy.deepcopy(guests_temp)  # restore guests

                """The next block of code is changing the order of self.guests
                It puts the unseated guests in the beginning of the list self.guests
                This would help the program to converge faster to a solution
                So again, what we do is try another order of guests
                this might help since the sitting is dependent on the order"""

                # removing the unseated guests from self.guests
                for unseated_guest in unseated_guests:
                    for guest in self.guests:
                        # if there are 2 guests with the same first name and last name this will fail, good enough
                        if unseated_guest.first_name == guest.first_name and unseated_guest.last_name == guest.last_name:
                            self.guests.remove(guest)

                # putting the unseated guests first
                unseated_guests.extend(self.guests)
                self.guests = copy.deepcopy(unseated_guests)

                # random.shuffle(self.guests)
            else:  # if all guests have a seat
                break  # we're done

        self.replace_group_number_with_guest_name()  # replaces group number to the group guests names


def run(tables, guests, groups, save_map=True):
    """Fill the passover map"""
    # convert the tables/guests into Table/Guest object list
    tables = [Table(table) for table in tables]
    guests = [Guest(guest) for guest in guests]
    group_guests = [Guest(guest) for guest in groups]

    passover_map = PassoverMap(tables=tables, guests=guests, groups=group_guests)
    passover_map.run()
    # print("Map Legal: {}\n\n".format(passover_map.is_map_legal()))
    # passover_map.print_map_by_tables()
    # passover_map.print_map_by_guests()
    if save_map:
        passover_map.save_map_by_guests_to_csv()
        passover_map.save_map_by_tables_to_csv()
        passover_map.save_last_names()

