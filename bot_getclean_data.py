import get_excel_download as ged
import join_many_excel as jme
import clean_data as cld

def start_on_qaudit(data_input):    
    ged.start_driver(data_input['full_path'])
    ged.get_web(data_input['url_web'])
    ged.login_web(data_input['user'], data_input['password'])

def exe_hds(data_input):
    start_on_qaudit(data_input)
    #hoja de swguimiento
    ged.enable_menu()
    ged.hds_exe(data_input['data'], data_input['option_selected'][0], data_input['fecha_inicio'])
    ged.end_driver()

def exe_hdr(data_input):
    start_on_qaudit(data_input)
    #hoja_de_ruta
    ged.enable_menu()
    ged.hdr_exe(data_input['data'], data_input['option_selected'][1], data_input['fecha_inicio'])
    ged.end_driver()

def main():
    path_load_hds = "C:\\Users\\edwin_paucar\\Downloads\\final_data_today_hds.xls"
    path_download_hds = "C:\\Users\\edwin_paucar\\Downloads\\final_data_today_hds_clean.xlsx"
    path_load_hdr = "C:\\Users\\edwin_paucar\\Downloads\\final_data_today_hdr.xls"
    path_download_hdr = "C:\\Users\\edwin_paucar\\Downloads\\final_data_today_hdr_clean.xlsx"
    limit_cliente = 70

    #df_dataframe, son los datos, limit: si es mayor de 50 toma el valor, sino toma todo
    data_input = ged.datain(ged.df_clientes(),limit_cliente)
    

    #OBTENER SEGUIMIENTO
    print('START DOWNLOAD EXCEL SEGUIMIENTO...')
    exe_hds(data_input)
    print('END DOWNLOAD EXCEL SEGUIMIENTO. ')
    print('START JOIN EXCEL SEGUIMIENTO... ')
    jme.join_excels(jme.list_excels_path(),"hds")
    jme.clean_directory()
    print('END JOIN EXCEL SEGUIMIENTO. ')
    
    #OBTENER HOJA DE RUTA
    print('START DOWNLOAD EXCEL HDR... ')
    exe_hdr(data_input)
    print('END DOWNLOAD EXCEL HDR. ')
    print('START JOIN EXCEL HDR... ')
    jme.join_excels(jme.list_excels_path(),"hdr")
    jme.clean_directory()
    print('END JOIN EXCEL HDR...')

    #LIMPIEZA DE LA DATA OBTENIDA HOJA DE RUTA Y HOJA DE SEGUIMIENTO
    cld.clean_hds(path_load_hds,path_download_hds)
    cld.clean_hdr(path_load_hdr,path_download_hdr)


if __name__=='__main__':
    main()