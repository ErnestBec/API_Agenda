def SchemaPermiso(permiso):
    return {
        "id":str(permiso["_id"]),
        "user_solicita":permiso["user_solicita"],
        "lectura":permiso["lectura"],
        "escritura":permiso["escritura"],
        "merge":permiso["merge"],
        "status":permiso["status"]
    }

def SchemaPermisos(lis_permisos):
    return[SchemaPermiso(permiso) for permiso in lis_permisos]