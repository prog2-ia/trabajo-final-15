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
    "Ctra. Toledo-Ocaña s/n Polígono Industrial Santa María de Benquerencia, Toledo, 45007 Toledo",

    # Zaragoza
    "Polígono Alcalde Caballero Avda. Alcalde Caballero 72, Zaragoza, 50014 Zaragoza"

])

# ----------------------------------------------------------
# DESPACHOS
# ----------------------------------------------------------
direcciones_despacho_txt = limpiar_direcciones([
    # Madrid
    "Calle Resina 39, Madrid, España",
    "Calle Jazmín 34, 28033 Madrid",
    "Gran Via 1, Madrid, España",
    "Calle Río Almanzora, 4, 28906 Getafe, Madrid",
    # "Calle Carpinteros 7, Getafe, España",
    "Calle Casas de Miravete 30, Villa de Vallecas, 28031 Madrid",
    "Polígono Industrial Urtinsa Calle Laguna, Alcorcon, 28923 Madrid",
    "Polígono Industrial Cobo Calleja Calle Manuel Cobo Calleja, Fuenlabrada, 28947 Madrid",
    # "Calle Sierra de Albarracín 2, Fuenlabrada, 28946 Fuenlabrada Madrid",
    # "Calle Constitución 5, Fuenlabrada, España",

    # Barcelona
    "C/ Mar Roja 51, Barcelona, 08040 Barcelona",
    "Paseo de la Zona Franca 73, Barcelona, 08038 Barcelona",
    "Avenida Josep Tarradellas 8, Barcelona, 08029 Barcelona",
    # "Muntaner 200, Barcelona, 08036 Barcelona",
    # "Paseo Peira 23, Barcelona, 08031 Barcelona",
    # "Calle Tuset 23, Barcelona, 08006 Barcelona",
    # "Calle Mallorca 260, Barcelona, 08008 Barcelona",
    "Riera de Montalegre 12, Badalona, 08916 Barcelona",
    # "Calle Guifré 12, Badalona, 08912 Barcelona",
    # "Carrer de Sant Gonçal 7, Badalona, 08912 Barcelona",
    "Carrer dels Voluntaris 87, Terrassa, 08225 Barcelona",
    # "Carrer de Francesc Eiximenis 6, Terrassa, 08205 Barcelona",
    # "Carrer Joan Monpeó 60, Terrassa, 08223 Barcelona",
    "Avinguda Onze de Setembre 111, Sabadell, 08208 Barcelona",
    # "Carrer de Francesc Eiximenis 6, Sabadell 08205 Barcelona",
    # "Carrer Bernat Metge 92, Sabadell 08205 Barcelona",

    # Zaragoza
    # "Ctra. Castellón km 233, Zaragoza, Zaragoza",
    # "Calle K 8, Zaragoza, 50016 Zaragoza",
    # "Calle D, 73, Polígono Malpica, 50016 Zaragoza",
    # "Calle O, 134, Polígono Malpica, 50016 Zaragoza",
    # "Camino de San Antonio, 4-5, 50013 Zaragoza",
    "Paseo Echegaray y Caballero 8, Zaragoza, 50003 Zaragoza",
    "Calle Ricardo del Arco 1,Zaragoza,  50015 Zaragoza",
    # "Calle Mar de Aragón 183, Zaragoza, 50014 Zaragoza",
    # "Calle Poeta Gabriel Celaya, 7, 50018 Zaragoza",
    "Urbanización Callejillas 13, Calatayud, 50300 Zaragoza",
    # "Polígono Industrial Mediavega, 50300 Calatayud",
    # "Polígono Industrial La Charluca, 50300 Calatayud",
    # "Polígono Industrial La Casaza, 50180 Utebo",
    "Calle Teruel 56, 50180 Utebo, Zaragoza",
    # "Urbanización Collarada, 50180 Utebo",

    # Alicante
    "Calle Valle Inclán 13, Alicante, España",
    "Calle Churruca 23, Alicante, España",
    # "Calle Trueno 125, Alicante, 03006 Alicante",
    # "Calle Aureliano Ibarra 16, Alicante, 03009 Alicante",
    "Calle Cottolengo 25, Sant Vicent del Raspeig, Alicante",
    # "Camino de los Frailes 3, Sant Vicent del Raspeig, Alicante",
    # "C. Torno, 14, Sant Vicent del Raspeig, Alicante",
    "Carrer del Mercat 13, Sant Joan d'Alacant, Alicante",
    # "Av. Jaime I 11, Sant Joan d'Alacant, Alicante",
    "Calle Sant Bartomeu 39, El Campello, Alicante",
    # "Av. Generalitat 23, El Campello, Alicante",
    # "Travessera d'Amadeu Vives 16, El Campello, Alicante",
    "Avinguda de la Llibertat 11, Elche, Alicante",
    "Calle Capitan Antonio Mena 78, Elche,Alicante",
    # "Calle Martín Soler, 11, 03203 Elche, Alicante",
    # "Calle Cerro de los Santos 6, 03290 Elche, Alicante",
    # "Carrer Almansa 8, Elche, España",

    # Valencia
    "C/ Bernat Descoll 39, Valencia, 46026 Valencia",
    "Eduardo Boscá 14, Valencia, 46023 Valencia",
    # "Padre Tomás de Montañana 26, Valencia, 46023 Valencia",
    "Calle Enrique Miquel Mossi 7, Torrent, 46900 Valencia",
    # "Calle Montreal 76, Torrent, 46900 Valencia",
    # "Avenida al Vedat 5, Torrent, 46900 Valencia",
    # "Calle Europa 4, Torrent, 46900 Valencia",
    # "Calle Joan d'Austria 11, Torrent, 46909 Valencia",
    "Calle Camp de Turia 1, Manises, 46940 Valencia",
    # "Calle Catedrático Agustín Escardino 9, Manises, 46940 Valencia",
    # "Aeropuerto de Valencia, Manises, Valencia",
    "Avenida Mare Nostrum 7, Alboraya, 46120 Valencia",
    # "Camino Hondo 25, Alboraya, 46120 Valencia",
    # "Avenida de la Horchata 19, Alboraya, 46120 Valencia",
    "Polígono Industrial La Mina s/n, Paiporta, 46200 Valencia",

    # Murcia
    "Pl. Camachos 2, Murcia, 30002 Murcia",
    "Avda. Principal, Lorca, 30564 Murcia",
    # "Polígono Industrial Saprelorca, Avenida Río Guadalentín, 30800 Lorca, Murcia",
    "Paraje Campo la Egesa, Librilla, 30892 Murcia",
    "Plaza Héroes de Cavite s/n, Cartagena, 30201 Murcia",
    # "Polígono Industrial Cabezo Beaza Calle Berlín, Cartagena, 30353 Murcia",
    # "Polígono Industrial La Serreta Calle Montevideo, Molina de Segura, 30500 Murcia",
    "Calle Mayor 45, Molina de Segura, 30500 Murcia",
    # "Polígono Industrial Base 2000 Calle Castillo de Aledo, Lorqui, 30564 Murcia",
    # "Polígono Industrial El Tapiado, 30500 Molina de Segura, Murcia",
    "Avenida Región Murciana, San Javier, 30730  Murcia",
    # "Polígono Industrial Los Torraos, 30560 Alguazas, Murcia",
    # "Carretera de Mazarrón, km 2, 30850 Totana, Murcia",
    # "Polígono Industrial El Labradorcico, 30880 Águilas, Murcia",

    # Albacete
    "Calle Federico García Lorca 6, Albacete,  02001 Albacete",
    "Calle de la Sierra 33, Valdeganga, 02150 Albacete",
    "Avenida Reyes Católicos 150, Villarrobledo, 02600 Albacete",
    # "Calle Hermanos Lumière, 02600 Villarrobledo, Albacete",
    "Apartado de Correos 584, 02640 Almansa, Albacete",
    # "Polígono Industrial Los Villares, 02640 Almansa, Albacete",
    # "Polígono Industrial El Salvador, La Roda, 02630 Albacete",
    "Plaza Mayor 47, La Roda, 02630 Albacete",
    # "Carretera de Murcia, km 1, 02400 Hellín, Albacete",
    "Calle Gran Vía 54, 02400 Hellín, Albacete",
    # "Carretera de Jaén, km 2, 02300 Alcaraz, Albacete",
    "Plaza Tercia 12, Alcaraz, 02300 Albacete",
    "Calle Rosario 15, Casas Ibañez, 02200 Albacete",
    # "Avenida Constitución 28, 02200 Casas Ibáñez, Albacete",
    # "Calle Feria 98, 02005 Albacete",

    # Toledo
    "Avenida Castilla-La Mancha s/n, Toledo, 45003 Toledo",
    "Calle Río Jarama 132, Toledo, 45007 Toledo",
    # "Calle París, 6, 45003 Toledo",
    # "Calle Dinamarca, 4, 45005 Toledo",
    "Avenida Toledo 3, Talavera de la Reina,  45600 Toledo",
    # "Calle del Prado 7, 45600 Talavera de la Reina, Toledo",
    # "Calle Edison, 45600 Talavera de la Reina, Toledo",
    "Calle Domenico Veneciano 5, Seseña, 45223 Toledo",
    # "C. las Margaritas 17, 45224 Seseña Nuevo, Toledo",
    # "C, Miguel de Unamuno, 26, Seseña, Toledo",
    "Avenida del Pilar 24, Torrijos, 45500 Toledo",
    # "Calle Gibraltar, 8, 45500 Torrijos, Toledo",
    "Carretera de Yepes, Ocaña, 45300 Toledo",
    "Calle Sierra de Guadarrama, Illescas, 45200 Toledo",
    # "Avenida Castilla-La Mancha, 45200 Illescas, Toledo",
    "Calle Joaquín Rodrigo 19, Dosbarrios, 45311 Toledo",
    "P.º Félix Rodríguez de la Fuente 5, Mocejón, 45270 Toledo",
    "Avenida Portugal 32, Pantoja, 45290 Toledo",
    # "Calle Santa Bárbara, 55, 45161 Polán, Toledo"
])
# ==========================================================
# TODAS LAS DIRECCIONES JUNTAS
# ==========================================================

todas_direcciones = (
        direcciones_central_txt +
        direcciones_base_txt +
        direcciones_despacho_txt
)
