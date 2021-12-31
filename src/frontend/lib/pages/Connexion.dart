// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:tez/common/constants.dart';


class Connexion extends StatefulWidget {
  const Connexion({ Key? key }) : super(key: key);
  
  @override
  _ConnexionState createState() => _ConnexionState();
}


class _ConnexionState extends State<Connexion> {
  @override
  Widget build(BuildContext context) {

    double margeBoutons = 10;
    double largeurBoutons = 250;
    double hauteurBoutons = 50;
    double taillePoliceBoutons = 23;
    double radiusBoutons = 15;
    Color couleurBoutons = lightGreen;
    
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'page de demarrage',
      home: Scaffold(
       
        backgroundColor: darkGreen,
        body: Center(
          child: SingleChildScrollView(
            padding: EdgeInsets.symmetric(
              horizontal: 20,
            ),
            child: Column(
              children: [
                
                Container(
                  child: Image(
                    image: AssetImage('assets/images/logo.png'),
                    width: 300
                  ),
                ),

                SizedBox(
                  height: 40,
                ),

                Form(
                  child: Column(
                    children: [
                      Align(
                        alignment: Alignment.centerLeft,
                        child: Text('Entrez votre email'),
                      ),
                      
                      TextFormField(
                        decoration: InputDecoration(
                          hintText: 'michel.dupont@exemple.fr',
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(radiusBoutons))
                        ),
                      )
                    ],
                  )
                ),

                SizedBox(
                  height: 20,
                ),

                Form(
                  child: Column(
                    children: [
                      Align(
                        alignment: Alignment.centerLeft,
                        child: Text('Entrez votre mot de passe'),
                      ),
                      
                      TextFormField(
                        obscureText: true,
                        decoration: InputDecoration(
                          hintText: 'ֹֹּּ**********',
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(radiusBoutons))
                        ),
                      )
                    ],
                  )
                ),

                SizedBox(
                  height: 20,
                ),

                Container(
                  width: largeurBoutons,
                  height: hauteurBoutons,
                
                  child: RaisedButton(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(radiusBoutons), 
                    ),
                    color: couleurBoutons,
                    child: Text(
                      'Valider',
                      style: TextStyle(fontSize: taillePoliceBoutons) 
                      ),
                    onPressed: () {
                    },
                  ),
                ),

              ],
            )
          )
        )
      )
    );  
  }
}


