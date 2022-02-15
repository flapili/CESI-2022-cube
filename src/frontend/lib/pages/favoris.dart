// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';
import 'package:ressources_relationnelles/common/constants.dart';

class Favoris extends StatefulWidget {
  const Favoris({Key? key}) : super(key: key);

  @override
  _FavorisState createState() => _FavorisState();
}

class _FavorisState extends State<Favoris> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Color(0xFFC1DFF0),
        appBar: AppBar(
          backgroundColor: darkGreen,
          centerTitle: true,
          title: Image.asset(
            'assets/images/logo.png',
            height: 70,
          ),
          leading: IconButton(
            onPressed: () {
              Navigator.pop(context);
            },
            icon: Icon(Icons.arrow_back_ios),),
        ),
        body: SingleChildScrollView(
        child: Column(
          children: [
                Padding(
                  padding: EdgeInsets.only(top: 10),
                  child: Card(
                    margin: EdgeInsets.all(10),
                    shadowColor: Colors.blueGrey,
                    elevation: 10,
                    child: Column(
                      children: [
                        ListTile(
                          leading: CircleAvatar(
                            backgroundImage: AssetImage('assets/images/profil/1.jpg'),
                          ),
                          title: Text('Reconnaître ses émotions',
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                color: cyanGreen
                              ),
                              textAlign: TextAlign.center),
                          subtitle: Text('Intelligence émotionnelle',
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
                                "L'objectif de cet exercice est de reconnaître les émotions sur soi. "
          "Pour ce faire, nous noterons dans un petit cahier prévu à cet effet, à des moments "
          "prédéfinis de la journée, comment nous nous sentons émotionnellement. "
          "Quelle émotion nous habite ? Cette émotion est-elle positive ou négative ? "
          "Avec quelle force ? Quel a été le facteur déclencheur ?",
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
                Padding(
                  padding: EdgeInsets.only(top: 0),
                  child: Card(
                    margin: EdgeInsets.all(10),
                    shadowColor: Colors.blueGrey,
                    elevation: 10,
                    child: Column(
                      children: [
                        ListTile(
                          leading: CircleAvatar(
                            backgroundImage: AssetImage('assets/images/profil/1.jpg'),
                          ),
                          title: Text('Emission ARTE : Travail | Travail, Salaire, Profit',
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                color: cyanGreen
                              ),
                              textAlign: TextAlign.center),
                          subtitle: Text('Monde professionnel',
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
                                "Lorem Ipsum is simply dummy text of the printing and typesetting industry. "
                                "Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown "
                                "printer took a galley of type and scrambled it to make a type specimen book. It has "
                                "survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.",
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
        )));
  }
}