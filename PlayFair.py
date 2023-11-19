from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import re

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def OsetriKlic(klic,czen):
    diakritika = {"Á":"A","Č":"C","É":"E","Ě":"E","Ď":"D","Í":"I","Ň":"N","Ó":"O","Ř":"R","Š":"S","Ť":"T","Ů":"U",
                  "Ú":"U","Ý":"Y","Ž":"Z","0":" NULA ","1":" JEDNA ","2":" DVA ","3":" TRI ","4":" CTYRI ","5":" PET ","6":" SEST ","7":" SEDM "
                  ,"8":" OSM ","9":" DEVET "}
    osetrenyKlic = ""
    klic1 = re.sub ('[!,*)@#%(&$_?.^]','',klic)
    klic1 = klic1.upper ()
    if czen == 1:
        validniAbeceda = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","X",
                          "Y","Z"]

    else:
        validniAbeceda = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X",
                          "Y","Z"]

    for i in klic1:

        if validniAbeceda.count (i) > 0:
            osetrenyKlic += i
        else:
            try:
                aaa = diakritika[i]
                osetrenyKlic += aaa
            except:
                pass
    return osetrenyKlic

def BKEY(klic):
    lookp_dict = {"NULA":"0","JEDNA":"1","DVA":"2","TRI":"3","CTYRI":"4","PET":"5","SEST":"6","SEDM":"7","OSM":"8","DEVET":"9"}
    temp = klic.split ()
    res = []
    for wrd in temp:
        res.append (lookp_dict.get (wrd,wrd))

    res = ' '.join (res)
    return res

class Playfair:

    def create_table(self, key):
        keytext = []
        row = []
        table = []
        for char in key.upper():
            if char not in keytext and char in alphabet:
                keytext.append(char)

        for char in alphabet:
            if char not in keytext:
                keytext.append(char)

        i = 1
        for char in keytext:
            row.append(char)
            if i % 5 == 0:
                table.append(row.copy())
                row.clear()
            i = i + 1
        return table

    def create_bitext(self, plaintext):

        if combobox1.get () == "CZ":
            plaintext = plaintext.upper().replace("Q", "K")
        elif combobox1.get () == "EN":
            plaintext = plaintext.upper().replace("J", "I")

        plaintext = plaintext.upper ()
        text = []
        bitext = []
        rep_char = ""
        for char in plaintext:
            if char in alphabet:
                text.append(char)

        for i in range(len(text)):
            if i % 2 == 0:
                rep_char = text[i]
                continue
            elif rep_char == text[i]:
                text.insert(i, 'X')

        if len(text) % 2 == 1:
            text.append('X')

        i = 0
        for j in range(int(len(text) / 2)):
            bitext.append(list(text[i] + text[i + 1]))
            i = i + 2

        return bitext

    def pf_encrypt(self, plaintext, key):
        cipher = ""
        bitext = self.create_bitext(plaintext)
        table = self.create_table(key)
        table_entry.insert(0,table)
        table_entry.configure (state='readonly')

        for bichar in bitext:
            colx = -1
            coly = -1
            rowx = -1
            rowy = -1
            for i in range(len(table)):
                if bichar[0] in table[i]:
                    colx = table[i].index(bichar[0])
                    rowx = i
                if bichar[1] in table[i]:
                    coly = table[i].index(bichar[1])
                    rowy = i

                if rowx != -1 and rowy != -1 and rowx == rowy:
                    if colx == 4:
                        colx = -1
                    if coly == 4:
                        coly = -1
                    cipher = cipher + table[rowx][colx + 1] + table[rowx][coly + 1]
                    break
                elif colx != -1 and coly != -1 and colx == coly:
                    if rowx == 4:
                        rowx = -1
                    if rowy == 4:
                        rowy = -1
                    cipher = cipher + table[rowx + 1][colx] + table[rowy + 1][coly]
                    break
                elif rowx != -1 and rowy != -1 and colx != -1 and coly != -1:
                    cipher = cipher + table[rowx][coly] + table[rowy][colx]
                    break
        return cipher

    def pf_decrypt(self, cipher, key):
        plaintext = ""
        bitext = self.create_bitext(cipher)
        table = self.create_table(key)

        for bichar in bitext:
            colx = -1
            coly = -1
            rowx = -1
            rowy = -1
            for i in range(len(table)):
                if bichar[0] in table[i]:
                    colx = table[i].index(bichar[0])
                    rowx = i
                if bichar[1] in table[i]:
                    coly = table[i].index(bichar[1])
                    rowy = i

                if rowx != -1 and rowy != -1 and rowx == rowy:
                    if colx == 0:
                        colx = 5
                    if coly == 0:
                        coly = 5
                    plaintext = plaintext + table[rowx][colx - 1] + table[rowx][coly - 1]
                    break
                elif colx != -1 and coly != -1 and colx == coly:
                    if rowx == 0:
                        rowx = 5
                    if rowy == 0:
                        rowy = 5
                    plaintext = plaintext + table[rowx - 1][colx] + table[rowy - 1][colx]
                    break
                elif rowx != -1 and rowy != -1 and colx != -1 and coly != -1:
                    plaintext = plaintext + table[rowx][coly] + table[rowy][colx]
                    break
        return plaintext


