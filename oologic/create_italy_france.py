from oologic.match import Match
from oologic.team import Team
from oologic.person import Player, Coach, Referee

#this will be removed with a graphic interface

def createItaFra():
    buffon = Player("Buffon", 1, "P", "Gold")
    grosso = Player("Grosso", 3, "TS", "Azur")
    cannavaro = Player("Cannavaro", 5, "DC", "Azur")
    gattuso = Player("Gattuso", 8, "CC", "Azur")
    toni = Player("Toni", 9, "ATT", "Azur")
    totti = Player("Totti", 10, "AT", "Azur")
    camoranesi = Player("Camoranesi", 16, "ED", "Azur")
    zambrotta = Player("Zambrotta", 19, "TD", "Azur")
    perrotta = Player("Perrotta", 20, "ES", "Azur")
    pirlo = Player("Grosso", 21, "CC", "Azur")
    materazzi = Player("Materazzi", 23, "DC", "Azur")

    zaccardo = Player("Zaccardo", 2, "DC", "Azur")
    deRossi = Player("De Rossi", 4, "CC", "Azur")
    barzagli = Player("Barzagli", 6, "DC", "Azur")
    delPiero = Player("Del Piero", 7, "AT", "Azur")
    gilardino = Player("Gilardino", 11, "ATT", "Azur")
    peruzzi = Player("Peruzzi", 12, "P", "Gold")
    nesta = Player("Nesta", 13, "DC", "Azur")
    amelia = Player("Amelia", 14, "P", "Gold")
    iaquinta = Player("Iaquinta", 15, "ATT", "Azur")
    barone = Player("Barone", 17, "CC", "Azur")
    inzaghi = Player("Inzaghi", 18, "ATT", "Azur")
    oddo = Player("Oddo", 22, "TD", "Azur")

    lippi = Coach("Lippi", "CT")

    homeRooster = []
    homeBanch= []
    homeRooster.extend((buffon, grosso, cannavaro, gattuso, toni, totti, camoranesi,
                       zambrotta, perrotta, pirlo, materazzi))
    homeBanch.extend((zaccardo, deRossi, barzagli, delPiero, gilardino, peruzzi,
                     nesta, amelia, iaquinta, barone, inzaghi, oddo))
    homeTeam = Team("ITALIA", homeRooster, homeBanch, lippi)

    abidal = Player("Abidal", 3, "DS", "Wite")
    vieira = Player("Vieira", 4, "CC", "Wite")
    gallas = Player("Gallas", 5, "DC", "Wite")
    makelele = Player("Makélélé", 6, "CC", "Wite")
    malouda = Player("Malouda", 7, "AS", "Wite")
    zidane = Player("Zidane", 10, "COC", "Wite")
    henry = Player("Henry", 12, "ATT", "Wite")
    thuram = Player("Thuram", 15, "DC", "Wite")
    barthez = Player("Barthez", 16, "P", "Black")
    sagnol = Player("Sagnol", 19, "DD", "Wite")
    ribery = Player("Ribéry", 22, "AD", "Wite")

    landreau = Player("Landreau", 1, "P", "Black")
    boumsong = Player("Boumsong", 2, "DC", "Wite")
    dhorasoo = Player("Dhorasoo", 8, "CC", "Wite")
    govou = Player("Govou", 9, "AD", "Wite")
    wiltord = Player("Wiltord", 11, "AT", "Wite")
    silvestre = Player("Silvestre", 13, "DC", "Wite")
    saha = Player("Saha", 14, "ATT", "Wite")
    givet = Player("Givet", 17, "DC", "Wite")
    diarra = Player("Diarra", 18, "CDC", "Wite")
    trezeguet = Player("Trezeguet", 20, "ATT", "Wite")
    chimbonda = Player("Chimbonda", 21, "DC", "Wite")
    coupet = Player("Coupet", 23, "P", "Black")

    domenech = Coach("Domenech", "CT")

    guestRooster = []
    guestBanch = []
    guestRooster.extend((abidal, vieira, gallas, makelele, malouda, zidane, henry,
                        thuram, barthez, sagnol, ribery))
    guestBanch.extend((landreau, boumsong, dhorasoo, govou,wiltord, silvestre, saha,
                      givet, diarra, trezeguet, chimbonda, coupet))
    guestTeam = Team("FRANCIA", guestRooster, guestBanch, domenech)

    referee = Referee("Elizondo", "REF", "Red")

    eventList = []

    return Match(homeTeam, guestTeam, referee, eventList)
