  $ export BEETSDIR="$PWD"

# Verify that beets works
  $ beet version >/dev/null

# Set up initial beets configuration

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > plugins: advisory
  > END

# Test explicit

  $ cp "$TESTDIR/data/250-milliseconds-of-silence.mp3" test.mp3
  $ "$TESTDIR"/scripts/set-itunesadvisory test.mp3 1
  $ beet import -qcWA test.mp3
  .*/test.mp3 (re)
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    advisory: 1
  Anar Software LLC - Blank Audio
    albumadvisory: 1

# Test clean

  $ cp test.mp3 test2.mp3
  $ "$TESTDIR"/scripts/set-itunesadvisory test2.mp3 2
  $ beet import -qcWA test2.mp3
  .*/test2.mp3 (re)
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    advisory: 2

# Test write

  $ rm library.db
  $ rm -f Anar*/**/*.mp3
  $ beet import -qcWA "$TESTDIR/data/250-milliseconds-of-silence.mp3"
  .*/250-milliseconds-of-silence.mp3 (re)
  $ beet ls -p
  .*/test_advisory.*/.* (re)
  $ beet modify -y id:1 advisory=1
  Modifying 1 items.
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    advisory: 1
  $ beet write-advisory
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    advisory: 0 -> 1
  $ "$TESTDIR"/scripts/get-itunesadvisory Anar*/**/*.mp3
  1

# Test noauto

  $ rm library.db; cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > plugins: advisory
  > advisory:
  >   auto: no
  > END
  $ beet import -qcWA test.mp3
  .*/test.mp3 (re)
  $ beet ls advisory:1
  $ beet read-advisory -p id:1
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    advisory: 1
  Anar Software LLC - Blank Audio
    albumadvisory: 1
  $ beet ls advisory:1
  $ beet read-advisory id:1
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    advisory: 1
  Anar Software LLC - Blank Audio
    albumadvisory: 1
  $ beet ls -f '$advisory'
  1
