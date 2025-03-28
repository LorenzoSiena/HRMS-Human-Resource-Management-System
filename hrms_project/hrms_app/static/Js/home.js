 // Funzione per generare l'orologio delle timbrature

function aggiornaOrologio() {
    let now = new Date();
    let giorno = now.getDate();
    let mese = now.toLocaleString("it-IT", { month: "long" });  // Nome del mese
    let anno = now.getFullYear();
    let ore = now.getHours().toString().padStart(2, '0');
    let minuti = now.getMinutes().toString().padStart(2, '0');
    let secondi = now.getSeconds().toString().padStart(2, '0');
    let data = `${giorno} ${mese} ${anno}`;
    let ora = `${ore}:${minuti}:${secondi}`;
    document.getElementById("ora").textContent = `${ora}`;
    document.getElementById("data").textContent = `${data}`;
}

setInterval(aggiornaOrologio, 1000); // Aggiorna ogni secondo
aggiornaOrologio(); // Imposta subito l'ora senza aspettare

function change_status() {
    let elemento = []

    elemento[0] = document.querySelector('label[for="id_ora_inizio"]') // Label ora inizio
    elemento[1] = document.getElementById("id_ora_inizio");  // Input ora inizio
    elemento[2] = document.querySelector('label[for="id_ora_fine"]'); // Label ora fine
    elemento[3] = document.getElementById("id_ora_fine"); // Input ora fine
    elemento[4] = document.querySelector('label[for="id_motivo"]'); // Label motivo
    elemento[5] = document.getElementById("id_motivo"); // Input motivo
    
    let attivo = document.querySelector('.tipo_richiesta input[type="radio"]:checked'); // Seleziona il radio button attivo

        // Se ho selezionato ferie nascondo gli elementi
        if (attivo.value == "ferie") {
            for (let i = 0; i < elemento.length; i++) {
                elemento[i].style.display = "none";
                elemento[i].required = false;
            }  
        // Se ho selezionato permesso mostro gli elementi              
        } else {
            for (let i = 0; i < elemento.length; i++) {
                elemento[i].style.display = "block";
                if (i < 4) {
                    elemento[i].required = true;
                }                    
            }
        }
}

change_status()