"""Test modifying EXIF attributes and getting new file contents."""

import binascii
import os
import textwrap
import unittest

from baseline import Baseline

from exif import Image

modified_noise_file = Baseline("""
    ffd8ffe000104a46494600010201004800480000ffe103a94578696600004d4d002a0000000800070112000300
    00000100010000011a00050000000100000062011b0005000000010000006a0128000300000001000200000131
    00020000001c0000007201320002000000140000008e8769000400000001000000a4000000d0000afc80000027
    10000afc8000002710507974686f6e00000000000000000000000000000000000000000000323031383a31323a
    32322032333a32323a34390000000003a00100030000000100010000a00200040000000100000006a003000400
    000001000000060000000000000006010300030000000100060000011a0005000000010000011e011b00050000
    00010000012601280003000000010002000002010004000000010000012e020200040000000100000273000000
    0000000048000000010000004800000001ffd8ffe000104a46494600010200004800480000ffed000c41646f62
    655f434d0001ffee000e41646f626500648000000001ffdb0084000c08080809080c09090c110b0a0b11150f0c
    0c0f1518131315131318110c0c0c0c0c0c110c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c
    0c010d0b0b0d0e0d100e0e10140e0e0e14140e0e0e0e14110c0c0c0c0c11110c0c0c0c0c0c110c0c0c0c0c0c0c
    0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0cffc00011080006000603012200021101031101ffdd000400
    01ffc4013f0000010501010101010100000000000000030001020405060708090a0b0100010501010101010100
    000000000000010002030405060708090a0b1000010401030204020507060805030c3301000211030421123105
    4151611322718132061491a1b14223241552c16233347282d14307259253f0e1f163733516a2b2832644935464
    45c2a3743617d255e265f2b384c3d375e3f3462794a485b495c4d4e4f4a5b5c5d5e5f55666768696a6b6c6d6e6
    f637475767778797a7b7c7d7e7f711000202010204040304050607070605350100021103213112044151617122
    130532819114a1b14223c152d1f0332462e1728292435315637334f1250616a2b283072635c2d2449354a31764
    4555367465e2f2b384c3d375e3f34694a485b495c4d4e4f4a5b5c5d5e5f55666768696a6b6c6d6e6f627374757
    67778797a7b7c7ffda000c03010002110311003f00d0babe9ff69c7165b59c1dee7d7b43db78b8179f42f7b196
    d97596d365ecc5b2fa71baad7451996d3fe129c84bc69255bd7c7fe57e4ff53fe6bff4b7f2fe75d1f5d7f94ffc
    6bdff7b8bff4bffed87fa39fffd9ffed084450686f746f73686f7020332e30003842494d04040000000000071c
    020000024000003842494d0425000000000010680e825d06f8f2a76b5514e1a59522843842494d03ed00000000
    0010004800000001000100480000000100013842494d042600000000000e000000000000000000003f80000038
    42494d040d000000000004000000783842494d04190000000000040000001e3842494d03f30000000000090000
    00000000000001003842494d271000000000000a000100000000000000023842494d03f5000000000048002f66
    660001006c66660006000000000001002f6666000100a1999a0006000000000001003200000001005a00000006
    000000000001003500000001002d000000060000000000013842494d03f80000000000700000ffffffffffffff
    ffffffffffffffffffffffffffffff03e800000000ffffffffffffffffffffffffffffffffffffffffffff03e8
    00000000ffffffffffffffffffffffffffffffffffffffffffff03e800000000ffffffffffffffffffffffffff
    ffffffffffffffffff03e800003842494d0408000000000010000000010000024000000240000000003842494d
    041e000000000004000000003842494d041a00000000033f000000060000000000000000000000060000000600
    000005006e006f0069007300650000000100000000000000000000000000000000000000010000000000000000
    000000060000000600000000000000000000000000000000010000000000000000000000000000000000000010
    000000010000000000006e756c6c0000000200000006626f756e64734f626a6300000001000000000000526374
    310000000400000000546f70206c6f6e6700000000000000004c6566746c6f6e67000000000000000042746f6d
    6c6f6e670000000600000000526768746c6f6e670000000600000006736c69636573566c4c73000000014f626a
    6300000001000000000005736c6963650000001200000007736c69636549446c6f6e6700000000000000076772
    6f757049446c6f6e6700000000000000066f726967696e656e756d0000000c45536c6963654f726967696e0000
    000d6175746f47656e6572617465640000000054797065656e756d0000000a45536c6963655479706500000000
    496d672000000006626f756e64734f626a6300000001000000000000526374310000000400000000546f70206c
    6f6e6700000000000000004c6566746c6f6e67000000000000000042746f6d6c6f6e6700000006000000005267
    68746c6f6e67000000060000000375726c54455854000000010000000000006e756c6c54455854000000010000
    000000004d7367655445585400000001000000000006616c74546167544558540000000100000000000e63656c
    6c54657874497348544d4c626f6f6c010000000863656c6c546578745445585400000001000000000009686f72
    7a416c69676e656e756d0000000f45536c696365486f727a416c69676e0000000764656661756c740000000976
    657274416c69676e656e756d0000000f45536c69636556657274416c69676e0000000764656661756c74000000
    0b6267436f6c6f7254797065656e756d0000001145536c6963654247436f6c6f7254797065000000004e6f6e65
    00000009746f704f75747365746c6f6e67000000000000000a6c6566744f75747365746c6f6e67000000000000
    000c626f74746f6d4f75747365746c6f6e67000000000000000b72696768744f75747365746c6f6e6700000000
    003842494d042800000000000c000000023ff00000000000003842494d0414000000000004000000013842494d
    040c00000000028f00000001000000060000000600000014000000780000027300180001ffd8ffe000104a4649
    4600010200004800480000ffed000c41646f62655f434d0001ffee000e41646f626500648000000001ffdb0084
    000c08080809080c09090c110b0a0b11150f0c0c0f1518131315131318110c0c0c0c0c0c110c0c0c0c0c0c0c0c
    0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c010d0b0b0d0e0d100e0e10140e0e0e14140e0e0e0e14110c0c
    0c0c0c11110c0c0c0c0c0c110c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0cffc0001108
    0006000603012200021101031101ffdd00040001ffc4013f000001050101010101010000000000000003000102
    0405060708090a0b0100010501010101010100000000000000010002030405060708090a0b1000010401030204
    020507060805030c33010002110304211231054151611322718132061491a1b14223241552c16233347282d143
    07259253f0e1f163733516a2b283264493546445c2a3743617d255e265f2b384c3d375e3f3462794a485b495c4
    d4e4f4a5b5c5d5e5f55666768696a6b6c6d6e6f637475767778797a7b7c7d7e7f7110002020102040403040506
    07070605350100021103213112044151617122130532819114a1b14223c152d1f0332462e17282924353156373
    34f1250616a2b283072635c2d2449354a317644555367465e2f2b384c3d375e3f34694a485b495c4d4e4f4a5b5
    c5d5e5f55666768696a6b6c6d6e6f62737475767778797a7b7c7ffda000c03010002110311003f00d0babe9ff6
    9c7165b59c1dee7d7b43db78b8179f42f7b196d97596d365ecc5b2fa71baad7451996d3fe129c84bc69255bd7c
    7fe57e4ff53fe6bff4b7f2fe75d1f5d7f94ffc6bdff7b8bff4bffed87fa39fffd9003842494d04210000000000
    5500000001010000000f00410064006f00620065002000500068006f0074006f00730068006f00700000001300
    410064006f00620065002000500068006f0074006f00730068006f007000200043005300340000000100384249
    4d04060000000000070008000100010100ffe11123687474703a2f2f6e732e61646f62652e636f6d2f7861702f
    312e302f003c3f787061636b657420626567696e3d22efbbbf222069643d2257354d304d7043656869487a7265
    537a4e54637a6b633964223f3e203c783a786d706d65746120786d6c6e733a783d2261646f62653a6e733a6d65
    74612f2220783a786d70746b3d2241646f626520584d5020436f726520342e322e322d633036332035332e3335
    323632342c20323030382f30372f33302d31383a31323a31382020202020202020223e203c7264663a52444620
    786d6c6e733a7264663d22687474703a2f2f7777772e77332e6f72672f313939392f30322f32322d7264662d73
    796e7461782d6e7323223e203c7264663a4465736372697074696f6e207264663a61626f75743d222220786d6c
    6e733a786d703d22687474703a2f2f6e732e61646f62652e636f6d2f7861702f312e302f2220786d6c6e733a64
    633d22687474703a2f2f7075726c2e6f72672f64632f656c656d656e74732f312e312f2220786d6c6e733a786d
    704d4d3d22687474703a2f2f6e732e61646f62652e636f6d2f7861702f312e302f6d6d2f2220786d6c6e733a73
    744576743d22687474703a2f2f6e732e61646f62652e636f6d2f7861702f312e302f73547970652f5265736f75
    7263654576656e74232220786d6c6e733a70686f746f73686f703d22687474703a2f2f6e732e61646f62652e63
    6f6d2f70686f746f73686f702f312e302f2220786d6c6e733a746966663d22687474703a2f2f6e732e61646f62
    652e636f6d2f746966662f312e302f2220786d6c6e733a657869663d22687474703a2f2f6e732e61646f62652e
    636f6d2f657869662f312e302f2220786d703a43726561746f72546f6f6c3d2241646f62652050686f746f7368
    6f70204353342057696e646f77732220786d703a437265617465446174653d22323031382d31322d3232543233
    3a30332d30353a30302220786d703a4d65746164617461446174653d22323031382d31322d32325432333a3232
    3a34392d30353a30302220786d703a4d6f64696679446174653d22323031382d31322d32325432333a32323a34
    392d30353a3030222064633a666f726d61743d22696d6167652f6a7065672220786d704d4d3a496e7374616e63
    6549443d22786d702e6969643a4139373730313638364130364539313138463133413546463234423231384636
    2220786d704d4d3a446f63756d656e7449443d22786d702e6469643a3834323938364133363730364539313141
    4142414334304131434542353735452220786d704d4d3a4f726967696e616c446f63756d656e7449443d22786d
    702e6469643a3834323938364133363730364539313141414241433430413143454235373545222070686f746f
    73686f703a436f6c6f724d6f64653d2233222070686f746f73686f703a49434350726f66696c653d2273524742
    2049454336313936362d322e312220746966663a4f7269656e746174696f6e3d22312220746966663a58526573
    6f6c7574696f6e3d223732303030302f31303030302220746966663a595265736f6c7574696f6e3d2237323030
    30302f31303030302220746966663a5265736f6c7574696f6e556e69743d22322220746966663a4e6174697665
    4469676573743d223235362c3235372c3235382c3235392c3236322c3237342c3237372c3238342c3533302c35
    33312c3238322c3238332c3239362c3330312c3331382c3331392c3532392c3533322c3330362c3237302c3237
    312c3237322c3330352c3331352c33333433323b37423443434534314437353642453631363343344341373633
    453442384635422220657869663a506978656c5844696d656e73696f6e3d22362220657869663a506978656c59
    44696d656e73696f6e3d22362220657869663a436f6c6f7253706163653d22312220657869663a4e6174697665
    4469676573743d2233363836342c34303936302c34303936312c33373132312c33373132322c34303936322c34
    303936332c33373531302c34303936342c33363836372c33363836382c33333433342c33333433372c33343835
    302c33343835322c33343835352c33343835362c33373337372c33373337382c33373337392c33373338302c33
    373338312c33373338322c33373338332c33373338342c33373338352c33373338362c33373339362c34313438
    332c34313438342c34313438362c34313438372c34313438382c34313439322c34313439332c34313439352c34
    313732382c34313732392c34313733302c34313938352c34313938362c34313938372c34313938382c34313938
    392c34313939302c34313939312c34313939322c34313939332c34313939342c34313939352c34313939362c34
    323031362c302c322c342c352c362c372c382c392c31302c31312c31322c31332c31342c31352c31362c31372c
    31382c32302c32322c32332c32342c32352c32362c32372c32382c33303b313939373037423041443037424132
    4139443534313645333230443430373843223e203c786d704d4d3a486973746f72793e203c7264663a5365713e
    203c7264663a6c692073744576743a616374696f6e3d2263726561746564222073744576743a696e7374616e63
    6549443d22786d702e6969643a3834323938364133363730364539313141414241433430413143454235373545
    222073744576743a7768656e3d22323031382d31322d32325432333a30332d30353a3030222073744576743a73
    6f6674776172654167656e743d2241646f62652050686f746f73686f70204353342057696e646f7773222f3e20
    3c7264663a6c692073744576743a616374696f6e3d227361766564222073744576743a696e7374616e63654944
    3d22786d702e6969643a4139373730313638364130364539313138463133413546463234423231384636222073
    744576743a7768656e3d22323031382d31322d32325432333a32323a34392d30353a3030222073744576743a73
    6f6674776172654167656e743d2241646f62652050686f746f73686f70204353342057696e646f777322207374
    4576743a6368616e6765643d222f222f3e203c2f7264663a5365713e203c2f786d704d4d3a486973746f72793e
    203c2f7264663a4465736372697074696f6e3e203c2f7264663a5244463e203c2f783a786d706d6574613e2020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
    202020202020202020202020202020202020202020203c3f787061636b657420656e643d2277223f3effe20c58
    4943435f50524f46494c4500010100000c484c696e6f021000006d6e74725247422058595a2007ce0002000900
    0600310000616373704d5346540000000049454320735247420000000000000000000000010000f6d600010000
    0000d32d4850202000000000000000000000000000000000000000000000000000000000000000000000000000
    000000000000000000001163707274000001500000003364657363000001840000006c77747074000001f00000
    0014626b707400000204000000147258595a00000218000000146758595a0000022c000000146258595a000002
    4000000014646d6e640000025400000070646d6464000002c400000088767565640000034c0000008676696577
    000003d4000000246c756d69000003f8000000146d6561730000040c0000002474656368000004300000000c72
    5452430000043c0000080c675452430000043c0000080c625452430000043c0000080c7465787400000000436f
    70797269676874202863292031393938204865776c6574742d5061636b61726420436f6d70616e790000646573
    630000000000000012735247422049454336313936362d322e3100000000000000000000001273524742204945
    4336313936362d322e310000000000000000000000000000000000000000000000000000000000000000000000
    00000000000000000000000000000058595a20000000000000f35100010000000116cc58595a20000000000000
    0000000000000000000058595a200000000000006fa2000038f50000039058595a2000000000000062990000b7
    85000018da58595a2000000000000024a000000f840000b6cf6465736300000000000000164945432068747470
    3a2f2f7777772e6965632e636800000000000000000000001649454320687474703a2f2f7777772e6965632e63
    680000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    000064657363000000000000002e4945432036313936362d322e312044656661756c742052474220636f6c6f75
    72207370616365202d207352474200000000000000000000002e4945432036313936362d322e31204465666175
    6c742052474220636f6c6f7572207370616365202d207352474200000000000000000000000000000000000000
    00000064657363000000000000002c5265666572656e63652056696577696e6720436f6e646974696f6e20696e
    2049454336313936362d322e3100000000000000000000002c5265666572656e63652056696577696e6720436f
    6e646974696f6e20696e2049454336313936362d322e3100000000000000000000000000000000000000000000
    0000000076696577000000000013a4fe00145f2e0010cf140003edcc0004130b00035c9e0000000158595a2000
    000000004c09560050000000571fe76d6561730000000000000001000000000000000000000000000000000000
    028f0000000273696720000000004352542063757276000000000000040000000005000a000f00140019001e00
    230028002d00320037003b00400045004a004f00540059005e00630068006d00720077007c00810086008b0090
    0095009a009f00a400a900ae00b200b700bc00c100c600cb00d000d500db00e000e500eb00f000f600fb010101
    07010d01130119011f0125012b01320138013e0145014c0152015901600167016e0175017c0183018b0192019a
    01a101a901b101b901c101c901d101d901e101e901f201fa0203020c0214021d0226022f02380241024b025402
    5d02670271027a0284028e029802a202ac02b602c102cb02d502e002eb02f50300030b03160321032d03380343
    034f035a03660372037e038a039603a203ae03ba03c703d303e003ec03f9040604130420042d043b0448045504
    630471047e048c049a04a804b604c404d304e104f004fe050d051c052b053a05490558056705770586059605a6
    05b505c505d505e505f6060606160627063706480659066a067b068c069d06af06c006d106e306f50707071907
    2b073d074f076107740786079907ac07bf07d207e507f8080b081f08320846085a086e0882089608aa08be08d2
    08e708fb09100925093a094f09640979098f09a409ba09cf09e509fb0a110a270a3d0a540a6a0a810a980aae0a
    c50adc0af30b0b0b220b390b510b690b800b980bb00bc80be10bf90c120c2a0c430c5c0c750c8e0ca70cc00cd9
    0cf30d0d0d260d400d5a0d740d8e0da90dc30dde0df80e130e2e0e490e640e7f0e9b0eb60ed20eee0f090f250f
    410f5e0f7a0f960fb30fcf0fec1009102610431061107e109b10b910d710f511131131114f116d118c11aa11c9
    11e81207122612451264128412a312c312e31303132313431363138313a413c513e5140614271449146a148b14
    ad14ce14f01512153415561578159b15bd15e0160316261649166c168f16b216d616fa171d17411765178917ae
    17d217f7181b18401865188a18af18d518fa19201945196b199119b719dd1a041a2a1a511a771a9e1ac51aec1b
    141b3b1b631b8a1bb21bda1c021c2a1c521c7b1ca31ccc1cf51d1e1d471d701d991dc31dec1e161e401e6a1e94
    1ebe1ee91f131f3e1f691f941fbf1fea20152041206c209820c420f0211c2148217521a121ce21fb2227225522
    8222af22dd230a23382366239423c223f0241f244d247c24ab24da250925382568259725c725f7262726572687
    26b726e827182749277a27ab27dc280d283f287128a228d429062938296b299d29d02a022a352a682a9b2acf2b
    022b362b692b9d2bd12c052c392c6e2ca22cd72d0c2d412d762dab2de12e162e4c2e822eb72eee2f242f5a2f91
    2fc72ffe3035306c30a430db3112314a318231ba31f2322a3263329b32d4330d3346337f33b833f1342b346534
    9e34d83513354d358735c235fd3637367236ae36e937243760379c37d738143850388c38c839053942397f39bc
    39f93a363a743ab23aef3b2d3b6b3baa3be83c273c653ca43ce33d223d613da13de03e203e603ea03ee03f213f
    613fa23fe24023406440a640e74129416a41ac41ee4230427242b542f7433a437d43c044034447448a44ce4512
    4555459a45de4622466746ab46f04735477b47c04805484b489148d7491d496349a949f04a374a7d4ac44b0c4b
    534b9a4be24c2a4c724cba4d024d4a4d934ddc4e254e6e4eb74f004f494f934fdd5027507150bb51065150519b
    51e65231527c52c75313535f53aa53f65442548f54db5528557555c2560f565c56a956f75744579257e0582f58
    7d58cb591a596959b85a075a565aa65af55b455b955be55c355c865cd65d275d785dc95e1a5e6c5ebd5f0f5f61
    5fb36005605760aa60fc614f61a261f56249629c62f06343639763eb6440649464e9653d659265e7663d669266
    e8673d679367e9683f689668ec6943699a69f16a486a9f6af76b4f6ba76bff6c576caf6d086d606db96e126e6b
    6ec46f1e6f786fd1702b708670e0713a719571f0724b72a67301735d73b87414747074cc7528758575e1763e76
    9b76f8775677b37811786e78cc792a798979e77a467aa57b047b637bc27c217c817ce17d417da17e017e627ec2
    7f237f847fe5804780a8810a816b81cd8230829282f4835783ba841d848084e3854785ab860e867286d7873b87
    9f8804886988ce8933899989fe8a648aca8b308b968bfc8c638cca8d318d988dff8e668ece8f368f9e9006906e
    90d6913f91a89211927a92e3934d93b69420948a94f4955f95c99634969f970a977597e0984c98b89924999099
    fc9a689ad59b429baf9c1c9c899cf79d649dd29e409eae9f1d9f8b9ffaa069a0d8a147a1b6a226a296a306a376
    a3e6a456a4c7a538a5a9a61aa68ba6fda76ea7e0a852a8c4a937a9a9aa1caa8fab02ab75abe9ac5cacd0ad44ad
    b8ae2daea1af16af8bb000b075b0eab160b1d6b24bb2c2b338b3aeb425b49cb513b58ab601b679b6f0b768b7e0
    b859b8d1b94ab9c2ba3bbab5bb2ebba7bc21bc9bbd15bd8fbe0abe84beffbf7abff5c070c0ecc167c1e3c25fc2
    dbc358c3d4c451c4cec54bc5c8c646c6c3c741c7bfc83dc8bcc93ac9b9ca38cab7cb36cbb6cc35ccb5cd35cdb5
    ce36ceb6cf37cfb8d039d0bad13cd1bed23fd2c1d344d3c6d449d4cbd54ed5d1d655d6d8d75cd7e0d864d8e8d9
    6cd9f1da76dafbdb80dc05dc8add10dd96de1cdea2df29dfafe036e0bde144e1cce253e2dbe363e3ebe473e4fc
    e584e60de696e71fe7a9e832e8bce946e9d0ea5beae5eb70ebfbec86ed11ed9cee28eeb4ef40efccf058f0e5f1
    72f1fff28cf319f3a7f434f4c2f550f5def66df6fbf78af819f8a8f938f9c7fa57fae7fb77fc07fc98fd29fdba
    fe4bfedcff6dffffffee000e41646f626500644000000001ffdb00840001010101010101010101010101010101
    010101010101010101010101010101010101010101010101010101020202020202020202020203030303030303
    030303010101010101010101010102020102020303030303030303030303030303030303030303030303030303
    0303030303030303030303030303030303030303030303ffc00011080006000603011100021101031101ffdd00
    040001ffc4005c0001000000000000000000000000000000080101010000000000000000000000000000070810
    010002030003000000000000000000000605070304080102151100020301010003000000000000000000030504
    06070208011213ffda000c03010002110311003f005e313b4179b16a5c081f01d8e71cce50a819ef031f631be8
    082bc2126d76f69d616a20364df35b21939add82c8a032ca0e88e80892a5d84b4364cd93e8c2a102b3b1f46b3a
    2e64aded23d34b7575d167ad5d2bab0bf37c358a4fbf1d58824254c91802114ec4921741550e302acba315ec76
    616f56809ad91d9b5e02f65a1e959aeb9dfa58f7982a69b51653661aa62b0f115a46b0d9ab56056581362e6669
    9f9b0742b201de77ca310451eb5c5558a18c8fffd9
    """)


class TestGetFile(unittest.TestCase):

    def setUp(self):
        noise = os.path.join(os.path.dirname(__file__), 'noise.jpg')
        with open(noise, 'rb') as image_file:
            self.image = Image(image_file)

    def test_get_file(self):
        self.image.software = "Python"
        file_hex = binascii.hexlify(self.image.get_file())
        self.assertEqual('\n'.join(textwrap.wrap(file_hex, 90)), modified_noise_file)