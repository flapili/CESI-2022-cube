// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';

class PostWidget extends StatefulWidget {
  const PostWidget({ Key? key }) : super(key: key);

  @override
  _PostWidgetState createState() => _PostWidgetState();
}

class _PostWidgetState extends State<PostWidget> {
  final List postItems = 
  [
    {
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
      "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean vehicula vel nisi vel vestibulum. Donec risus tellus, tempor ultrices leo a, viverra ornare est."
    },
    {
      "categorie": "Monde professionnel",
      "titre": "Emission ARTE : Travail | Travail, Salaire, Profit",
      "contenu": "test test test test test testtesttesttesttesttesttesttesttesttesttest",
      "pseudo": "ipsum",
      "date_publication": "10/12/2021",
      "photo": "assets/images/posts/2.jpg",
      "photoProfil": "assets/images/profil/1.jpg",
      "description": "ceci est une description"
    },
    {
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
        children: postItems.map((post){
          return Column(
            children: [
              Container(
              height: 60,            
              color: Colors.white,
              
              padding: const EdgeInsets.symmetric(horizontal: 10),
              child: Row(
                //crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  CircleAvatar(
                    backgroundImage: AssetImage(post['photoProfil']),
                    ),
                    const SizedBox(width: 10),
                  Text(
                    post['pseudo'],
                    style: const TextStyle(fontWeight: FontWeight.bold)
                  ),
                  Text(
                    ' - '
                  ),
                  Text(
                        post['date_publication'],
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w500,
                          color: Colors.grey.shade600),
                      ),
                  Expanded(child: Container()),
                  IconButton(
                    onPressed: () {},
                    icon: const Icon(Icons.more_horiz),
                  )
                ],
              )
            ),
            Column(
              children: [
                Text(
                  post['titre'],
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.green,
                  ),
                  textAlign: TextAlign.center
                ),
                Text(
                  post['categorie'],
                  style: TextStyle(
                    fontWeight: FontWeight.w400,
                    color: Colors.green.shade600,
                  ),
                  textAlign: TextAlign.center
                )
              ],
            ),
            
            Container(
              margin: const EdgeInsets.only(top: 15),
              padding: EdgeInsets.symmetric(horizontal: 10),
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
              decoration: BoxDecoration(
                
                //borderRadius: BorderRadius.circular(10),
                /*image: DecorationImage(
                  image: AssetImage(post['photo']),
                  fit: BoxFit.cover,
                )*/
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  IconButton(
                    onPressed: () {
                      setState((){
                        _isPressed = !_isPressed;
                      });
                    },
                    icon: _isPressed ? Icon(Icons.favorite, color: Colors.red) : const Icon(Icons.favorite_outline),
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
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Text(
                        '10 commentaires',
                        style: TextStyle(
                          fontWeight: FontWeight.w600,
                          color: Colors.grey.shade400
                        ),
                      ), 
                  const SizedBox(height: 10),
                  const Divider(
                   color: Colors.black
                  )
                ],
              )
            )
          ],
        );
      }).toList(),
    ),
);
  }
}
