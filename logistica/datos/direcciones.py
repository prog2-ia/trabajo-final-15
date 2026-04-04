# ==========================================================
# DIRECCIONES LOGÍSTICAS (LIMPIAS Y SIN DUPLICADOS)
# ==========================================================

def limpiar_direcciones(lista):
    """
    - Elimina duplicados
    - Normaliza espacios
    - Devuelve lista limpia
    """
    limpias = set()

    for d in lista:
        d = d.strip()
        d = " ".join(d.split())  # elimina espacios dobles
        limpias.add(d)

    return sorted(limpias)


# ----------------------------------------------------------
# CENTRAL
# ----------------------------------------------------------

direcciones_central_txt = [
    "Ctra. Villaverde a Vallecas, 257, Madrid, España"
]


# ----------------------------------------------------------
# BASES
# ----------------------------------------------------------
direcciones_base_txt = limpiar_direcciones([
    # Madrid
    "Calle Industrias 14, Alcorcón, España",

    # Barcelona
    "Calle Joaquim Molins, 5, 08028 Barcelona",

    # Valencia
    "Avenida Espioca, 84, Silla, Valencia, España",

    # Alicante
    "Av. Euro 9, Alicante, España",

    # Murcia
    "Polígono Industrial Oeste, Calle Venezuela, 30820 Alcantarilla, Murcia",

    # Albacete
    "Calle Varsovia, 6, Polígono Industrial Romica, 02007 Albacete",

    # Toledo
    "Ctra. Toledo-Ocaña, s/n, Polígono Industrial Santa María de Benquerencia, 45007 Toledo"

])


