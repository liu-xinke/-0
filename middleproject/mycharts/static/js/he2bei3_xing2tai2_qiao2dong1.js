(function (root, factory) {if (typeof define === 'function' && define.amd) {define(['exports', 'echarts'], factory);} else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {factory(exports, require('echarts'));} else {factory({}, root.echarts);}}(this, function (exports, echarts) {var log = function (msg) {if (typeof console !== 'undefined') {console && console.error && console.error(msg);}};if (!echarts) {log('ECharts is not Loaded');return;}if (!echarts.registerMap) {log('ECharts Map is not loaded');return;}echarts.registerMap('邢台市桥东区', {"type":"FeatureCollection","features":[{"type":"Feature","id":"130502","properties":{"name":"桥东区","cp":[114.507058,37.071287],"childNum":1},"geometry":{"type":"Polygon","coordinates":["@@@CACFA@CC@ACBA@AC@E@@C@CC@@CD@@KB@AE@AE@@A@@K@AF@BM@AB@H@BBB@FBDBBDB@B@@DB@AJ@AB@F@@@@@@A@B@@BAD@BA@@@@@@BEL@BAB@BCF@B@FB@BF@@@@CB@AG@@D@D@D@BE@@B@D@@@@@H@@@B@BBFBH@@@BBHBB@B@DBB@DBDBF@@@@@DBH@@BH@B@BB@@@@B@BH@@@@D@@E@@FBDD@BBB@F@@B@@@@BBA@@@@B@@B@@A@@@CBB@CA@BA@CC@@@@AA@@@B@@CEB@@@A@AL@BC@@D@B@@@@BD@@DH@@BB@DDH@@@BA@@@@@BBF@@@@@A@E@@@@AOBA@@B@TFF@@@D@BE@CAK@IBADA@@J@BCLA@KH@F@D@L@BD@@R@@EB@@@F@B@@CF@@@@G@E@@@EI@AGAACCEAE@BFQ@E@BFI@@CA@@@AB@BA@ABA@@BEB@BA@AG@@B@@A@CF@@AG@@AE@@BA@A@C@C@@DC@@DI@C@AAACAAA@@A@A@A@@CA@ACAE@@AJ@@A@@@A@EGA@ABAF@@ENAB@@A@AE@G@O@G@A@CA@A@A"],"encodeOffsets":[[117263,37910]]}}],"UTF8Encoding":true});}));