import pandas as pd
from pandas import DataFrame
import csv

def overwrite_myheritage_on_FTDNA(template,FTDNA_file,out_name):

    headers = []
    autosomal = []
    xychromosome = []
    FTDNA = []

    # read MyHeritage template data
    with open(template, 'r') as fin1:
        reader = csv.reader(fin1)
        for row in reader:
            if row[0].startswith('#') or row[0]=='RSID':
                headers.append(row)
            elif row[1]=='X' or row[1]=='Y':
                xychromosome.append(row)
            else:
                autosomal.append(row)
    fin1.close()

    # read FTDNA data
    with open(FTDNA_file, 'r') as fin2:
        reader = csv.reader(fin2)
        for row in reader:
            if row[0]!='RSID':
                FTDNA.append(row)
    fin2.close()

    # overwrite MyHeritage
    myheritage_df = pd.DataFrame(autosomal)
    FTDNA_df = pd.DataFrame(FTDNA)
    dfdst = pd.merge(myheritage_df, FTDNA_df, on=[0,1,2],how='left')
    dfdst = dfdst.drop('3_x', axis=1)
    autosomal = dfdst.values.tolist()

    # save formatted FTDNA data
    with open(out_name, 'w') as fout:
        writer = csv.writer(fout, lineterminator='\n',delimiter=',',quotechar='"',quoting=csv.QUOTE_NONE)
        writer.writerows(headers)
        writer = csv.writer(fout, lineterminator='\n',delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
        writer.writerows(autosomal)
        writer.writerows(xychromosome)
    fout.close()

if __name__ == '__main__':

    overwrite_myheritage_on_FTDNA('MyHeritage_Templete.txt','Autosomal_o37_Results.csv','MyHeritageformattedFTDNAresult.txt')