# ----------------------------------------------------------
# DESPACHOS
# ----------------------------------------------------------
direcciones_despacho_txt = limpiar_direcciones([
    # Madrid
    "Calle Resina 39, Madrid, España",
    "Calle Jazmín, 34, 28033 Madrid",
    "Gran Via 1, Madrid, España",
    "Calle Río Almanzora, 4, 28906 Getafe, Madrid",
    "Calle Carpinteros 7, Getafe, España",
    "Calle Casas de Miravete, 30, Villa de Vallecas, 28031 Madrid",
    "Polígono Industrial Urtinsa, Calle Laguna, 28923 Alcorcón, Madrid",
    "Polígono Industrial Cobo Calleja, Calle Manuel Cobo Calleja, 28947 Fuenlabrada, Madrid",
    "Calle Sierra de Albarracín, 2, 28946 Fuenlabrada, Madrid",
    "Calle Constitución 5, Fuenlabrada, España",

    # Barcelona
    "C/ Mar Roja, 51, 08040 Barcelona",
    "Paseo de la Zona Franca, 73, 08038 Barcelona",
    "Avenida Josep Tarradellas, 8, 08029 Barcelona",
    "Muntaner, 200, 08036 Barcelona",
    "Paseo Peira, 23, 08031 Barcelona",
    "Calle Tuset, 23, 08006 Barcelona",
    "Calle Mallorca, 260, 08008 Barcelona",
    "Riera de Montalegre, 12, 08916 Badalona",
    "Calle Guifré, 12, 08912 Badalona",
    "Carrer de Sant Gonçal, 7, 08912 Badalona",
    "Carrer dels Voluntaris, 87, 08225 Terrassa, Barcelona",
    "Carrer de Francesc Eiximenis, 6, 08205 Terrassa",
    "Carrer Joan Monpeó, 60, 08223 Terrassa",
    "Avinguda Onze de Setembre, 111, 08208 Sabadell",
    "Carrer de Francesc Eiximenis, 6, 08205 Sabadell",
    "Carrer Bernat Metge, 92, 08205 Sabadell",

    # Zaragoza
    "Polígono Alcalde Caballero, Avda. Alcalde Caballero, 72, 50014 Zaragoza",
    "Ctra. Castellón, km 233, Zaragoza",
    "Calle K, 8, 50016 Zaragoza",
    "Calle D, 73, Polígono Malpica, 50016 Zaragoza",
    "Calle O, 134, Polígono Malpica, 50016 Zaragoza",
    "Camino de San Antonio, 4-5, 50013 Zaragoza",
    "Paseo Echegaray y Caballero, 8, 50003 Zaragoza",
    "Calle Ricardo del Arco, 1, 50015 Zaragoza",
    "Calle Mar de Aragón, 183, 50014 Zaragoza",
    "Calle Poeta Gabriel Celaya, 7, 50018 Zaragoza",
    "Urbanización Callejillas, 13, 50300 Calatayud",
    "Polígono Industrial Mediavega, 50300 Calatayud",
    "Polígono Industrial La Charluca, 50300 Calatayud",
    "Polígono Industrial La Casaza, 50180 Utebo",
    "Calle Teruel, 56, 50180 Utebo",
    "Urbanización Collarada, 50180 Utebo",

    # Alicante
    "Calle Valle Inclán 13, Alicante, España",
    "Calle Churruca 23, Alicante, España",
    "Calle Trueno, 125, 03006 Alicante",
    "Calle Aureliano Ibarra, 16, 03009 Alicante",
    "Calle Cottolengo 25, Sant Vicent del Raspeig, Alicante, España",
    "Camino de los Frailes 3, Sant Vicent del Raspeig, Alicante, España",
    "C. Torno, 14, Sant Vicent del Raspeig, Alicante, España",
    "Carrer del Mercat 13, Sant Joan d'Alacant, España",
    "Av. Jaime I 11, Sant Joan d'Alacant, España",
    "Calle Sant Bartomeu 39, El Campello, España",
    "Av. Generalitat 23, El Campello, España",
    "Travessera d'Amadeu Vives 16, El Campello, Alicante, España",
    "Avinguda de la Llibertat 11, Elche, España",
    "Calle Capitan Antonio Mena 78, Elche",
    "Calle Martín Soler, 11, 03203 Elche",
    "Calle Cerro de los Santos 6, 03290 Elche",
    "Carrer Almansa 8, Elche, España",

    # Valencia
    "C/ Bernat Descoll, 39, 46026 Valencia",
    "Eduardo Boscá, 14, 46023 Valencia",
    "Eduardo Boscá, 14, 46023 Valencia",
    "Padre Tomás de Montañana, 26, 46023 Valencia",
    "Calle Enrique Miquel Mossi, 7, 46900 Torrent",
    "Calle Montreal, 76, 46900 Torrent",
    "Avenida al Vedat, 5, 46900 Torrent",
    "Calle Europa, 4, 46900 Torrent",
    "Calle Joan d'Austria, 11, 46909 Torrent",
    "Calle Camp de Turia, 1, 46940 Manises",
    "Calle Catedrático Agustín Escardino, 9, 46940 Manises",
    "Aeropuerto de Valencia, Manises",
    "Avenida Mare Nostrum, 7, 46120 Alboraya",
    "Camino Hondo, 25, 46120 Alboraya",
    "Avenida de la Horchata, 19, 46120 Alboraya",
    "Polígono Industrial La Mina, s/n, 46200 Paiporta",

    # Murcia
    "Pl. Camachos, 2, 30002 Murcia",
    "Avda. Principal, 30564 Lorca, Murcia",
    "Paraje Campo la Egesa, 30892 Librilla, Murcia",
    "Plaza Héroes de Cavite, s/n, 30201 Cartagena, Murcia",
    "Polígono Industrial Cabezo Beaza, Calle Berlín, 30353 Cartagena, Murcia",
    "Polígono Industrial Saprelorca, Avenida Río Guadalentín, 30800 Lorca, Murcia",
    "Polígono Industrial La Serreta, Calle Montevideo, 30500 Molina de Segura, Murcia",
    "Calle Mayor, 45, 30500 Molina de Segura, Murcia",
    "Polígono Industrial Base 2000, Calle Castillo de Aledo, 30564 Lorquí, Murcia",
    "Polígono Industrial El Tapiado, 30500 Molina de Segura, Murcia",
    "Avenida Región Murciana, 30730 San Javier, Murcia",
    "Polígono Industrial Los Torraos, 30560 Alguazas, Murcia",
    "Carretera de Mazarrón, km 2, 30850 Totana, Murcia",
    "Polígono Industrial El Labradorcico, 30880 Águilas, Murcia",
    "Calle Federico García Lorca, 6, 02001 Albacete",

    # Albacete
    "Calle de la Sierra, 33, 02150 Valdeganga, Albacete",
    "Avenida Reyes Católicos, 150, 02600 Villarrobledo, Albacete",
    "Calle Hermanos Lumière, 02600 Villarrobledo, Albacete",
    "Apartado de Correos 584, 02640 Almansa, Albacete",
    "Polígono Industrial Los Villares, 02640 Almansa, Albacete",
    "Polígono Industrial El Salvador, 02630 La Roda, Albacete",
    "Plaza Mayor, 47, 02630 La Roda, Albacete",
    "Carretera de Murcia, km 1, 02400 Hellín, Albacete",
    "Calle Gran Vía, 54, 02400 Hellín, Albacete",
    "Carretera de Jaén, km 2, 02300 Alcaraz, Albacete",
    "Plaza Tercia, 12, 02300 Alcaraz, Albacete",
    "Calle Rosario, 15, 02200 Casas Ibáñez, Albacete",
    "Avenida Constitución, 28, 02200 Casas Ibáñez, Albacete",
    "Calle Feria, 98, 02005 Albacete",

    # Toledo
    "Avenida Castilla-La Mancha, s/n, 45003 Toledo",
    "Calle Río Jarama, 132, 45007 Toledo",
    "Calle París, 6, 45003 Toledo",
    "Calle Dinamarca, 4, 45005 Toledo",
    "Avenida Toledo, 3, 45600 Talavera de la Reina, Toledo",
    "Calle del Prado, 7, 45600 Talavera de la Reina, Toledo",
    "Calle Edison, 45600 Talavera de la Reina, Toledo",
    "Calle Domenico Veneciano, 5, 45223 Seseña, Toledo",
    "C. las Margaritas, 17, 45224 Seseña Nuevo, Toledo",
    "C, Miguel de Unamuno, 26, Seseña, Toledo",
    "Avenida del Pilar, 24, 45500 Torrijos, Toledo",
    "Calle Gibraltar, 8, 45500 Torrijos, Toledo",
    "Carretera de Yepes, 45300 Ocaña, Toledo",
    "Calle Sierra de Guadarrama, 45200 Illescas, Toledo",
    "Avenida Castilla-La Mancha, 45200 Illescas, Toledo",
    "Calle Joaquín Rodrigo, 19, 45311 Dosbarrios, Toledo",
    "P.º Félix Rodríguez de la Fuente, 5, 45270 Mocejón, Toledo",
    "Avenida Portugal, 32, 45290 Pantoja, Toledo",
    "Calle Santa Bárbara, 55, 45161 Polán, Toledo"
])

