import os
import urllib.request

os.makedirs("img", exist_ok=True)

bandeiras = {
    "ac.svg": "https://upload.wikimedia.org/wikipedia/commons/4/4c/Bandeira_do_Acre.svg",
    "ap.svg": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Bandeira_do_Amap%C3%A1.svg",
    "am.svg": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Bandeira_do_Amazonas.svg",
    "pa.svg": "https://upload.wikimedia.org/wikipedia/commons/0/02/Bandeira_do_Par%C3%A1.svg",
    "ro.svg": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Bandeira_de_Rond%C3%B4nia.svg",
    "rr.svg": "https://upload.wikimedia.org/wikipedia/commons/9/98/Bandeira_de_Roraima.svg",
    "to.svg": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Bandeira_do_Tocantins.svg",
    "al.svg": "https://upload.wikimedia.org/wikipedia/commons/8/88/Bandeira_de_Alagoas.svg",
    "ba.svg": "https://upload.wikimedia.org/wikipedia/commons/2/28/Bandeira_da_Bahia.svg",
    "ce.svg": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Bandeira_do_Cear%C3%A1.svg",
    "ma.svg": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Bandeira_do_Maranh%C3%A3o.svg",
    "pb.svg": "https://upload.wikimedia.org/wikipedia/commons/b/bb/Bandeira_da_Para%C3%ADba.svg",
    "pe.svg": "https://upload.wikimedia.org/wikipedia/commons/5/59/Bandeira_de_Pernambuco.svg",
    "pi.svg": "https://upload.wikimedia.org/wikipedia/commons/3/33/Bandeira_do_Piau%C3%AD.svg",
    "rn.svg": "https://upload.wikimedia.org/wikipedia/commons/3/30/Bandeira_do_Rio_Grande_do_Norte.svg",
    "se.svg": "https://upload.wikimedia.org/wikipedia/commons/b/be/Bandeira_de_Sergipe.svg",
    "df.svg": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Bandeira_do_Distrito_Federal_%28Brasil%29.svg",
    "go.svg": "https://upload.wikimedia.org/wikipedia/commons/b/be/Bandeira_de_Goi%C3%A1s.svg",
    "mt.svg": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Bandeira_de_Mato_Grosso.svg",
    "ms.svg": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Bandeira_de_Mato_Grosso_do_Sul.svg",
    "pr.svg": "https://upload.wikimedia.org/wikipedia/commons/9/93/Bandeira_do_Paran%C3%A1.svg",
    "rs.svg": "https://upload.wikimedia.org/wikipedia/commons/6/63/Bandeira_do_Rio_Grande_do_Sul.svg",
    "sc.svg": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Bandeira_de_Santa_Catarina.svg",
    "es.svg": "https://upload.wikimedia.org/wikipedia/commons/1/12/Bandeira_do_Esp%C3%ADrito_Santo.svg",
    "mg.svg": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Bandeira_de_Minas_Gerais.svg",
    "rj.svg": "https://upload.wikimedia.org/wikipedia/commons/7/73/Bandeira_do_estado_do_Rio_de_Janeiro.svg",
    "sp.svg": "https://upload.wikimedia.org/wikipedia/commons/5/54/Bandeira_do_estado_de_S%C3%A3o_Paulo.svg"
}

for arquivo, url in bandeiras.items():
    destino = os.path.join("img", arquivo)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(destino, "wb") as out:
        out.write(resp.read())
    print(f"Baixado: {destino}")
