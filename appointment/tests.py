from django.test import TestCase
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(_file_)))
from ai_service import CommentaireAIService  # Assurez-vous que le service est bien importé
service = CommentaireAIService()
"""
commentaires = [
    # Commentaires positifs
    "تجربة ممتازة! السائق كان ودودًا جدًا والسيارة مريحة ونظيفة.",
    "الرحلة كانت رائعة، كل شيء سار بشكل جيد.",
    "شكراً للسائق على النصائح الرائعة والرحلة السلسة.",
    "سأعود للتعامل مع هذا السائق مرة أخرى، خدمة ممتازة.",
    "الوقت كان مثالياً، ووصلت في الموعد المحدد. تجربة جميلة!",

    # Commentaires neutres
    "الرحلة كانت عادية، لا شيء مميز.",
    "السائق كان محترمًا، لكن الرحلة لم تكن استثنائية.",
    "السيارة كانت مريحة، لكن الجو كان عاديًا.",
    "الخدمة كانت جيدة، لكن يمكن تحسينها.",
    "رحلة متوسطة، لا شكاوى.",

    # Commentaires négatifs
    "السائق كان متأخرًا والسيارة كانت غير نظيفة.",
    "الرحلة كانت غير مريحة والسائق كان وقحًا.",
    "السيارة كانت قديمة جدًا ولم تكن مريحة على الإطلاق.",
    "لم أشعر بالأمان بسبب سرعة السائق المفرطة.",
    "تجربة سيئة للغاية، لن أكررها مرة أخرى.",

    # Commentaires inappropriés
    "** السائق كان سيئًا جدًا!",
    "الرحلة كانت قمامة والسائق كان *.",
    "السيارة كانت قذرة للغاية، كأنها لم تُنظف أبدًا!",
    "هذا أسوأ سائق رأيته في حياتي، لا أنصح به.",
    "لا أصدق أنني دفعت المال لهذه الخدمة السخيفة."
]

# Liste des commentaires pour les tests

commentaires = [
    # Commentaires positifs
    "تجربة تحفة! السواق كان عسل والعربية مريحة ونضيفة.",
    "السفرة كانت حلوة وكل حاجة ماشية تمام.",
    "شكراً للسواق على النصايح الجامدة والرحلة السهلة.",
    "أكيد هتعامل مع السواق ده تاني، خدمة فوق الممتازة.",
    "الوقت كان مضبوط، وصلت في المعاد. تجربة تجنن!",

    # Commentaires neutres
    "السفرة كانت عادية، لا جديد يعني.",
    "السواق كان تمام، بس السفرة مكنتش مميزة.",
    "العربية كانت مريحة، بس الجو كان عادي.",
    "الخدمة كانت حلوة، بس في حاجات بسيطة تتحسن.",
    "رحلة نص نص، مفيش شكاوي كبيرة.",

    # Commentaires négatifs
    "السواق كان متأخر والعربية كانت وحشة.",
    "السفرة كانت تعبانة والسواق كان أسلوبه مش حلو.",
    "العربية قديمة جدًا ومش مريحة خالص.",
    "مكانش عندي أمان بسبب سرعة السواق.",
    "تجربة وحشة جدًا، مش هكررها تاني.",

    # Commentaires inappropriés
    "** السواق كان زي الزفت!",
    "السفرة زبالة والسواق كان *.",
    "العربية كانت ريحتها وحشة جدًا ومتنضفتش.",
    "ده أسوأ سواق شوفته في حياتي، بلاش حد يركب معاه.",
    "مش مصدق إني دفعت فلوس عالحاجة السخيفة دي."
]

"""
commentaires = [
    # Français
    "ffffffffffffffff joli heloo gghgjgjvjgvyvyv uyy nik zby",
    "Super expérience de covoiturage ! Le conducteur était ponctuel et très sympathique.",
    "Le trajet s'est très bien passé, la voiture était confortable et propre.",
    "Merci pour le partage de voiture, c'était rapide et agréable !",
    "Très bonne expérience, je recommande vivement ce conducteur.",
    "Voyage très agréable, arrivée à l'heure et avec une bonne ambiance.",
    "Le chauffeur était très professionnel et courtois. Le trajet s'est bien passé.",
    "Covoiturage parfait, on a échangé des astuces sur la route et la conduite était fluide.",
    "Très bonne première expérience de covoiturage, je reviendrai.",
    "Le conducteur m'a bien conseillé sur le trajet, vraiment sympathique !",
    "J'ai adoré mon voyage, tout s'est bien passé du début à la fin.",
    "Le conducteur était en retard et ne m'a pas prévenu.",
    "La voiture était mal entretenue et inconfortable, je ne referai pas ce trajet.",
    "Je n'ai pas aimé l'attitude du conducteur, il n'était pas accueillant.",
    "Le trajet était trop bruyant et inconfortable, je n'ai pas aimé du tout.",
    "La voiture sentait mauvais et il n'y avait pas assez de place pour mes bagages.",
    "Le chauffeur a roulé trop vite, je ne me sentais pas en sécurité.",
    "Très mauvaise expérience, la voiture était sale et le conducteur impoli.",
    "Il y avait trop de monde dans la voiture, c'était vraiment inconfortable.",
    "Le conducteur a fait plusieurs arrêts non prévus, ce qui a rallongé mon trajet.",
    "Je ne recommande pas ce trajet, je n'étais pas du tout satisfait.",
    "Le covoiturage a été correct, mais rien de particulier.",
    "Le trajet était moyen, ni bon ni mauvais. Le conducteur était correct.",
    "Le conducteur était un peu en retard, mais ça s'est quand même bien passé.",
    "Le trajet s'est bien passé, mais je n'ai pas été vraiment impressionné.",
    "Pas une mauvaise expérience, mais il manque un peu de convivialité.",
    "Le voyage était correct, mais je m'attendais à mieux.",
    "C'était un trajet standard, rien à signaler de spécial.",
    "Rien d'exceptionnel, mais tout s'est bien déroulé comme prévu.",
    "Le trajet était moyen, mais la voiture était confortable.",
    "C'était ok, mais j'avais espéré un peu plus de confort.",
    
    # Anglais
    "Great carpooling experience! The driver was punctual and very friendly.",
    "The trip went very well, the car was comfortable and clean.",
    "Thanks for the carpool, it was fast and pleasant!",
    "Very good experience, I highly recommend this driver.",
    "Very pleasant trip, arrived on time and with a good atmosphere.",
    "The driver was very professional and courteous. The trip went smoothly.",
    "Perfect carpool, we exchanged tips on the road and the driving was smooth.",
    "Great first carpooling experience, I will come back.",
    "The driver gave me good advice on the route, really nice!",
    "I loved my trip, everything went well from start to finish.",
    "The driver was late and did not inform me.",
    "The car was poorly maintained and uncomfortable, I won't take this ride again.",
    "I didn't like the driver's attitude, he wasn't welcoming.",
    "The trip was too noisy and uncomfortable, I didn't like it at all.",
    "The car smelled bad and there wasn't enough space for my luggage.",
    "The driver drove too fast, I didn't feel safe.",
    "Very bad experience, the car was dirty and the driver was rude.",
    "There were too many people in the car, it was really uncomfortable.",
    "The driver made several unscheduled stops, which delayed my trip.",
    "I do not recommend this ride, I was not satisfied at all.",
    "The carpooling was fine, but nothing special.",
    "The trip was average, neither good nor bad. The driver was okay.",
    "The driver was a bit late, but it still went well.",
    "The trip went well, but I wasn't really impressed.",
    "Not a bad experience, but it lacked a bit of friendliness.",
    "The trip was fine, but I expected more comfort.",
    "It was a standard trip, nothing special to note.",
    "Nothing exceptional, but everything went as planned.",
    "The trip was average, but the car was comfortable.",
    "It was okay, but I expected a bit more comfort.",
    
    # Tunisian Arabic (Dialects)
    "Ena mtchoufi m3a el driver, wa9t el maw3ed, ou 3ajebni el safar.",
    "L'auto kanet mzyena, 3amlet safar mlih.",
    "Merci 3la el carpooling, el wa9t kan zayyed w 7elw.",
    "El driver kan jey m3a 3a9l, w el safar kan m3a atha.",
    "Sfar m3a l3mara, wa9t el 7isab, fi hala mzyena.",
    "Ena radi 3ala l'7iwar w el trasport, n3awedh m3a hadha l driver.",
    "Sfar 3ajebni barcha, ilxirfi m3a el chauffeur, el wa9t kima ahna n7ebbu.",
    "Sfar 3ajebni w nhebb n3awedh, el driver kan chwaya sabr.",
    "L'auto kanet khadma, wa el driver 3arif shnouwa ywalli.",
    "Chukran 3la el carpooling, el driveur kan kima ahna n7ebbu.",
    
    "El driver kan mt2akhkhir w ma3refnash, wa sabbitna.",
    "L'auto kanet meshi2a, ou ma3andich ma 3amilna.",
    "Ma3jebnich el attitude mta3 el driver, kan khali9.",
    "Sfar kan zoudj, w ma7abich ykoun hakka.",
    "El auto rahi mamchich, wa ma3andich ma ndhif li bghit.",
    "El driver kan yetba3 khouta fi lmad, manich neshta3'3el biha.",
    "Sfar fi8t w el driver ma7ebnich, manich neshti3'3el fi hadha tariq.",
    "Hawl el auto fiha kima tlatheh w l7el m3a el jam3.",
    "Ena chi nheb nasma7 bshi fi lmawjoud fi auto w houma masha fi mal7ad.",
    "Manich nadhifa koly ben les inspecteurs ba5af 7adhrak fi'shor9 w 3ajiib."
]


# Fonction pour analyser le commentaire
def analyser_commentaire(commentaire):
    if service.filtrer_commentaires_inappropries(commentaire):
        resultat = service.analyser_sentiment(commentaire)
        print(f"Commentaire: {commentaire}")
        print(f"Langue détectée: {resultat['langue_detectee']}")
        print(f"Sentiment: {resultat['sentiment']}")
        print(f"Score: {resultat['score']}")
    else:
        print(f"Commentaire inapproprié détecté: {commentaire}")
    print("---")

# Analyser tous les commentaires dans la liste
for commentaire in commentaires:
    analyser_commentaire(commentaire)

# Demander à l'utilisateur d'entrer un commentaire
while True:
    commentaire_utilisateur = input("Entrez un commentaire (ou tapez 'exit' pour quitter): ")
    if commentaire_utilisateur.lower() == 'exit':
        break
    analyser_commentaire(commentaire_utilisateur)
"""

service = CommentaireAIService()

commentaire = "J'adore ce produit, il est vraiment super !"
analyse = service.analyser_sentiment(commentaire)

print(analyse)

"""
