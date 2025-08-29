# Presentazione
 La presentazione che verrà discussa è `presentazione_progetto.slides.html`. Una versione originale, più estesa, è stata lasciata nel repository.

# Altri file riguardanti il progetto
Il notebook `analisi_corrispettivi_la_di_cjastelan.ipynb ` contiene uno scritto che documenta per esteso tutti i passaggi fatti nello studio del dataset, dall'importazione all'analisi. I risultati più interessanti sono poi confluiti nella presentazione.

Nel notebook `lista_correzioni_web_df.ipynb` ho registrato tutte le correzioni fatte nel dataset, per futura consultazione.

# Integrazione di 3 CFU
I file riguardanti la web-app sviluppata per l'integrazione sono quasi tutti nella cartella `app`. La cartella `instance` contiene il file di configurazione e conterrà il file SQLite dopo la prima esecuzione.
Per avviare l'app basta eseguire `flask run --debug` dalla root directory del repository. Occorrerà installare le dipendenze che *dovrebbero* essere: `flask`, `flask-sqlalchemy`, `sqlalchemy`.

La relazione che spiega in modo consuntivo cosa è stato sviluppato è nel file `relazione_integrazione.ipynb`.
