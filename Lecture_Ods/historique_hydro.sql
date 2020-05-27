CREATE TABLE public.historique_hydro
(
    nbjours integer,
    date date,
    bilan_mensuel_kw integer,
    "marché" character varying(100) COLLATE pg_catalog."default",
    facteur_de_charge double precision,
    total_puissance integer,
    total_ml integer,
    total_oa integer,
    evenement text COLLATE pg_catalog."default",
    commentaire text COLLATE pg_catalog."default",
    padt character varying(100) COLLATE pg_catalog."default"
)