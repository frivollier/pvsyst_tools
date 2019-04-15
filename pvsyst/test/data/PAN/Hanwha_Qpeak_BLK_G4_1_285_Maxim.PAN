PVObject_=pvModule
  Version=6.78
  Flags=$02100743

  PVObject_Commercial=pvCommercial
    Flags=$0041
    Manufacturer=Hanwha Q Cells
    Model=Q.PEAK BLK-G4.1 285 Maxim
    DataSource=Manufacturer/Maxim 2017
    YearBeg=2017
    Width=1.000
    Height=1.670
    Depth=0.032
    Weight=18.800
    NPieces=100
    PriceDate=23/12/18 01:35
    Remarks, Count=6
      Str_1=Frame: Black anodized Aluminium
      Str_2=Structure: 3.2mm thermally pre-stressed glass with anti-reflection
      Str_3=technology
      Str_4
      Str_5
      Str_6=Maxim optimizer MAX20800
    End of Remarks=Maxim optimizer MAX20800
  End of PVObject pvCommercial

  Technol=mtSiMono
  NCelS=60
  NCelP=1
  NDiode=3
  GRef=1000
  TRef=25.0
  PNom=285.0
  PNomTolLow=0.00
  PNomTolUp=1.80
  Isc=9.560
  Voc=38.91
  Imp=8.980
  Vmp=31.73
  muISC=3.82
  muVocSpec=-108.9
  muPmpReq=-0.390
  RShunt=250
  Rp_0=1000
  Rp_Exp=5.50
  RSerie=0.292
  Gamma=0.976
  muGamma=-0.0003
  VMaxIEC=1000
  VMaxUL=1000
  Absorb=0.90
  ARev=3.200
  BRev=11.472
  RDiode=0.010
  VRevDiode=-0.70
  AirMassRef=1.500
  CellArea=237.4
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
