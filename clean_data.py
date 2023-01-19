from typing import final
import pandas as pd
import re
import numpy as np
import connection_db as cdb

def type_estados():
    azure_dev = cdb.datain_db()
    db = cdb.create_engine_db(azure_dev['server'],azure_dev['database'],azure_dev['username'],azure_dev['password'])
    hds_estados = pd.read_sql_query("""
        select trim(id_maedet) as id_maedet, trim(maedetdes) as maedetdes, trim(maedetcod) as maedetcod  from HOM.TbEstados
        where maecabcod = 'INVEST'
    """,db)
    
    hdr_estados = pd.read_sql_query("""
        select trim(id_maedet) as id_maedet, trim(maedetdes) as maedetdes, trim(maedetcod) as maedetcod  from HOM.TbEstados
        where maecabcod like 'HOMEST'
    """,db)    
    return {'hds_estados':hds_estados,'hdr_estados':hdr_estados}


def limit_list():  #solo cogemos los datos que filtramos 
    azure_dev = cdb.datain_db()
    db = cdb.create_engine_db(azure_dev['server'],azure_dev['database'],azure_dev['username'],azure_dev['password'])
    
    list_ocmnum = pd.read_sql_query("""
        select ocmnum from hom.tbOrdenesComerciales
        where
        dotemicod = '70933'
        and ocmest <> 0
        and isnull(ocmnum,'') <> ''
        and ocmfehcre >= convert(date,dateadd(year,-3,getdate()))
    """,db)    
    return list_ocmnum


def dict_std2num(df_types):  #devuelve un diccionario entre (estado : numero de estado)
    maedetdes = df_types['maedetdes'].to_list()
    maedetcod = df_types['maedetcod'].to_list()
    dic = dict(zip(maedetdes,maedetcod))
    return dic

def dict_std2cod(df_types): #devuelve un diccionario entre (estado : código de estado)
    maedetdes = df_types['maedetdes'].to_list()    
    id_maedet = df_types['id_maedet'].to_list()
    dic = dict(zip(maedetdes,id_maedet))
    return dic

def clean_ruc(ruc):
    if ruc is None:
        data = '0'
    else:
        data = ruc.replace("'","")              
    return data

def state2num(estado,dict_std2num): ##cover to 002-HOMEST-XX    
    # 1000: NO TIENE DATO, 1001: ESTA EN BLANCO EL DATO, 1002:ES UN NUEVO ESTADO
    #dict_std2num = dict_hds_num
    if estado is None:
        data = 1000
    elif estado == "":
        data = 1001
    elif estado in dict_std2num:
        data = dict_std2num[estado]
    else:
        data = 1002        
    return data

def state2cod(estado,dict_std2cod):   #cover to 002-INVEST-XX
    # NO_DATA: NO TIENE DATO, BLANCO: ESTA EN BLANCO EL DATO, NEWESTADO:ES UN NUEVO ESTADO
    #dict_std2cod = dict_hds_cod
    if estado is None:
        data = 'NO_DATA'
    elif estado == "":
        data = 'BLANCO'
    elif estado in dict_std2cod:
        data = dict_std2cod[estado]
    else:
        data = 'NEWESTADO'
    return data

def clean_hds(path_load, path_download):
    #hoja de seguimiento
#    try:
    dict_hds_num = dict_std2num(type_estados()['hds_estados'])
    dict_hds_cod = dict_std2cod(type_estados()['hds_estados'])  
    df_hds = pd.read_excel(path_load,header=0)
    data_hds_copy = df_hds.copy()
    #anadiendo nuevos campos limpios
    data_hds_copy['NEW_ESTADO'] = data_hds_copy['Estado'].apply(state2num, args=(dict_hds_num ,))
    data_hds_copy['NEW_ESTADO_ID'] = data_hds_copy['Estado'].apply(state2cod, args=(dict_hds_cod ,))
    data_hds_copy['NEW_RUC'] = data_hds_copy['RUC'].apply(clean_ruc)
    #validando que ocmnum contamos
    lista_aptos = limit_list()['ocmnum'].to_list()  #no es necesario cambia a str
    final_data = data_hds_copy[data_hds_copy['Num_Proyecto'].isin(lista_aptos)]
    final_data.to_excel(path_download)
#    except Exception as e:
#        print("Clean_hds => ", e)

def clean_hdr(path_load, path_download):
    dict_hdr_num = dict_std2num(type_estados()['hdr_estados'])
    dict_hdr_cod = dict_std2cod(type_estados()['hdr_estados'])    
    df_hdr = pd.read_excel(path_load,header=0)
    data_hdr_copy = df_hdr.copy()
    #separando la columna proyecto
    data_ocmnum = data_hdr_copy['Proyecto'].str.split('-',expand=True)
    data_hdr_copy['Num_proyecto']  = data_ocmnum[0]
    data_hdr_copy['Num_oi']  = data_ocmnum[1]
    #limpieza adicional
    data_hdr_copy["NEW_RUC"] = data_hdr_copy["Ruc"].apply(clean_ruc)
    data_hdr_copy['NEW_ESTADO'] = data_hdr_copy['Estado'].apply(state2num, args=(dict_hdr_num ,))
    data_hdr_copy['NEW_ESTADO_ID'] = data_hdr_copy['Estado'].apply(state2cod, args=(dict_hdr_cod ,))
    #validamos que ocmnum contamos
    lista_aptos = [ str(x) for x in limit_list()['ocmnum'].to_list() ]  #es necesario cambiar el tipo de los datos en la lista a str
    final_data = data_hdr_copy[data_hdr_copy['Num_proyecto'].isin(lista_aptos)]
    final_data.to_excel(path_download)

def main():
    path_load_hds = "C:\\Users\\edwin_paucar\\Downloads\\final_data_today_hds.xls"
    path_download_hds = "C:\\Users\\edwin_paucar\\Downloads\\final_data_today_hds_clean.xlsx"
    path_load_hdr = "C:\\Users\\edwin_paucar\\Downloads\\final_data_today_hdr.xls"
    path_download_hdr = "C:\\Users\\edwin_paucar\\Downloads\\final_data_today_hdr_clean.xlsx"
    #hoja de seguimiento
    #dict_hds_num = dict_std2num(type_estados()['hds_estados'])
    #dict_hds_cod = dict_std2cod(type_estados()['hds_estados'])
    #hoja de ruta  type_estados()['hdr_estados']
    #dict_hdr_num = dict_std2num(type_estados()['hdr_estados'])
    #dict_hdr_cod = dict_std2cod(type_estados()['hdr_estados'])

    #print(type_estados()['hdr_estados'])

    #clean_hds(path_load_hds,path_download_hds)
    clean_hdr(path_load_hdr,path_download_hdr)

if __name__=='__main__':
    main()