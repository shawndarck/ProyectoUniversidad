
import solcx
 
# Ver las versiones disponibles de Solc
print(solcx.get_installable_solc_versions())
 
# Instalar una versión específica de Solc (por ejemplo, 0.8.7)
solcx.install_solc('0.8.7')
 
# Establecer la versión de Solc que deseas usar
solcx.set_solc_version('0.8.7')