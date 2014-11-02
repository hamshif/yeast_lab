
import subprocess


class Exiv2:
    
    def addComment(self, img_full_path_name = '', comment = ''):
        
        print('len(comment): ', len(comment))
        
        if len(comment) > 100:
            
            print('Error img_dict was longer than 100 chars it wont fit the image format constrictions')
            return
        
        subprocess.call(["exiv2", "-M", "set Exif.Photo.UserComment charset=Ascii ~" + comment + "^", img_full_path_name])
    

    def getComment(self, img_full_path_name = ''):
       
        p = subprocess.Popen(["exiv2", "-g", "Exif.Photo.UserComment", img_full_path_name], stdout=subprocess.PIPE)
        out, err = p.communicate()
        
        a = out.decode()
        
        if '~' in a:
            i = a.index('~') + 1
            end = a.index('^')
        
            b = a[i:end]
        
            return ''.join(['Exif comment: ',  b])
        
#             print(len(b))
        else:
            return 'The image doesnt have the searched comment'


