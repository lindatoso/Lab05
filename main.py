import flet as ft
from flet import MainAxisAlignment
from flet.controls import alignment

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    titolo_strumenti = ft.Text(value="Aggiungi nuovo strumento", size=20) # Inserisco titolo come testo
    campo_tipo = ft.TextField(label="Tipo") # Tipo come text field vuoto, inserisco solo etichetta
    campo_marca = ft.TextField(label="Marca")
    campo_anno = ft.TextField(label="Anno")

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    def conferma_str(e): # definisco funzione per creare un oggetto strumento quando viene premuto il bottone
        tipo=campo_tipo.value # per tipo e marca prendo semplicemente i valori inseriti nel textfield
        marca=campo_marca.value
        try: # controllo formato anno e valore
            anno=int(campo_anno.value) # cerco di memorizzarli come interi
            valore=int(campo_valore.value)
            deposito.aggiungi_strumento(tipo, marca, anno, valore) # creo srumento richiamando metodo in deposito_strumenti
            aggiorna_lista_strumenti() # richiamo questa funzione per aggiungere lo strumento alla list view
            campo_tipo.value = "" # resetto i campi
            campo_marca.value = ""
            campo_anno.value = ""
            campo_valore.value = '0'

            page.update() # aggiorno la pagina

        except ValueError: # se non riesco a convertire i campi anno e valore in interi
            alert.show_alert("Il valore inserito non è corretto") # richiamo il metodo show_alert per lanciare messaggio di errore
            page.update() # aggiorno la pagina

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def handle_add(e): # definisco un handle per il bottone +
        valore = int(campo_valore.value) # prendo come valore ciò che c'è nel textfield campo_valore
        campo_valore.value = str(valore + 1) # aggiungo 1 e trasformo in stringa (textfield lavora con stringhe)
        campo_valore.update() # aggiorno il textfield campo_valore

    def handle_remove(e): # definisco un handle per il bottone -
        valore = int(campo_valore.value)
        campo_valore.value = str(valore - 1) # uguale al precedente ma sottraggo 1
        campo_valore.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    riga_tema=ft.Row(controls=[toggle_cambia_tema], alignment=MainAxisAlignment.START) # creo una riga per allineare il toggle cambio tema a sx
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    bottone_meno = ft.IconButton(icon=ft.Icons.REMOVE,
                                 icon_color="red",
                                 icon_size=24, on_click=handle_remove) # creo bottone - e richiamo funzione
    bottone_piu = ft.IconButton(icon=ft.Icons.ADD,
                                icon_color="green",
                                icon_size=24, on_click=handle_add) # creo bottone + e richiamo funzione
    campo_valore = ft.TextField(width=100, disabled=True, value='0', text_align=ft.TextAlign.CENTER) # creo textfield campo_valore

    riga_valore = ft.Row([bottone_meno, campo_valore, bottone_piu],
                         alignment=ft.MainAxisAlignment.CENTER) # creo una riga con bottone -, campo valore, bottone +

    # --- LAYOUT ---
    page.add(
        riga_tema, # aggiungo la riga con il toggle del tema

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        titolo_strumenti, # aggiungo titolo
        ft.Row(controls=[campo_tipo, campo_marca, campo_anno, riga_valore],
               alignment=MainAxisAlignment.CENTER), # aggiungo la riga con tutti i textfield
        ft.Button("Aggiungi strumento", on_click=conferma_str), # aggiungo bottone di conferma

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()
    page.update() # aggiorno la pagina

ft.run(main)
