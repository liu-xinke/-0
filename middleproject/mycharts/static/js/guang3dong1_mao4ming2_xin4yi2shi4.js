(function (root, factory) {if (typeof define === 'function' && define.amd) {define(['exports', 'echarts'], factory);} else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {factory(exports, require('echarts'));} else {factory({}, root.echarts);}}(this, function (exports, echarts) {var log = function (msg) {if (typeof console !== 'undefined') {console && console.error && console.error(msg);}};if (!echarts) {log('ECharts is not Loaded');return;}if (!echarts.registerMap) {log('ECharts Map is not loaded');return;}echarts.registerMap('信宜市', {"type":"FeatureCollection","features":[{"type":"Feature","id":"440983","properties":{"name":"信宜市","cp":[110.947043,22.354385],"childNum":1},"geometry":{"type":"Polygon","coordinates":["@@AB@@@@A@@@@BA@@@CDABCD@@EBCBC@A@KHMFC@CB@BDDBBBBAB@BABEBCBG@ECAE@CGCA@E@C@ABAB@BEFEDC@C@EAECEECCA@E@GDADADOHGD@PAFAHDFFFDDDBBBDFDHBBBBDDDD@BBB@BBBBFBDDBBB@BABC@EBC@CBCFCFEDCDDDBDDD@D@DABEFYB@XCJABINCBADCDABA@C@CBABCBABA@@D@B@D@BAB@DBDBD@B@DGNCFAFAFABID@@GBCDC@CAAAACAEC@A@ABABAD@BCBCDED@BADAD@HBHBBDBAJ@F@FEF@@CHAB@FB@@BDBBFDDBDBF@BAV@B@N@DADCDCDABABI@C@GBA@ABAD@NABCBCDADA@@BAFCL@BB@@BDDDBD@B@FADAFCFGHGDAFAFCFAH@B@B@H@F@FBFBH@FBBBJP@@@F@@GNEJAB@BDHAB@D@DBDBBDBBDBD@B@D@D@BDFDDD@DBFAH@@@BBB@AD@@CHCF@BADAB@BCD@D@BDHDF@D@B@BABCBCBEDCF@@@B@@BBHBPDFL@DAHAHADAF@DDDBA@@DAD@D@BB@BBDBBF@HC@ABABEDC@@DCFAFCFCBC@CDMFGB@DBD@DB@@@D@B@B@D@DBHFFDDHDBBF@BBD@FBFBBB@BHBDBJ@D@FADAFAH@DBDDDDB@DADAB@DBFADAJCJ@JBJHLJ@@A@BHBFAFCDAF@F@B@@BFB@B@HAH@@@D@FAFADBH@FAD@FCHAH@H@D@JDB@FBHDFFBBBDBB@DBB@BBD@HADCF@BBBD@J@BBF@BBFDFBF@D@F@B@DA@GB@FCBAB@DCD@@BBD@BDDDBFBB@DBBB@B@BBD@BD@B@DBB@BB@@DBBBD@BBD@BBD@BABC@ABAB@DABAB@DBBB@BBBD@B@D@D@D@DBDAD@B@BBBBBBBDB@@B@B@B@@@B@B@@BB@DAB@B@@@B@@B@BB@BB@D@D@B@BAB@BBD@BBBBBBBB@B@BBB@B@BBDBBDDBDB@BB@@BD@DBBBB@@D@@B@B@B@D@@D@F@B@D@B@B@BBF@B@@@B@@BAB@DBDBDDB@BD@B@BAB@D@B@D@B@@ABADB@@B@BA@@@C@@AABAB@@A@AB@BABABCD@@ABABABAB@DABA@A@@AA@ABC@A@C@A@@@A@CA@AAAACCEEA@@A@@@ABABA@A@A@A@@BABA@ABG@CBADA@CBCAA@A@@BA@@B@BCDA@@DA@ABC@CB@@C@CAA@A@C@@@AD@B@DAD@B@FCBABAB@F@B@BADEDCDCBCBADEDAB@B@DAD@D@B@DAB@@BBBB@B@B@B@BBBB@@BAB@BB@@@B@BB@B@DADC@ABB@A@@BA@AB@@AB@DA@A@A@A@CBABAD@F@BAB@BABC@@BA@A@C@A@AB@B@B@DAD@@@B@D@B@D@BAB@FAB@B@D@@BBBDBBA@@BAB@B@D@@BBDBBBBBBD@B@B@DBDBD@B@DBB@DBD@@AD@D@D@D@DAB@B@@ADAF@B@B@@A@A@@BAB@B@B@@AB@BCB@B@B@B@BADA@@BA@A@C@@@ABA@@A@@AA@@AA@BABC@ADADADA@AB@FCDADCFABADAD@DA@@@A@A@A@A@AAAA@AAAAC@C@C@A@C@CA@@ABA@A@AAA@AAA@C@C@A@C@CBA@CA@CAA@CAA@AAC@C@CAA@AA@@AAA@CACAC@AAAA@@@CA@AAAAAA@CA@A@C@AACAAAA@AACAA@CACBC@C@AB@BC@A@AB@BABABBDB@DBB@B@BBBB@BBB@B@@CBABCBBBBBBBD@D@DBBBBB@B@D@@@B@B@DBB@D@BBB@DDBB@@BBBAB@DAB@D@@@BDBB@DDB@@BB@@BAB@D@D@B@B@BBBBFD@DB@BBB@B@BA@A@ABAB@B@BA@ABCBA@AB@@CBABA@ABAB@@@BBBB@@BADABBD@B@BD@BB@DB@@FDHBHBB@@ADA@ABADA@BB@BCB@BABBB@BBDBBBB@@@B@BABB@@BBB@B@B@B@B@@AB@BB@@BBBB@@D@@AB@@AB@@@B@B@FADA@@@@BCAA@A@CBAAAAA@EAE@CAC@C@@AAAA@AACAAAACA@@AEBABCBAB@B@BC@AC@BA@AB@BCAC@@@CBABA@C@@AC@A@A@ABABA@@AABA@AB@@A@AB@BADAB@B@DBB@BCAAAA@E@AAA@C@CA@AAAA@CBC@ADAB@@CBAD@B@BABB@@@BD@B@B@BAB@BB@BB@B@@AB@B@D@BB@BAB@BB@@BB@BDB@BHBB@BBDBBDAD@F@H@DBDBB@B@BCF@D@D@BDBD@DDFDB@B@D@@BBB@BB@BBBAD@@A@C@AB@DAB@D@BCB@DBB@B@BABBD@DBBB@BB@BAB@@ABA@@D@@ABCAABABBBAB@DB@BBBBBB@BB@B@B@B@@DBB@BD@BB@FBBDBDBB@D@DCBABA@ADAB@@@BAB@BABA@@B@B@D@BABABAB@B@BC@AB@BABAB@BAD@@ABABA@A@A@@DA@AD@D@BAB@DBBBBBBBB@BD@BBBB@B@@B@D@@B@@BBBB@BBBB@B@BBBDBDBBBAB@B@@AB@B@D@B@B@B@B@BBD@B@D@@A@@BBBBBD@BBB@BBD@HBBBB@B@B@@BAD@BA@@@@@@B@BDBBBBBBDDBBBDB@BBBAB@@BBDBFBB@DBBBDBDB@BD@D@DBDBBBFBB@B@BABAB@DBD@D@DABABAB@BA@ABC@A@A@AAA@A@AAA@A@A@AB@BBBBBBB@BADABAA@A@@A@@@A@AB@@A@@AA@A@A@AB@BA@A@AA@AAAAB@D@@@B@D@@@@AAE@C@CAC@CA@EA@AA@BAB@@CBA@CBA@ABA@@@AB@BBBBAB@B@BDDBB@DBB@B@B@BD@BAD@DC@@@@AA@ABABABABAD@BADB@ABAB@D@B@BB@@BA@CB@B@BBB@B@D@BBD@BB@BB@BAD@B@D@B@BBB@B@BBD@@@BABA@ABABA@@BAB@BA@@@CAA@A@ABABA@CAA@A@A@AB@BC@@AC@A@CB@BA@C@CBABA@A@EAECC@AAA@A@CAA@@AAA@CE@@A@CAAA@A@A@ACACAAAAAAA@@@CAC@@AAA@ACCAA@AAAABAAAA@AAACA@AAAAA@AE@@A@A@AA@AAA@AAA@AAAAACCCCAAAACAAAAA@A@ABAAAA@@@CAEACAACCAAAAC@AAA@AA@CB@BABA@A@C@A@A@@@@C@AA@A@ACCECG@C@EBAAAA@@AAAAACAA@A@AAC@CBCBC@E@CBCBA@C@ABA@ABA@AAA@C@A@AA@AA@CC@A@@AAA@E@CC@@CAAA@@ABCBA@ABC@C@A@@@AAGE@@A@AAA@A@AAAA@AACABA@CBC@ABC@AB@B@BAB@BC@A@CE@AAA@C@@AA@CAG@AACGEAAC@CC@@CCEAEA@@ACAC@CCAA@C@AAABA@ADA@C@A@CAC@@A@AA@CBA@A@A@CAAAAAA@BABABA@A@@@@@@@ACAAA@A@@AAAC@CAACG@@@AAAA@A@A@EA@@@ABAB@DAB@@@B@@@BA@@B@@ABA@AB@B@@@BAA@@AA@A@CCAC@E@@BA@CAAAA@C@EA@@ABAACA@@@@A@AB@BBBA@A@A@A@@AC@ACAA@A@AACBA@@BA@@@A@@@ABCAA@A@@@ABA@GDGBA@@@@@AAAAA@C@A@CAA@A@A@CCA@AAAC@AAA@A@A@AC@CA@CA@A@AAAAA@A@@BA@@A@@@AA@AACCAAAA@@EAGA@@GBA@@A@A@A@@@AAAAAABAAA@A@AB@BA@ABABABCB@B@@A@ABABA@A@@B@B@B@BB@@B@@BBB@BB@B@@@@@BBD@BABAB@B@BCBA@AB@@BBB@B@B@@B@@AB@@@DAB@BABABAB@B@@@B@BABABAB@BA@A@AB@@C@@@A@A@A@A@CBAAABA@@@AB@@CBA@ABABAB@@A@A@AB@BABA@@B@@@DCDABA@@BADA@CDABC@A@AAAAAAA@A@C@A@C@C@AACBAAA@CAC@C@CAECCAAAAA@CAAAAAA@A@@C@@@AA@A@@AACAAA@ABA@C@AAAAAAA@ABA@AA@AA@AA@A@A@A@C@A@ACA@A@A@ABAAAA@@@AAA@AB@BA@AAAAAA@@B@BABA@A@C@@AC@CAABA@@B@@@F@@AB@BA@@@ADCBCB@BA@AD@B@DAB@@BBAB@@A@A@C@A@C@A@AB@AAA@A@CA@AA@A@A@@CAA@ABC@AB@BA@@B@BAB@@AA@@AA@AA@AAAAA@CC@AAAAC@A@@B@@A@ABAA@A@@A@@@@CA@AAA@AA@@AA@A@@@CA@AAAA@CB@@C@ABA@@AA@@@C@AAAAA@@@AAAAABA@A@A@A@@@A@A@AAA@ABA@@@@B@B@B@DCBADA@AA@AAAAA@A@@AA@@A@A@AAA@A@A@AAA@CAA@GAAAABC@A@AB@B@@C@@A@@A@AAACAAC@@@A@A@@@A@A@A@A@ABA@A@@ACEA@@@A@AAAA@AA@AAABAAA@A@@AA@A@AB@BA@@@AB@BA@AB@@AB@@@BA@A@@@@AA@AA@A@@BA@A@@A@A@A@CAA@A@AAA@CAA@AACAA@AB@@AAA@@BA@@@A@A@@A@AAA@AAAABABA@@@AAA@A@A@A@AAC@A@AAAAA@@AA@AB@BBB@BAD@@ADA@@BB@A@@BA@A@@BA@@BA@A@CBA@@@@B@B@D@@AB@@@BAB@BAB@@AB@@A@CAA@@B@B@BAB@BABA@@AAB@@C@@@ABABABAB@@@AA@@@BA@A@@AA@AB@@CAA@A@@AAA@@AAAA@@@@AAA@AAAA@CAA@AABA@A@A@@AAAAA@A@A@@AA@A@@@A@A@AA@@AAAA@@AA@AAAC@A@CAAAAA@AAAAAAC@@AAAAA@AAC@@@ABA@@@A@A@G@MBCBCDGDEBCACAACCCEAC@O@GBGBGCECACCCCE@@CIEECAEACAAAGAGBCBCBC@A@AAAA@AAEAKCIGCGDGJEBC@I@CAAA@AFOAA@@EEG@A@IHAB@@@@"],"encodeOffsets":[[113537,22723]]}}],"UTF8Encoding":true});}));