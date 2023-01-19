from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import connection_db as cdb


def start_driver(full_path):
    #directorio de drivechrome
    global driver 
    driver = webdriver.Chrome(executable_path=full_path)

def get_web(url_web):
    #web a investigar
    driver.get(url_web)

def login_web(user,password):
    #ingresando con las credenciales
    wait_time = WebDriverWait(driver, 10)
    try:        
        usuario_ele = wait_time.until(EC.presence_of_element_located((By.ID,'usuario')))
        password_ele = wait_time.until(EC.presence_of_element_located((By.ID,'password')))
        button = wait_time.until(EC.presence_of_element_located((By.ID,"ctl00_CPHColumnLeft_logon")))
        #usuario_ele = driver.find_element(By.ID,'usuario')        
        #password_ele = driver.find_element(By.ID,'password')        
        #button = driver.find_element(By.ID,"ctl00_CPHColumnLeft_logon")      
    except Exception as e:
        print("login_web_function => \n", e)

    usuario_ele.send_keys(user)
    password_ele.send_keys(password)    
    button.click()
    #time.sleep(5)

def enable_menu():
    #habilitando el menu q_audit
    wait_time = WebDriverWait(driver, 10)
    try:
        #menu = driver.find_element(By.ID,"subMenuFirst")
        menu = wait_time.until(EC.presence_of_element_located((By.ID,"subMenuFirst")))
        menu_action = ActionChains(driver)
        menu_action.double_click(menu).perform()
        #t
    except Exception as e: 
        print("enable_menu_function => \n", e)

def select_over_menu(name):
    tipos = {
        'seguimiento':'mnu_12',
        'hoja_de_ruta':'mnu_14'  
    }
    return tipos[name]

def select_option(name):
    #Ingresando a la hoja de seguimiento     
    try:
        wait_time = WebDriverWait(driver, 10)
        #hds = driver.find_element(By.ID,select_over_menu(name))
        hds = wait_time.until(EC.presence_of_element_located((By.ID,select_over_menu(name))))
        hds.click()
        #time.sleep(3)
    except Exception as e:
        print("select_option => \n",e)

def open_option(name_select):
    #solo hace minusculas todo para minimizar errores
    #escogiendo la opción (id de la opción) que queremos pasar de todas las opciones de menuto principal
    name_select = name_select.lower()
    select_option(name_select)

def hds_working_option(data,fecha_inicio):

    wait_time = WebDriverWait(driver, 10)
    try:        
        #seleccionar cliente por ocmnum data 
        btn_buscar_mandante = wait_time.until(EC.presence_of_element_located((By.ID,"ctl00_cph_btnFind")))
        btn_buscar_mandante.click()
        #time.sleep(3)
    except Exception as e:
        print("hds_working_option_btn_buscar => \n",e)    
    

    #MANEJANDO EL POP-UPS DE BUSQUEDA DE CLIENTES
    try:
        ventana_principal = driver.current_window_handle
        for ventana in driver.window_handles:
            if ventana != ventana_principal:
                ventana_pop = ventana
        driver.switch_to.window(ventana_pop)
        #time.sleep(3)
    except Exception as e:
        print("hds_working_option_pop-ups_buscar_mandante=> \n",e)


    #POP-UPS INGRESANDO DATOS
    try:
        #INGRESAMOS EL NOMBRE EN EL CAMPO DE NOMBREDELCLIENTE EN EL POP-UPS
        input_name_ele = wait_time.until(EC.presence_of_element_located((By.ID,"Uc_find_ol_proy1_txtOcmNum")))
        input_name_ele.send_keys(data)
        #REALISAMOZ LA BUSQUEDA del data
        #btn_buscar = driver.find_element(By.ID,"Uc_find_cliente1_btnBuscar")
        btn_buscar = wait_time.until(EC.presence_of_element_located((By.ID,"Uc_find_ol_proy1_Buscar")))
        btn_buscar.click()
        #time.sleep(5)
        #DE LOS RESULTADOS OBTENIDOS SELECCIONAMOS EL PRIMERO   

        table_clientes_first = wait_time.until(EC.presence_of_element_located((By.CSS_SELECTOR,".rowStyle > td:nth-child(1) > a:nth-child(1) ")))
        table_clientes_first.click()
    except Exception as e:
        print("hds_working_option_popups_buscar_mandante_fill => \n",e)


    #RECUPERANDO EL CONTROL DE LA PRIMERA VENTANA
    driver.switch_to.window(ventana_principal)
    #time.sleep(3)


    try:
        #COLOCAMOS LA FECHA DE INICIO (LA FECHA DE FIN NO ES NECESARIO)
        #fecha_inicio_ele = driver.find_element(By.ID,"ctl00_cph_txFecCreSegDel")
    #    fecha_inicio_ele = wait_time.until(EC.presence_of_element_located((By.ID,"ctl00_cph_txFecCreSegDel")))
    #    fecha_inicio_ele.send_keys(fecha_inicio)
        #time.sleep(3)

        #BTN GENERAR EL REPORTE SOLICITADO
        btn_generar = wait_time.until(EC.presence_of_element_located((By.ID,"ctl00_cph_btGenerar")))
        btn_generar.click()
    except Exception as e:
        print("hds_working_option_datos_fecha_and_general => \n",e)

    #time.sleep(40)

    #SE ABRE UN POP-UPS DESCARGA DE DATOS HDS
    try:
    #SELECCIONAR EL POP-UPS DE DESCARGA
        ventana_principal = driver.current_window_handle
        for ventana in driver.window_handles:
            if ventana != ventana_principal:
                ventana_download = ventana
        driver.switch_to.window(ventana_download)
    except Exception as e:        
        print("hds_working_option_datos_fecha_and_general => \n",e)


    #DESCARGANDO -POR AHROA NO ES NECESARIO VALIDAR EL RADIO BUTON ESTE EN EXCEL (porque se esta ahí por default)
    try:
        #validar que el número de paginas este cargado
        wait_time_download = WebDriverWait(driver,10)
        #esperemos que cargue los datos, por ejemplo el número de paginas que es importante //*[@id="ReportViewer1_ctl01_ctl01_ctl04"]
        btn_solo_datos = wait_time_download.until(EC.presence_of_element_located((By.XPATH,"//*[@id='ReportViewer1_ctl01_ctl01_ctl04']")))
        #initial = btn_solo_datos.text
        btn_solo_datos = wait_time.until(EC.presence_of_element_located((By.ID,"Button1"))) #driver.find_element(By.ID,"Button1")
        btn_solo_datos.click()
        time.sleep(4)  #obligatorio para validar que el archivo ya se ah descargado
    except Exception as a:
        print("hds_working_option_download_and_close => \n",e)

    #Cerramos el pop-up y regresmoa a la pagina principal 
    driver.close()    
    driver.switch_to.window(ventana_principal)

