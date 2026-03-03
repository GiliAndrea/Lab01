import TriviaGame as tg

nuovoGioco = tg.TriviaGame("domande.txt", "punti.txt")
nuovoGioco.preparazioneDomande()
nuovoGioco.caricamentoPunteggi()
nuovoGioco.inizioGioco()