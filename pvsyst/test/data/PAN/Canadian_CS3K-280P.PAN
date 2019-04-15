PVObject_=pvModule
  Version=6.78
  Flags=$00100043

  PVObject_Commercial=pvCommercial
    Comment=www.canadiansolar.com
    Flags=$0041
    Manufacturer=Canadian Solar Inc.
    Model=CS3K - 280P
    DataSource=Manufacturer 2017 TUV-SUD data
    YearBeg=2017
    Width=0.992
    Height=1.675
    Depth=0.040
    Weight=18.500
    NPieces=100
    PriceDate=23/12/18 00:55
    Remarks, Count=5
      Str_1=Frame: Anodized aluminium alloy
      Str_2=Structure: 3.2mm Glass / EVA / Backsheet
      Str_3=Connections: Cable, T4 series
      Str_4
      Str_5
    End of Remarks
  End of PVObject pvCommercial

  Technol=mtSiPoly
  NCelS=60
  NCelP=2
  NDiode=3
  SubModuleLayout=slTwinHalfCells
  GRef=1000
  TRef=25.0
  PNom=280.0
  PNomTolLow=0.00
  PNomTolUp=1.80
  Isc=9.470
  Voc=37.90
  Imp=8.980
  Vmp=31.20
  muISC=4.74
  muVocSpec=-117.1
  muPmpReq=-0.390
  RShunt=300
  Rp_0=1200
  Rp_Exp=5.50
  RSerie=0.217
  Gamma=0.968
  muGamma=-0.0003
  VMaxIEC=1000
  VMaxUL=1000
  Absorb=0.90
  ARev=3.200
  BRev=11.040
  RDiode=0.010
  VRevDiode=-0.70
  AirMassRef=1.500
  CellArea=122.8
  SandiaAMCorr=50.000

  PVObject_IAM=pvIAM
    Flags=$00
    IAMMode=UserProfile
    IAMProfile=TCubicProfile
      NPtsMax=9
      NPtsEff=9
      LastCompile=$B18D
      Mode=3
      Point_1=10.0,0.99800
      Point_2=20.0,0.99800
      Point_3=30.0,0.99500
      Point_4=40.0,0.99200
      Point_5=50.0,0.98600
      Point_6=60.0,0.97000
      Point_7=70.0,0.91700
      Point_8=80.0,0.76300
      Point_9=90.0,0.00000
    End of TCubicProfile
  End of PVObject pvIAM
End of PVObject pvModule
