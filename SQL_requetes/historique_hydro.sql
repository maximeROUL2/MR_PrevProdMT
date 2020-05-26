Drop table historique_hydro;

CREATE TABLE historique_hydro
(
    padt VARCHAR(10) PRIMARY KEY NOT NULL,
    nbjours INT,
	date DATE,
    bilan_mensuel_kw INT,
    marché VARCHAR(50),
    facteur_de_charge DOUBLE PRECISION,
    Total_puissance INT,
    Total_ML INT,
    Total_OA INT,
    Evenement VARCHAR(150),
    Commentaire VARCHAR(150)
)

