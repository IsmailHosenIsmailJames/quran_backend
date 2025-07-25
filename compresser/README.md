# Quran Backend - Compressor

This directory contains a Dart-based command-line application for compressing the data used in the Quran backend.

## Usage

To use the compressor, run the following command from the `compresser` directory:

```bash
dart run
```

This will process the files in the `public/quranic_universal_library/translation/fix_wdw_simplifer` directory and output compressed versions to `public/quranic_universal_library/compressed_translation_word_by_word`.

## How it Works

The compressor uses the `archive` package to create compressed archives of the data files. The main logic is in `bin/compresser.dart`, which reads the files, compresses them using BZip2, and then saves them to the specified output directory.

## Contributing

Contributions to this project are welcome. Please see the main project's `README.md` for more information on how to contribute.