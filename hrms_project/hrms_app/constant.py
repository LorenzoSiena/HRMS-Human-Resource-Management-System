PERMESSI_APP = {

    'gestione_dipendenti' : frozenset(['view_dipendenti', 'add_dipendenti', 'change_dipendenti', 'delete_dipendenti']),
    'gestione_ruoli' : frozenset(['view_ruoli', 'add_ruoli', 'change_ruoli', 'delete_ruoli']),
    'gestione_autorizzazioni' : frozenset(['view_permission', 'add_permission', 'change_permission', 'delete_permission']),
    'gestione_ferie' : frozenset(['view_ferie','change_ferie']),
    'gestione_permessi' : frozenset(['view_permessi','change_permessi']),
    'visualizza_report' : frozenset(['view_reportpermessi', 'view_reportpresenze', 'view_reportferie']),
    'gestione_messaggi_bacheca' : frozenset(['add_bacheca', 'change_bacheca', 'delete_bacheca']),
    'gestione_bustepaga' : frozenset(['view_bustepaga', 'add_bustepaga', 'change_bustepaga', 'delete_bustepaga']),
    'gestione_documenti' : frozenset(['view_certificati', 'add_certificati', 'change_certificati', 'delete_certificati'])

}