def cb_change(event):
    key_entry.delete(0, 'end')



pf = Playfair()
window = Tk()

window.title('Playfair šifra')
window.geometry("320x230")
Label(window, text='Jazyk').grid(row=0, column=0, padx=7, pady=5, sticky="w")
combobox1 = Combobox(window,
                     values=(
                         'CZ', 'EN'
                     ), state='readonly', width=10)
combobox1.grid(row=0, column=1, sticky="w", pady=5)
combobox1.set("CZ")
combobox1.bind('<<ComboboxSelected>>', cb_change)



Label(window, text='Klíč').grid(row=1, column=0, padx=7, pady=5, sticky="w")
key_text = StringVar()
key_entry = Entry(window, textvariable=key_text, width=13)
key_entry.grid(row=1, column=1, sticky="w")

first_label = Label(window, text='Text')
first_label.grid(row=2, column=0, padx=8, pady=5, columnspan=10, sticky="w")
before_text = StringVar()
before_entry = Entry(window, textvariable=before_text, width=24)
before_entry.grid(row=3, column=0, columnspan=2, padx=10, sticky="w")

second_label = Label(window, text='Zašifrovaný text')
second_label.grid(row=2, column=2, padx=0, pady=5, columnspan=2, sticky="w")
after_text = StringVar()
after_entry = Entry(window, textvariable=after_text, width=24)
after_entry.grid(row=3, column=2, columnspan=2, sticky="w")

table_label = Label(window, text='Abeceda')
table_label.grid(row=5, column=0, padx=7, pady=5, columnspan=2, sticky="w")
table_text = StringVar()
table_entry = Entry(window, textvariable=table_text, width=50)
table_entry.grid(row=6, column=0, columnspan=10, padx=10, sticky="w")

def onclick_encrypt():
        key = key_text.get ()

        if key.isalpha():
            if combobox1.get () == "CZ":
                key1 = OsetriKlic (key,1)
                after_text.set (pf.pf_encrypt(before_text.get(),key1))
                print(before_text.get())
                # print(key1)
            elif combobox1.get () == "EN":
                key1 = OsetriKlic (key,2)
                after_text.set (pf.pf_encrypt(OsetriKlic(before_text.get(),2),key1))
        else:
            messagebox.showerror('Error', 'Klíč musí obsahovat text a nemůže obsahovat čísla!')




def onclick_decrypt():
        key = key_text.get ()
        if key.isalpha():
            if combobox1.get () == "CZ":
                key1 = OsetriKlic (key,1)
                # print(key1)
            elif combobox1.get () == "EN":
                key1 = OsetriKlic (key,2)
            before_text.set(pf.pf_decrypt(BKEY(after_text.get()), key1))
        else:
            messagebox.showerror('Error', 'Klíč musí obsahovat text a nemůže obsahovat čísla!')


encrypt_button = Button(window, text='Zašifrovat', command=onclick_encrypt)
encrypt_button.grid(row=4, column=0, padx=10, pady=10, columnspan=2, sticky="w")
decrypt_button = Button(window, text='Odšifrovat', command=onclick_decrypt)
decrypt_button.grid(row=4, column=2, padx=0, pady=10, columnspan=2, sticky="w")

window.mainloop()
