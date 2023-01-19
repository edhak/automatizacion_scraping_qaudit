import pandas as pd
from datetime import date 
import os
import re


def log_join(actual_df, final_df,join_df, actual_path, final_path,tipo):
    col_count = "Num_Proyecto" if tipo == "hds" else "Proyecto"
    print("CONCAT: ")
    print("\t INFO: path dataset actual: {}".format(actual_path))
    print("\t INFO: path dataset final: {}".format(final_path))
    print("\t size_actual: {}   size_final: {}, size_join: {}".format(actual_df[col_count].count(), 
                                                final_df[col_count].count(),
                                                join_df[col_count].count()
                                                )
                                            )

def list_excels_path():
    patrona = re.compile("^Datos")
    base_ruta = "C:\\Users\\edwin_paucar\\Downloads" 
    archivos = os.listdir(base_ruta)
    list_datos = []
    for file in archivos:
        if patrona.search(file):            
            list_datos.append(file)
    return list_datos

def clean_directory():
    #liminamos los archivos que comiencen con Datos
    patrona = re.compile("^Datos")
    base_ruta = "C:\\Users\\edwin_paucar\\Downloads" 
    archivos = os.listdir(base_ruta)
    
    for file in archivos:
        if patrona.search(file):            
            os.remove(base_ruta + '\\'+file)

def join_excels(list_excels_path, tipo):
    base_ruta = "C:\\Users\\edwin_paucar\\Downloads\\"
    final_path = f"C:\\Users\\edwin_paucar\\Downloads\\final_data_today_{tipo}.xls"

    #la ruta final inicial es C:\\Users\\edhak\\Downloads\\Datos.xls  (tener en cuenta que read_html devuelve una lista)
    initial_path = base_ruta + list_excels_path[0]
    df_final = pd.read_html(initial_path,header=0)[0]
    number_files = len(list_excels_path)

    for i in range(1,number_files):
        #generamos el nombre del archivo
        #muleta = "" if i==0 else " ("+ str(i)+")"
        #file_path = base_ruta.format(muleta)
        file_path = base_ruta + list_excels_path[i]
        #concatenamos el file 1 con los demás
        df_temp = pd.read_html(file_path,header=0)[0]  #dataset actual
        df_join = pd.concat([df_final,df_temp])     #dataset unido el final con el actual(df_temp)
        df_join.to_excel(final_path,index=False)
        log_join(df_temp,df_final,df_join,file_path,final_path,tipo)
        df_final = pd.read_excel(final_path)

def main():
    print(f"la candidad total es {len(list_excels_path())}")
    #los tipos son "hdr","hds"
    #print(list_excels_path())
    print(f"primer elemento:{list_excels_path()[0].strip()}")
    print("primer elemento:", len(list_excels_path()[0]))
    hh = "verde" if "Datos.xls" in list_excels_path() else "rojo"
    print(hh)
    join_excels(list_excels_path(),"hdr")
    #clean_directory()

if __name__=="__main__":
    main()