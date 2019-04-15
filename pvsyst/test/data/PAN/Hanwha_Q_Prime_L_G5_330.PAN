PVObject_=pvModule
  Version=6.78
  Flags=$00100043

  PVObject_Commercial=pvCommercial
    Comment=www.hanwha-solar.com
    Flags=$0041
    Manufacturer=Hanwha Q Cells
    Model=Q.PRIME L-G5 330
    DataSource=Manufacturer 2017
    YearBeg=2017
    Width=0.991
    Height=1.960
    Depth=0.035
    Weight=22.500
    NPieces=100
    PriceDate=21/12/18 02:41
    Remarks, Count=5
      Str_1=Frame: Anodised aluminium
      Str_2=Structure: 3.2mm tempered glass with anti reflective coating
      Str_3=Connections: Intermateable connector with H4, MC4
      Str_4=6 busbar
      Str_5
    End of Remarks
  End of PVObject pvCommercial

  Technol=mtSiMono
  NCelS=72
  NCelP=1
  NDiode=3
  GRef=1000
  TRef=25.0
  PNom=330.0
  PNomTolLow=0.00
  PNomTolUp=1.50
  Isc=9.290
  Voc=45.70
  Imp=8.760
  Vmp=37.70
  muISC=5.57
  muVocSpec=-142.1
  muPmpReq=-0.400
  RShunt=350
  Rp_0=1400
  Rp_Exp=5.50
  RSerie=0.319
  Gamma=0.915
  muGamma=-0.0005
  VMaxIEC=1000
  Absorb=0.90
  ARev=3.200
  BRev=11.150
  RDiode=0.010
  VRevDiode=-0.70
  AirMassRef=1.500
  CellArea=243.4
  SandiaAMCorr=50.000

  PVObject_IAM=pvIAM
    Flags=$00
    IAMMode=UserProfile
    IAMProfile=TCubicProfile
      NPtsMax=9
      NPtsEff=9
      LastCompile=$B18D
      Mode=3
      Point_1=0.0,1.00000
      Point_2=20.0,1.00000
      Point_3=40.0,1.00000
      Point_4=60.0,0.97000
      Point_5=70.0,0.90000
      Point_6=75.0,0.83000
      Point_7=80.0,0.69000
      Point_8=85.0,0.44000
      Point_9=90.0,0.00000
    End of TCubicProfile
  End of PVObject pvIAM
End of PVObject pvModule
