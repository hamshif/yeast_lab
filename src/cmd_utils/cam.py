import socket
from lab_util.util import pr


class PlateCam:
    """
    """
    
    def snapshot(self, full_name):
        
        full_name = full_name
        
        HOST = 'gphoto'    # The remote host
        PORT = 8888              # The same port as used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        
        
        s.send(bytes(full_name, 'UTF-8'))
        data = s.recv(1024)
        
        s.close()
        
        return_message = repr(data)
        
        print('CamClient received: ')
        pr('return_message: ' + return_message)
        
        print(return_message.split(':')[0])
        
        if 'NOK' in return_message:
            print('NOK')
        else:
            print('OK   ' + full_name)
#             os.system('open ' + "'" + full_name +"'")

            return True
        
        
        return False
    

        