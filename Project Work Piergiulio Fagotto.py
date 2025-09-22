

import random


# Funzione I: genera lotto dalla composizione casuale 

# Definisco il valore massimo di cui il lotto deve essere composto
def genera_lotto(max_articoli=700):
    # Definisco in maniera randomica a quanto deve ammontare il numero di articoli del lotto
    totale_lotto = random.randint(1, max_articoli)
    # Definisco in maniera randomica quali e quanti articoli appartengono al lotto
    maglie = random.randint(0, totale_lotto)
    rimanenti = totale_lotto - maglie
    pantaloni = random.randint(0, rimanenti)
    gonne = totale_lotto - maglie - pantaloni
    
    #Inizializzo un dizionario a cui passo le variabili create
    lotto = {"Maglie": maglie, "Pantaloni": pantaloni, "Gonne": gonne, "Totale": totale_lotto}
    return lotto

 
# Funzione II: genera parametri casuali

def genera_parametri():
    #Genero in maniera randomica quanti minuti impiega un determinato articolo ad essere prodotto
    tempo_unitario_gonne = random.randint(26, 32)
    tempo_unitario_pantaloni = random.randint(32, 40)
    tempo_unitario_maglie = random.randint(30, 34)

    # Calcolo la capacità giornaliera di ogni singolo articolo
    capacita_giornaliera_gonne = 480 // tempo_unitario_gonne
    capacita_giornaliera_pantaloni = 480 // tempo_unitario_pantaloni
    capacita_giornaliera_maglie = 480 // tempo_unitario_maglie

    # Capacità giornaliera totale che ammonta alla cifra più alta tra le capacità degli articoli
    capacita_giornaliera = max(
        capacita_giornaliera_gonne,
        capacita_giornaliera_pantaloni,
        capacita_giornaliera_maglie
    )
    
    #Inizializzo un ulteriore dizionario a  cui passo le variabili generate
    parametri = {
        "Gonne": {"tempo_unitario": tempo_unitario_gonne},
        "Pantaloni": {"tempo_unitario": tempo_unitario_pantaloni},
        "Maglie": {"tempo_unitario": tempo_unitario_maglie},
        "capacita_giornaliera": capacita_giornaliera,
        "capacita_giornaliera_gonne": capacita_giornaliera_gonne,
        "capacita_giornaliera_pantaloni": capacita_giornaliera_pantaloni,
        "capacita_giornaliera_maglie": capacita_giornaliera_maglie
    }
    return parametri


# Funzione III: Produce il lotto stabilito nella prima funzione, usando i parametri randomici 
#               generati nella seconda funzione

