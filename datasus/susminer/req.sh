curl 'http://tabnet.datasus.gov.br/csv/sih_cnv_spabr202930186_207_198_136.csv' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'Connection: keep-alive' \
  #-H 'Cookie: TS014879da=01e046ca4cd7cdf315f6028d35cd39674705d6416b40de4cfc2ef5bccaa4b8ae449befe9099e97dc849dc2cede881ce4d119e6d5d4' \
  -H 'DNT: 1' \
  -H 'Referer: http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sih/cnv/spabr.def' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 X11; Linux x86_64 AppleWebKit/537.36 KHTML: like Gecko Chrome/120.0.0.0 Safari/537.36' \
  --compressed \
  --insecure