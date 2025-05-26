import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/scan_result.dart';

class ScanService {
  // Get API URL from environment or use default Codespace URL
  static String get baseUrl {
    // When running in Codespace, this will be replaced with the actual URL
    const codespaceUrl = String.fromEnvironment(
      'API_URL',
      defaultValue: 'http://localhost:8000',
    );
    return codespaceUrl;
  }

  Future<ScanResult> performScan({
    required String url,
    bool scanSsl = false,
    bool scanCms = false,
    bool scanHeaders = false,
    bool scanCdn = false,
    bool scanDns = false,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/scan'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'url': url,
          'scan_ssl': scanSsl,
          'scan_cms': scanCms,
          'scan_headers': scanHeaders,
          'scan_cdn': scanCdn,
          'scan_dns': scanDns,
        }),
      );

      if (response.statusCode == 200) {
        return ScanResult.fromJson(jsonDecode(response.body));
      } else {
        throw Exception('Failed to perform scan: ${response.body}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
} 