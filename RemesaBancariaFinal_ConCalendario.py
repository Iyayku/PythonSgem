# -*- coding: utf-8 -*-
from Tkinter import *
from ttk import Frame, Label, Entry, Style, Button
import tkMessageBox
import psycopg2, psycopg2.extras
import time
import CalendarioModif

class RemesaForm(Frame):
    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Ficha de remesa bancaria")
        self.style = Style()
        self.style.theme_use("clam")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lblCod = Label(frame1, text="Cod. Remesa", anchor="center").grid(row= 0, column=0)
        lblFecha = Label(frame1, text="Fecha creación", anchor="center").grid(row= 0, column=1)
        lblFechaCargo = Label(frame1, text="Fecha de cargo:", anchor="center").grid(row= 0, column=2)
        lblDescrip = Label(frame1, text="Descripción del contenido de la remesa", anchor="center").grid(row= 0, column=3)
        lblFichNom = Label(frame1, text="Nombre fichero", anchor="center").grid(row= 0, column=4)

        entr_codRem = Entry(frame1).grid(row=1, column=0)
        entr_fechCrea = Entry(frame1)
        entr_fechCrea.insert(END, time.strftime("%Y/%m/%d"))
        entr_fechCrea.grid(row=1, column=1)


        # entr_fechCargo = Entry(frame1).grid(row=1, column=2)

        entr_fechCargo2=  CalendarioModif.Datepicker(frame1).grid(row=1,column=2)

        entr_DescpCont = Entry(frame1, width=60).grid(row=1, column=3)
        entr_NomFich = Entry(frame1)
        entr_NomFich.insert(END, 'remesa')
        entr_NomFich.grid(row=1, column=4)

        lblCuentaBancaria = Label(frame1, text="Cuenta Bancaria", anchor="center").grid(row= 2, columnspan=4)
        lblNumRecibos = Label(frame1, text="Num.recibos", anchor="center").grid(row= 2, column=4)

        entr_CuentaBancaria = Entry(frame1,width=123)
        entr_CuentaBancaria.insert(END, '44445555917894561230')
        entr_CuentaBancaria.grid(row=3, columnspan=4)
        entr_NumRecibos = Entry(frame1)
        entr_NumRecibos.insert(END, '2')
        entr_NumRecibos.grid(row=3, column=4)

        lblVacia= Label(frame1, anchor="center").grid(row= 4, column=1)
        lblDatos= Label(frame1, text="DNI - Apellidos, Nombre-Cuenta Bancaria - Codigo del curso - Duracion - Coste", anchor="center").grid(row= 5, columnspan=4)

        lista = Listbox(frame1, width=145, selectmode="multiple")
        lista.grid(row=6, columnspan=5)

        frame1.pack(side=TOP,fill= X, padx=5, pady=5)


        frame1.update()
        print (frame1.winfo_geometry())

        # variable de conexión
        ccon = "host = 'localhost' dbname ='Masanz05' user = 'sgem' password = 'sgempwd'"
        # imprime la cadena de conexión
        print ("cadena de conexión: {}").format(ccon)
        objcon = psycopg2.connect(ccon)
        # ejecutar consultas a la base de datos
        objCursor = objcon.cursor()

        objcon.commit()
        # Obtener lista alumnos
        objCursor.execute("SELECT * FROM \"Alumnos\";")
        registros = objCursor.fetchall()
        for i in range(0, len(registros)):
            cadena = ""
            for j in range(0, len(registros[i])):
                cadena += str(registros[i][j]) + "-"
            lista.insert(i, cadena)

        # Lista de cuentas
        cursor = objcon.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT \"Cuenta Bancaria (Entidad, Oficina, DC, Cuenta)\" FROM \"Alumnos\";")

        row_count = 0
        cts = []
        for row in cursor:
            row_count += 1
            print "Cuenta: %s    %s\n" % (row_count, row[0])
            cts.append(row[0])

        print cts[0]
        print cts[1]
        print cts[2]
        print cts[3]

        cursor.close()
        objCursor.close()
        objcon.close()

        def valorCifras(cifras):
            LETRAS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            items = []
            for cifra in cifras:
                posicion = LETRAS.find(cifra)
                items.append(str(posicion) if posicion >= 0 else "-")
            return "".join(items)

        def modulo(cifras, divisor):
            CUENTA, resto, i = 13, 0, 0
            while i < len(cifras):
                dividendo = str(resto) + cifras[i: i + CUENTA]
                resto = int(dividendo) % divisor
                i += CUENTA
            return resto

        def cerosIzquierda(cifras, largo):
            cantidad = largo - len(cifras)
            ceros = "0" * cantidad
            return ceros + cifras

        def calcularIBAN(ccc, pais="es"):
            print ccc
            pais = pais.upper()
            cifras = ccc + valorCifras(pais) + "00"
            resto = modulo(cifras, 97)
            return pais + cerosIzquierda(str(98 - resto), 2)

        def creartxt():
            archi = open('remesa.txt')
            archi.close()

        def grabartxt():
            archi = open('remesa.txt', 'w')
            archi.write('ES' + str(entr_CuentaBancaria.get())[
                               8:10] + '001' + '    ' + '12345678A' + '    ' + 'Maria Ana Sanz' + '    ' + time.strftime(
                "%Y/%m/%d\n"))
            archi.write(
                'ES' + str(entr_CuentaBancaria.get())[8:10] + '001' + '    ' + '12345678A' + '    ' + 'Maria Ana Sanz\n')
            archi.write('ACAIXESBBXX\n')
            archi.write(calcularIBAN("44445555917894561230") + '44445555917894561230\n')
            archi.write(calcularIBAN(str(cts[1])) + str(cts[1]) + '\n')
            # archi.write('ES ' + '    ' + '44445555917894561230')
            archi.close()

        # creartxt()
        # grabartxt()

        frame2 = Frame(self)
        frame2.pack(fill=X)
        BtnAceptar = Button(frame2, text="Aceptar", command=grabartxt).pack(side=LEFT, padx=5, pady=5)
        BtnCancelar = Button(frame2, text="Cancelar").pack(side=LEFT, padx=5, pady=5)
        BtnBorrar = Button(frame2, text="Borrar").pack(side=LEFT, padx=5, pady=5)
        # BtnCapturarRecibos = Button(vent, text="Capturar recibos").grid(row= 6,columnspan=4)

def main():
    root = Tk()
    root.geometry("880x500+300+300")

    app = RemesaForm(root)

    root.mainloop()


if __name__ == '__main__':
    main()