import '../database/db_helper.dart';
import 'dart:convert';
import 'dart:math';

enum QuerySource { offline, online, sms, prediction, none }

class QueryResult {
  final String title;
  final String answer;
  final QuerySource source;
  final double confidence;
  final List<String> followUps;

  QueryResult({
    required this.title,
    required this.answer,
    required this.source,
    this.confidence = 1.0,
    this.followUps = const [],
  });
}

class QueryEngine {
  final DatabaseHelper _dbHelper = DatabaseHelper();
  static const double offlineThreshold = 0.1; // Lowered to be more lenient

  /// Main entry point for processing a query
  Future<QueryResult> processQuery(String query) async {
    // 1. Translator Hook (Placeholder for friend's module)
    String translatedQuery = await _translateIfNeeded(query);
    
    String cleanQuery = translatedQuery.toLowerCase().trim();

    // 2. Step 1: Search Offline Database
    final offlineResults = await _dbHelper.ftsSearch(cleanQuery);
    if (offlineResults.isNotEmpty) {
      final bestMatch = offlineResults.first;
      double confidence = _calculateConfidence(cleanQuery, bestMatch);
      
      // Handle negations (e.g. "other than")
      if (_hasNegation(cleanQuery)) {
        final filtered = _filterNegated(offlineResults, cleanQuery);
        if (filtered.isNotEmpty) {
          return _formatOfflineResponse(filtered.first, confidence);
        }
      } 
      
      // Return best match regardless of threshold for better user experience during testing
      return _formatOfflineResponse(bestMatch, confidence);
    }

    // 3. Step 2: Check for predictable data (e.g. Weather)
    if (_isPredictable(cleanQuery)) {
      return _getPrediction(cleanQuery);
    }

    // 4. Step 3: Online / SMS Fallback Path
    return await _handleConnectivityFallback(cleanQuery);
  }

  /// Placeholder for Translator Integration
  Future<String> _translateIfNeeded(String query) async {
    // This is where your friend's translator module will be integrated.
    // For now, it returns the original query.
    return query;
  }

  /// Step 2 logic: Is this query predictable (e.g. weather trends)?
  bool _isPredictable(String query) {
    return query.contains('weather') || query.contains('rain') || query.contains('temperature');
  }

  /// Predictive model placeholder (using previous trends)
  QueryResult _getPrediction(String query) {
    // In a real app, this would use a local model or historical CSV data.
    return QueryResult(
      title: 'Historical Weather Prediction',
      answer: "Based on Mandya's historical data for this season, expect moderate rainfall and temperatures between 24°C and 30°C. \n\n(Note: This is a prediction from historical trends as internet is unavailable).",
      source: QuerySource.prediction,
      followUps: ['See full seasonal trend', 'Previous year data'],
    );
  }

  /// Step 3 logic: Check Internet -> SMS -> Fail
  Future<QueryResult> _handleConnectivityFallback(String query) async {
    bool hasInternet = await _checkInternet();
    
    if (hasInternet) {
      return await _searchOnline(query);
    } else {
      // SMS Path Placeholder
      return await _sendSMSQuery(query);
    }
  }

  Future<bool> _checkInternet() async {
    // Logic to check real connectivity
    return false; // Defaulting to false to test offline paths
  }

  Future<QueryResult> _searchOnline(String query) async {
    // This is where your server-side LLM call happens
    return QueryResult(
      title: 'Online Expert Advisory',
      answer: "Connecting to server for real-time information on \"$query\"...",
      source: QuerySource.online,
    );
  }

  Future<QueryResult> _sendSMSQuery(String query) async {
    // This is where the SMS fallback logic goes
    return QueryResult(
      title: 'No Internet Connection',
      answer: "I couldn't find this information offline. \n\n**Would you like to request this via SMS?** (SMS advisory may take a few minutes).",
      source: QuerySource.sms,
      followUps: ['Send SMS Request', 'Try another question'],
    );
  }

  QueryResult _formatOfflineResponse(Map<String, dynamic> match, double confidence) {
    final title = match['title'] ?? 'Farming Advisory';
    final content = match['content'] ?? '';
    
    // Wrap in conversational language for "human-understandable" output
    final formattedAnswer = _wrapInConversationalLanguage(title, content);

    return QueryResult(
      title: title,
      answer: formattedAnswer,
      source: QuerySource.offline,
      confidence: confidence,
      followUps: ['Detailed guide', 'Similar crops', 'Common diseases'],
    );
  }

  String _wrapInConversationalLanguage(String title, String content) {
    final templates = [
      "Here is what I found regarding **$title**:\n\n$content",
      "According to our agricultural records for **$title**:\n\n$content",
      "I have some guidance about **$title** that might help you:\n\n$content",
      "For **$title**, the expert recommendation is:\n\n$content",
    ];
    return templates[Random().nextInt(templates.length)];
  }

  // --- Helper Math / Filtering Logic ---

  double _calculateConfidence(String query, Map<String, dynamic> match) {
    List<String> queryTerms = query.split(RegExp(r'\s+')).where((t) => t.length > 2).toList();
    if (queryTerms.isEmpty) return 0.5;
    String content = ((match['title'] ?? '') + ' ' + (match['content'] ?? '')).toLowerCase();
    int hits = 0;
    for (var term in queryTerms) {
      if (content.contains(term)) hits++;
    }
    return hits / queryTerms.length;
  }

  bool _hasNegation(String query) => query.contains('other than') || query.contains('not') || query.contains('except');

  List<Map<String, dynamic>> _filterNegated(List<Map<String, dynamic>> results, String query) {
    final negated = _extractNegatedTerms(query);
    return results.where((r) {
      final title = (r['title'] ?? '').toString().toLowerCase();
      return !negated.any((term) => title.contains(term));
    }).toList();
  }

  List<String> _extractNegatedTerms(String query) {
    final List<String> negated = [];
    final patterns = ['other than', 'not', 'except'];
    for (var p in patterns) {
      if (query.contains(p)) {
        final parts = query.split(p);
        if (parts.length > 1) {
          final wordsAfter = parts[1].trim().split(' ');
          if (wordsAfter.isNotEmpty) negated.add(wordsAfter[0].replaceAll(RegExp(r'[^\w]'), ''));
        }
      }
    }
    return negated;
  }
}
