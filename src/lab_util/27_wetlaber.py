import os, sys, shutil

DEST = '/cs/wetlab/dev_growth_data'


def walkthrough():
    """
    """
    
    sys_path = os.path.join('/cs/wetlab/gid_dev/downloads')
#         sys_path = os.path.join('/cs/wetlab/yeast_library_images', inner_path)   
       
    if not os.path.exists(sys_path):
        os.makedirs(sys_path)
    else:
        try:
           
            for root, dirs, files in os.walk(sys_path):
                print "Current directory: " + root
                print "Sub directories: " + str(dirs)
                print "Files: " + str(files)
        
        except Exception:    
            print sys.exc_info()
            print 'just printed exception'
            

#walkthrough()

def writeToWetlab(sys_path, inner_path, file_name):
    """
    """
    origin = os.path.join(sys_path, inner_path)
    print 'origin: ', origin
    
    
    destination = os.path.join(DEST, inner_path)
    print 'destination: ', destination
    
    if not os.path.exists(destination):
        os.makedirs(destination)
        
    
    shutil.copy(os.path.join(origin, file_name), destination)
    
    
writeToWetlab('/cs/system/gideonbar/Desktop/local/downloads', 'stam', 'plate.png')