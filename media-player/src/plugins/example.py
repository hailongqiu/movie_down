
class plugin_class_name(object):
    def __init__(self):
        pass
		  
    def init_values(self, this, gui, ldmp):		  
        pass
		  		  
    def auto(self): 
        return True
		  
    def start(self):
        print "start plugin..."
		  
    def stop(self): 
        print "stop plugin..."
		  
    def name(self): 
        return "deepin_media_player_plugin_class_name_***" 
		  
    def insert(self): 
        return None
		  
    def icon(self): 
        return None
		  
    def version(self):
        return "2.0"
    
    def author(self):
        return "hailongqiu"
	  
	  
def return_plugin(): 
    return plugin_class_name

