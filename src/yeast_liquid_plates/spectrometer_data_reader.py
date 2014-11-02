
import os, traceback, sys, datetime, xlrd, psycopg2

from excels.lib_parser import getNumValue
from db_util.db_manager import DB_Manager 

class SpectrometerDataReader:
        
    def getData(self, db_name, path, plate_id, format_id, process_id, process_table_name):
    
        print('getData:', datetime.datetime.now())
        sys.stdout.flush()
        
        print(db_name, plate_id, format_id)
        
        try:
            self.manager = DB_Manager(db_name)
            
            self.con = psycopg2.connect(host = 'cab-27', database=db_name, user='gideonbar') 
            self.cur = self.con.cursor() 
            
            self.cur.execute('SELECT width_loci, length_loci FROM ' + 'yeast_libraries_plateformat_model' + ' WHERE id = ' + str(format_id))
            tu =  self.cur.fetchone()
            total_wells = tu[0] * tu[1]
#             print('total_wells: ', total_wells)
            
            sheets = self.getSheets(os.path.join(path, 'data'))
            
            sheet = sheets[0]
            
#             print('')
            
            
            liquid_procedure_pk, user, description, dilution_time, end_time = self.extractLiquidProcedure(plate_id, total_wells, path, sheet)
            hardware_config_pk = self.extractHardwareConfig(sheet)
            spectrometer_procedure_pk  = self.extractSpectrometerProcedure(sheet)
             
#             print(path)
            data_dir_name = path.split('/')[-1:][0]
#             print('data_dir_name:', data_dir_name)
             
             
            table = 'yeast_liquid_plates_spectrometerexperiment_model'
            column_names = ['plate_id', 'hardware_config_id', 'liquid_procedure_id', 'spectrometer_procedure_id', 'description', '"user"', 'data_dir_name', 'dilution_time', 'end_time']
            values = [plate_id, hardware_config_pk, liquid_procedure_pk, spectrometer_procedure_pk, description, user, data_dir_name, dilution_time, end_time]
             
            created, experiment_pk = self.manager.getOrCreate(table, column_names, values, 'id')
            
#             print('experiment_pk: ', experiment_pk, 'was created: ', created)
 
#             print('')
               
 
            for sheet in sheets:
                   
                self.extractWellData(sheet, experiment_pk)
    
#                 print('')
#                 print('new excel file')
#                 print('')
             
            
            self.cur.execute("UPDATE " + process_table_name + " SET status = 'complete' WHERE id = " + str(process_id))
            self.cur.execute("UPDATE " + process_table_name + " SET experiment_id = " + str(experiment_pk) + " WHERE id = " + str(process_id))
            self.con.commit()
             
           
        except Exception:
              
            print('exception: ', sys.exc_info)
            traceback.print_exc()
            
            try:
                if self.con:
                    self.con.close()
                self.con = psycopg2.connect(host = 'cab-27', database=db_name, user='gideonbar') 
                self.cur = self.con.cursor() 
                self.cur.execute("UPDATE " + process_table_name + " SET status = 'failed' WHERE id = " + str(process_id))
                self.con.commit()
                print('failed default transpired')
                
            except Exception:
                print('exception: ', sys.exc_info)
                traceback.print_exc()
         
        finally:
             
            if self.con:
                self.con.close()
             
            if self.manager:    
                self.manager.close()
                
        
    
    
    def extractLiquidProcedure(self, plate_id, total_wells, path, sheet):
        
        try:
            r = os.listdir(path = os.path.join(path))
            
#             print('path: ', path);
#             print('list of inner dirs: ', r);
            
            ff = ''
            
            for f in r:
                
                if f.endswith('information.txt'):
                    
#                     print('information file: ', f)
                    ff = open(os.path.join(path, f), 'r')
                    break
            
#             if ff=='':
#                 
#                 return HttpResponse(json.dumps({'error': 'couldnot find information text'})) 
#             
            
            lines = ff.readlines()
            ff.close()
            
            
            for l  in lines[1:]:
                l = l.strip()
                
                if 'User:' in l:
                    l = l.replace('User:', '')
                    l = l.strip()
                    user = l
                    
                elif 'Description:' in l:
                    l = l.replace('Description:', '')
                    l = l.strip()
                    description = l
                
                elif 'Plate type:' in l:
                    l = l.replace('Plate type:', '')
                    l = l.strip()
                    plate_type = float(l)
                    
                    if total_wells == plate_type:
                        ''
