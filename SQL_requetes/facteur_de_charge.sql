create materialized view facteur_de_charge as

	select pr.padt, puissance_installee_kw, energy_kwh as prod_mensuel_kwh, type_de_centrale, code_postal, month,
	round(energy_kwh / puissance_installee_kw * 24 * 30) as facteur_de_charge_approximatif
	from producteurs as pr, rp12_mensuels_cor as rp12
	where pr.padt = cast(rp12.padt as text)
	order by padt, month

