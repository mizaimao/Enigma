# Enigma
Emulation of Enigma machine M3. Built and tested on macOS 14.0 with Python 3.11.3.

### Examples

After machine config and ciphers (may not be the correct word here) are generated, call

`python enigma/utils/config_gen.py`

and it will print how this machine is configured and the messages before, and after encryption.

```
+---------------------------------------------+
|         ENIGMA CONFIGURATION LOADED         |
+---------------------------------------------+
|   CONFIGURED BY DATE    |        01         |
|      ROTORS IN USE      |      V IV I       |
| ROTOR INITIAL POSITIONS |     16 03 17      |
|          PLUGS          | AR ZP XO KG QV TJ |
|       INDICATORS        |  slq iqv obd nqz  |
+---------------------------------------------+
INPUT -> ENCODED -> DECODED:
CHICKENMIZAIMAO -> DKKXVPPEFJMDXLK -> CHICKENMIZAIMAO
```

#### Generate code table and machine configuration
Running the following will generate a table like [this one](https://en.wikipedia.org/wiki/Enigma_machine#/media/File:Enigma_keylist_3_rotor.jpg) from Wikipedia.

`python enigma/utils/code_gen.py`

The generated table will be printed. Parameters like seed, number of rotors, number of plugs, etc. can be found in that script.

Note that these fields are printed in natural language, while different representations (ASCII) are used in the generated csv.

```
-------------------------------------------------------------------
DAY     ROTORS       RINGS           PLUGS             INDICATORS  
-------------------------------------------------------------------
31    V III IV     08 24 08    LS QN PI BM ZW OC    zkl uqb uwe egk
30    II V III     12 18 04    PA BH QU ZW OI RS    lmp inj lir rds
29    III I II     15 14 21    VN JR WG BF HL IY    fje zfm aci uyn
28    II IV III    26 18 11    RY HC ZJ FV MO DN    mig cgb jlf mnd
27    II IV I      11 11 22    WG AK PC DE RM ZH    iux gsz wsf yeu
26    V II I       09 05 09    BX PW CR ZQ DL JF    sbf vtx yio lof
25    V III IV     01 03 03    OL ED RW JK SF CU    jqu xpr syd jtk
24    III V I      21 19 19    VG FS AY CO IW BT    med wmi jpu iof
23    V III I      13 19 05    JL DF SN UO TV RG    ynd tga ewd oxp
22    IV I III     24 14 25    BZ FW IS KA CT QV    qku glk wmh vsw
21    III V IV     04 13 19    FZ OD RE SY TW KJ    txk zgk qty htw
20    V IV I       13 12 05    AO FL XK SY HD ZR    kml xpt vdw bza
19    II I V       10 07 08    ES YU MI BX WF OA    oxu qpf akg rbi
18    I V II       18 17 16    LD KA VT QB UP SI    pft axn qut dbe
17    I V II       10 25 03    XG RI JV QD NF CH    lni bnp mkw wyn
16    IV I III     09 04 09    VY OK IE JU NX GA    gkm bcl ysw pzq
15    V I IV       26 10 24    CK AW GQ UB YJ IO    sjx ogn gkh coy
14    V IV II      13 19 12    YN VE KF MB JG ZX    wcz dsg hbj stv
13    V III I      07 20 26    TV DX NP QB SG ZO    rng ico drf arn
12    V I III      07 21 07    SC GY LI OD ME ZA    rts ifw jya obm
11    I II V       19 21 12    FY MO VB UP WD XJ    yxg ayx wvn dbz
10    IV V III     20 08 03    WE UY ZM DI GX QH    vks wpu gco dyw
09    IV I II      03 12 24    SB ZC EW QK AF JR    rxh dfq udw wat
08    IV II III    04 12 19    YH BN RE XD KI AZ    xcv lqo pdc udo
07    V I III      06 19 08    SA JH OF RT DW KE    brk brx zuv hqs
06    V I III      22 16 15    AN ZI DJ OT SX UL    azf uib swd szl
05    V II I       05 13 23    YN ZS IK DC WB LE    iqs gqw nuz ubm
04    II V III     01 20 13    JW RY GC LS ZU BT    fuv ifx pqa wyx
03    I V III      19 18 12    DR MI FK JU PY AQ    fwr ytl jvq lkf
02    I III II     09 17 04    JH VG KL IX RU ET    gvk rfa btf mlc
01    V IV I       16 03 17    AR ZP XO KG QV TJ    slq iqv obd nqz
-------------------------------------------------------------------
Saving csv to /CLONED_PATH/enigma/tables/default.csv...
```

We also need a machine configuration file, which can be generated using

`python enigma/utils/config_gen.py`

There is no preview for this one, but its path is printed. Both files are saved as csv file so it should be easy to preview.

```Saving csv to /CLONED_PATH/enigma/configs/default.csv...```

Finally, adjust parameters and run

`python enigma/run.py`
