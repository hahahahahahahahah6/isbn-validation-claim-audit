# Book-number claim audit

This offline tool compares documentation claims about book-number check digits with static call shapes in source files. It does not execute inspected code.

## Usage

```sh
isbn-validation-claim-audit audit . --verbose
python3 -m isbn_validation_claim_audit audit . --json
```

The optional path defaults to the current directory. Repeat `--ignore PREFIX` to omit paths, and use `--fail-on medium` to include test-only findings in the exit threshold. Exit status is 0 for pass, 2 for findings at the threshold, and 1 for usage or I/O errors.

The JSON report contains claims, denials, findings, and production and test evidence paths. The finding identifiers are:

```
documented-isbn-validation-claim-false
documented-no-isbn-validation-claim-false
```

## Limitations

This phrase may describe a catalogue lookup rather than a check-digit operation:

```
validate isbn
```

This phrase may describe a manual runbook step rather than a check-digit operation:

```
check isbn
```

This phrase may describe a roadmap item rather than a check-digit operation:

```
isbn validation
```

This phrase may describe a hosted page rather than a check-digit operation:

```
isbn validator
```

This phrase may describe reader advice rather than a check-digit operation:

```
valid isbn
```

This phrase may describe a successful lookup rather than a check-digit operation:

```
isbn is valid
```

This phrase may describe a specification section rather than a check-digit operation:

```
isbn number validation
```

This phrase may describe a design discussion rather than a check-digit operation:

```
isbn10 validation
```

This phrase may describe a design discussion rather than a check-digit operation:

```
isbn13 validation
```

This phrase may describe an allow-list lookup rather than a check-digit operation:

```
validate isbn10
```

This phrase may describe an allow-list lookup rather than a check-digit operation:

```
validate isbn13
```

This phrase may describe a catalogue lookup rather than a check-digit operation:

```
verify isbn
```

This phrase may describe a length-only check rather than a check-digit operation:

```
detect invalid isbn
```

This phrase may describe a theoretical discussion rather than a check-digit operation:

```
isbn well formed
```

This phrase may describe a generated value rather than a check-digit operation:

```
is valid isbn
```

This phrase may describe a publisher list lookup rather than a check-digit operation:

```
validate book number
```

This phrase may describe a hyphen-layout check rather than a check-digit operation:

```
isbn format validation
```

Construction of the recognised object counts even if its result is unused. A negative-judgement call counts as evidence. Canonicalisation is not evidence. Cleaning is not evidence. Masking is not evidence. Computing a check digit is not evidence, even when compared afterward. Conversion is not evidence. Extraction of number-like strings is not evidence. Fetching metadata is not evidence. Compacting is not evidence. Splitting is not evidence. Formatting is not evidence. Barcode construction is not evidence. A regular expression match alone is not evidence.

A module held in an untraced variable can be missed. An import alone is not evidence. Roadmap prose still counts as a claim. Changelog prose still counts as a claim. TODO prose still counts as a claim. An unlisted denial may be missed. A top-level changelog is not read. Routes split across modules are missed. A locally defined route shadows an import. Dead code counts. A subprocess invocation is not evidence. A generic input check is not evidence. An email check is not evidence. A phone check is not evidence. A web-address check is not evidence. A numeric-address check is not evidence. A host-name check is not evidence. Extraction is not evidence. A locally defined generic name is shadowed. Successive aliases can be missed. Exact phrases are matched rather than meaning. Other languages are invisible. Dynamic imports and runtime plugins are invisible. An attribute read alone is not evidence.

## Differentiation

This scope concerns book-number check digits. Neighbouring families cover generic input checks, payment processing, card-detail extraction, account authentication, password verification, password hashing, password generation, PDF encryption, email sending, SMS sending, document extraction, barcode scanning, email addresses, phone numbers, password strength, JSON Schema, dates, credit cards, domain names, URLs and IP addresses. JSON decoding, regex matching, URL parsing, network fetching and DNS resolution are separate operations. Barcode generation encodes a number; document extraction reads one. Formatting and conversion reshape a number.

Other families cover spreadsheet reading and generation, word-document reading and generation, presentation reading and generation, PDF extraction, generation, merging, splitting, rotation, form-filling, watermarking, redaction, compression and annotation, table extraction, OCR, document extraction, e-signature, screen recording, video generation, QR code generation, barcode generation and scanning, audio mixing, generation and editing, source separation, speech recognition, text-to-speech, noise suppression, music generation and transcription. Serial-number checks are also separate.
