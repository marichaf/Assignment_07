#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions - creating CD inventory
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# M Friedman, 8/14, updated to complete assignment - add functions and organize code
# M Friedman, 8/20, updated to separate and fix functions, add binary file, structured exceptions
#------------------------------------------#

# -- DATA -- #

import pickle

strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file - FOR INITIAL UPLOAD ONLY
strDatFileName = 'CDInventory.dat' # data storage file
objFile = None  # file object
intIDDel = None #ID of CD user wants to delete
cd_new = [] # list of cd info the user wants to add


# -- PROCESSING -- #
class DataProcessor:

    @staticmethod
    def add_cd(strID, strTitle, strArtist, table):
        '''Adds individual CD data to 2D list in memory
        
        Args:
            strID: the ID no. of the CD to add
            strTitle: the Title of CD to add
            strArtist: the Artist Name of CD to add
            table: table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
            
        Retuns:
            None.
        '''
        # 3.3.2 Add item to the table
        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dicRow)
    
    @staticmethod
    def remove_cd(table, IDno):
        '''Removes individual CD data from 2D list in memory
        
        Args:
            table: table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
            IDno: the ID number of CD to find and delete
            
        Retuns:
            None.
        '''
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == IDno:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed\n')
        else:
            print('Could not find this CD!\n')
 

class FileProcessor:
    """Processing the data to and from text file"""
    pass

    @staticmethod
    def read_file_txt(file_name, table):
        """Function to manage data ingestion from TEXT file to a list of dictionaries
        Only necessary the first time the script is run. Can be removed after.
        After the first time the script is run, a new binary storage file is created
        for future use.

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()

    
    
    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from .dat file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        with open(file_name, 'rb') as objFile:
            data = pickle.load(objFile)
        return data
        
    @staticmethod
    def write_file(file_name, table):
        '''Writes the in-memory inventory to a .dat file
        
        Args:
            file_name (string): name of file used to write the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None.
        '''
        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)
            #no error handling here because with 'wb' mode the file is created if it doesn't exist

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    # TODO - add docstring
    def error_read_file(file_name):
        '''Evaluates if the file to be read exists in the directory.
        
        Args: 
            file_name (string): name of file used to write the data to
            
        Returns:
            Result (Boolean): True if file is in directory, False if not.
        '''
        try:
            with open(file_name, 'rb'):
                print('File found. Loading...')
                result = True
        except FileNotFoundError:
            print('File', file_name, 'not found.')
            result = False
        return result

    
    def inp_delete(): 
        '''Gets user input for which CD to delete from inventory

        Args:
            None.

        Returns:
            Result: integer of ID of CD to delete. 
        '''
        #TODO for assignment 7 - add structured error handling
        while True:
            result = input('Which ID would you like to delete? ')
            try:
                int(result)
                break
            except ValueError as e:
                print('That is not an integer, please try again. Error message: ', e)
        return int(result)
    
    @staticmethod
    def inp_newcd():
        '''Gets user input to add new CD information to inventory.
        
        Args:
            None
            
        Returns:
            strID (integer): ID no. of CD
            strTitle (string): Title of CD
            strArtist (string): CD Artist's name
        '''
        while True:
            strID = input('Enter ID: ')
            try:
                int(strID)
                break
            except ValueError as e:
                print('That is not an integer, please try again. Error message: ', e)
        strID = strID.strip()
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, strArtist
    
        
       
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file_txt(strFileName, lstTbl) # load .txt file for first script run
# can be commented out subsequently. The "load" function in script uses binary file.

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
        if IO.error_read_file(strDatFileName) == True:
            print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
            strYesNo = input('type \'yes\' to continue and reload from file. Otherwise, reload will be canceled: ')
            if strYesNo.lower() == 'yes':
                print('reloading...')
                lstTbl = FileProcessor.read_file(strDatFileName)
                IO.show_inventory(lstTbl)
            else:
                input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
                IO.show_inventory(lstTbl)
        else:
            print('File not found. No data will be loaded.')
            continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strTitle, strArtist = IO.inp_newcd()
        DataProcessor.add_cd(strID, strTitle, strArtist, lstTbl) # added this after moving the code to that function def above
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
        intIDDel = IO.inp_delete()
        # 3.5.2 search thru table and delete CD
        DataProcessor.remove_cd(lstTbl, intIDDel)
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
            FileProcessor.write_file(strDatFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




