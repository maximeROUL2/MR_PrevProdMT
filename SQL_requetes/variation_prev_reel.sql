
# classer les centrales les plus fausses en nombre de KwH
select sum(diff_kwh) as somme_erreur_kwh, padt, count(month)
from erreurs_prev_reel
group by padt
order by somme_erreur_kwh

#Erreur moyenne de prévision
select round(avg(diff_kwh)) as moyenne_erreur_kwh, padt
from erreurs_prev_reel
group by padt
order by moyenne_erreur_kwh

#Traitement globalisé du volume prévisionnel comparé au reel
select (volume_previsionnel_kwh), round(energy_kwh) as energy_kwh_reel, round(volume_previsionnel_kwh - energy_kwh) as erreur_kw,
abs(round(volume_previsionnel_kwh - energy_kwh)/ energy_kwh) as purcent_error,rp12.padt, rp12.month
from pvpm, rp12_mensuels as rp12
where pvpm.padt = cast(rp12.padt as text) and pvpm.mois = rp12.month and energy_kwh != 0
order by erreur_kw

CREATE MATERIALIZED VIEW public.erreurs_prev_reel_local
TABLESPACE pg_default
AS
 SELECT pvpm.volume_previsionnel_kwh,
    round(rp12.energy_kwh) AS energy_kwh_reel,
    round(pvpm.volume_previsionnel_kwh - rp12.energy_kwh) AS erreur_kw,
    abs(round(pvpm.volume_previsionnel_kwh - rp12.energy_kwh) / rp12.energy_kwh) AS purcent_error,
    rp12.padt,
    rp12.month
   FROM pvpm,
    rp12_mensuels rp12
  WHERE pvpm.padt = rp12.padt::text AND pvpm.mois = rp12.month AND rp12.energy_kwh <> 0::double precision
  ORDER BY (round(pvpm.volume_previsionnel_kwh - rp12.energy_kwh))