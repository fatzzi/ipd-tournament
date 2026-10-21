import sys, statistics
from hubfield import load_hub
from field import FIELD
from sim import tournament_1v1, MATS
from perop_helper import total_vs
src = open(sys.argv[1]).read()
real = load_hub()
for v in ('0.0', '0.5', '0.6', '0.7', '0.8'):
    g = {}; exec(src.replace('RETURN_MIN = 0.6 ', f'RETURN_MIN = {v} '), g); me = g['sentinel']
    a = total_vs(me, real); b = total_vs(me, FIELD)
    print(f'RETURN_MIN {v}: real field total {a:.2f} (avg {a/len(real):.3f})   synthetic total {b:.2f} (avg {b/len(FIELD):.3f})', flush=True)
