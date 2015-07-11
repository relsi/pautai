# -*- coding: utf-8 -*-

#########################################################################
# funções utlitárias
#########################################################################

def limita_texto(s, l):
    return s if len(s)<=l else s[0:l-3]+' [...]'

def data_extenso(data):
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    ano, mes, dia = data.split("-")
    return '%02d de %s de %d' %(int(dia),meses[int(mes)-1],int(ano))
