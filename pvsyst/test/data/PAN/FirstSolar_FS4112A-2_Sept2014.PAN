PVObject_=pvModule
  Version=6.78
  Flags=$00100043

  PVObject_Commercial=pvCommercial
    Comment=www.firstsolar.com   (USA)
    Flags=$0041
    Manufacturer=First Solar
    Model=FS-4112A-2 Sept2014
    DataSource=Manfacturer Sept 2014
    YearBeg=2015
    Width=0.600
    Height=1.200
    Depth=0.007
    Weight=12.000
    NPieces=100
    PriceDate=22/12/18 00:52
    Remarks, Count=5
      Str_1=Frame: Frameless module
      Str_2=Structure: Glass-polyolefin-glass laminate
      Str_3=Connections: MultiContact MC4 connectors
      Str_4
      Str_5
    End of Remarks
  End of PVObject pvCommercial

  Technol=mtCdTe
  NCelS=108
  NCelP=2
  NDiode=4
  GRef=1000
  TRef=25.0
  PNom=112.5
  PNomTolLow=-5.00
  PNomTolUp=5.00
  Isc=1.750
  Voc=87.74
  Imp=1.601
  Vmp=70.16
  muISC=0.70
  muVocSpec=-79.8
  muPmpReq=-0.340
  RShunt=7500
  Rp_0=15000
  Rp_Exp=4.00
  RSerie=4.230
  Gamma=1.484
  muGamma=0.0011
  D2MuTau=0.250
  VMaxIEC=1500
  VMaxUL=1000
  Absorb=0.90
  ARev=3.200
  BRev=3.920
  RDiode=0.010
  VRevDiode=-0.70
  AirMassRef=1.500
  CellArea=31.3
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
      Point_2=30.0,1.00000
      Point_3=55.0,0.98700
      Point_4=60.0,0.96400
      Point_5=65.0,0.96000
      Point_6=70.0,0.91800
      Point_7=75.0,0.85000
      Point_8=80.0,0.72700
      Point_9=90.0,0.00000
    End of TCubicProfile
  End of PVObject pvIAM
End of PVObject pvModule