def hdr_working_option(ciades_mandante,fecha_inicio):
    wait_time = WebDriverWait(driver, 10)
    try: 
        #seleccionar cliente
        btn_buscar_mandante = wait_time.until(EC.presence_of_element_located((By.ID,"ctl00_cph_btnFind")))
        btn_buscar_mandante.click()
        #time.sleep(3)
    except Exception as e:
        print("hdr_working_option_btn_buscar => \n",e)    
    
    #MANEJANDO EL POP-UPS DE BUSQUEDA DE CLIENTES
    try:    
        #MANEJANDO EL POP-UPS DE BUSQUEDA DE CLIENTES
        ventana_principal = driver.current_window_handle
        for ventana in driver.window_handles:
            if ventana != ventana_principal:
                ventana_pop = ventana
        driver.switch_to.window(ventana_pop)
        #time.sleep(3)
    except Exception as e:
        print("hdr_working_option_pop-ups_buscar_mandante=> \n",e)
    
    #POP-UPS INGRESANDO DATOS
    try:    
        #INGRESAMOS EL NOMBRE EN EL CAMPO DE NOMBREDELCLIENTE EN EL POP-UPS
        input_name_ele = wait_time.until(EC.presence_of_element_located((By.ID,"Uc_find_ol_proy1_txtOcmNum")))
        input_name_ele.send_keys(ciades_mandante)
        #REALIzAMOs LA BUSQUEDA del ciades_mandante
        btn_buscar = wait_time.until(EC.presence_of_element_located((By.ID,"Uc_find_ol_proy1_Buscar")))
        btn_buscar.click()
        #time.sleep(3)
        #DE LOS RESULTADOS OBTENIDOS SELECCIONAMOS EL PRIMERO
        #.rowStyle > td:nth-child(1) > a:nth-child(1)
        table_clientes_first = wait_time.until(EC.presence_of_element_located((By.CSS_SELECTOR,".rowStyle > td:nth-child(1) > a:nth-child(1)")))
        table_clientes_first.click()
    except Exception as e:
        print("hdr_working_option_popups_buscar_mandante_fill => \n",e)

    #RECUPERANDO EL CONTROL DE LA PRIMERA VENTANA
    driver.switch_to.window(ventana_principal)
    #time.sleep(3)
    try:
        #COLOCAMOS LA FECHA DE INICIO (LA FECHA DE FIN NO ES NECESARIO) fecha de ingreso al proceso
    #    fecha_inicio_ele = wait_time.until(EC.presence_of_element_located((By.ID,"ctl00_cph_txFecIngProDel")))
    #    fecha_inicio_ele.send_keys(fecha_inicio)
        #time.sleep(3)
        #BTN GENERAR EL REPORTE SOLICITADO
        btn_generar = wait_time.until(EC.presence_of_element_located((By.ID,"ctl00_cph_btGenerar")))
        btn_generar.click()
    except Exception as e:
        print("hdr_working_option_datos_fecha_and_general => \n",e)


    #SE ABRE UN POP-UPS DESCARGA DE DATOS HDR
    try:
        #SELECCIONAR EL POP-UPS DE DESCARGA
        ventana_principal = driver.current_window_handle
        for ventana in driver.window_handles:
            if ventana != ventana_principal:
                ventana_download = ventana
        driver.switch_to.window(ventana_download)
    except Exception as e:        
        print("hdr_working_option_datos_fecha_and_general => \n",e)

    #DESCARGANDO -POR AHROA NO ES NECESARIO VALIDAR EL RADIO BUTON ESTE EN EXCEL (porque se esta ahí por default)
    try:
        #validar que el número de paginas este cargado
        wait_time_download = WebDriverWait(driver,10)
        #esperemos que cargue los datos, por ejemplo el número de paginas que es importante
        btn_solo_datos = wait_time_download.until(EC.presence_of_element_located((By.XPATH,"//*[@id='ReportViewer1_ctl01_ctl01_ctl04']")))
        
        btn_solo_datos = driver.find_element(By.ID,"Button1")
        btn_solo_datos.click()
        time.sleep(4)
    except Exception as a:
        print("hds_working_option_download_and_close => \n",e)
    #Cerramos el pop-up y regresmoa a la pagina principal 

    driver.close()
    driver.switch_to.window(ventana_principal)

