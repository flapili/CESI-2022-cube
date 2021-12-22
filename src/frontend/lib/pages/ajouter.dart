// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';

class Ajouter extends StatefulWidget {
  const Ajouter({ Key? key }) : super(key: key);

  @override
  _AjouterState createState() => _AjouterState();
}

class _AjouterState extends State<Ajouter> {
  final TextEditingController _controller = TextEditingController();
  final TextEditingController _controller2 = TextEditingController();
  var categories = [
    'Communication',
    'Culture',
    'Développement personnel',
    'Intelligence émotionnelle',
    'Loisirs',
    'Monde professionnel',
    'Parentalité',
    'Qualité de vie',
    'Recherche de sens',
    'Santé physique',
    'Spiritualité',
    'Vie affective',
  ];
  var public = [
    'Soi',
    'Conjoints',
    'Famille : enfants/parents/fratrie',
    'Professionnelle : collègues, collaborateurs et managers',
    'Amis et communautés',
    'Inconnus',
  ];
  @override
  Widget build(BuildContext context) {
return SingleChildScrollView(
    child: Column(children: [
      Padding(
        padding: EdgeInsets.all(20),
        child: TextField(
          decoration: InputDecoration(
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10.0),),
              hintText: 'Titre de la rrrrrrrrrressource',
              fillColor: Colors.white,
              filled: true,
            ),
          cursorColor: Colors.black,
          style: TextStyle(color: Colors.black),
        ),
      ),
      Padding(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: Row(
          children: <Widget>[
            Expanded(
              child: TextField(
                decoration: InputDecoration(
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10.0),),
              hintText: 'Catégorie de la ressource',
              fillColor: Colors.white,
              filled: true,
            ),
                controller: _controller
              )
            ),
            PopupMenuButton<String>(
              icon: const Icon(Icons.arrow_drop_down),
              onSelected: (String value) {
                _controller.text = value;
              },
              itemBuilder: (BuildContext context) {
                return categories.map<PopupMenuItem<String>>((String value) {
                  return PopupMenuItem(
                      child: Text(value), value: value);
                }).toList();
              },
            ),
          ],
        ),
      ),
      Padding(
        padding: EdgeInsets.symmetric(vertical: 20, horizontal: 20),
        child: Row(
          children: <Widget>[
            Expanded(
              child: TextField(
                decoration: InputDecoration(
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10.0),),
              hintText: 'Public de la ressource',
              fillColor: Colors.white,
              filled: true, 
            ),
                controller: _controller2
              )
            ),
            PopupMenuButton<String>(
              icon: const Icon(Icons.arrow_drop_down),
              onSelected: (String value) {
                _controller2.text = value;
              },
              itemBuilder: (BuildContext context) {
                return public.map<PopupMenuItem<String>>((String value) {
                  return PopupMenuItem(
                      child: Text(value), value: value);
                }).toList();
              },
            ),
          ],
        ),
      ),
      Padding(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: 
        TextField(
          decoration: InputDecoration(
            
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10.0),),
              hintText: 'Texte',
              fillColor: Colors.white,
              filled: true, 
              suffixIcon: Icon(Icons.notes_outlined, color: Colors.black),
            ),
          maxLines: null,
          cursorColor: Colors.black,
          style: TextStyle(color: Colors.black),
        ),
      ),
      Padding(
        padding: EdgeInsets.symmetric(vertical: 20, horizontal: 20),
        child: 
        TextField(
          decoration: InputDecoration(
            
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10.0),),
              hintText: 'Image (optionnel)',
              fillColor: Colors.white,
              filled: true, 
              suffixIcon: Icon(Icons.image_outlined, color: Colors.black),
            ),
          cursorColor: Colors.black,
          style: TextStyle(color: Colors.black),
        ),
      ),
      Container(
        padding: EdgeInsets.symmetric(vertical: 30, horizontal: 0),
        child: IconButton(
            onPressed: () {

            },
            icon: const Icon(
            Icons.add_circle_outline,
            size: 60,
            color: Colors.black,
            ),
          ),
      )
    ])
);
  }
}
