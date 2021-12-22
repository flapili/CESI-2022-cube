import 'package:flutter/material.dart';
import 'package:ressources_relationnelles/pages/accueil.dart';
//import 'post_widget.dart';
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
        backgroundColor: Colors.green[100],
        appBar: AppBar(
          centerTitle: true,
          backgroundColor: Colors.grey[600],
          elevation: 0,
          leading: IconButton(
            onPressed: () {},
            icon: const Icon(
            Icons.settings_outlined,
            color: Colors.black,
            ),
          ),
          title: Image.asset(
            'assets/images/logo.png',
            height: 70,
          ),
        actions: [
          IconButton(
            onPressed: () {},
            icon: const Icon(
            Icons.logout,
            color: Colors.black,
            ),
          ),
        ],
        ),
        body:
              //PostWidget(),
              //Accueil(),
              _page[_selectedIndex],
bottomNavigationBar: BottomNavigationBar(
        items: [
            BottomNavigationBarItem(
              icon: const Icon(Icons.home),
              label:'Accueil',
              backgroundColor: Colors.grey[600],
            ),
            BottomNavigationBarItem(
              icon: const Icon(Icons.search),
              label:'Rechercher',
              backgroundColor: Colors.grey[600],
            ),
            BottomNavigationBarItem(
              icon: const Icon(Icons.add_circle_outline),
              label:'Ajouter article',
              backgroundColor: Colors.grey[600],
            ),
            BottomNavigationBarItem(
              icon: //Icon(Icons.person_outline),
              const CircleAvatar(backgroundImage: AssetImage('assets/images/profil/1.jpg'),),
              
              label:'Profil',
              backgroundColor: Colors.grey[600],
            ),
          ],
        currentIndex: _selectedIndex,
        selectedItemColor: Colors.amber[800],
        onTap: _onItemTapped,
      ),
      )
    );
  }
}