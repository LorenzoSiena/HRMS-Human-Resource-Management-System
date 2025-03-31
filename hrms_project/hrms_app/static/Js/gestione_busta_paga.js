// Funzione per caricare la busta paga
function carica_busta_paga(dipendente_id) {
    let modal = new bootstrap.Modal(document.getElementById('uploadPayslipModal'));
    modal.show();
    // Imposta l'ID del dipendente nel campo nascosto del form
    elemento_nascosto = document.getElementById('dipendente_id');
    elemento_nascosto.value = dipendente_id;
}

// Funzione per visualizzare le buste paga di un dipendente

function visualizza_busta_paga(dipendente_id) {
    let modal = new bootstrap.Modal(document.getElementById('viewPayslipsModal'));
    modal.show();
}