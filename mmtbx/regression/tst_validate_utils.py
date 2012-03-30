#(jEdit options) :folding=explicit:collapseFolds=1:
from mmtbx.validation.ramalyze import ramalyze
from mmtbx.validation.rotalyze import rotalyze
from mmtbx.validation.cbetadev import cbetadev
from mmtbx.validation.clashscore import clashscore
from mmtbx.validation.rna_validate import rna_validate
from mmtbx.rotamer.rotamer_eval import find_rotarama_data_dir
from iotbx import pdb
from libtbx.test_utils import show_diff
import libtbx.load_env

import sys, os

#{{{ exercise_rna_validate
def exercise_rna_validate():
  regression_pdb = libtbx.env.find_in_repositories(
    relative_path="phenix_regression/pdb/pdb2goz_refmac_tls.ent",
    test=os.path.isfile)
  if (regression_pdb is None):
    print "Skipping exercise_regression(): input pdb (pdb2goz_refmac_tls.ent) not available"
    return
  pdb_io = pdb.input(file_name=regression_pdb)
  rv=rna_validate()
  rv.analyze_pdb(pdb_io=pdb_io)
  assert len(rv.pucker_outliers) == 2
  assert len(rv.bond_outliers) == 2
  assert len(rv.angle_outliers) == 0
  assert len(rv.suite_outliers) == 3

#{{{ exercise_clashscore
def exercise_clashscore():
  regression_pdb = libtbx.env.find_in_repositories(
    relative_path="phenix_regression/pdb/pdb1zff.ent",
    test=os.path.isfile)
  if (regression_pdb is None):
    print "Skipping exercise_regression(): input pdb (pdb1zff.ent) not available"
    return
  pdb_io = pdb.input(file_name=regression_pdb)

  r = clashscore()
  score, bad_clashes = clashscore.analyze_clashes(r,pdb_io)
  clash_out = 'clashscore = %f' % score['']
  assert not show_diff(clash_out, "clashscore = 56.962025")
#}}}

