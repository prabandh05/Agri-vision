import 'package:flutter/services.dart';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'package:flutter/foundation.dart';
import 'dart:io' show Platform, Directory, File;

class DatabaseHelper {
  static final DatabaseHelper _instance = DatabaseHelper._internal();
  static dynamic _database;

  factory DatabaseHelper() => _instance;
  DatabaseHelper._internal();

  Future<dynamic> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<dynamic> _initDatabase() async {
    if (kIsWeb) {
      // Return a dummy database object for Web to allow UI testing
      return _MockDatabase();
    }

    if (Platform.isLinux || Platform.isWindows) {
      sqfliteFfiInit();
      databaseFactory = databaseFactoryFfi;
    }

    var databasesPath = await getDatabasesPath();
    var path = join(databasesPath, "mandya_agri.db");

    // Check if the database exists
    var exists = await databaseExists(path);

    if (!exists) {
      // Should happen only the first time you launch your application
      print("Creating new copy from asset");

      // Make sure the parent directory exists
      try {
        await Directory(dirname(path)).create(recursive: true);
      } catch (_) {}

      // Copy from asset
      ByteData data = await rootBundle.load(join("assets", "db", "mandya_agri.db"));
      List<int> bytes =
          data.buffer.asUint8List(data.offsetInBytes, data.lengthInBytes);

      // Write and flush the bytes written
      await File(path).writeAsBytes(bytes, flush: true);
    } else {
      print("Opening existing database");
    }

    // open the database
    return await openDatabase(path, readOnly: true);
  }

  /// Full-text search using FTS5
  Future<List<Map<String, dynamic>>> ftsSearch(String query, {int limit = 15}) async {
    if (kIsWeb) {
      return _getWebMockResults(query);
    }
    final db = await database;
    
    // Sanitize query for FTS5
    String sanitized = query.replaceAll(RegExp(r'[^\w\s]'), ' ').trim();
    if (sanitized.isEmpty) return [];
    
    List<String> tokens = sanitized.split(RegExp(r'\s+')).where((t) => t.length > 1).toList();
    if (tokens.isEmpty) return [];
    
    String ftsQuery = tokens.join(' OR ');

    try {
      final List<Map<String, dynamic>> results = await db.rawQuery('''
        SELECT k.doc_id, k.category, k.title, k.content, k.metadata, k.crop, k.tags, fts.rank
        FROM knowledge_fts fts
        JOIN knowledge k ON k.id = fts.rowid
        WHERE knowledge_fts MATCH ?
        ORDER BY fts.rank
        LIMIT ?
      ''', [ftsQuery, limit]);
      
      return results;
    } catch (e) {
      print("FTS5 Search Error: $e");
      return [];
    }
  }

  Future<List<Map<String, dynamic>>> getByCategory(String category, {int limit = 20}) async {
    if (kIsWeb) {
      return _getWebMockResults(category);
    }
    final db = await database;
    return await db.query(
      'knowledge',
      where: 'category = ? AND doc_id NOT LIKE ?',
      whereArgs: [category, '%_faq_%'],
      orderBy: 'title',
      limit: limit,
    );
  }

  List<Map<String, dynamic>> _getWebMockResults(String query) {
    // Mock data for Web testing - Expanded for better testing
    final List<Map<String, dynamic>> allData = [
      {'title': 'Coconut Cultivation', 'category': 'crop', 'content': 'Coconut requires saline sandy soil and high humidity. Major plantation in Mandya.', 'doc_id': 'crop_coconut'},
      {'title': 'Paddy (Rice)', 'category': 'crop', 'content': 'Paddy is a major food crop. Requires standing water and high nitrogen.', 'doc_id': 'crop_paddy'},
      {'title': 'Sugarcane', 'category': 'crop', 'content': 'Sugarcane is a commercial crop. Requires heavy irrigation and urea.', 'doc_id': 'crop_sugarcane'},
      {'title': 'Ragi (Finger Millet)', 'category': 'crop', 'content': 'Drought resistant crop. Very popular in Karnataka for health benefits.', 'doc_id': 'crop_ragi'},
      {'title': 'Banana', 'category': 'crop', 'content': 'Needs well-drained soil and regular organic manure. Keep soil moist.', 'doc_id': 'crop_banana'},
      {'title': 'Mango', 'category': 'crop', 'content': 'Grown in dry areas. Requires minimal water once established.', 'doc_id': 'crop_mango'},
      {'title': 'Blast Disease', 'category': 'disease', 'content': 'Fungal disease in paddy causing diamond spots. Control with Tricyclazole.', 'doc_id': 'dis_blast'},
      {'title': 'Red Rot', 'category': 'disease', 'content': 'Fungal disease in Sugarcane. Leaves turn yellow. Destroy infected plants.', 'doc_id': 'dis_redrot'},
      {'title': 'Leaf Spot', 'category': 'disease', 'content': 'Small brown spots on leaves. Use copper-based fungicides.', 'doc_id': 'dis_leafspot'},
      {'title': 'PM-KISAN', 'category': 'scheme', 'content': 'Direct income support of 6000 INR per year to all landholding farmers.', 'doc_id': 'sch_pmkisan'},
      {'title': 'Crop Insurance', 'category': 'scheme', 'content': 'Pradhan Mantri Fasal Bima Yojana covers crop loss due to natural calamities.', 'doc_id': 'sch_bima'},
      {'title': 'Kisan Credit Card', 'category': 'scheme', 'content': 'Provides timely credit to farmers for their cultivation needs.', 'doc_id': 'sch_kcc'},
    ];

    if (query == 'crop' || query == 'disease' || query == 'scheme') {
      return allData.where((d) => d['category'] == query).toList();
    }

    return allData.where((d) {
      final title = d['title'].toString().toLowerCase();
      final content = d['content'].toString().toLowerCase();
      return title.contains(query.toLowerCase()) || content.contains(query.toLowerCase());
    }).toList();
  }
}

// Dummy class to satisfy type requirements on Web
class _MockDatabase {
}
