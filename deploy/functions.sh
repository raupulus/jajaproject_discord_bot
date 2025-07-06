#!/usr/bin/env bash

##
## Comprueba si existe una variable=valor en un archivo o la añade.
## La comprobación se hace: Comienza por el nombre de la variable hasta
## encontrar un "=", por ejemplo "mi_variable="
##
replace_or_add_var_in_file() {
    local FILE="${1}"
    local VAR="${2}"
    local VALUE_RAW="${3}"

    VALUE=$(echo ${VALUE_RAW} | sed 's/\//\\\//g')

    ## Almaceno la línea compuesta de variable=valor.
    local LINE="${VAR}=${VALUE}"

    local REGEXP="s/^.*${VAR}\s*=.*$/${LINE}/"

    echo "La línea completa quedará así: ${LINE}"
    echo "La expresión regular quedará así: ${REGEXP}"

    sed -r -i "${REGEXP}" "${FILE}"
}
