// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:ressources_relationnelles/common/constants.dart';

class Accueil extends StatefulWidget {
  const Accueil({Key? key}) : super(key: key);

  @override
  _AccueilState createState() => _AccueilState();
}

class _AccueilState extends State<Accueil> {
  final List postItems = [
    {
      "id": 1,
      "categorie": "Intelligence émotionnelle",
      "titre": "Reconnaître ses émotions",
      "contenu": "L'objectif de cet exercice est de reconnaître les émotions sur soi. "
          "Pour ce faire, nous noterons dans un petit cahier prévu à cet effet, à des moments "
          "prédéfinis de la journée, comment nous nous sentons émotionnellement. "
          "Quelle émotion nous habite ? Cette émotion est-elle positive ou négative ? "
          "Avec quelle force ? Quel a été le facteur déclencheur ?",
      "pseudo": "lorem",
      "date_publication": "08/12/2021",
      "photo": "assets/images/posts/1.jpg",
      "photoProfil": "assets/images/profil/1.jpg",
      "description":
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean vehicula vel nisi vel vestibulum. Donec risus tellus, tempor ultrices leo a, viverra ornare est."
    },
    {
      "id": 2,
      "categorie": "Monde professionnel",
      "titre": "Emission ARTE : Travail | Travail, Salaire, Profit",
      "contenu":
          "test test test test test testtesttesttesttesttesttesttesttesttesttest",
      "pseudo": "ipsum",
      "date_publication": "10/12/2021",
      "photo": "assets/images/posts/2.jpg",
      "photoProfil": "assets/images/profil/1.jpg",
      "description": "ceci est une description"
    },
    {
      "id": 3,
      "categorie": "Monde professionnel",
      "titre": "Le rire au travail et l'éthique",
      "contenu": "test",
      "pseudo": "pseudo 3",
      "date_publication": "10/12/2021",
      "photo": "assets/images/posts/3.jpg",
      "photoProfil": "assets/images/profil/1.jpg",
      "description": "ceci est une description"
    },
    {
      "id": 4,
      "categorie": "Qualité de vie",
      "titre": "Partager des vrais moments de vie de famille",
      "contenu": "test",
      "pseudo": "pseudo 4",
      "date_publication": "10/12/2021",
      "photo": "assets/images/posts/4.jpg",
      "photoProfil": "assets/images/profil/1.jpg",
      "description": "ceci est une description"
    },
    {
      "id": 5,
      "categorie": "Développement personnel",
      "titre": "Partager des vrais moments de vie de famille",
      "contenu": "test",
      "pseudo": "pseudo 5",
      "date_publication": "11/12/2021",
      "photo": "assets/images/posts/5.jpg",
      "photoProfil": "assets/images/profil/1.jpg",
      "description": "ceci est une description"
    }
  ];
  bool _isPressed = false;
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: postItems.map((post) {
          return Column(
            children: [
              Container(
                margin: const EdgeInsets.only(top: 10),
                child: Card(
                    margin: EdgeInsets.all(10),
                    shadowColor: Colors.blueGrey,
                    elevation: 10,
                    child: Column(
                      children: [
                        ListTile(
                          leading: CircleAvatar(
                            backgroundImage: AssetImage(post['photoProfil']),
                          ),
                          title: Text(post['titre'],
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                color: cyanGreen
                              ),
                              textAlign: TextAlign.center),
                          subtitle: Text(post['categorie'],
                              style: TextStyle(
                                fontWeight: FontWeight.w400,
                                color: cyanGreen
                              ),
                              textAlign: TextAlign.center),
                          trailing: IconButton(
                            onPressed: () {},
                            icon: const Icon(Icons.more_horiz),
                          ),
                        ),
                        Padding(
                          padding: EdgeInsets.symmetric(
                              horizontal: 10, vertical: 10),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              Text(
                                post['contenu'],
                                style: TextStyle(
                                    fontSize: 14,
                                    fontWeight: FontWeight.w500,
                                    color: Colors.grey.shade600),
                              ),
                            ],
                          ),
                        ),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: [
                            IconButton(
                              onPressed: () {
                                setState(() {
                                  _isPressed = !_isPressed;
                                });
                              },
                              icon: _isPressed
                                  ? Icon(Icons.favorite, color: Colors.red)
                                  : const Icon(Icons.favorite_outline),
                            ),
                            IconButton(
                              onPressed: () {},
                              icon: const Icon(Icons.message_outlined),
                            ),
                            IconButton(
                              onPressed: () {},
                              icon: const Icon(Icons.share),
                            ),
                          ],
                        ),
                      ],
                    )),
              ),
            ],
          );
        }).toList(),
      ),
    );
  }
}
