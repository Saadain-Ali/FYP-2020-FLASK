import csv
import pandas

class students_editor:
    '''It contains all the csv file handlings'''
    def __init__(self,file_name,fieldnames):
        self.file_name = file_name
        self.fieldnames = fieldnames

    def print_file(self,index_col):
        '''index for student = sid , for finds student_1'''
        df = pandas.read_csv(self.file_name,index_col=index_col)
        print(df)

    def new_file(self,value):
        with open(self.file_name, 'a',newline='') as new_file:
            csv_writer = csv.DictWriter(new_file, fieldnames = self.fieldnames)
            csv_writer.writeheader()
            csv_writer.writerow(value)

    def append_file(self,value): #value = dictionary
        with open(self.file_name,'a',newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writerow(value)

    def delete_student(self,value,): #value = dictionary
        with open(self.file_name,'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writerow(value)


