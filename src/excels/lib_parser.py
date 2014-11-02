import sys, xlrd, traceback
from yeast_libraries.models import YeastStrain_Model, YeastLibrary_Model, PlateFormat_Model, PlateLocus_Model, PlateScheme_Model


def getNumValue(s):
        
    s = s.lower()
    total_gematric_value = 0
    output = []
    
    for character in s:
        number = ord(character) - 96
        total_gematric_value = total_gematric_value + number
        output.append(number)
    
#         print('list of gematric values: ', output)
#         print('total gematric value: ', total_gematric_value)
    
    return total_gematric_value



class LibraryParser:
    

    def getNumValue(self, s):
        
        s = s.lower()
        total_gematric_value = 0
        output = []
        
        for character in s:
            number = ord(character) - 96
            total_gematric_value = total_gematric_value + number
            output.append(number)
        
#         print('list of gematric values: ', output)
#         print('total gematric value: ', total_gematric_value)
        
        return total_gematric_value
    
    
    def libraryExcelParser(self, bytes_stream, personal_name):
    
        print('libraryExcelParser()')
        print('personal_name: ', personal_name)
    #funky python for discerning full path name from bytstreem
        if type(bytes_stream) == type(''):
            """
            """
            libname = bytes_stream.split('/')[-1]
            
            print('libraryExcelParser     libname:', libname)
             
            lib = YeastLibrary_Model.objects.filter(name=libname)
             
            if lib.count() == 0:
                 
                workbook = xlrd.open_workbook(bytes_stream)
                 
                print('going to create initial library from local excel: ', libname)
            else:
                print('already have library: ', libname, ', registered')
                return
                 
                 
        else:
             
            libname = bytes_stream.name
            workbook = xlrd.open_workbook(libname, file_contents=bytes_stream.read())
        
        
        libname = libname[0:-4]
        print('libraryExcelParser     libname:', libname)
        

      
          
        sheet_name = workbook.sheet_names()[0]
        sheet = workbook.sheet_by_name(sheet_name)
          
        num_rows = sheet.nrows -1
        num_columns = sheet.ncols -1
          
        if num_columns >= 3:
            
            #find out or deduce how many rows
            
            plate_num = 1
            current_row = 1
            row_index = 1
            highest_row = 1
            
            while plate_num == 1:
                
                plate_num = sheet.cell_value(current_row, 0)
                row_index = sheet.cell_value(current_row, 1)
                
                num_value = self.getNumValue(row_index)
                
                if num_value > highest_row:
                    
                    highest_row = num_value
                    
                
                current_row = current_row + 1
                    
            
            print('highest_row: ', highest_row)
            highest_column = 16
            
            
            if highest_row <= 8:
                
                highest_row = 8
                
            elif highest_row <= 16:
                
                highest_row = 16
                highest_column = 24
                
            else:
                
                highest_row = 24
                highest_column = 48 
            
            print('highest_row: ', highest_row)
            print('highest_column: ', highest_column)

            
            plate_format, created = PlateFormat_Model.objects.get_or_create(width_loci=highest_column, length_loci=highest_row)
                   
            stack_index = 1    
               
            try:
                library, created = YeastLibrary_Model.objects.get_or_create(name=libname)

                library.personal_name=personal_name
                library.save();
                
                if created:
                    print('library created')
                else:
                    print('library retrieved')
                      
#                 library.plate_schemes.clear()
#                 print('schemes cleared')
                  
                plate_scheme, created = PlateScheme_Model.objects.get_or_create(format = plate_format, library=library, index=stack_index)
                if created:
                    print('plate_scheme created')
                else:
                    print('plate_scheme retrieved')
                    
                strain, created = YeastStrain_Model.objects.get_or_create(name = 'empty')
                
                  
            except Exception:
                print(sys.exc_info())
                traceback.print_exc() 
            
            #sparse matrix              
                
                  
            current_row = 0
            
            
            try:
             
                while current_row < num_rows:
                    current_row += 1
                     
                    temp_plate_index = sheet.cell_value(current_row, 0)
                    row = sheet.cell_value(current_row, 1)
                    column = sheet.cell_value(current_row, 2)
                    strain_name = sheet.cell_value(current_row, 3)
                    
    #                 print(strain_name, 'plate:', str(temp_plate_index), 'row:', str(row), 'column', str(column))
                    print('plate: ', str(temp_plate_index), 'row:', row, 'column', str(column)[:-2])
                    
                    if 'null' in strain_name.lower():
                        print('The word null appears in the excel ORF column the row is ignored comparison must use sparse matrix method')
                        continue
                      
                    if temp_plate_index != stack_index:
                        
                        stack_index = temp_plate_index
                         
                        plate_scheme, created = PlateScheme_Model.objects.get_or_create(format = plate_format, library=library, index=stack_index)
                        if created:
                            print('plate_scheme created')
                        else:
                            print('plate_scheme retrieved')
                      
                      
                    strain, created = YeastStrain_Model.objects.get_or_create(name = strain_name)
                    if created:     
                        print('strain: ', strain.__str__(), ' was created')
                      
                    locus, created = PlateLocus_Model.objects.get_or_create(
                        
                        scheme = plate_scheme,
                        strain = strain,
                        row = row,
                        column = column,
                        )
                     
                    print('locus.__str__(): ',locus.__str__())
                    
                    
                print('out of while')
                
                
            except Exception:
                print(sys.exc_info())
                traceback.print_exc() 
                
                
            return