def end_driver():
    #quit browser
    driver.quit()

def hds_exe(clients, opt_selected, fecha_inicio):
    #PARA LA HOJA DE SEGUIMIENTO
    open_option(opt_selected)    
    #EJECUTAMOS PARA TODOS LOS CLIENTES QUE CONCIDEREMOS
    for item in clients:
        hds_working_option(item,fecha_inicio)  #termina en la pantalla de ingreso de datos 

def hdr_exe(clients, opt_selected, fecha_inicio):
    open_option(opt_selected)
    for item in clients:
        hdr_working_option(item,fecha_inicio)

def datain(df_clientes,limit):
    if limit < 50:
        data = df_clientes['ocmnum'][0:limit].to_list()
        #ciacod = df_clientes['ciacod'][0:limit]
    else:
        data = df_clientes['ocmnum'].to_list()
        #ciacod = df_clientes['ciacod']

    #DATOS DE INICIO EN LA WEB
    data_dic = {'full_path':'C:\\Users\\edwin_paucar\\Documents\\Proyects_SGS\\driver_chrome\\chromedriver.exe',
        'url_web' :'https://qaudit.sgs.com/default.aspx',
        'user' : 'kcaballero',
        'password': 'Password2022!',
        'option_selected' : ['seguimiento','hoja_de_ruta'],
        'data':data,
        'fecha_inicio' : '01/01/2019'
        }
    return data_dic

def df_clientes():
    azure_dev = cdb.datain_db()
    db = cdb.create_engine_db(azure_dev['server'],azure_dev['database'],azure_dev['username'],azure_dev['password'])

    #sacar los datos por el nombre
    #data_ciente = pd.read_sql_query("""
    #    select  trim(ciacod) as ciacod, trim(ciades) as ciades
    #    from [sqldb-pe-sgsanalytics-dev].[HOM].[TbOrdenesComerciales]
    #    where isnull(ciades,'')<>''
    #    group by ciacod,ciades
    #""",db)
    #scar los datos por OL
    data_ciente = pd.read_sql_query("""
        select  distinct(ocmnum) as ocmnum  from hom.tbOrdenesComerciales
        where
        dotemicod = '70933'
        and ocmest <> 0
        and isnull(ocmnum,'') <> ''
        and ocmfehcre >= convert(date,dateadd(year,-3,getdate()))
    """,db)
    return data_ciente

def main():
    limit_cliente = 5
    #print(df_clientes())


    #datos iniciales
    #df_dataframe, son los datos, limit: si es mayor de 50 toma el valor, sino toma todo
    data_input = datain(df_clientes(),limit_cliente)
    start_driver(data_input['full_path'])
    print(data_input)
    get_web(data_input['url_web'])
    login_web(data_input['user'], data_input['password'])
    #hoja_de_seguimiento
    #enable_menu()
    #hds_exe(data_input['data'], data_input['option_selected'][0], data_input['fecha_inicio'])
    #hoja_de_ruta
    enable_menu()
    hdr_exe(data_input['data'], data_input['option_selected'][1], data_input['fecha_inicio'])

    end_driver()


if __name__ == "__main__":
    main()