#                         print('total_wells match between data and plate')
                    else:
                        ''
#                         print("total_wells don't match between data and plate!!!")
#                         return HttpResponse(json.dumps({'error': "The number of wells in the data doesn't the affiliated plate"}))
                    
                elif 'Volume:' in l:
                    l = l.replace('Volume:', '')
                    l = l.strip()
                    well_volume = float(l)
    
                elif 'Target OD:' in l:
                    l = l.replace('Target OD:', '')
                    l = l.strip()
                    target_od = float(l)
                    
                elif 'Upper bound OD:' in l:
                    l = l.replace('Upper bound OD:', '')
                    l = l.strip()
                    upper_bound_od = float(l)
                
                elif 'Measure O/N:' in l:
                    l = l.replace('Measure O/N:', '')
                    l = l.strip()
                    measure_o_n = float(l)
                    
                elif 'O/N growth:' in l:
                    l = l.replace('O/N growth:', '')
                    l = l.strip()
                    o_n_growth = l.replace('every ', '').replace(' min for ', ',').replace(' hours', '')
                    o_n_growth = o_n_growth.split(',')
                    
                    interval = float(o_n_growth[0])
                    duration = float(o_n_growth[1])
                    
#                     print('o_n_growth: ', o_n_growth)
                    
                    
                elif 'Dilution:' in l:
                    l = l.replace('Dilution:', '')
                    l = l.strip()
                    dilution = float(l)
                
                elif 'Dilution time:' in l:
                    l = l.replace('Dilution time:', '')
                    l = l.strip()
                    
                    dilution_time = datetime.datetime.strptime(l, '%d/%m/%Y %H:%M:%S')
                    dilution_time = dilution_time.strftime('%m/%d/%Y %I:%M:%S %p')
#                     print('dilution_time: ', dilution_time)
                        
                    
                elif 'End time:' in l:
                    l = l.replace('End time:', '')
                    l = l.strip()
                    end_time = datetime.datetime.strptime(l, '%d/%m/%Y %H:%M:%S')
                    end_time = end_time.strftime('%m/%d/%Y %I:%M:%S %p')
                    
#                     print('end_time: ', end_time)
    
                    
                elif 'Final growth:' in l:
                    l = l.replace('Final growth:', '')
                    l = l.strip()
                    final_growth = l.replace('measure every ', '').replace('  min (not dilution for the first ', ',').replace(' hours)', '')
#                     print('final_growth: ', final_growth)
                    
                    final_growth = final_growth.split(',')
                    dilution_onset_delay = float(final_growth[1])
                    
                    
                elif 'MCA tips position:' in l:
                    l = l.replace('MCA tips position:', '')
                    l = l.strip()
                    mca_tips_position = float(l)
                
#                 print(l)    
                
                
            table = 'yeast_liquid_plates_liquidyeastplate_model'
            column_names = ['id']
            values = [plate_id]
            
            created, liquid_plate_pk = self.manager.getOrCreate(table, column_names, values, 'id')
            
            if created:
                print('liquid_plate_pk: ', liquid_plate_pk, 'was created')
                print('this is  problemsince it should exist from copy registry')
            
            
            table = 'lab_experimentschedule_model'
            column_names = ['fixed_interval', 'duration ', 'onset_delay', 'schedule_csv']
            values = [interval, duration , dilution_onset_delay, '']
            
            created, schedule_pk = self.manager.getOrCreate(table, column_names, values, 'id')
#             print('schedule_pk: ', schedule_pk, 'was created: ', created)
            
            
            index = self.pinCellInColumn(sheet, 0, 'Settle')
            settle_time = sheet.cell_value(index, 4)
#             print('settle_time: ', settle_time)
            
            table = 'yeast_liquid_plates_liquidprocedure_model'
            column_names = ['experiment_schedule_id', 'target_od', 'upper_bound_od', 'measure_o_n', 'dilution', 'mca_tips_position', 'settle_time', 'well_volume']
            values = [schedule_pk, target_od, upper_bound_od, measure_o_n, dilution, mca_tips_position, settle_time, well_volume]
            
            created, liquid_procedure_pk = self.manager.getOrCreate(table, column_names, values, 'id')
