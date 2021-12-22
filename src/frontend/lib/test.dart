import 'package:flutter/material.dart';
import 'package:ressources_relationnelles/pages/accueil.dart';
import 'post_widget.dart';
import 'pages/accueil.dart';
import 'pages/rechercher.dart';
import 'pages/ajouter.dart';
import 'pages/profil.dart';
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
    //Connexion(),
    //Inscription(),
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
        backgroundColor: Colors.green[100],

        body:
              //PostWidget(),
              //Accueil(),
              _page[_selectedIndex],

      )
    );
  }
}