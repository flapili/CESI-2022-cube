// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';
import 'package:ressources_relationnelles/pages/accueil.dart';
import 'common/constants.dart';
import 'pages/accueil.dart';
import 'pages/rechercher.dart';
import 'pages/ajouter.dart';
import 'pages/profil.dart';
import './pages/components/app_bar.dart';
//import 'test.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({ Key? key }) : super(key: key);

  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  int _selectedIndex = 0;
  final List<Widget> _page = [
    Accueil(),
    Rechercher(),
    //Body(),
    Ajouter(),
    Profil()
  ];
  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ressources relationnelles',
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        backgroundColor: lightGreen,
        
        body: UpBar()
              //PostWidget(),
              //Accueil(),
      )
    );
  }
}