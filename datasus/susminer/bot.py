import requests
from bs4 import BeautifulSoup

url = "http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sih/cnv/spabr.def"

payload = "{\"data-raw\":\"Linha=Munic%EDpio&Coluna=Grupo_procedimento&Incremento=Quantidade_aprovada&Arquivos=spabr0809.dbf&pesqmes1=Digite+o+texto+e+ache+f%E1cil&SMunic%EDpio=TODAS_AS_CATEGORIAS__&pesqmes2=Digite+o+texto+e+ache+f%E1cil&SCapital=TODAS_AS_CATEGORIAS__&pesqmes3=Digite+o+texto+e+ache+f%E1cil&SRegi%E3o_de_Sa%FAde_%28CIR%29=TODAS_AS_CATEGORIAS__&pesqmes4=Digite+o+texto+e+ache+f%E1cil&SMacrorregi%E3o_de_Sa%FAde=TODAS_AS_CATEGORIAS__&pesqmes5=Digite+o+texto+e+ache+f%E1cil&SMicrorregi%E3o_IBGE=TODAS_AS_CATEGORIAS__&pesqmes6=Digite+o+texto+e+ache+f%E1cil&SRegi%E3o_Metropolitana_-_RIDE=TODAS_AS_CATEGORIAS__&pesqmes7=Digite+o+texto+e+ache+f%E1cil&STerrit%F3rio_da_Cidadania=TODAS_AS_CATEGORIAS__&pesqmes8=Digite+o+texto+e+ache+f%E1cil&SMesorregi%E3o_PNDR=TODAS_AS_CATEGORIAS__&SAmaz%F4nia_Legal=TODAS_AS_CATEGORIAS__&SSemi%E1rido=TODAS_AS_CATEGORIAS__&SFaixa_de_Fronteira=TODAS_AS_CATEGORIAS__&SZona_de_Fronteira=TODAS_AS_CATEGORIAS__&SMunic%EDpio_de_extrema_pobreza=TODAS_AS_CATEGORIAS__&pesqmes14=Digite+o+texto+e+ache+f%E1cil&SProcedimento_Principal=TODAS_AS_CATEGORIAS__&SGrupo_Procedimento_Principal=TODAS_AS_CATEGORIAS__&pesqmes16=Digite+o+texto+e+ache+f%E1cil&SSubgrupo_Proced.Principal=TODAS_AS_CATEGORIAS__&pesqmes17=Digite+o+texto+e+ache+f%E1cil&SForma_organiza%E7%E3o_Principal=TODAS_AS_CATEGORIAS__&pesqmes18=Digite+o+texto+e+ache+f%E1cil&SProcedimento=TODAS_AS_CATEGORIAS__&SGrupo_procedimento=TODAS_AS_CATEGORIAS__&pesqmes20=Digite+o+texto+e+ache+f%E1cil&SSubgrupo_proced.=TODAS_AS_CATEGORIAS__&pesqmes21=Digite+o+texto+e+ache+f%E1cil&SForma_organiza%E7%E3o=TODAS_AS_CATEGORIAS__&SComplexidade=TODAS_AS_CATEGORIAS__&STipo_de_Financiamento=TODAS_AS_CATEGORIAS__&pesqmes24=Digite+o+texto+e+ache+f%E1cil&SSubTipo_de_Financiamento=TODAS_AS_CATEGORIAS__&pesqmes25=Digite+o+texto+e+ache+f%E1cil&SServi%E7o%2FClassifica%E7%E3o=TODAS_AS_CATEGORIAS__&SCBO_do_Profissional=TODAS_AS_CATEGORIAS__&zeradas=exibirlz&formato=table&mostre=Mostra\"}"
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  # 'Cookie': 'TS014879da=01e046ca4c445832e6f2cfb8df59fc3595c3c6f8c62e94977c4cb3bb5c81d260d639d01408f73fbbaa6974d28b7a6f93347c58fac3; TS014879da=01e046ca4cc962acf44854618d460670689b95a0bd4cf7fe0b31dc126280d02900f4a74385c4f5b3c5d9f623dbdc872d70dcead90e',
  'DNT': '1',
  'Origin': 'http://tabnet.datasus.gov.br',
  'Referer': 'http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/spabr.def',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 X11; Linux x86_64 AppleWebKit/537.36 KHTML: like Gecko Chrome/120.0.0.0 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload)

soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar a tag 'A' dentro da tag 'td'
tag_a = soup.find('td', class_='botao_opcao').find('a')

# Extrair o HREF e o texto da tag 'A'
href = tag_a['href']
texto = tag_a.get_text(strip=True)

print("HREF:", href)
print("Texto:", texto)


