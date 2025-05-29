# messages.py

## Description
Ce fichier contient tous les messages textuels affichés par le ransomware éducatif EduLocker. Il centralise les chaînes de caractères dans différentes langues, permettant une internationalisation facile et une séparation claire entre le code et le contenu textuel.

## Structure principale
### RANSOM_MESSAGES
Un dictionnaire Python qui contient tous les messages du ransomware, organisés par langue:

#### Langues disponibles
1. **french**: Messages en français
2. **english**: Messages en anglais

#### Types de messages (pour chaque langue)
- `title`: Titre principal affiché en haut de l'écran de verrouillage
- `subtitle`: Sous-titre explicatif
- `main_message`: Message principal de la demande de rançon
- `warning`: Message d'avertissement court
- `description`: Description détaillée de la situation
- `unlock_prompt`: Texte pour le champ de saisie du code
- `unlock_button`: Texte du bouton de déverrouillage
- `attempts_remaining`: Message indiquant le nombre de tentatives restantes
- `invalid_code`: Message d'erreur pour code invalide
- `system_unlocked`: Message de confirmation de déverrouillage
- `emergency_unlock`: Message pour le déverrouillage d'urgence
- `unlock_instruction`: Instructions pour le déverrouillage
- `unlock_code_hint`: Indice pour le code de déverrouillage (vide par défaut)
- `emergency_hint`: Indice pour le code d'urgence (vide par défaut)

## Fonctions
- `get_messages(language="french")`: Récupère les messages dans la langue spécifiée, avec le français comme langue par défaut

## Exemple de contenu
Les messages incluent:
- Des émojis pour attirer l'attention (🔒, ⚠️)
- Des instructions fictives de paiement
- Des menaces factices concernant la destruction des données
- Des délais artificiels pour créer un sentiment d'urgence

## Intégration avec le projet
Ce fichier est importé par:
- `config/settings.py` pour intégrer les messages dans la configuration globale
- `core/locker.py` pour afficher les messages dans l'interface de verrouillage

## Note éducative
Les messages sont conçus pour ressembler à ceux d'un vrai ransomware afin de sensibiliser aux techniques d'ingénierie sociale utilisées par les attaquants, notamment:
- Création d'un sentiment d'urgence
- Utilisation de menaces pour inciter au paiement
- Instructions détaillées pour le paiement
- Ton autoritaire et intimidant