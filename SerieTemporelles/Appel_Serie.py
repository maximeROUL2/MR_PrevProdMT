from MR_PrevProdMT.SerieTemporelles.ModelPred_HW import HoltWinters
from MR_PrevProdMT.Lecture_Ods.lecture_historique import LectureHistoriqueOds

def main():
    data = LectureHistoriqueOds().fc_opendata_df()
    select = data.loc[data['Code INSEE région'] == 94]

    Serie = HoltWinters(24, select, 'Mois', 'FC moyen mensuel solaire (%)')
    Serie.affichage_pred_cache()
    Serie.HW_erreurs()

    Serie2 = HoltWinters(12, select, 'Mois', 'FC moyen mensuel éolien (%)')
    Serie2.affichage_pred_cache()
    Serie2.HW_erreurs()

if __name__ == "__main__":
    main()

