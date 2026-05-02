import 'package:flutter/material.dart';
import 'screens/chat_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const AgriVisionApp());
}

class AgriVisionApp extends StatelessWidget {
  const AgriVisionApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AgriVision',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: const Color(0xFF4CAF6F),
        scaffoldBackgroundColor: const Color(0xFF0D1B0F),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF4CAF6F),
          secondary: Color(0xFFF9A825),
          surface: Color(0xFF152217),
          onSurface: Color(0xFFE8F5E9),
        ),
        textTheme: const TextTheme(
          titleLarge: TextStyle(color: Color(0xFFE8F5E9), fontWeight: FontWeight.bold),
          bodyMedium: TextStyle(color: Color(0xFFA5D6A7)),
        ),
        useMaterial3: true,
      ),
      home: const ChatScreen(),
    );
  }
}
