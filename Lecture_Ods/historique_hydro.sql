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

CREATE TABLE public.historique_hydro
(
    padt character varying(100) COLLATE pg_catalog."default"
    facteur_de_charge_ods double precision,
    facteur_de_charge_ods double precision,
    facteur_de_charge_ods double precision,
    date date,
    bilan_mensuel_kw integer,
    "marché" character varying(100) COLLATE pg_catalog."default",
    facteur_de_charge double precision,
    total_puissance integer,
    total_ml integer,
    total_oa integer,
    evenement text COLLATE pg_catalog."default",
    commentaire text COLLATE pg_catalog."default",

)

Select padt, max(total_oa) as puissance_oa_kw, max(total_puissance) as puissance_installee_kw,
max(total_ml) as puissance_ml_kw,
case when max(total_oa) = 0 then "Marché libre"
     when max(total_oa) > 0 then "Surplus d'OA"
     end as typologie_contrat
from historique_hydro
where total_oa > 0
group by padt

create materialized view facteur_de_charge_historiqueHY as

	SELECT historique_hydro.padt, date as mois, bilan_mensuel_kw, facteur_de_charge, "marché", total_oa, typologie_contrat,

	case
	when ("marché" = 'marché libre' and total_oa = 0) then cast(bilan_mensuel_kw as float) / ((nbjours * 24 * total_puissance) + 1)
	when "marché" = 'totale' and total_oa = 0 then cast(bilan_mensuel_kw as float) / ((nbjours * 24 * total_puissance) + 1)
	when "marché" = 'marché libre' and total_oa > 0 then cast(bilan_mensuel_kw as float) / ((nbjours * 24 * total_ml) + 1)
	when "marché" = 'totale' and total_oa > 0 and cast(bilan_mensuel_kw - (total_oa * 24 * nbjours) as float) / ((nbjours * 24 * total_puissance)+1) < 0 then 0
	when "marché" = 'totale' and total_oa > 0 then cast(bilan_mensuel_kw - (total_oa * 24 * nbjours)as float) / ((nbjours * 24 * total_puissance) + 1)
	end as facteur_de_charge_corr,

	case when typologie_contrat = 'Surplus OA' and cast(bilan_mensuel_kw - (puissance_oa_kw * 24 * nbjours) as float) / ((nbjours * 24 * total_puissance)+1) < 0 then 0
	when typologie_contrat = 'Surplus OA' then cast(bilan_mensuel_kw - (puissance_oa_kw * 24 * nbjours) as float) / ((nbjours * 24 * total_puissance)+1)
	end as facteur_de_charge_oa_supprimer

	FROM public.historique_hydro, public.producteurs_histo
	where historique_hydro.padt = producteurs_histo.padt

create materialized view producteurs_historique_comparaison as

select pr.padt, pr.puissance_installee_kw, prh.puissance_installee_kw as max_puissance_installee_kw_histo, typologie_contrat, type_de_centrale
from producteurs as pr, producteurs_histo as prh
where pr.padt = prh.padt or (pr.padt = '302644' and prh.padt like '302644%')


create materialized view all_facteur_de_charge as

	select padt, prod_mensuel_kwh as bilan_mensuel_kw, month as mois,
	facteur_de_charge, facteur_de_charge as facteur_de_charge_corr, facteur_de_charge as facteur_de_charge_oa_supprimer
	from facteur_de_charge2
	union
	select padt, bilan_mensuel_kw, mois,
	facteur_de_charge, facteur_de_charge_corr, facteur_de_charge_oa_supprimer
	from facteur_de_charge_historiquehy2