// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:tez/common/constants.dart';
import 'package:tez/connexion.dart';


class VeryFirstPage extends StatefulWidget {
  const VeryFirstPage({ Key? key }) : super(key: key);
  
  @override
  _VeryFirstPageState createState() => _VeryFirstPageState();
}


class _VeryFirstPageState extends State<VeryFirstPage> {
  @override
  Widget build(BuildContext context) {

    double margeBoutons = 10;
    double largeurBoutons = 1000;
    double hauteurBoutons = 80;
    double taillePoliceBoutons = 23;
    double radiusBoutons = 15;
    Color couleurBoutons = lightGreen;
    
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        /*appBar: AppBar(
          backgroundColor: darkGreen,
          title: Center(
            child: Image(
              image: AssetImage('assets/images/logo.png'),
              width: 90
            ),
          ), 
        ),*/
        backgroundColor: darkGreen,
        body: Center(
          child: SingleChildScrollView(
            padding: EdgeInsets.symmetric(
              horizontal: 20,
            ),
            child: Column(
              children: [
                
                Container(
                  margin: EdgeInsets.all(30),
                  child: Image(
                    image: AssetImage('assets/images/logo.png'),
                    width: 300
                  ),
                ),

                Container(
                  width: largeurBoutons,
                  height: hauteurBoutons,
                  margin: EdgeInsets.all(margeBoutons),
                  child: RaisedButton(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(radiusBoutons), 
                    ),
                    color: couleurBoutons,
                    child: Text(
                      'S\'inscrire',
                      style: TextStyle(fontSize: taillePoliceBoutons) 
                      ),
                    onPressed: () {
                    },
                  ),
                ),

                Container(
                  width: largeurBoutons,
                  height: hauteurBoutons,
                  margin: EdgeInsets.all(margeBoutons),
                  child: RaisedButton(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(radiusBoutons), 
                    ),
                    color: couleurBoutons,
                    child: Text(
                      'Se connecter',
                      style: TextStyle(fontSize: taillePoliceBoutons) 
                      ),
                    onPressed: () {
                    },
                  ),
                ),

                Container(
                  width: largeurBoutons,
                  height: hauteurBoutons,
                  margin: EdgeInsets.all(margeBoutons),
                  child: RaisedButton(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(radiusBoutons), 
                    ),
                    color: couleurBoutons,
                    child: Text(
                      'Utilisateur anonyme',
                      style: TextStyle(fontSize: taillePoliceBoutons) 
                      ),
                    onPressed: () {
                    },
                  ),
                ),

                /*Container(
                  width: largeurBoutons,
                  height: hauteurBoutons,
                  margin: EdgeInsets.all(margeBoutons),
                  child: RaisedButton(
                    
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(radiusBoutons), 
                    ),
                    color: couleurBoutons,
                    child: Text('eeeeee'),  
                    onPressed: () {
                    },
                  ),
                ),*/

                /*Container(
                  width: largeurBoutons,
                  height: hauteurBoutons,
                  margin: EdgeInsets.all(margeBoutons),
                  child: RaisedButton(
                    color: couleurBoutons,
                    child: Text('essai'),
                    onPressed: () {
                    },
                  ),
                ),*/

                /*Container(
                  width: largeurBoutons,
                  height: hauteurBoutons,
                  margin: EdgeInsets.all(margeBoutons),
                  child: TextButton.icon(
                    
                    onPressed: null,
                    icon: Icon(Icons.delete),
                    label: Text('dededdd'),
                    
                  ),
                ),*/


              ],
            )
          ) 
        )
      )
    );  
  }
}


