create materialized view facteur_de_charge as

	select pr.padt, 
	round(puissance_installee_kw) as puissance_installee_kw, 
	round(energy_kwh) as prod_mensuel_kwh, 
	type_de_centrale, 
	code_postal, month, substring(code_postal, 0, 3) as departement, 
	(energy_kwh / (puissance_installee_kw*24*30)) as facteur_de_charge
	from producteurs as pr, rp12_mensuels as rp12
	where pr.padt = cast(rp12.padt as text)
	order by padt, month

create materialized view FC_mensuel as 	
	
	select 
	departement, type_de_centrale, month,
	sum(puissance_installee_kw) as somme_puissance_installee,
	sum(prod_mensuel_kwh) as somme_prod,
	sum(facteur_de_charge) / count(facteur_de_charge) as FC_mensuel
	from facteur_de_charge
	group by month, type_de_centrale, departement



select round(avg(facteur_de_charge_approximatif)), month, code_departement, type_de_centrale 
from facteur_de_charge3
group by month, code_departement, type_de_centrale
order by month


select avg(facteur_de_charge) as FC_moyen,
                                date_part('year'::text, month) as annee, padt
                                 from facteur_de_charge
                                where type_de_centrale = 'HY'
                                group by annee, padt

select count(padt), month, type_de_centrale
from facteur_de_charge
group by month, type_de_centrale
order by month, type_de_centrale


#Recuperer les facteurs de charge par departement par type pour croiser à l etat
select avg(facteur_de_charge) as fc_moyen, month, cast(departement as text), type_de_centrale 
from facteur_de_charge2
group by month, departement, type_de_centrale
order by month


