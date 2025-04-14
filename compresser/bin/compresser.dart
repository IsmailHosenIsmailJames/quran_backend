import 'dart:convert';
import 'dart:io';

import 'package:archive/archive_io.dart';
import 'package:path/path.dart';

void main(List<String> arguments) async {
  DateTime startTime = DateTime.now();
  Directory tafsirDir = Directory(
    '../public/quranic_universal_library/translation/wdw_simplifer',
  );
  for (FileSystemEntity lang in tafsirDir.listSync()) {
    Directory languageDir = Directory(lang.path);
    for (FileSystemEntity file in languageDir.listSync()) {
      DateTime dateTime = DateTime.now();
      print("Processing -> \t${file.path}");
      String jsonData = await File(file.path).readAsString();
      BZip2Encoder bZip2Encoder = BZip2Encoder();
      List<int> compressedBytes = bZip2Encoder.encode(utf8.encode(jsonData));
      String compressedBase64String = base64Encode(compressedBytes);
      String savingPath = join(
        tafsirDir.parent.path,
        "compressed_translation_word_by_word",
        languageDir.path.split("/").last,
      );
      if (!(await Directory(savingPath).exists())) {
        Directory(savingPath).createSync(recursive: true);
      }
      await File(
        '${join(savingPath, basename(file.path))}.txt'.replaceAll(' ', '_'),
      ).writeAsString(compressedBase64String);
      print(
        "Success -> \t${DateTime.now().difference(dateTime).inMilliseconds / 1000} seconds",
      );
    }
  }
  print(
    "Program finished in ${DateTime.now().difference(startTime).inSeconds} seconds",
  );
}
