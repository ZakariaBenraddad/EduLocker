# ransom_screen.py

## Description
Ce fichier est un module GUI destiné à contenir l'implémentation de l'écran de rançon pour le projet EduLocker. Actuellement, il s'agit d'un fichier vide qui sert de placeholder pour une future implémentation.

## Fonctionnalité prévue
Ce module serait destiné à:
- Implémenter une interface graphique dédiée pour l'écran de rançon
- Séparer la logique d'affichage (GUI) de la logique de verrouillage
- Permettre une personnalisation plus poussée de l'interface utilisateur

## Relation avec le projet actuel
Dans la version actuelle d'EduLocker, la fonctionnalité d'affichage de l'écran de rançon est directement implémentée dans le module `core/locker.py` via la classe `SystemLocker`. Ce fichier pourrait permettre une meilleure séparation des responsabilités dans une future version:
- `locker.py` gérerait uniquement la logique de verrouillage
- `ransom_screen.py` gérerait uniquement l'interface utilisateur

## Note technique
L'implémentation d'une interface graphique séparée pourrait faciliter:
- L'ajout de nouvelles fonctionnalités visuelles
- La personnalisation de l'apparence selon différents "thèmes" de ransomware
- L'adaptation à différents environnements de bureau
- Les tests unitaires en isolant la logique d'affichage