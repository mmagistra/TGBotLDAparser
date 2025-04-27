from vector_manager import vector_manager as mgr
import LDA_parser as LDA

class user:
    def __init__(self, message):
        self.id = message.chat.id
        self.banlist = []
        self.last_message = None
        self.vector_db = None
        self.message_urls = []
        self.local_manager = mgr()

    
    def set_message(self, new_message):
        self.last_message = new_message
        self.message_urls = self.last_message.text.split('\n')
        print(self.message_urls)
        
    
    def get_message(self): 
        return self.last_message 
        
    
    def set_banlist(self, ban_message: str):
        self.banlist = ban_message.lower().split(",")
        print(self.banlist)
        self.local_manager.create_vector_database(self.banlist)

    def get_banlist(self):
        return self.banlist 
    
    def set_banlist_vectorize(self, db):
        self.vector_db = db

    def get_banlist_vectorize(self, db):
        return self.vector_db
    
    def check_urls(self):
        output = ""
        for url in self.message_urls:
            output = output + str(url)
            themes = LDA.extract_unique_topics_from_url(url)
            if self._check_topics(themes):
                output += "❌\n"
            else:            
                output += "✔️\n"
        return output

    def _check_topics(slef, themes):
        for topic in themes:
            if slef.local_manager.compare_with_distance_threshold(topic, 26):
                return 1
            else :
                return 0