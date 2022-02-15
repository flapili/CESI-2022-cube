// ignore_for_file: prefer_const_literals_to_create_immutables, prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:ressources_relationnelles/pages/accueil.dart';
import '../../common/constants.dart';
import '../../pages/accueil.dart';
import '../../pages/rechercher.dart';
import '../../pages/ajouter.dart';
import '../../pages/profil.dart';

class UpBar extends StatefulWidget {
  const UpBar({Key? key}) : super(key: key);

  @override
  _UpBarState createState() => _UpBarState();
}

class _UpBarState extends State<UpBar> {
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
    return Scaffold(
      backgroundColor: lightGreen,
      appBar: AppBar(
        centerTitle: true,
        backgroundColor: darkGreen,
        elevation: 0,
        title: Image.asset(
          'assets/images/logo.png',
          height: 70,
        ),
        actions: [
          Padding(
              padding: EdgeInsets.only(right: 15),
              child: PopupMenuButton(
                  color: Colors.white.withOpacity(0.95),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.all(
                      Radius.circular(5.0),
                    ),
                  ),
                  child: Icon(Icons.menu_outlined, color: Colors.white),
                  itemBuilder: (context) => [
                        PopupMenuItem(
                          child: ListTile(
                            leading: Icon(Icons.groups_outlined, color: Colors.black),
                            title: Text('Groupes'),
                          ),
                          value: 1,
                        ),
                        PopupMenuItem(
                          child: ListTile(
                            leading: Icon(Icons.settings_outlined, color: Colors.black),
                            title: Text('Paramètres'),
                          ),
                          value: 2,
                        ),
                        PopupMenuItem(
                          child: ListTile(
                            leading: Icon(Icons.help_outlined, color: Colors.black),
                            title: Text('Aide'),
                          ),
                          value: 3,
                        ),
                        PopupMenuItem(
                          child: ListTile(
                            leading: Icon(Icons.logout_outlined, color: Colors.black),
                            title: Text('Déconnexion'),
                          ),
                          value: 4,
                        )
                      ]))
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
            label: 'Accueil',
            backgroundColor: darkGreen,
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.search),
            label: 'Rechercher',
            backgroundColor: darkGreen,
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.add_circle_outline),
            label: 'Ajouter ressource',
            backgroundColor: darkGreen,
          ),
          BottomNavigationBarItem(
              icon: //Icon(Icons.person_outline),
                  CircleAvatar(
                backgroundImage: AssetImage('assets/images/profil/1.jpg'),
              ),
              label: 'Profil',
              backgroundColor: darkGreen),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: lightGreen,
        onTap: _onItemTapped,
      ),
    );
  }
}