#{{{ exercise_cbetadev
def exercise_cbetadev():
  regression_pdb = libtbx.env.find_in_repositories(
    relative_path="phenix_regression/pdb/pdb1jxt.ent",
    test=os.path.isfile)
  if (regression_pdb is None):
    print "Skipping exercise_regression(): input pdb (pdb1jxt.ent) not available"
    return
  pdb_io = pdb.input(file_name=regression_pdb)

  r = cbetadev()
  output, summary, output_list = cbetadev.analyze_pdb(r,filename=regression_pdb,
                                                      pdb_io=pdb_io,
                                                      outliers_only=True)
  assert not show_diff(output, """\
pdb:alt:res:chainID:resnum:dev:dihedralNABB:Occ:ALT:
pdb1jxt :a:ile: A:   7 :  0.260: -46.47:   0.45:a:
pdb1jxt :b:val: A:   8 :  0.258:  80.92:   0.30:b:
pdb1jxt :c:val: A:   8 :  0.641: -53.98:   0.20:c:
pdb1jxt :b:thr: A:  30 :  0.812: -76.98:   0.30:b:
pdb1jxt :b:thr: A:  39 :  0.924:  56.41:   0.30:b:
pdb1jxt :b:asp: A:  43 :  0.500:   7.56:   0.25:b:""")

  output, summary, output_list = cbetadev.analyze_pdb(r,filename=regression_pdb,
                                                      pdb_io=pdb_io,
                                                      outliers_only=False)
  assert not show_diff(output, """\
pdb:alt:res:chainID:resnum:dev:dihedralNABB:Occ:ALT:
pdb1jxt : :thr: A:   1 :  0.102:  11.27:   1.00: :
pdb1jxt :a:thr: A:   2 :  0.022: -49.31:   0.67:a:
pdb1jxt : :cys: A:   3 :  0.038: 103.68:   1.00: :
pdb1jxt : :cys: A:   4 :  0.047:-120.73:   1.00: :
pdb1jxt : :pro: A:   5 :  0.069:-121.41:   1.00: :
pdb1jxt : :ser: A:   6 :  0.052: 112.87:   1.00: :
pdb1jxt :a:ile: A:   7 :  0.260: -46.47:   0.45:a:
pdb1jxt :b:ile: A:   7 :  0.153: 122.97:   0.55:b:
pdb1jxt :a:val: A:   8 :  0.184:-155.36:   0.50:a:
pdb1jxt :b:val: A:   8 :  0.258:  80.92:   0.30:b:
pdb1jxt :c:val: A:   8 :  0.641: -53.98:   0.20:c:
pdb1jxt : :ala: A:   9 :  0.061: -82.84:   1.00: :
pdb1jxt :a:arg: A:  10 :  0.023: 172.24:   1.00:a:
pdb1jxt : :ser: A:  11 :  0.028:-129.11:   1.00: :
pdb1jxt :a:asn: A:  12 :  0.021: -80.80:   0.50:a:
pdb1jxt :b:asn: A:  12 :  0.199:  50.01:   0.50:b:
pdb1jxt :a:phe: A:  13 :  0.067: -37.32:   0.65:a:
pdb1jxt :b:phe: A:  13 :  0.138:  19.24:   0.35:b:
pdb1jxt : :asn: A:  14 :  0.065: -96.35:   1.00: :
pdb1jxt : :val: A:  15 :  0.138: -96.63:   1.00: :
pdb1jxt : :cys: A:  16 :  0.102: -28.64:   1.00: :
pdb1jxt : :arg: A:  17 :  0.053:-106.79:   1.00: :
pdb1jxt : :leu: A:  18 :  0.053:-141.51:   1.00: :
pdb1jxt : :pro: A:  19 :  0.065:-146.95:   1.00: :
pdb1jxt : :thr: A:  21 :  0.086:  53.80:   1.00: :
pdb1jxt :a:pro: A:  22 :  0.092: -83.39:   0.55:a:
pdb1jxt :a:glu: A:  23 :  0.014:-179.53:   0.50:a:
pdb1jxt :b:glu: A:  23 :  0.050:-179.78:   0.50:b:
pdb1jxt : :ala: A:  24 :  0.056: -88.96:   1.00: :
pdb1jxt : :leu: A:  25 :  0.084:-106.42:   1.00: :
pdb1jxt : :cys: A:  26 :  0.074: -94.70:   1.00: :
pdb1jxt : :ala: A:  27 :  0.056: -62.15:   1.00: :
pdb1jxt : :thr: A:  28 :  0.056:-114.82:   1.00: :
pdb1jxt :a:tyr: A:  29 :  0.068:   0.22:   0.65:a:
pdb1jxt :a:thr: A:  30 :  0.180: 103.27:   0.70:a:
pdb1jxt :b:thr: A:  30 :  0.812: -76.98:   0.30:b:
pdb1jxt : :cys: A:  32 :  0.029: -84.07:   1.00: :
pdb1jxt : :ile: A:  33 :  0.048:-119.17:   1.00: :
pdb1jxt : :ile: A:  34 :  0.045:  99.02:   1.00: :
pdb1jxt : :ile: A:  35 :  0.052:-128.24:   1.00: :
pdb1jxt : :pro: A:  36 :  0.084:-142.29:   1.00: :
pdb1jxt : :ala: A:  38 :  0.039:  50.02:   1.00: :
pdb1jxt :a:thr: A:  39 :  0.093: -96.63:   0.70:a:
pdb1jxt :b:thr: A:  39 :  0.924:  56.41:   0.30:b:
pdb1jxt : :cys: A:  40 :  0.013:-144.12:   1.00: :
pdb1jxt : :pro: A:  41 :  0.039: -97.09:   1.00: :
pdb1jxt :a:asp: A:  43 :  0.130:-146.91:   0.75:a:
pdb1jxt :b:asp: A:  43 :  0.500:   7.56:   0.25:b:
pdb1jxt : :tyr: A:  44 :  0.085:-143.63:   1.00: :
pdb1jxt : :ala: A:  45 :  0.055:  33.32:   1.00: :
pdb1jxt : :asn: A:  46 :  0.066: -50.46:   1.00: :""")
#}}}

