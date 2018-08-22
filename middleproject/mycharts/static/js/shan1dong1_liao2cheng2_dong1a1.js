(function (root, factory) {if (typeof define === 'function' && define.amd) {define(['exports', 'echarts'], factory);} else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {factory(exports, require('echarts'));} else {factory({}, root.echarts);}}(this, function (exports, echarts) {var log = function (msg) {if (typeof console !== 'undefined') {console && console.error && console.error(msg);}};if (!echarts) {log('ECharts is not Loaded');return;}if (!echarts.registerMap) {log('ECharts Map is not loaded');return;}echarts.registerMap('东阿县', {"type":"FeatureCollection","features":[{"type":"Feature","id":"371524","properties":{"name":"东阿县","cp":[116.247579,36.334917],"childNum":1},"geometry":{"type":"Polygon","coordinates":["@@GACAECCC@CAEQFMDOBABGBIBIFCBKJ@HAL@BAL@DCR@FEN@B@BINADM@@JHFB@FBBF@D@@BFNNDDDFDDFFFHBDDFFPBJABAF@J@BABC@@B@L@DADC@@@@F@BB@@BCLAFCH@FD@@B@@@D@DBDfAB@@DBADABDBJBDBDBBHABBD@B@@C@AFCDABAFABABAHGHEBCBAFALAPBTFB@XFFBLFJFAF@DBD@BAD@BEFABCB@B@BFFFHHBDDFFDF@FCJ@BCJAF@D@BBBDBH@BBBBDJFJDH@BADEDCBAB@BCFHFJBB@RJJCD@HDDANELBNLDALCPLDNDFB@BDLF@@HBPN@@@@DBDD@@@@JLBBFFLHBBH@JBJBFBJBRHBBDDFDB@FFFDJHANALAB@RPNHDVJ@@BDX\\BDB@BBDHDFDDFFFD@BBADAHALCNAHCFCFAHEHIFCHGDCFC@AB@DCHMBCDI@G@A@GCICG@EBGJKX@@@B@DAL@BB@@BBB@BBBBBBB@@@BB@@@@@@B@@ABADCLANABA@@AAACD@@EDAFBBA@AAEAC@@@@AA@ADEB@DCDABB@@LG@@@ADBB@TJD@BA@AGQF@@C@@BA@@@@@@HDFDD@BCEKBAAAA@BACAAAA@GKCEA@@AEGACACCCICGA@@AAIIAA@@GECCGE@AGG@CCE@ACIAAAAECCE@@CIAGAAECC@ODGBQ@@@M@CAC@CE@@AAEKCKEEA@MAA@KBM@@@C@O@MCOG@@CAGCIECAICUEOCAAGA@@OCEAICGC@@CAMIMMACCCCE@@CKCKCCGGAAEEGEAA@@EEEGEI@MCCACAAAAOMGCAAGCGECCAAKKCCAAAAAAA@@ACCAC@@GGACAA@AIE@AECAACA@@@@C@GCIAQBG@C@A@C@O@IBE@U@GCAA@I@E@@DQCKUESAMAEAGACAAA"],"encodeOffsets":[[118915,37005]]}}],"UTF8Encoding":true});}));