def produci_lotto(lotto):
    #Inizializza un ulteriore dizionario e vi collega i valori generati nella prima funzione.
    #In poche parole vi registra il numero di gonne pantaloni e maglie che appartengono al lotto 
    #che devono essere ancora prodotte
    
    rimanenti = {"Gonne": lotto["Gonne"], "Pantaloni": lotto["Pantaloni"], "Maglie": lotto["Maglie"]}
    
    #Inizializzo 2 variabili pari a 0 e una lista vuota
    giorni = 0
    tempo_totale = 0
    produzione_per_giorno = []
    
    #Inizzializzo il numero di minuti in una giornata di produzione
    MINUTI_GIORNO = 480  # 8 ore
    
    #Inizializzo il ciclo produttivo
    while sum(rimanenti.values()) > 0:
        giorni += 1
        minuti_rimanenti = MINUTI_GIORNO

        #Richiamo la funzione che genera i parametri dal dizionario "parametri"
        #per ogni giorno di produzione e li associo a delle nuove variabili
        parametri = genera_parametri()

       
        capacita_totale = parametri["capacita_giornaliera"]
        cap_gonne = parametri["capacita_giornaliera_gonne"]
        cap_pantaloni = parametri["capacita_giornaliera_pantaloni"]
        cap_maglie = parametri["capacita_giornaliera_maglie"]

        capacita_rimanente = capacita_totale
        
        #Inizializzo un nuovo dizinario che mi servirà per il reportage giornaliero
        produzione_oggi = {"Gonne": 0, "Pantaloni": 0, "Maglie": 0, "Totale": 0}
        tempo_giornata = 0

        # Inizio la produzione giornaliera degli articoli seguendo l'ordine gonna, pantalone, maglia
        for prodotto in ["Gonne", "Pantaloni", "Maglie"]:
            if rimanenti[prodotto] == 0:
                continue

            # Inizializzo la capacità massima giornaliera per ogni articolo
            if prodotto == "Gonne":
                cap_prodotto = cap_gonne
            elif prodotto == "Pantaloni":
                cap_prodotto = cap_pantaloni
            else:
                cap_prodotto = cap_maglie

            # Inizializza il numero massimo producibile oggi per questo articolo
            # nel momento in cui viene prodotto con i seguenti vincoli:
            # - articoli rimanenti da produrre
            # - capacità massima giornaliera per articolo
            # - capacità massima totale giornaliera residua
            # selezionando il minore
            max_producibili = min(
                rimanenti[prodotto],
                capacita_rimanente,
                cap_prodotto,
                minuti_rimanenti // parametri[prodotto]["tempo_unitario"]
            )
            

            #Finchè non finisco gli articoli da produrre continuo l'esecuzione del ciclo
            if max_producibili == 0:
                continue


            #Finita la giornata vengono aggiornati i dati del reportage giornaliero

            produzione_oggi[prodotto] = max_producibili
            produzione_oggi["Totale"] += max_producibili
            tempo_giornata += max_producibili * parametri[prodotto]["tempo_unitario"]

            # Aggiorno qunti articoli del Lotto rimangono da produrre
            rimanenti[prodotto] -= max_producibili
            capacita_rimanente -= max_producibili
            minuti_rimanenti -= max_producibili * parametri[prodotto]["tempo_unitario"]

            if capacita_rimanente == 0 or minuti_rimanenti <= 0:
                break
        
        
        #Registro i dati di produzione di un giorno all’interno della lista produzione per giorno
        #e aggiungo la voce che riguarda i tempi in minuti che sono stati generati dalla funzione
        #genera parametri durante questa giornata lavorativa
        produzione_per_giorno.append({
            "Giorno": giorni,
            "Produzione": produzione_oggi,
            "Tempo_giornata": tempo_giornata,
            "Capacita_oggi": capacita_totale,
            "Capacita_articolo": {
                "Gonne": cap_gonne,
                "Pantaloni": cap_pantaloni,
                "Maglie": cap_maglie
            },
            "Tempi_unitari": {p: parametri[p]["tempo_unitario"] for p in ["Gonne","Pantaloni","Maglie"]}
        })

        tempo_totale += tempo_giornata
    # 
    # restituisce:
    # il numero di giorni impiegati per produrre il lotto 
    # il tempo totale in minuti per produrre il lotto
    # il rapporto giornaliero 
    return {
        "Giorni_totali": giorni,
        "Tempo_totale": tempo_totale,
        "Produzione_per_giorno": produzione_per_giorno
    }


#Chiamo la prima funzione e genero il lotto
lotto = genera_lotto()

#Stampo i dati del lotto
print("=== Lotto generato ===")
print(f"Totale articoli: {lotto['Totale']}")
print(f"Gonne: {lotto['Gonne']}, Pantaloni: {lotto['Pantaloni']}, Maglie: {lotto['Maglie']}\n")

#Inizio la produzione
risultato = produci_lotto(lotto)

#Stampo il report di ogni giorno
print("=== Report giornaliero di produzione ===")
for giorno in risultato["Produzione_per_giorno"]:
    prod = giorno["Produzione"]
    cap_art = giorno["Capacita_articolo"]
    tempi = giorno["Tempi_unitari"]
    print(f"Giorno {giorno['Giorno']}:")
    print(f"  Capacità giornaliera totale: {giorno['Capacita_oggi']}")
    print(f"  Capacità per articolo: Gonne={cap_art['Gonne']}, Pantaloni={cap_art['Pantaloni']}, Maglie={cap_art['Maglie']}")
    print(f"  Tempi unitari (minuti): Gonne={tempi['Gonne']}, Pantaloni={tempi['Pantaloni']}, Maglie={tempi['Maglie']}")
    print(f"  Articoli prodotti: Gonne={prod['Gonne']}, Pantaloni={prod['Pantaloni']}, Maglie={prod['Maglie']}, Totale={prod['Totale']}")
    print(f"  Tempo giornata: {giorno['Tempo_giornata']:.2f} minuti\n")

# Stampo il report complessivo a fine produzione
print("=== Risultati complessivi ===")
print(f"Numero di giornate lavorative da 8 ore: {risultato['Giorni_totali']}")
print(f"Tempo totale di produzione: {risultato['Tempo_totale']:.2f} minuti, {giorno['Giorno']} giorni lavorativi")
print(f"Articoli totali prodotti: {lotto['Totale']} (Gonne={lotto['Gonne']}, Pantaloni={lotto['Pantaloni']}, Maglie={lotto['Maglie']})")
