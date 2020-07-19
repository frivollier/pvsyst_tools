PVObject_=pvModule
  Version=6.84
  Flags=$00D00443

  PVObject_Commercial=pvCommercial
    Comment=www.canadiansolar.com
    Flags=$0041
    Manufacturer=Canadian Solar Inc.
    Model=CS3W-440MB-AG 1500V
    DataSource=Preliminary 2019 TUV-SUD data
    YearBeg=2019
    Width=1.048
    Height=2.132
    Depth=0.030
    Weight=28.400
    NPieces=0
    PriceDate=22/07/16 16:29
    Currency=EUR
    Remarks, Count=3
      Str_1=Frame: Anodized aluminium alloy
      Str_2=Structure: 2.0mm Glass / EVA / 2.0mm Glass
      Str_3=Connections: Cable, T4 series
    End of Remarks=Connections: Cable, T4 series
  End of PVObject pvCommercial

  Technol=mtSiMono
  NCelS=72
  NCelP=2
  NDiode=3
  SubModuleLayout=slTwinHalfCells
  GRef=1000
  TRef=25.0
  PNom=440.0
  PNomTolLow=0.00
  PNomTolUp=1.10
  BifacialityFactor=0.700
  Isc=11.530
  Voc=48.30
  Imp=10.980
  Vmp=40.10
  muISC=5.75
  muVocSpec=-140.0
  muPmpReq=-0.360
  RShunt=2500
  Rp_0=10000
  Rp_Exp=5.50
  RSerie=0.237
  Gamma=0.986
  muGamma=-0.0004
  VMaxIEC=1500
  VMaxUL=1500
  Absorb=0.90
  ARev=3.200
  BRev=11.600
  RDiode=0.010
  VRevDiode=-0.70
  AirMassRef=1.500
  CellArea=137.1
  SandiaAMCorr=50.000
  RelEffic800=0.50
  RelEffic400=-0.50
  RelEffic200=-2.30

  PVObject_IAM=pvIAM
    Flags=$00
    IAMMode=UserProfile
    IAMProfile=TCubicProfile
      NPtsMax=9
      NPtsEff=9
      LastCompile=$B18D
      Mode=3
      Point_1=10.0,1.00000
      Point_2=20.0,1.00000
      Point_3=30.0,1.00000
      Point_4=40.0,1.00000
      Point_5=50.0,1.00000
      Point_6=60.0,0.99000
      Point_7=70.0,0.93000
      Point_8=80.0,0.74000
      Point_9=90.0,0.00000
    End of TCubicProfile
  End of PVObject pvIAM

  OperPoints, list of=3 tOperPoint
    Point_1=False,800,25.0,0.50,0.00,0.000,0.000,0.00
    Point_2=False,400,25.0,-0.50,0.00,0.000,0.000,0.00
    Point_3=False,200,25.0,-2.30,0.00,0.000,0.000,0.00
  End of List OperPoints
End of PVObject pvModule
