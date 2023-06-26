from sdv.datasets.local import load_csvs
from sdv.metadata import SingleTableMetadata
import datetime
import pandas as pd
import uuid
import os
from sdv.lite import SingleTablePreset
from sdv.evaluation.single_table import evaluate_quality
from sdv.evaluation.single_table import get_column_plot
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.evaluation.single_table import get_column_pair_plot

class singleSDVbuilder:
    def __init__(self, folder_name, table_name, num_rows=500):
        self.datasets = load_csvs(folder_name) #type: dict
        ##change the "weekly" to any other, e.g. happy.csv then switch weekly to happy
        self.single_table = self.datasets[table_name]
        self.metadata = SingleTableMetadata()
        self.metadata.detect_from_dataframe(data=self.single_table)
        self.num_rows = num_rows #num_rows to synthesize
        self.synthetic_data = None
    
    def single_table_keys(self):
        return self.single_table.keys()
    
    def detect_datetime_format(date_string):
        formats = [
            "%Y-%m-%d",  
            "%Y/%m/%d",  
            "%d %b %Y",  
            "%d-%b-%Y",  
            "%d/%b/%Y"
        ]

        for fmt in formats:
            try:
                datetime.datetime.strptime(date_string, fmt)
                return fmt
            except ValueError:
                continue

        return None 
    
    def metadata_update(self):
        ## update specified metadata
        for i in self.single_table.columns:
            if "date" in i.lower():
                datetime_format = self.detect_datetime_format(self.single_table[i][0])
                print(datetime_format)
                self.metadata.update_column(
                    column_name=i,
                    sdtype='datetime',
                    datetime_format=datetime_format
                )

        for i in self.single_table.columns:
            if "email" in i.lower():
                    self.metadata.update_column(
                    column_name="email",
                    sdtype="email",
                    pii=True
                )

        for i in self.single_table.columns:
            if "address" in i.lower():
                self.metadata.update_column(
                column_name="address",
                sdtype="address",
                pii=True
                )

        for i in self.single_table.columns:
            if "card" in i.lower():
                self.metadata.update_column(
                column_name="card",
                sdtype="card",
                pii=True
                )
                
        ## check primary key
    def check_unique_columns(df):
        unique_columns = []
        for column in df.columns:
            if df[column].nunique() == df.shape[0]:
                unique_columns.append(column)
        return unique_columns

    def create_unique_column(df):
        new_column_name = str(uuid.uuid4())  
        df[new_column_name] = None  
        return df
    
    def check_unique_column(self):
        unique_columns = self.check_unique_columns(self.single_table)

        if len(unique_columns) == 0:
            self.single_table = self.create_unique_column(self.single_table)
            self.metadata.set_primary_key(
            column_name=self.single_table.columns[-1]
        )
        else:
            self.single_table.columns[-1]
            
    def metadata_json(self):
        if os.path.exists('metadata.json'):
            os.remove('metadata.json')
        self.metadata.save_to_json('metadata.json')
        self.metadata = SingleTableMetadata.load_from_json('metadata.json')
        
        
    def synthesize_data(self, method):
        '''
        method:['FAST_ML', 'GaussianCopula']
        '''
        if method == 'FAST_ML':
            self.synthesizer = SingleTablePreset(self.metadata, name='FAST_ML')
        elif method == 'GaussianCopula':
            self.synthesizer = GaussianCopulaSynthesizer(self.metadata)
        self.synthesizer.fit(data=self.single_table)
        self.synthetic_data = self.synthesizer.sample(self.num_rows)
        self.synthesizer.save('my_synthesizer.pkl')
        print(self.synthetic_data)
        
    def quality_report(self):
        self.quality_report = evaluate_quality(
            self.single_table,
            self.synthetic_data,
            self.metadata)
        
    def get_column_plots(self):
        for i in self.single_table.columns:
            print(f"This is the synthetic evaluation for attribute:{i}")
            fig = get_column_plot(
                real_data=self.single_table,
                synthetic_data=self.synthetic_data,
                column_name=i,
                metadata=self.metadata
            )

            fig.show()
    
    def get_column_pair_plot(self):
        fig = get_column_pair_plot(
            real_data=self.single_table,
            synthetic_data=self.synthetic_data,
            column_names=self.single_table.columns,
            metadata=self.metadata
        )

        fig.show()
        
        
    def loadGaussianCopula(self, method):
        if method == 'GaussianCopula':
            self.synthesizer = GaussianCopulaSynthesizer.load('my_synthesizer.pkl')

if __name__ =="__main__":
    print("hello")
    folder_name = 'data/'
    table_name = 'test2'
    sdv = singleSDVbuilder(folder_name, table_name)
    print(sdv)
    print("-------------------------sdv.single_table-----------------------------")
    print(sdv.single_table)
    print("-------------------------sdv.metadata-----------------------------")
    print(sdv.metadata)
    print("-------------------------synthetic data-----------------------------")
    sdv.synthesize_data('GaussianCopula')
    print(sdv.synthetic_data)




import csv
from faker import Faker

# 创建 Faker 实例
faker = Faker()

# 读取原始 CSV 文件
with open('test.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

# 添加新列的标题
header = rows[0]
header.extend(['Email', 'Credit Card', 'Phone', 'Address'])

# 生成并添加随机数据
for row in rows[1:]:
    email = faker.email()
    credit_card = faker.credit_card_number()
    phone = faker.numerify(text='#######')
    address = faker.address()

    row.extend([email, credit_card, phone, address])

# 写入带有新列的 CSV 文件
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

