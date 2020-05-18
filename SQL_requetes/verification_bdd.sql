
#Erreur des volumes prévisionnels => aucune
select pc.identifiant_centrale, pc.date_start, pc.date_end, pvpm.date_start
from producteurs_contracts as pc, producteurs_volumes_previsionnels_par_mois as pvpm
where pvpm.date_start > all (
	select pc.date_end
	from producteurs_contracts as pc , producteurs_volumes_previsionnels_par_mois as pvpm
	where pc.identifiant_centrale = pvpm.identifiant_centrale)
limit 100
