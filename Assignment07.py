#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# Muhammad Mannan, 2021-Aug-11 Modified File
# Muhammad Mannan, 2021-Aug-23, Updated File:
#                               now uses binary data to
#                               store data permanently
#                               in .dat file. Also added
#                               error handling.
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = ''  # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file

objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Processing data to lstTbl"""
    @staticmethod
    def addCD(addInfo, data):
        """Function used to add element to a list of dictionaries

        References the following values:
        The tuple which is returned from (IO.cdInfo),then appends it to a
        dictionary (dicRow). The dictionary is then appended to our 2d table (lstTbl).
        Args:
            addInfo (Tuple): Tuple containing input values from a function
            table (list of dict): 2D data structure (list of dicts) that holds the data in memory during runtime.
        Returns:
            None.
        """
        dicRow = {'ID': (int(addInfo[0])),
                  'Title': addInfo[1], 'Artist': addInfo[2]}
        data.append(dicRow)
        

    @staticmethod
    def removeCD(cdNumber, cdList):
        """Function that is utilized to delete and entry from the inventory or
        an element from the list containing dictionaries. The value/entry number
        the user enters is used to search in the dictionary containing the key
        and value the user has entered and then deletes that element from the 2d table (lstTbl).
        Args:
            cdNumber (integer): an integer value is entered which corresponds to the entry number for the cd the
            user would to remove from inventory
            cdList (list containing dictionaries): 2D table of date (or a list of dictionaries)
            which contains the data in memory during the time the program is running.

        Returns:
            None.
        """
        try:
            intRowNr = -1
            for row in cdList:
                intRowNr += 1
                if row['ID'] == cdNumber:
                    del cdList[intRowNr]
                    CDRemoved = True
                    break
            return CDRemoved
        except UnboundLocalError:
            print("Please pick a valid entry to remove")


class FileProcessor:
    """Processing the data to and from data file"""

    @staticmethod
    def read_file(file_name, data):
        """Function to manage data ingestion from file to a list of dictionaries
        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        Returns:
            None.
        """
        data.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'rb')
        pcklFile = pickle.load(objFile)
        for line in pcklFile:
            data.append(line)
        objFile.close()

    @staticmethod
    def write_file(file_name, data):
        """Function to write data in lstTbl to a .dat file

        Writes the data from a 2D table (lstTbl) into a data file file_name
        (list of dicts) table one line in the file represents one dictionary row in table.
        Args:
            file_name (string): file name which is used to write data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        Returns:
            None.
        """
        objFile = open(file_name, 'wb+')
        pickle.dump(data, objFile)
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user.
        Args:
            None.
        Returns:
            None.
        """

        print(
            'Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection.
        Args:
            None.
        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input(
                'Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(data):
        """Displays current inventory table.
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in data:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def cdInfo():
        """Asks user to input the CD ID, Title, and Artist name to add a new cd into inventory:
            None.
        Returns:
            Tuple: objects with the user's entered inputs for new CD ID, Title, and Artist name
        """
        while True:
            try:
                strID = int(input('Enter ID: ').strip())
                break
            except ValueError:
                print('Please enter a number!')
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return (strID, strTitle, stArtist)

    def removalInfo():
        """Asks user to input the CD ID to determine which entry to remove from inventory currently in memory.
        Returns:
            Int: entry (integer) number. 
        """
        while True:
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except ValueError:
                print('Please enter an ID number')
        return intIDDel


# 1. When program starts, read in the currently saved Inventory
try:
    FileProcessor.read_file(strFileName, lstTbl)
except FileNotFoundError:  # the file is created if it doesn't already exist
    FileProcessor.write_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input(
            'type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input(
                'canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        addInfo = IO.cdInfo()
        # 3.3.2 Add item to the table
        DataProcessor.addCD(addInfo, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        cdNumber = IO.removalInfo()
        # 3.5.2 search thru table and delete CD
        removedCD = DataProcessor.removeCD(cdNumber, lstTbl)
        if removedCD:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input(
                'The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')