#{{{ exercise_ramalyze
def exercise_ramalyze():
  regression_pdb = libtbx.env.find_in_repositories(
    relative_path="phenix_regression/pdb/jcm.pdb",
    test=os.path.isfile)
  if (regression_pdb is None):
    print "Skipping exercise_ramalyze(): input pdb (jcm.pdb) not available"
    return
  if (find_rotarama_data_dir(optional=True) is None):
    print "Skipping exercise_ramalyze(): rotarama_data directory not available"
    return
  pdb_io = pdb.input(file_name=regression_pdb)

  r = ramalyze()
  output, output_list = r.analyze_pdb(pdb_io=pdb_io, outliers_only=True)
  assert output.count("OUTLIER") == 100
  assert output.count("Favored") == 0
  assert output.count("Allowed") == 0
  assert output.count("General") == 64
  assert output.count("Glycine") == 6
  assert output.count("Trans-proline") == 1
  assert output.count("Cis-proline") == 0
  assert output.count("Pre-proline") == 4
  assert output.count("Isoleucine or valine") == 25

  output, output_list = r.analyze_pdb(pdb_io=pdb_io, outliers_only=False)
  assert output.count("OUTLIER") == 100
  assert output.count("Favored") == 461
  assert output.count("Allowed") == 162
  assert output.count("General") == 513
  assert output.count("Glycine") == 39
  assert output.count("Trans-proline") == 23
  assert output.count("Cis-proline") == 0
  assert output.count("Pre-proline") == 21
  assert output.count("Isoleucine or valine") == 127
  numtotal = r.get_phi_psi_residues_count()
  assert r.get_outliers_count_and_fraction()  == (100, 100./numtotal)
  assert r.get_allowed_count_and_fraction()   == (162, 162./numtotal)
  assert r.get_favored_count_and_fraction()   == (461, 461./numtotal)
  assert r.get_general_count_and_fraction()   == (513, 513./numtotal)
  assert r.get_gly_count_and_fraction()       == (39, 39./numtotal)
  assert r.get_trans_pro_count_and_fraction() == (23, 23./numtotal)
  assert r.get_cis_pro_count_and_fraction()   == (0, 0./numtotal)
  assert r.get_prepro_count_and_fraction()    == (21, 21./numtotal)
  assert r.get_ileval_count_and_fraction()    == (127, 127./numtotal)
  assert numtotal == 75+154+494
  output_lines = output.splitlines()
  assert len(output_lines) == 723
  assert output_lines[0] == "A  15  SER:35.07:-83.26:131.88:Favored:General"
  assert output_lines[1] == "A  16  SER:0.74:-111.53:71.36:Allowed:General"
  assert output_lines[168] == "A 191  ASP:2.66:-42.39:121.87:Favored:Pre-proline"
  assert output_lines[169] == "A 192  PRO:0.31:-39.12:-31.84:Allowed:Trans-proline"
  assert output_lines[713] == "B 368  LYS:56.44:-62.97:-53.28:Favored:General"
  assert output_lines[714] == "B 369  GLU:8.89:-44.36:-45.50:Favored:General"
  assert output_lines[715] == "B 370  LYS:40.00:-50.00:-39.06:Favored:General"
  assert output_lines[716] == "B 371  VAL:68.24:-60.38:-51.85:Favored:Isoleucine or valine"
  assert output_lines[717] == "B 372  LEU:0.02:-61.13:-170.23:OUTLIER:General"
  assert output_lines[718] == "B 373  ARG:0.02:60.09:-80.26:OUTLIER:General"
  assert output_lines[719] == "B 374  ALA:0.13:-37.21:-36.12:Allowed:General"
  assert output_lines[720] == "B 375  LEU:11.84:-89.81:-41.45:Favored:General"
  assert output_lines[721] == "B 376  ASN:84.33:-58.30:-41.39:Favored:General"
  assert output_lines[722] == "B 377  GLU:30.88:-56.79:-21.74:Favored:General"

  regression_pdb = libtbx.env.find_in_repositories(
    relative_path="phenix_regression/pdb/pdb1jxt.ent",
    test=os.path.isfile)
  if (regression_pdb is None):
    print "Skipping exercise_ramalyze(): input pdb (pdb1jxt.ent) not available"
    return
  pdb_io = pdb.input(file_name=regression_pdb)

  r = ramalyze()
  output, output_list = r.analyze_pdb(pdb_io=pdb_io, outliers_only=True)
  assert output.count("Favored") == 0
  assert output.count("Allowed") == 0
  assert output.count("OUTLIER") == 0

  output, output_list = r.analyze_pdb(pdb_io=pdb_io, outliers_only=False)
  assert output.count("Favored") == 47
  assert output.count("Allowed") == 1
  assert output.count("OUTLIER") == 0
  assert output.count("General") == 27
  assert output.count("Glycine") == 4
  assert output.count("Trans-proline") == 4
  assert output.count("Cis-proline") == 0
  assert output.count("Pre-proline") == 5
  assert output.count("Isoleucine or valine") == 8
  numtotal = r.get_phi_psi_residues_count()
  assert r.get_outliers_count_and_fraction()  == (0, 0./numtotal)
  assert r.get_allowed_count_and_fraction()   == (1, 1./numtotal)
  assert r.get_favored_count_and_fraction()   == (47, 47./numtotal)
  assert r.get_general_count_and_fraction()   == (27, 27./numtotal)
  assert r.get_gly_count_and_fraction()       == (4, 4./numtotal)
  assert r.get_trans_pro_count_and_fraction() == (4, 4./numtotal)
  assert r.get_cis_pro_count_and_fraction()   == (0, 0./numtotal)
  assert r.get_prepro_count_and_fraction()    == (5, 5./numtotal)
  assert r.get_ileval_count_and_fraction()    == (8, 8./numtotal)
  output_lines = output.splitlines()
  assert len(output_lines) == 48
  assert output_lines[0] == "A   2  ATHR:33.85:-106.92:144.23:Favored:General"
  assert output_lines[1] == "A   2  BTHR:37.07:-97.44:137.00:Favored:General"
  assert output_lines[6] == "A   7  AILE:98.76:-61.91:-44.35:Favored:Isoleucine or valine"
  assert output_lines[7] == "A   7  BILE:61.50:-56.21:-51.56:Favored:Isoleucine or valine"
  assert output_lines[8] == "A   8  AVAL:23.11:-50.35:-49.64:Favored:Isoleucine or valine"
  assert output_lines[9] == "A   8  BVAL:12.01:-83.20:-12.14:Favored:Isoleucine or valine"
  assert output_lines[10] == "A   8  CVAL:73.11:-61.22:-36.49:Favored:Isoleucine or valine"
  assert output_lines[44] == "A  43  AASP:51.81:-94.64:5.45:Favored:General"
  assert output_lines[45] == "A  43  BASP:56.98:-88.69:-0.12:Favored:General"
  assert output_lines[46] == "A  44  TYR:1.76:-133.10:58.75:Allowed:General"
  assert output_lines[47] == "A  45  ALA:57.37:-86.61:-8.57:Favored:General"

