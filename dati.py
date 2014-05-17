#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Autore: Cristian Consonni <kikkocristian@gmail.com>
#
# The code is released with an MIT license
# please see the LICENSE file for details.

import requests
import pywikibot

site = pywikibot.Site('it', 'wikipedia')
site.login()
repo = site.data_repository()

WIKIDATA_PROPERTY = u'P58'

if __name__ == '__main__':
    url = 'http://dati.camera.it/sparql?default-graph-uri=&query=SELECT+DISTINCT+%3Fpersona+%3Fcognome+%3Fnome+%0D%0A%3FdataNascita++%3Fnato+%3FluogoNascita+%3Fgenere+%0D%0A%3Fcollegio+%3FnomeGruppo+%3Fsigla+%3Fcommissione+%3Faggiornamento++%0D%0AWHERE+%7B%0D%0A%3Fpersona+ocd%3Arif_mandatoCamera+%3Fmandato%3B+a+foaf%3APerson.%0D%0A%0D%0A%23%23+deputato%0D%0A%3Fd+a+ocd%3Adeputato%3B+ocd%3Aaderisce+%3Faderisce%3B%0D%0Aocd%3Arif_leg+%3Chttp%3A%2F%2Fdati.camera.it%2Focd%2Flegislatura.rdf%2Frepubblica_17%3E%3B%0D%0Aocd%3Arif_mandatoCamera+%3Fmandato.%0D%0A%0D%0A%23%23anagrafica%0D%0A%3Fd+foaf%3Asurname+%3Fcognome%3B+foaf%3Agender+%3Fgenere%3Bfoaf%3AfirstName+%3Fnome.%0D%0AOPTIONAL%7B%0D%0A%3Fpersona+%3Chttp%3A%2F%2Fpurl.org%2Fvocab%2Fbio%2F0.1%2FBirth%3E+%3Fnascita.%0D%0A%3Fnascita+%3Chttp%3A%2F%2Fpurl.org%2Fvocab%2Fbio%2F0.1%2Fdate%3E+%3FdataNascita%3B+%0D%0Ardfs%3Alabel+%3Fnato%3B+ocd%3Arif_luogo+%3FluogoNascitaUri.+%0D%0A%3FluogoNascitaUri+dc%3Atitle+%3FluogoNascita.+%0D%0A%7D%0D%0A%0D%0A%23%23aggiornamento+del+sistema%0D%0AOPTIONAL%7B%3Fd+%3Chttp%3A%2F%2Flod.xdams.org%2Fontologies%2Fods%2Fmodified%3E+%3Faggiornamento.%7D%0D%0A%0D%0A%23%23+mandato%0D%0A%3Fmandato+ocd%3Arif_elezione+%3Felezione.++%0D%0AMINUS%7B%3Fmandato+ocd%3AendDate+%3FfineMandato.%7D%0D%0A%0D%0A%23%23+elezione%0D%0A%3Felezione+dc%3Acoverage+%3Fcollegio.%0D%0A%0D%0A%23%23+adesione+a+gruppo%0D%0A%3Faderisce+ocd%3Arif_gruppoParlamentare+%3Fgruppo.%0D%0A%3Fgruppo+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2Falternative%3E+%3Fsigla%3B+%0D%0Adc%3Atitle+%3FnomeGruppo.%0D%0AMINUS%7B%3Faderisce+ocd%3AendDate+%3FfineAdesione%7D%0D%0A%0D%0A%23%23+organo%0D%0A%3Fd+ocd%3Amembro+%3Fmembro.%3Fmembro+ocd%3Arif_organo+%3Forgano.+%0D%0A%3Forgano+dc%3Atitle+%3Fcommissione+.%0D%0AMINUS%7B%3Fmembro+ocd%3AendDate+%3FfineMembership%7D%0D%0A%7D+&format=application%2Fsparql-results%2Bjson&timeout=0&debug=on'

    res = requests.get(url)

    if res.ok:
        data = res.json()

    for person in data['results']['bindings']:
        identifier = person['persona']['value'].split('/')[-1]
        data_nascita = person['dataNascita']['value']
        nome = person['nome']['value']
        cognome = person['cognome']['value']

        wikititle = '{nome} {cognome}'.format(
            nome=nome,
            cognome=cognome).title()

        page = pywikibot.Page(pywikibot.Link(wikititle, site))

        item = page.data_item()

        claim = pywikibot.Claim(repo, WIKIDATA_PROPERTY)
        claim.setTarget(identifier)
        item.addClaim(claim)

        import pdb
        pdb.set_trace()

        item.save()

    exit(0)
