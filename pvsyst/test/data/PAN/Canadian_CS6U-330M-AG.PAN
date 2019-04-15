PVObject_=pvModule
  Version=6.78
  Flags=$00100043

  PVObject_Commercial=pvCommercial
    Comment=www.canadiansolar.com
    Flags=$0041
    Manufacturer=Canadian Solar Inc.
    Model=CS6U-330M-AG 1500V
    DataSource=Manufacturer 2017 TUV-Rheinland data
    YearBeg=2017
    Width=0.992
    Height=1.960
    Depth=0.040
    Weight=25.600
    NPieces=100
    PriceDate=23/12/18 08:12
    Remarks, Count=5
      Str_1=Frame: Anodized aluminium alloy
      Str_2=Structure: 2.0mm Glass / EVA / 2.0mm Glass
      Str_3=Connections: Cable,  T4 series
      Str_4
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
  Isc=9.310
  Voc=45.90
  Imp=8.800
  Vmp=37.50
  muISC=4.66
  muVocSpec=-141.8
  muPmpReq=-0.410
  RShunt=350
  Rp_0=1400
  Rp_Exp=5.50
  RSerie=0.332
  Gamma=0.948
  muGamma=-0.0005
  VMaxIEC=1500
  VMaxUL=1500
  Absorb=0.90
  ARev=3.200
  BRev=11.600
  RDiode=0.010
  VRevDiode=-0.70
  AirMassRef=1.500
  CellArea=244.3
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
