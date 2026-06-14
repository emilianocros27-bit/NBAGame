#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera medias.json y medias.csv con los 150 jugadores: nombre, equipo,
media (OVR) NBA 2K26, posicion, rareza y ruta de la foto.
Medias de estrellas = Top 100 oficial 2K26. Roleros = mejor valor actual recopilado."""
import os, json, csv

BASE = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.join(BASE, "fotos-nba")

# slug -> (Nombre, OVR, posicion)
DATA = {
    # 01 Oklahoma City Thunder
    "shai-gilgeous-alexander": ("Shai Gilgeous-Alexander", 98, "PG"),
    "jalen-williams": ("Jalen Williams", 90, "SF"),
    "chet-holmgren": ("Chet Holmgren", 88, "C"),
    "isaiah-hartenstein": ("Isaiah Hartenstein", 82, "C"),
    "luguentz-dort": ("Luguentz Dort", 81, "SG"),
    # 02 New York Knicks
    "jalen-brunson": ("Jalen Brunson", 93, "PG"),
    "karl-anthony-towns": ("Karl-Anthony Towns", 92, "C"),
    "og-anunoby": ("OG Anunoby", 85, "SF"),
    "mikal-bridges": ("Mikal Bridges", 84, "SF"),
    "mitchell-robinson": ("Mitchell Robinson", 80, "C"),
    # 03 Denver Nuggets
    "nikola-jokic": ("Nikola Jokic", 98, "C"),
    "jamal-murray": ("Jamal Murray", 86, "PG"),
    "cameron-johnson": ("Cameron Johnson", 83, "SF"),
    "aaron-gordon": ("Aaron Gordon", 82, "PF"),
    "christian-braun": ("Christian Braun", 80, "SG"),
    # 04 Orlando Magic
    "paolo-banchero": ("Paolo Banchero", 89, "PF"),
    "franz-wagner": ("Franz Wagner", 86, "SF"),
    "desmond-bane": ("Desmond Bane", 83, "SG"),
    "jalen-suggs": ("Jalen Suggs", 82, "SG"),
    "wendell-carter-jr": ("Wendell Carter Jr.", 80, "C"),
    # 05 Houston Rockets
    "kevin-durant": ("Kevin Durant", 93, "SF"),
    "alperen-sengun": ("Alperen Sengun", 87, "C"),
    "amen-thompson": ("Amen Thompson", 87, "PG"),
    "jabari-smith-jr": ("Jabari Smith Jr.", 80, "PF"),
    "dorian-finney-smith": ("Dorian Finney-Smith", 75, "SF"),
    # 06 Minnesota Timberwolves
    "anthony-edwards": ("Anthony Edwards", 95, "SG"),
    "julius-randle": ("Julius Randle", 86, "PF"),
    "rudy-gobert": ("Rudy Gobert", 84, "C"),
    "jaden-mcdaniels": ("Jaden McDaniels", 82, "PF"),
    "mike-conley": ("Mike Conley", 77, "PG"),
    # 07 LA Clippers
    "kawhi-leonard": ("Kawhi Leonard", 92, "SF"),
    "james-harden": ("James Harden", 89, "PG"),
    "ivica-zubac": ("Ivica Zubac", 87, "C"),
    "john-collins": ("John Collins", 82, "PF"),
    "bradley-beal": ("Bradley Beal", 77, "SG"),
    # 08 Golden State Warriors
    "stephen-curry": ("Stephen Curry", 94, "PG"),
    "jimmy-butler": ("Jimmy Butler", 87, "SF"),
    "draymond-green": ("Draymond Green", 81, "PF"),
    "brandin-podziemski": ("Brandin Podziemski", 78, "SG"),
    "al-horford": ("Al Horford", 77, "C"),
    # 09 Atlanta Hawks
    "trae-young": ("Trae Young", 90, "PG"),
    "dyson-daniels": ("Dyson Daniels", 83, "SG"),
    "jalen-johnson": ("Jalen Johnson", 81, "PF"),
    "onyeka-okongwu": ("Onyeka Okongwu", 81, "C"),
    "zaccharie-risacher": ("Zaccharie Risacher", 77, "SF"),
    # 10 Los Angeles Lakers
    "luka-doncic": ("Luka Doncic", 95, "PG"),
    "lebron-james": ("LeBron James", 94, "SF"),
    "austin-reaves": ("Austin Reaves", 85, "SG"),
    "rui-hachimura": ("Rui Hachimura", 81, "PF"),
    "deandre-ayton": ("Deandre Ayton", 79, "C"),
    # 11 Dallas Mavericks
    "anthony-davis": ("Anthony Davis", 93, "PF"),
    "cooper-flagg": ("Cooper Flagg", 82, "SF"),
    "daniel-gafford": ("Daniel Gafford", 80, "C"),
    "klay-thompson": ("Klay Thompson", 79, "SG"),
    "dangelo-russell": ("D'Angelo Russell", 76, "PG"),
    # 12 San Antonio Spurs
    "victor-wembanyama": ("Victor Wembanyama", 97, "C"),
    "deaaron-fox": ("De'Aaron Fox", 85, "PG"),
    "devin-vassell": ("Devin Vassell", 82, "SG"),
    "stephon-castle": ("Stephon Castle", 82, "SG"),
    "harrison-barnes": ("Harrison Barnes", 77, "SF"),
    # 13 Cleveland Cavaliers
    "donovan-mitchell": ("Donovan Mitchell", 93, "SG"),
    "evan-mobley": ("Evan Mobley", 89, "PF"),
    "jarrett-allen": ("Jarrett Allen", 84, "C"),
    "deandre-hunter": ("De'Andre Hunter", 79, "SF"),
    "sam-merrill": ("Sam Merrill", 77, "SG"),
    # 14 Detroit Pistons
    "cade-cunningham": ("Cade Cunningham", 92, "PG"),
    "ausar-thompson": ("Ausar Thompson", 82, "SF"),
    "jalen-duren": ("Jalen Duren", 82, "C"),
    "jaden-ivey": ("Jaden Ivey", 81, "SG"),
    "tobias-harris": ("Tobias Harris", 80, "PF"),
    # 15 Indiana Pacers
    "pascal-siakam": ("Pascal Siakam", 89, "PF"),
    "bennedict-mathurin": ("Bennedict Mathurin", 82, "SG"),
    "aaron-nesmith": ("Aaron Nesmith", 81, "SF"),
    "andrew-nembhard": ("Andrew Nembhard", 81, "PG"),
    "isaiah-jackson": ("Isaiah Jackson", 74, "C"),
    # 16 Toronto Raptors
    "scottie-barnes": ("Scottie Barnes", 85, "SF"),
    "brandon-ingram": ("Brandon Ingram", 84, "SF"),
    "rj-barrett": ("RJ Barrett", 82, "SG"),
    "immanuel-quickley": ("Immanuel Quickley", 81, "PG"),
    "jakob-poeltl": ("Jakob Poeltl", 80, "C"),
    # 17 Memphis Grizzlies
    "ja-morant": ("Ja Morant", 91, "PG"),
    "jaren-jackson-jr": ("Jaren Jackson Jr.", 89, "PF"),
    "santi-aldama": ("Santi Aldama", 81, "PF"),
    "jaylen-wells": ("Jaylen Wells", 79, "SF"),
    "kentavious-caldwell-pope": ("Kentavious Caldwell-Pope", 76, "SG"),
    # 18 Philadelphia 76ers
    "joel-embiid": ("Joel Embiid", 92, "C"),
    "tyrese-maxey": ("Tyrese Maxey", 86, "PG"),
    "paul-george": ("Paul George", 81, "SF"),
    "quentin-grimes": ("Quentin Grimes", 78, "SG"),
    "vj-edgecombe": ("VJ Edgecombe", 76, "SG"),
    # 19 Sacramento Kings
    "domantas-sabonis": ("Domantas Sabonis", 87, "C"),
    "demar-derozan": ("DeMar DeRozan", 85, "SF"),
    "zach-lavine": ("Zach LaVine", 85, "SG"),
    "keegan-murray": ("Keegan Murray", 79, "PF"),
    "dennis-schroder": ("Dennis Schroder", 77, "PG"),
    # 20 Boston Celtics
    "jaylen-brown": ("Jaylen Brown", 90, "SF"),
    "derrick-white": ("Derrick White", 87, "SG"),
    "payton-pritchard": ("Payton Pritchard", 82, "PG"),
    "neemias-queta": ("Neemias Queta", 79, "C"),
    "sam-hauser": ("Sam Hauser", 78, "SF"),
    # 21 New Orleans Pelicans
    "zion-williamson": ("Zion Williamson", 87, "PF"),
    "trey-murphy-iii": ("Trey Murphy III", 82, "SF"),
    "herbert-jones": ("Herbert Jones", 81, "SF"),
    "yves-missi": ("Yves Missi", 77, "C"),
    "jordan-poole": ("Jordan Poole", 76, "PG"),
    # 22 Phoenix Suns
    "devin-booker": ("Devin Booker", 91, "SG"),
    "jalen-green": ("Jalen Green", 83, "SG"),
    "dillon-brooks": ("Dillon Brooks", 82, "SF"),
    "mark-williams": ("Mark Williams", 80, "C"),
    "ryan-dunn": ("Ryan Dunn", 76, "SF"),
    # 23 Milwaukee Bucks
    "giannis-antetokounmpo": ("Giannis Antetokounmpo", 97, "PF"),
    "myles-turner": ("Myles Turner", 83, "C"),
    "kevin-porter-jr": ("Kevin Porter Jr.", 79, "PG"),
    "kyle-kuzma": ("Kyle Kuzma", 79, "SF"),
    "gary-trent-jr": ("Gary Trent Jr.", 76, "SG"),
    # 24 Miami Heat
    "bam-adebayo": ("Bam Adebayo", 88, "C"),
    "norman-powell": ("Norman Powell", 84, "SG"),
    "andrew-wiggins": ("Andrew Wiggins", 81, "SF"),
    "kelel-ware": ("Kel'el Ware", 80, "C"),
    "davion-mitchell": ("Davion Mitchell", 79, "PG"),
    # 25 Portland Trail Blazers
    "deni-avdija": ("Deni Avdija", 82, "SF"),
    "toumani-camara": ("Toumani Camara", 82, "PF"),
    "donovan-clingan": ("Donovan Clingan", 82, "C"),
    "jrue-holiday": ("Jrue Holiday", 81, "PG"),
    "shaedon-sharpe": ("Shaedon Sharpe", 81, "SG"),
    # 26 Chicago Bulls
    "coby-white": ("Coby White", 83, "SG"),
    "josh-giddey": ("Josh Giddey", 82, "PG"),
    "nikola-vucevic": ("Nikola Vucevic", 82, "C"),
    "matas-buzelis": ("Matas Buzelis", 81, "PF"),
    "kevin-huerter": ("Kevin Huerter", 77, "SG"),
    # 27 Charlotte Hornets
    "lamelo-ball": ("LaMelo Ball", 87, "PG"),
    "kon-knueppel": ("Kon Knueppel", 83, "SG"),
    "brandon-miller": ("Brandon Miller", 82, "SF"),
    "miles-bridges": ("Miles Bridges", 82, "PF"),
    "mason-plumlee": ("Mason Plumlee", 76, "C"),
    # 28 Washington Wizards
    "alexandre-sarr": ("Alexandre Sarr", 81, "C"),
    "cj-mccollum": ("CJ McCollum", 81, "SG"),
    "khris-middleton": ("Khris Middleton", 78, "SF"),
    "corey-kispert": ("Corey Kispert", 78, "SF"),
    "bub-carrington": ("Bub Carrington", 76, "PG"),
    # 29 Brooklyn Nets
    "michael-porter-jr": ("Michael Porter Jr.", 82, "SF"),
    "cam-thomas": ("Cam Thomas", 81, "SG"),
    "nicolas-claxton": ("Nicolas Claxton", 80, "C"),
    "ziaire-williams": ("Ziaire Williams", 76, "SF"),
    "egor-demin": ("Egor Demin", 72, "PG"),
    # 30 Utah Jazz
    "lauri-markkanen": ("Lauri Markkanen", 84, "PF"),
    "walker-kessler": ("Walker Kessler", 82, "C"),
    "keyonte-george": ("Keyonte George", 81, "PG"),
    "isaiah-collier": ("Isaiah Collier", 77, "PG"),
    "ace-bailey": ("Ace Bailey", 77, "SF"),
}

def equipo_bonito(folder):
    # "01-Oklahoma-City-Thunder" -> "Oklahoma City Thunder"
    return folder.split("-", 1)[1].replace("-", " ")

players = []
missing_files = []
for slug, (name, ovr, pos) in DATA.items():
    pass

# recorrer carpetas para garantizar match 1:1 con las fotos
seen = set()
for team_folder in sorted(os.listdir(FOTOS)):
    tdir = os.path.join(FOTOS, team_folder)
    if not os.path.isdir(tdir):
        continue
    for fn in sorted(os.listdir(tdir)):
        if not fn.lower().endswith(".jpg"):
            continue
        slug = os.path.splitext(fn)[0]
        seen.add(slug)
        if slug not in DATA:
            missing_files.append(f"{team_folder}/{slug}")
            continue
        name, ovr, pos = DATA[slug]
        players.append({
            "nombre": name,
            "slug": slug,
            "equipo": equipo_bonito(team_folder),
            "equipo_carpeta": team_folder,
            "media": ovr,
            "posicion": pos,
            "foto": f"fotos-nba/{team_folder}/{fn}",
        })

# jugadores en DATA sin foto
no_photo = [s for s in DATA if s not in seen]

players.sort(key=lambda p: (-p["media"], p["nombre"]))

with open(os.path.join(BASE, "medias.json"), "w", encoding="utf-8") as f:
    json.dump(players, f, ensure_ascii=False, indent=2)

with open(os.path.join(BASE, "medias.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["nombre", "equipo", "media", "posicion", "foto"])
    for p in players:
        w.writerow([p["nombre"], p["equipo"], p["media"], p["posicion"], p["foto"]])

print(f"Jugadores escritos: {len(players)}")
print(f"Fotos sin media en DATA: {missing_files}")
print(f"Medias en DATA sin foto: {no_photo}")
print("\nTop 5:")
for p in players[:5]:
    print(f"  {p['media']} {p['nombre']} ({p['equipo']})")
print("Bottom 5:")
for p in players[-5:]:
    print(f"  {p['media']} {p['nombre']} ({p['equipo']})")
