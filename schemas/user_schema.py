def SchemaContact(contact)-> dict:
    return{
        "id":str(contact["_id"]),
        "nombre": contact["nombre"],
        "telefono":contact["telefono"],
        "correo":contact["correo"],
        "direccion":contact["direccion"]
    }

def SchemaContacts(contacts)->list:
    return [ SchemaContact(contact) for contact in contacts]



def SchemaUser(usuario)->dict:
    return{
        "id":str(usuario["_id"]),
        "nombre": usuario["nombre"],
        "correo":usuario["correo"],
        "contraseña":usuario["contraseña"],
        "url":usuario["url"]
    }
def SchemaUsers(users)->dict:
    return[SchemaUser(user) for user in users]

def SchemaMergeUser(merge)-> dict:
    return{
        "id":str(merge["_id"]),
        "usuario_merge":merge["usuario_merge"],
        "contacts":merge["contacts"]
    }

def schemasMerges(list_merge)->list:
    return [SchemaMergeUser(merge) for merge in list_merge]