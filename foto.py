#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Autore: Cristian Consonni <kikkocristian@gmail.com>
#
# The code is released with an MIT license
# please see the LICENSE file for details.

import os
import requests

TEXT_MALE = '''{nome} {cognome}, politico italiano'''

TEXT_FEMALE = '''{nome} {cognome}, politica italiana'''


if __name__ == '__main__':
    url = 'http://dati.camera.it/sparql?default-graph-uri=&query=SELECT+DISTINCT+%3Fpersona+%3Fcognome+%3Fnome+%0D%0A%3FdataNascita++%3Fnato+%3FluogoNascita+%3Fgenere+%3Ffoto%0D%0A++%0D%0AWHERE+{%0D%0A%3Fpersona+ocd%3Arif_mandatoCamera+%3Fmandato%3B+a+foaf%3APerson.%0D%0A%0D%0A%23%23+deputato%0D%0A%3Fd+a+ocd%3Adeputato%3B+ocd%3Aaderisce+%3Faderisce%3B%0D%0Aocd%3Arif_leg+%3Chttp%3A%2F%2Fdati.camera.it%2Focd%2Flegislatura.rdf%2Frepubblica_17%3E%3B%0D%0Aocd%3Arif_mandatoCamera+%3Fmandato.%0D%0A%0D%0A%23%23anagrafica%0D%0A%3Fd+foaf%3Asurname+%3Fcognome%3B+foaf%3Agender+%3Fgenere%3Bfoaf%3AfirstName+%3Fnome%3B+foaf%3Adepiction+%3Ffoto.%0D%0AOPTIONAL{%0D%0A%3Fpersona+%3Chttp%3A%2F%2Fpurl.org%2Fvocab%2Fbio%2F0.1%2FBirth%3E+%3Fnascita.%0D%0A%3Fnascita+%3Chttp%3A%2F%2Fpurl.org%2Fvocab%2Fbio%2F0.1%2Fdate%3E+%3FdataNascita%3B+%0D%0Ardfs%3Alabel+%3Fnato%3B+ocd%3Arif_luogo+%3FluogoNascitaUri.+%0D%0A%3FluogoNascitaUri+dc%3Atitle+%3FluogoNascita.+%0D%0A}%0D%0A%0D%0A}&format=text%2Fhtml&timeout=0&debug=on&format=json'
    res = requests.get(url)

    if res.ok:
        data = res.json()

    for person in data['results']['bindings']:
        identifier = person['persona']['value'].split('/')[-1]
        data_nascita = person['dataNascita']['value']
        nome = person['nome']['value']
        cognome = person['cognome']['value']
        foto_url = person['foto']['value']
        genere = person['genere']['value']

        print 'Processing {nome} {cognome} ...'.format(
            nome=nome,
            cognome=cognome), 'requesting: ', foto_url

        filename = nome + '_' + cognome + '_' + 'daticamera.jpg'
        filename = os.path.join('foto', filename)
        # with open(filename, 'wb') as handle:
        #     response = requests.get(foto_url, stream=True)

        #     if not response.ok:
        #         # Something went wrong
        #         continue

        #     for block in response.iter_content(1024):
        #         if not block:
        #             break

        #         handle.write(block)

        txt_filename = nome + '_' + cognome + '_' + 'daticamera.txt'
        txt_filename = os.path.join('testi', txt_filename)

        if genere == 'male':
            text = TEXT_MALE.format(nome=nome.title(), cognome=cognome.title())
        else:
            text = TEXT_FEMALE.format(nome=nome.title(), cognome=cognome.title())

        with open(txt_filename, 'w+') as output:
            output.write(text)

    exit(0)
