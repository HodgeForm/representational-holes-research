"""Unregistered supplementary falsification check. Original HF005 gate untouched."""
import json
import numpy as np
import run
from pathlib import Path
out={}
for idx,name in enumerate(run.TASK_NAMES):
 t=run.construct(name)
 rg=np.random.default_rng(60599+idx)
 yy=t['y'].copy()
 rg.shuffle(yy) # destroy input-output association, retaining prevalence
 t['y']=yy
 fields,cv=run.select(t)
 te=t['te'];tr=t['tr']
 base=run.pred_single_split(t['base'],t['binary'],yy,tr,te,())
 selected=run.pred_single_split(t['base'],t['binary'],yy,tr,te,fields['deployed'])
 delta=float(np.mean((base-yy[te])**2-(selected-yy[te])**2))
 out[name]={'selected_fields':fields['deployed'],'cv_gain':cv['deploy_vs_baseline_cv_gain'],'null_holdout_brier_gain':delta,'null_improves':delta>0}
results={'scope':'ONE shuffled-label run per source task; exploratory, not preregistered','controls':out,'tasks_improved':sum(x['null_improves'] for x in out.values()),'null_passes_four_of_five':sum(x['null_improves'] for x in out.values())>=4}
(Path(__file__).parent/'negative_control_exploratory.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
