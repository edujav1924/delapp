import datetime
def write(texto):
   f = open('misestados.log','a')
   f.write(texto+ " -- "+str(datetime.datetime.now())+"\n")
   f.close()