#             print('liquid_procedure_pk: ', liquid_procedure_pk, 'was created: ', created)
            
            
            return [liquid_procedure_pk, user, description, dilution_time, end_time]
            
        
        except Exception: 
                
            print('exception: ', sys.exc_info)
            traceback.print_exc()
            ff.close()
            
    
    def rowToCSV(self, row):
        csv_str = ''
        
        for cell in row:
            
            try:
                cell_value = cell.value
                
                if not cell_value == '':
                    
                    csv_str = csv_str + cell_value + ', '
                
            except Exception:
#                             print(sys.exc_info())
                traceback.print_exc()
                
        if csv_str.endswith(', '):
            csv_str = csv_str[0:-2]
    
        return csv_str
    
    
    
    def extractHardwareConfig(self, sheet):
        
        row = sheet.row(0)
        application = self.rowToCSV(row)
#         print('application: ', application)
        
        row = sheet.row(1)
        device = self.rowToCSV(row)
#         print('device: ', device)
        
        row = sheet.row(2)
        firmware = self.rowToCSV(row)
#         print('firmware: ', firmware)
        
        row = sheet.row(9)
        user = self.rowToCSV(row)
#         print('user: ', user)
        
#         print('')
        
        table = 'lab_hardwareconfig_model'
        column_names = ['application', 'device', 'firmware', '"user"']
        values = [application, device, firmware, user]
        
        created, hardware_pk = self.manager.getOrCreate(table, column_names, values, 'id')
#         print('hardware_pk: ', hardware_pk, 'was created', created)
            
        return hardware_pk
        
        
    def extractSpectrometerProcedure(self, sheet):
        """
        """
#         print('')
        
        row = sheet.row(10)
        plate_description = self.rowToCSV(row)
#         print('plate_description: ', plate_description)
        
        index = self.pinCellInColumn(sheet, 0, 'Multiple Reads per Well (XY-Line)')
        v = sheet.cell_value(index, 4) 
        v = v.split(' x ')
        read_matrix_width = float(v[0])
#         print('read_matrix_width: ', read_matrix_width)
        read_matrix_height = float(v[0])
#         print('read_matrix_height: ', read_matrix_height)
        
        
        index = self.pinCellInColumn(sheet, 0, 'Multiple Reads per Well (Border)')
        v = sheet.cell_value(index, 4) 
        reades_per_well_border = v
#         print('reades_per_well_border: ', reades_per_well_border)

        index = self.pinCellInColumn(sheet, 0, 'Wavelength')
        wave_length = sheet.cell_value(index, 4) 
#         print('wave_length: ', wave_length)
        
        index = self.pinCellInColumn(sheet, 0, 'Bandwidth')
        band_width = sheet.cell_value(index, 4)
#         print('band_width: ', band_width)
    
    
        index = self.pinCellInColumn(sheet, 0, 'Number of Flashes')
        flashes = sheet.cell_value(index, 4)
#         print('flashes: ', flashes)
        
        
        
        index = self.pinCellInColumnStrats(sheet, 0, 'Well')
        row = sheet.row(index)
        sampled_indexes_csv = self.rowToCSV(row).replace('Well, Mean, StDev, ', '')
#         print('sampled_indexes_csv: ', sampled_indexes_csv)
        
        
        index = self.pinCellInColumn(sheet, 5, 'Target Temperature')
        
        if index >= 0:
        
            v = sheet.cell_value(index, 5)
            v = v.replace('Target Temperature:', '').strip()
            target_temperature = float(v[:-2])
#             print('target_temperature: ', target_temperature)
        else:
#             print('oops!!!!!!!!!!!! this version of excel output did not have a target temperature!!!!!!!!!!!!')
            target_temperature = 0.0
        
        table = 'yeast_liquid_plates_spectrometerprocedure_model'
        column_names = ['reades_per_well_border', 'wave_length', 'band_width', 'flashes', 'read_matrix_width', 'read_matrix_height', 'sampled_indexes_csv', 'target_temperature']
        values = [reades_per_well_border, wave_length, band_width, flashes, read_matrix_width, read_matrix_height, sampled_indexes_csv, target_temperature]
        
        created, spectrometer_procedure_pk = self.manager.getOrCreate(table, column_names, values, 'id')
#         print('spectrometer_procedure_pk: ', spectrometer_procedure_pk, 'was created: ', created)
        
        return spectrometer_procedure_pk
    
        
    
    def extractWellData(self, sheet, experiment_pk):
        
        index = self.pinCellInColumnStrats(sheet, 0, 'Start Time:')
        
        
        v = sheet.cell_value(index, 1)
        start_time = datetime.datetime.strptime(v, '%m/%d/%Y %I:%M:%S %p' )
        start_time = start_time.strftime('%m/%d/%Y %I:%M:%S %p' )
