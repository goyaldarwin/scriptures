# Test fixtures

Data the tests use and the library does not. Each is used only by `tools/site/ux_test.py`.

- `shirdi-transcribed/`: an audio source of the Shirdi Dhūpa Āratī (the Sai Aashirwad upload, YouTube `QKf_JPbN6Lw`) whose starts come only from its transcript and hand-checked word times (`fixes.json`, `fixes.md`), with no times set by ear. The workflow test copies it into a temporary library as `tools/works/shirdi-sai-dhoop-aarti/audio/pramod-medhi` and sends it starts with `tools/audio/apply_owner_timing.py`.
