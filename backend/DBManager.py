class DBManager:
    
    def __init__(self, db_file):
        self.db_file = db_file
    
    def search_for_label(self, searchTerm):
        raise NotImplementedError()
    
    def get_info_on_label(self, label):
        raise NotImplementedError()
    