PVObject_=pvModule
  Version=6.79
  Flags=$00100043

  PVObject_Commercial=pvCommercial
    Comment=www.canadiansolar.com
    Flags=$0041
    Manufacturer=Canadian Solar Inc.
    Model=CS3U-350P 1500V P4
    DataSource=Manufacturer 2018 TUV-SUD data
    YearBeg=2017
    Width=0.992
    Height=2.000
    Depth=0.040
    Weight=22.400
    NPieces=100
    PriceDate=07/04/19 22:09
    Remarks, Count=5
      Str_1=Frame: Anodized aluminium alloy
      Str_2=Structure: 3.2mm Glass / EVA / Backsheet
      Str_3=Connections: Cable,T4 series
      Str_4
      Str_5
    End of Remarks
  End of PVObject pvCommercial

  Technol=mtSiPoly
  NCelS=72
  NCelP=2
  NDiode=3
  SubModuleLayout=slTwinHalfCells
  FrontSurface=fsARCoating
  GRef=1000
  TRef=25.0
  PNom=350.0
  PNomTolLow=0.00
  PNomTolUp=1.40
  Isc=9.510
  Voc=46.60
  Imp=8.940
  Vmp=39.20
  muISC=4.75
  muVocSpec=-135.1
  muPmpReq=-0.370
  RShunt=350
  Rp_0=5000
  Rp_Exp=5.50
  RSerie=0.202
  Gamma=1.002
  muGamma=-0.0003
  VMaxIEC=1500
  VMaxUL=1500
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
