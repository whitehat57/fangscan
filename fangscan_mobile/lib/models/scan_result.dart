class ScanResult {
  final String url;
  final Map<String, dynamic>? sslInfo;
  final Map<String, List<String>>? technologies;
  final Map<String, String>? cms;
  final List<String>? javascriptFrameworks;
  final Map<String, dynamic>? serverInfo;
  final Map<String, List<String>>? dns;
  final Map<String, dynamic>? headers;

  ScanResult({
    required this.url,
    this.sslInfo,
    this.technologies,
    this.cms,
    this.javascriptFrameworks,
    this.serverInfo,
    this.dns,
    this.headers,
  });

  factory ScanResult.fromJson(Map<String, dynamic> json) {
    return ScanResult(
      url: json['url'] as String,
      sslInfo: json['ssl_info'] as Map<String, dynamic>?,
      technologies: (json['technologies'] as Map<String, dynamic>?)?.map(
        (k, v) => MapEntry(k, List<String>.from(v as List)),
      ),
      cms: (json['cms'] as Map<String, dynamic>?)?.map(
        (k, v) => MapEntry(k, v.toString()),
      ),
      javascriptFrameworks: json['javascript_frameworks'] != null
          ? List<String>.from(json['javascript_frameworks'] as List)
          : null,
      serverInfo: json['server_info'] as Map<String, dynamic>?,
      dns: (json['dns'] as Map<String, dynamic>?)?.map(
        (k, v) => MapEntry(k, List<String>.from(v as List)),
      ),
      headers: json['headers'] as Map<String, dynamic>?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'url': url,
      if (sslInfo != null) 'ssl_info': sslInfo,
      if (technologies != null) 'technologies': technologies,
      if (cms != null) 'cms': cms,
      if (javascriptFrameworks != null)
        'javascript_frameworks': javascriptFrameworks,
      if (serverInfo != null) 'server_info': serverInfo,
      if (dns != null) 'dns': dns,
      if (headers != null) 'headers': headers,
    };
  }
} 