import eredes.perfil_consumo
import eredes.perfil_perdas


print("Energy Data Analysis")

f_consumo = r'data/E-REDES_Perfil_Consumo_2023.xlsx'
f_perdas = r'data/E-REDES_Perfil_Perdas_2023.xlsx'



def main():
    print("main")

if __name__ == "__main__":
    main()
    pf = eredes.perfil_consumo.load_perfil(f_consumo)
    #pp = eredes.perfil_perdas.load_perfil_perdas(f_perdas)

    print(pf.info())
    #print(pf['btn_c'].count())

    #pf_slice = pf.loc['2023-03-26 23:00':'2023-03-27 02:00']
    pf_slice = pf.loc['2023-10-29 00:00':'2023-10-29 02:00']

    print(pf_slice)


