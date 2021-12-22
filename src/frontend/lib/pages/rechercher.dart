// ignore_for_file: prefer_const_constructors
import 'package:flutter/material.dart';

main() => runApp(
      MaterialApp(
        home: Rechercher()
      ),
    );

class Rechercher extends StatefulWidget {
  const Rechercher({Key? key}) : super(key: key);

  @override
  _RechercherState createState() => _RechercherState();
}

class _RechercherState extends State<Rechercher> {
  late TextEditingController controller;

  @override
  void initState() {
    super.initState();
    controller = TextEditingController();
  }

  @override
  Widget build(BuildContext context) {
      return Scaffold(
        backgroundColor: Color(0xFFC1DFF0),
        appBar: AppBar(
          backgroundColor: Colors.grey.shade50,
          actions: const [
            Padding(
              padding: EdgeInsets.only(right: 10),
              child: Icon(
                Icons.search,
                color:Colors.black
              ),
            )
          ],
          title: TextField(
            decoration: InputDecoration(
                border: InputBorder.none,
                hintText: 'Rechercher une ressource'),
            controller: controller,
            cursorColor: Colors.black,
            style: TextStyle(color: Colors.black),
          ),
        ),
        //body: TabBarView(children: [Container(), Container()]),
      );
  }
}