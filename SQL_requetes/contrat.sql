select padt, date_start, date_end, (date_end - date_start) as duree_contrat
from producteurs_contracts
where date_start > '2019-12-30' and date_start < '2020-12-30'

select producteurs.padt, puissance_installee_kw,
case when (date_end - date_start) - (date_start  - '2020-01-01') < 0 then (date_end - date_start)
	when (date_end - date_start) - (date_start  - '2020-01-01') > 365 then 365 - (date_start  - '2020-01-01')
	when (date_end - date_start) - (date_start  - '2020-01-01') > 0 then (date_end - date_start) - (date_start  - '2020-01-01')
end as duree_contrat_annuel
from producteurs_contracts as pc, producteurs
where date_start > '2019-12-30' and date_start < '2020-12-31' and producteurs.padt= pc.padt

# Nombre de producteur historique sous contrat
select pr.padt
from producteurs as pr, producteurs_histo as prh, producteurs_contracts as prc
where pr.padt = prh.padt and pr.padt = prc.padt and date_start > '2019-12-30'
group by pr.padt