import 'package:flutter/material.dart';
import '../database/db_helper.dart';

class BrowseScreen extends StatefulWidget {
  const BrowseScreen({super.key});

  @override
  State<BrowseScreen> createState() => _BrowseScreenState();
}

class _BrowseScreenState extends State<BrowseScreen> {
  final DatabaseHelper _dbHelper = DatabaseHelper();
  List<Map<String, dynamic>> _crops = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadCrops();
  }

  Future<void> _loadCrops() async {
    final crops = await _dbHelper.getByCategory('crop', limit: 100);
    setState(() {
      _crops = crops;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Browse Crops"),
        backgroundColor: Colors.transparent,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _crops.length,
              itemBuilder: (context, index) {
                final crop = _crops[index];
                return Card(
                  color: const Color(0xFF1E3022),
                  margin: const EdgeInsets.only(bottom: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  child: ListTile(
                    leading: const CircleAvatar(
                      backgroundColor: Color(0xFF1B5E20),
                      child: Text("🌾"),
                    ),
                    title: Text(crop['title'] ?? 'Unknown Crop', style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text(crop['crop'] ?? 'Agricultural resource', style: const TextStyle(color: Color(0xFF5C8A62))),
                    trailing: const Icon(Icons.chevron_right, color: Color(0xFF4CAF6F)),
                    onTap: () {
                      // Navigate back to chat with the crop name as query
                      Navigator.pop(context, crop['title']);
                    },
                  ),
                );
              },
            ),
    );
  }
}
