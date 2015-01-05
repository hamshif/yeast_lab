
import os, traceback, sys, psycopg2

class DB_Manager():
    
    def __init__(self, db_name):
        
        self.con = psycopg2.connect(host = 'cab-27', database=db_name) 
        self.cur = self.con.cursor() 
        
    
    def close(self):
        
        if self.con:
            self.con.close()  
    
    
        
    def getOrCreate(self, table, column_names, values, pk_name):
        
        l = len(column_names)
        
        if len(values) > l:
        
            print('len(values) > len(column_names)')
            raise Exception("can't map values to columns")
        
        val_dict = []
        val_str = '('
        col_name_str = '('
        
        
        
        for i in range(l):
            
            v = values[i]
            
            if isinstance(v, str):
                v = "'" + v + "'"
            
            val_dict.append(column_names[i] + "=" + str(v))
            
            
            if i > 0:
                val_str = val_str + ", " + str(v)
            else:
                val_str = val_str + str(v)
            
            col_name_str = col_name_str + ', '
            
            

        val_dict = '(' + ' AND '.join(val_dict) + ')'
#         print('val_dict: ', val_dict)
        
        val_str = val_str + ')'
#         print('val_str: ', val_str)
        
        col_name_str = '(' + ', '.join(column_names) + ')'
#         print('col_name_str: ', col_name_str)
        
        
        try:
            command = 'SELECT ' + pk_name +' FROM ' + table + ' WHERE ' + val_dict
#             print('command: ', command)
#             print('')
            
            self.cur.execute(command)
            return_value = self.cur.fetchone()
             
#             print('return_value: ', return_value, '  type(return_value):', type(return_value))
             
            if return_value is None:
                 
                command = "INSERT INTO " + table + " " + col_name_str + " VALUES " + val_str + " RETURNING " + pk_name
#                 print('command: ', command)
                 
                self.cur.execute(command)
                idd = self.cur.fetchone()[0]
#                 print('idd: ', idd)
                self.con.commit()
                
                return [True, idd]
                
            else:
#                 print('retrieved')
                return [False, return_value[0]]
                
        except Exception: 
                
            print('exception: ', sys.exc_info)
            traceback.print_exc()
            
            if self.con:
                self.con.close()  
            
