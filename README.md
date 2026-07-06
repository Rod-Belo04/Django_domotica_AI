# Dashboard Domotica con Integrazione AI

Questo progetto consiste in una web app Django pensata per monitorare e controllare un piccolo sistema di domotica. L'app raccoglie dati da dispositivi/sensori, li salva in un database e li presenta in una dashboard web. Include inoltre una prima integrazione con OpenAI per permettere all'utente di interagire con il sistema tramite richieste in linguaggio naturale.


## Funzionalita principali

- Dashboard web per visualizzare dati di temperatura, consumo energetico e irrigazione.
- Endpoint POST per ricevere dati da microcontrollori o sensori esterni.
- Salvataggio dei dati in database tramite modelli Django.
- Elaborazione dei dati lato backend prima della visualizzazione nella pagina.
- Interfaccia responsiva utilizzabile anche da smartphone.
- Controllo tapparelle tramite slider con invio del valore da 0 a 100.
- Sezione "chiedi all' AI" per inviare richieste testuali a un modello OpenAI.
- Meccanismo di tool calling per collegare le risposte del modello a funzioni Python reali.

## Tecnologie utilizzate

### Django

Il progetto utilizza Django come framework principale. Django gestisce il routing, le view, i template HTML e l'accesso al database. La struttura e organizzata in una app `dash`, che contiene modelli, view, template e funzioni di supporto.

### Django ORM

I dati dei sensori sono rappresentati tramite modelli Django:

- `Thermo`, per le letture di temperatura.
- `ConsumoElettrico`, per i dati di consumo energetico.
- `Irrigazione`, per lo stato o la data relativa all'irrigazione.

L'ORM permette di inserire, leggere e filtrare dati senza scrivere SQL manuale, mantenendo il codice piu leggibile e vicino alla logica applicativa.


### HTTP e microcontrollori

Il progetto e pensato per comunicare con dispositivi esterni tramite richieste HTTP. I microcontrollori possono inviare dati alla web app con richieste POST, mentre alcune funzioni Python possono inviare comandi ai dispositivi, ad esempio per modificare la posizione delle tapparelle o avviare l'irrigazione.

## Integrazione AI

Una parte importante del progetto e l'integrazione con OpenAI. La dashboard include una sezione "chiedi all'AI" in cui l'utente puo scrivere una richiesta in linguaggio naturale.

Il flusso previsto e:

1. L'utente scrive una richiesta nella dashboard.
2. La richiesta viene inviata alla view Django dedicata.
3. La view chiama il modello OpenAI tramite API.
4. Il modello può rispondere direttamente oppure richiedere l'esecuzione di una funzione.
5. Django intercetta la chiamata funzione e invoca il tool Python corrispondente.
6. Il risultato viene mostrato nuovamente nella dashboard.

Questo approccio rende possibile collegare comandi in linguaggio naturale a funzioni applicative reali. Per esempio, l'utente puo chiedere di controllare le tapparelle, leggere l'ultima temperatura o ottenere informazioni sui consumi.

## Tool calling

Il progetto definisce una lista di tool che descrive al modello quali azioni puo richiedere. Ogni tool ha:

- un nome;
- una descrizione del suo comportamento;
- uno schema dei parametri;
- una funzione Python corrispondente.

Le funzioni disponibili includono:

- cambio posizione tapparelle;
- avvio irrigazione;
- lettura dell'ultima temperatura;
- lettura dell'ultima irrigazione;
- lettura dell'ultimo consumo elettrico.

Il modello interpreta la richiesta dell'utente, mentre il backend Django mantiene il controllo sulle azioni effettivamente eseguite.


## Note importanti

- Il progetto richiede una chiave API OpenAI. L'utente deve configurare la propria chiave, ad esempio tramite variabile d'ambiente `OPENAI_API_KEY`.
- Gli indirizzi IP dei microcontrollori devono essere configurati dall'utente. Nel codice, i precedenti indirizzi hardcoded sono stati sostituiti con la stringa `rimpiazza_con_tuo_ip`.
- Per permettere alla pagina di renderizzare correttamente i dati della dashboard, il database deve contenere almeno una entry per ognuna delle tre tabelle principali: temperatura, consumo elettrico e irrigazione.
