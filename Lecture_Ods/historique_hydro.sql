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

Select padt, max(total_oa) as puissance_oa_kw, max(total_puissance) as puissance_installee_kw,
max(total_ml) as puissance_ml_kw,
case when max(total_oa) = 0 then "Marché libre"
     when max(total_oa) > 0 then "Surplus d'OA"
     end as typologie_contrat
from historique_hydro
where total_oa > 0
group by padt