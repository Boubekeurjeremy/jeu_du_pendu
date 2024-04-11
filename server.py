from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'JBBreakingBad2024' 

#############

def lire_fichier(dictionnaire):
    donnees = []
    with open(dictionnaire, 'r', encoding='utf-8') as fichier:
        for index, ligne in enumerate(fichier, start=1):
            elements = ligne.strip().split(';')
            donnees.append((index, elements))
    return donnees

###############

def mot_cache():
    mot_cache = ""
    for lettre_mot, lettre_trouvee in zip(mot_aleatoire, chaine_nettoyee):
        if lettre_trouvee in lettres_recues:
            mot_cache += lettre_mot
        else:
            mot_cache += " _ "
   
    return mot_cache

##############

def nettoyer_chaine(chaine, caracteres_speciaux):
    for special, origine in caracteres_speciaux.items():
        chaine = chaine.replace(special, origine)
    return chaine


#############

donnees_recuperees = lire_fichier('dictionnaire.txt')
mot_aleatoire = random.choice(donnees_recuperees)[1][0]
print(f"Le mot aleatoire commencer partie est : {mot_aleatoire}")

caracteres_speciaux = {
    "à": "a",
    "â": "a",
    "é": "e",
    "è": "e",
    "ê": "e",
    "ë": "e",
    "î": "i",
    "ï": "i",
    "ô": "o",
    "ò": "o",
    "û": "u",
    "ù": "u",
    "ç": "c",
}

chaine_nettoyee = nettoyer_chaine(mot_aleatoire, caracteres_speciaux)
message_fin_jeu= ""
lettres_recues = []
vies = 5
potence = []
elements_pendu = ["│", "│", "│", "─", "👿"]
info_vies = "Vies"

####################
@app.route("/")

@app.route("/", methods=["GET","POST"])
def home():
    erreur = None
    nom = ""
    if request.method == "POST":
        nom = request.form['nom_user'].strip()
        if nom == "":
            erreur = "Veuillez remplir le champ : Nom"
        else:
            return redirect(url_for("play", nom=nom))  
    return render_template('home.html', erreur=erreur, nom=nom)

############

@app.route("/recommencer-partie", methods=["GET"])
def recommencer_partie():
    global lettres_recues, mot_aleatoire, chaine_nettoyee, vies, message_fin_jeu, potence, info_vies
   
    lettres_recues = []
    mot_aleatoire = random.choice(donnees_recuperees)[1][0]
    print(f"Le mot aléatoire recommencer partie est : {mot_aleatoire}" )
    chaine_nettoyee = nettoyer_chaine(mot_aleatoire, caracteres_speciaux)
    vies = 5
    message_fin_jeu = ""
    potence = []  
    info_vies = "Vies"
    nom = session.get("nom")
    return redirect(f"/play?nom={nom}")

#############
    
@app.route("/play", methods=["GET", "POST"])
def play():  
    global lettres_recues, mot_aleatoire,chaine_nettoyee,vies, message_fin_jeu, potence, info_vies

    alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    nom = request.args.get('nom') 
    session['nom'] = nom
    if request.method == 'POST':
        lettre_recue = request.form['lettre']
        nom = session.get('nom', None) 
        
        # Vérifie si la lettre est déjà dans la liste.

        if lettre_recue in lettres_recues:
            print(f"La lettre {lettre_recue} a déjà été utilisée.")

        # Vérifie si la lettre n'est pas dans l'alphabet.

        elif lettre_recue not in alphabet:
            print(f"La lettre {lettre_recue} n'est pas dans l'alphabet.")
        else:

        # Ajoute la lettre tapée à la liste lettres_recues.

            lettres_recues.append(lettre_recue)
            if lettre_recue in chaine_nettoyee:
                print(f"La lettre {lettre_recue} est dans le mot aléatoire")

                # Occurrences trouvées de la lettre. 
                           
                for index, lettre in enumerate(chaine_nettoyee):
                    if lettre == lettre_recue:
                        print(f"Lettre : {lettre} (Position : {index + 1})")

            # Vérifie si la lettre n'est pas dans le mot aléatoire.

            else:
                print(f"La lettre {lettre_recue} n'est pas dans le mot aléatoire")
                potence.append(elements_pendu[5 - vies])
                vies -= 1 
               
                mot_en_cache = mot_cache() 
                if vies <= 1:
                    info_vies = f"Vie" 

                # Partie perdu

                if vies <= 0:
                                           
                        message_fin_jeu = f'Désolé, vous avez perdu.<br>Le mot était : <br>" {mot_aleatoire} ".'

                        return render_template("play.html",potence=potence, message_fin_jeu=message_fin_jeu, vies=vies, lettre=lettres_recues, nom=nom,        
                                       alphabet=alphabet, mot_en_cache=mot_en_cache, mot_aleatoire=mot_aleatoire, info_vies=info_vies)
        mot_en_cache = mot_cache() 

    # Vérifie si le joueur a trouvé le mot
        if all(lettre.lower() in lettres_recues for lettre in chaine_nettoyee.lower()):
              
                message_fin_jeu = f'Félicitations, vous avez gagné !<br>Le mot était : <br>" {mot_aleatoire} ".'

                return render_template("play.html",potence=potence, message_fin_jeu=message_fin_jeu, vies=vies, lettre=lettres_recues, nom=nom,
                                   alphabet=alphabet, mot_en_cache=mot_en_cache, mot_aleatoire=mot_aleatoire, info_vies=info_vies)
 
    mot_en_cache = mot_cache()  
    return render_template("play.html",potence=potence, message_fin_jeu=message_fin_jeu, vies=vies, lettre=lettres_recues, nom=nom,
                           alphabet=alphabet, mot_en_cache=mot_en_cache, mot_aleatoire=mot_aleatoire, info_vies=info_vies)
    



if __name__ == '__main__':
    app.run(debug=True)  