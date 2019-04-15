PVObject_=pvModule
  Version=6.78
  Flags=$00100043

  PVObject_Commercial=pvCommercial
    Comment=Hanwha Q CELLS GmbH (www.q-cells.com)
    Flags=$0041
    Manufacturer=Hanwha Q Cells
    Model=Q.PLUS L-G4.2 350
    DataSource=Manufacturer 2017
    YearBeg=2016
    Width=1.000
    Height=1.994
    Depth=0.035
    Weight=24.000
    NPieces=100
    PriceDate=21/12/18 15:10
    Remarks, Count=5
      Str_1=Frame: Anodized aluminum
      Str_2=Structure: 3.2 mm thermally pre-stressed glass w. anti-reflection
      Str_3=Connections: MC4 or MC4-EVO 2, IP65 and IP68
      Str_4
      Str_5
    End of Remarks
  End of PVObject pvCommercial

  Technol=mtSiPoly
  NCelS=72
  NCelP=1
  NDiode=3
  GRef=1000
  TRef=25.0
  PNom=350.0
  PNomTolLow=0.00
  PNomTolUp=1.40
  Isc=9.690
  Voc=47.71
  Imp=9.150
  Vmp=38.23
  muISC=3.88
  muVocSpec=-137.9
  muPmpReq=-0.400
  RShunt=350
  Rp_0=1400
  Rp_Exp=5.50
  RSerie=0.384
  Gamma=1.041
  muGamma=-0.0005
  VMaxIEC=1500
  VMaxUL=1500
  Absorb=0.90
  ARev=3.200
  BRev=10.880
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