#}}}

#{{{ exercise_rotalyze
def exercise_rotalyze():
  regression_pdb = libtbx.env.find_in_repositories(
    relative_path="phenix_regression/pdb/jcm.pdb",
    test=os.path.isfile)
  if (regression_pdb is None):
    print "Skipping exercise_rotalyze(): input pdb (jcm.pdb) not available"
    return
  if (find_rotarama_data_dir(optional=True) is None):
    print "Skipping exercise_rotalyze(): rotarama_data directory not available"
    return
  pdb_io = pdb.input(file_name=regression_pdb)

  r = rotalyze()
  output, output_list = r.analyze_pdb(pdb_io, outliers_only=True)
  #print output
  assert output.count("OUTLIER") == 113
  #print output.count(":")
  assert output.count(":") == 791
  output_lines = output.splitlines()
  assert len(output_lines) == 113
  for lines in output_lines:
    assert float(lines[11:14]) <= 1.0

  output, output_list = r.analyze_pdb(pdb_io, outliers_only=False)
  assert output.count("OUTLIER") == 113
  assert output.count(":") == 4501
  assert output.count("p") == 121
  assert output.count("m") == 333
  assert output.count("t") == 495
  output_lines = output.splitlines()
  assert len(output_lines) == 643
  assert output_lines[0]   == "A  14  MET:1.00:3.3:29.2:173.3:287.9::ptm"
  assert output_lines[1]   == "A  15  SER:1.00:0.1:229.0::::OUTLIER"
  assert output_lines[2]   == "A  16  SER:1.00:4.2:277.9::::m"
  assert output_lines[42]  == "A  58  ASN:1.00:2.0:252.4:343.6:::m-20"
  assert output_lines[43]  == "A  59  ILE:1.00:2.0:84.2:186.7:::pt"
  assert output_lines[168] == "A 202  GLU:1.00:0.4:272.7:65.9:287.8::OUTLIER"
  assert output_lines[169] == "A 203  ILE:1.00:5.0:292.9:199.6:::mt"
  assert output_lines[450] == "B 154  THR:1.00:0.1:356.0::::OUTLIER"
  assert output_lines[587] == "B 316  TYR:1.00:5.4:153.7:68.6:::t80"
  assert output_lines[394] == "B  86  ASP:1.00:2.2:321.4:145.1:::m-20"
  assert output_lines[641] == "B 377  GLU:1.00:45.3:311.7:166.2:160.1::mt-10"
  assert output_lines[642] == "B 378  THR:1.00:23.5:309.4::::m"

  regression_pdb = libtbx.env.find_in_repositories(
    relative_path="phenix_regression/pdb/pdb1jxt.ent",
    test=os.path.isfile)
  if (regression_pdb is None):
    print "Skipping exercise_ramalyze(): input pdb (pdb1jxt.ent) not available"
    return
  pdb_io = pdb.input(file_name=regression_pdb)
  r = rotalyze()
  output, output_list = r.analyze_pdb(pdb_io, outliers_only=True)
  #print output
  assert output == "A  29  BTYR:0.35:0.3:191.3:322.7:::OUTLIER"

  output, output_list = r.analyze_pdb(pdb_io, outliers_only=False)
  assert not show_diff(output,"""\
A   1  THR:1.00:96.6:299.5::::m
A   2  ATHR:0.67:55.0:56.1::::p
A   2  BTHR:0.33:93.8:298.1::::m
A   3  CYS:1.00:28.5:310.5::::m
A   4  CYS:1.00:89.0:293.1::::m
A   5  PRO:1.00:90.6:30.2::::Cg_endo
A   6  SER:1.00:84.6:68.4::::p
A   7  AILE:0.45:62.7:290.8:178.2:::mt
A   7  BILE:0.55:14.3:284.4:298.4:::mm
A   8  AVAL:0.50:3.6:156.7::::t
A   8  BVAL:0.30:9.7:71.3::::p
A   8  CVAL:0.20:74.3:172.1::::t
A  10  AARG:0.65:23.4:176.8:66.5:63.9:180.0:tpp180
A  10  BARG:0.35:20.1:176.8:72.8:66.4:171.9:tpp180
A  11  SER:1.00:49.6:300.9::::m
A  12  AASN:0.50:96.0:286.1:343.8:::m-20
A  12  BASN:0.50:99.2:288.4:337.6:::m-20
A  13  APHE:0.65:42.3:187.2:276.4:::t80
A  13  BPHE:0.35:84.7:179.6:263.1:::t80
A  14  ASN:1.00:95.9:289.6:333.0:::m-20
A  15  VAL:1.00:47.4:168.2::::t
A  16  CYS:1.00:44.7:176.5::::t
A  17  ARG:1.00:23.6:289.7:282.8:288.6:158.7:mmm180
A  18  LEU:1.00:75.1:287.2:173.3:::mt
A  19  PRO:1.00:43.6:24.4::::Cg_endo
A  21  THR:1.00:8.5:314.0::::m
A  22  APRO:0.55:78.5:333.5::::Cg_exo
A  23  AGLU:0.50:92.5:290.9:187.1:341.8::mt-10
A  23  BGLU:0.50:94.5:292.0:183.8:339.2::mt-10
A  25  ALEU:0.50:96.7:294.4:173.6:::mt
A  26  CYS:1.00:92.2:295.0::::m
A  28  THR:1.00:37.5:52.9::::p
A  29  ATYR:0.65:23.0:161.8:67.8:::t80
A  29  BTYR:0.35:0.3:191.3:322.7:::OUTLIER
A  30  ATHR:0.70:68.5:57.4::::p
A  30  BTHR:0.30:8.8:78.1::::p
A  32  CYS:1.00:69.2:301.7::::m
A  33  ILE:1.00:37.5:66.5:173.4:::pt
A  34  AILE:0.70:66.6:303.6:167.6:::mt
A  34  BILE:0.30:33.9:308.5:296.8:::mm
A  35  ILE:1.00:48.4:62.4:170.0:::pt
A  36  PRO:1.00:36.1:22.5::::Cg_endo
A  39  ATHR:0.70:18.3:311.0::::m
A  39  BTHR:0.30:17.7:288.8::::m
A  40  CYS:1.00:99.0:294.4::::m
A  41  PRO:1.00:61.4:34.4::::Cg_endo
A  43  AASP:0.75:29.6:56.5:340.3:::p-10
A  43  BASP:0.25:45.3:59.6:349.3:::p-10
A  44  TYR:1.00:85.6:290.9:85.1:::m-85
A  46  ASN:1.00:34.0:301.6:117.9:::m120""")
#}}}

def run():
  verbose = "--verbose" in sys.argv[1:]
  if (not libtbx.env.has_module(name="phenix")):
    print \
      "Skipping exercise_rna_validate():" \
      " phenix not available"
  else:
    exercise_rna_validate()
  exercise_ramalyze()
  exercise_rotalyze()
  exercise_cbetadev()
  if (not libtbx.env.has_module(name="probe")):
    print \
      "Skipping exercise_clashscore():" \
      " probe not available"
  else:
    exercise_clashscore()
  print "OK"

if (__name__ == "__main__"):
  run()
