class TriviaGame:

    def __init__(self, fileDomande, filePlayer):
        self.fileDomande = fileDomande
        self.filePlayer = filePlayer
        self.listaDomande = []
        self.listaPlayerPunteggio = []
        self.dictDomande = {}

    def preparazioneDomande (self):
        with open(self.fileDomande, "r", encoding="utf-8") as file:
            contenuto = file.read()
            listaElementi = contenuto.split("\n")
            for i in range (0, len(listaElementi), 7):
                domandaNuova = Domanda(listaElementi[i], listaElementi[i + 1],
                                       [listaElementi[i+2], listaElementi[i+3], listaElementi[i+4],
                                        listaElementi[i+5]], listaElementi[i + 2])
                self.listaDomande.append(domandaNuova)

        self.dictDomande = self.preparazioneDomande1()

    def preparazioneDomande1(self):
        dictDomande = {}
        for d in self.listaDomande:
            if d.livello not in dictDomande.keys():
                dictDomande[d.livello] = []
                dictDomande[d.livello].append(d)
            if d.livello in dictDomande.keys():
                dictDomande[d.livello].append(d)
        return dictDomande

    def presentazioneDomanda(self, livello):
        import random
        n = random.randint(0,len(self.dictDomande[livello])-1)
        return self.dictDomande[livello][n]

    def caricamentoPunteggi(self):
        listaGiocatori = []
        with open(self.filePlayer, "r", encoding="utf-8") as file:
            for r in file:
                r.strip()
                info = r.split(" ")
                nuovoGiocatore = Player(info[0], int(info[1]))
                listaGiocatori.append(nuovoGiocatore)
        self.listaPlayerPunteggio = listaGiocatori

    def aggiornaPunteggi(self, nickname, punteggio):
        nuovoGiocatore = Player(nickname, punteggio)
        self.listaPlayerPunteggio.append(nuovoGiocatore)

    def rilasciaPunteggio(self):
        self.listaPlayerPunteggio.sort(reverse = True)
        with open(self.filePlayer, "w", encoding="utf-8") as file:
            for p in self.listaPlayerPunteggio:
                file.write(f"{p.nickname} {p.punteggio}\n")

    def inizioGioco(self):
        punteggio = 0
        livello = 0
        domanda = self.presentazioneDomanda(f"{livello}")
        domanda.dichiararsi()
        risposta = input(" Inserisci la tua risposta: ")
        while domanda.risposte[int(risposta) - 1] == domanda.rGiusta:
            punteggio = punteggio + 1
            print(" Risposta corretta!\n")
            livello = livello + 1
            domanda = self.presentazioneDomanda(f"{livello}")
            domanda.dichiararsi()
            risposta = input(" Inserisci la tua risposta: ")
        print(f" Risposta sbagliata! La risposta corretta era: {domanda.indiceRGiusta()}\n")
        print(f"Hai totalizzato {punteggio} punti!")
        nickname = input("Inserisci il tuo nickname: ")
        self.aggiornaPunteggi(nickname, punteggio)
        self.rilasciaPunteggio()


class Domanda:

    def __init__(self, domanda, livello, risposte, rGiusta):
        self.domanda = domanda
        self.livello = livello
        self.risposte = risposte
        self.rGiusta = rGiusta

    def preparazioneRisposte (self):
        import random
        random.shuffle(self.risposte)
        risultato = ""
        for i in range(0, len(self.risposte)):
            risultato = risultato + "\n         " + f"{i+1}. {self.risposte[i]}"
            i = i + 1
        risultato = risultato.replace("\n", "", 1)
        return risultato

    def dichiararsi (self):
        print(f" Livello {self.livello}) {self.domanda}\n{self.preparazioneRisposte()}")

    def indiceRGiusta(self):
        for i in range(0, len(self.risposte)):
            if self.rGiusta == self.risposte[i]:
                return i + 1


class Player:

    def __init__(self, nickname, punteggio):
        self.nickname = nickname
        self.punteggio = punteggio

    def __lt__(self, other: "Player"):
        return self.punteggio < other.punteggio


def esecuzioneTest():
     nuovoGioco = TriviaGame("domande.txt", "punti.txt")
     nuovoGioco.preparazioneDomande()
     nuovoGioco.listaDomande[0].dichiararsi()


if __name__ == "__main__":
    esecuzioneTest()