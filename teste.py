import bdballot

usuario = bdballot.Usuario.select()

for i in usuario:
    print(i.senha)

print(bdballot.Usuario.senha)
