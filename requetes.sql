
Nouvelle note 1

Select * from rp12_mensuels limit 100

CREATE MATERIALIZED VIEW public.pvpm_mensuel
TABLESPACE pg_default
AS
 SELECT producteurs.padt,
    pvpm.date_start AS mois,
    pvpm.volume_previsionnel_kwh
   FROM producteurs_volumes_previsionnels_par_mois pvpm,
    producteurs
  WHERE pvpm.identifiant_centrale = producteurs.identifiant_centrale
  GROUP BY producteurs.padt, pvpm.date_start, pvpm.volume_previsionnel_kwh
  ORDER BY producteurs.padt, pvpm.date_start
WITH DATA;

ALTER TABLE public.pvpm_mensuel
    OWNER TO polen;


# différence entre le prédit et le réalisé par mois
select abs(volume_previsionnel_kwh - energy_kwh), rp12.padt, month
from rp12_mensuels as rp12, pvpm
where cast(rp12.padt as text) = pvpm.padt
order by abs(volume_previsionnel_kwh - energy_kwh) desc
limit 100

#Moyenne des différences
select avg(abs(volume_previsionnel_kwh - energy_kwh))
from rp12_mensuels as rp12, pvpm
where cast(rp12.padt as text) = pvpm.padt

#Comparaison des moyenne des energy)
select (avg(energy_kwh) - avg(volume_previsionnel_kwh))
from rp12_mensuels as rp12, pvpm
where cast(rp12.padt as text) = pvpm.padt

#Comparaison des moyenne de prevision / réalisé mensuel
select (avg(energy_kwh) - avg(volume_previsionnel_kwh)), month
from rp12_mensuels as rp12, pvpm
where cast(rp12.padt as text) = pvpm.padt
group by month

#Comparaison direct entre le prévi et le réalisé par centrale
select (energy_kwh - volume_previsionnel_kwh) as difference,month, pv.padt, rp12.padt
from rp12_mensuels as rp12, pvpm as pv
where pv.padt = cast(rp12.padt as text)
limit 100

create materialized view as

	select round(energy_kwh - volume_previsionnel_kwh) as diff_kwh,month, pv.padt
	from rp12_mensuels as rp12, pvpm as pv
	where pv.padt = cast(rp12.padt as text)


select sum(diff_kwh), month
from erreurs_prev_reel
group by month
limit 100