#         print('start_time: ', start_time)
        
        num_rows = sheet.nrows
        
        i = 100
        
        while i < num_rows-1:
            
            i = i+1
            
            v = sheet.cell_value(i, 0)
#             print('cell value: ', v)
            
            if 'End Time:' in v:
                
                v = sheet.cell_value(i, 1)
                end_time = datetime.datetime.strptime(v, '%m/%d/%Y %I:%M:%S %p' )
                end_time = end_time.strftime('%m/%d/%Y %I:%M:%S %p' )
#                 print('end_time: ', end_time)
                
                break
                
            
        
        if not end_time:
            
#             print("didn't find end time")
            return
    

        table = 'yeast_liquid_plates_spctrometersample_model'
        column_names = ['experiment_id', 'start_time', 'end_time']     
        values = [experiment_pk, start_time, end_time]
        
        created, sample_pk = self.manager.getOrCreate(table, column_names, values, 'id')
#         print('sample_pk: ', sample_pk, 'was created: ', created)
        
        
        index = self.pinCellInColumnStrats(sheet, 0, 'Well')
        i = index + 1
        
        while i < num_rows-1:  
             
            i = i+1
            
            e_row = sheet.row(i)

            raw_xy = e_row[0].value
            
            if not raw_xy == '': 
                
                if 'End Time:' in raw_xy:
                
#                     v = e_row[1].value
#                     end_time = datetime.datetime.strptime(v, '%m/%d/%Y %I:%M:%S %p' )
#                     print('')
#                     print('end_time: ', end_time)
                    break
                
                
                c = ord(raw_xy[1])  
                
                
                if c >= 65 and c <=122: #if the 2cnd char is a letter
                    c = raw_xy[0:1]
                    column = int(raw_xy[2:])
                else:
                    c = raw_xy[0]
                    column = int(raw_xy[1:])
                    
                row = getNumValue(c)
                
#                 print('row: ', row, ' col:', column, end = " ")
                
#             extract spectrometer reads

                j = 3
                
                opacity_samples_csv = ''
                
                while j < len(e_row) -1:
                    
                    v = e_row[j].value
                    
                    if not v=='':
                        
                        opacity_samples_csv = opacity_samples_csv + str(v) + ', '
                    
                    j = j+1
                
                opacity_samples_csv = opacity_samples_csv[0:-2]    
#                 print(' opacity_samples_csv: ', opacity_samples_csv, end = " ")  
                
                table = 'yeast_liquid_plates_spectrometerwelldata_model'
                column_names = ['sample_id', 'row', '"column"', 'opacity_samples_csv']  
                

                values = [sample_pk, row, column, opacity_samples_csv]
                
                created, well_pk = self.manager.getOrCreate(table, column_names, values, 'id')
#                 print('    well_pk: ', well_pk, 'was created: ', created, end = " ")
                
                
                     
             
#             print('')
            
        
            
        
    
    
    def getSheets(self, data_dir):

        excel_files = os.listdir(data_dir)
        
#         print('list of inner dirs: ', excel_files);
        
#         print('')
        
        
        sheets = []
        
        for f in excel_files:
            
            if f.endswith('.xls'):
                
                workbook = xlrd.open_workbook(os.path.join(data_dir, f))
                sheet_name = workbook.sheet_names()[0]
                sheet = workbook.sheet_by_name(sheet_name)
                sheets.append(sheet)
        
        return sheets
        
                    
    def pinCellInColumn(self, sheet, column, value):
     
        for i in range(len(sheet.col(column))):
            
            v = sheet.cell_value(i, column)
            
            if type(v) == type('string'):
            
                if value in v:
                    
#                     try:
#                         print(v)
#                     except Exception: 
#                     
#                         print('exception: ', sys.exc_info)
#                         traceback.print_exc()
                    
                    
                    return i
                
        return -1
                
    def pinCellInColumnStrats(self, sheet, column, value):
     
        for i in range(len(sheet.col(column))):
            
            v = sheet.cell_value(i, column)
            
            if v.startswith(value):
                
#                 print('caught')
                return i

#             try:
#                 print(v)
#             except Exception: 
#                 
#                 print('exception: ', sys.exc_info)
#                 traceback.print_exc()
            

def affiliateData(db_name, path, format_id):
    
    spectrometerReader = SpectrometerDataReader()
    spectrometerReader.getData(db_name, path, format_id)


 