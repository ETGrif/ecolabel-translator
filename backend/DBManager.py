class DBManager:
    """
    Handles all interactions with the server's database
    
    Attributes:
        db_file (string): A string filename to the MongoDB
    """
    def __init__(self, db_file):
        self.db_file = db_file
    
    def search_for_label(self, searchTerm):
        """
        Searches the database for potential matches based on the user provided searchTerm
        
        Args:
            searchTerm (string): The text entered by the user to search for a label
            
        Returns:
            potential_matches (dict<string, string>): A dictionary of label names to the corresponding logo image filename
        """
        raise NotImplementedError()
    
    def get_info_on_label(self, label):
        """
        Queries the database for all information about the provided label
        
        Args:
            label (string): the name of the label selected by the user
            
        Returns:
            label_info (dict<string, string>): a dictionary representation of info pulled from the db
                Ex: { "epa_description" : "<data from epa website>" }
        """
        raise NotImplementedError()
    