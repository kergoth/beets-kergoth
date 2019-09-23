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
  $ beet ls -p
  (.*)/test_advisory.t/(.*)/00 250 Milliseconds of Silence.mp3 (re)
  $ beet ls -f '$advisory'
  1
  $ beet ls -a -f '$albumadvisory'
  1

# Test clean

  $ cp test.mp3 test2.mp3
  $ "$TESTDIR"/scripts/set-itunesadvisory test2.mp3 2
  $ beet import -qcWA test2.mp3
  .*/test2.mp3 (re)
  $ beet ls -f '$advisory' id:2
  2
  $ beet ls -a -f '$albumadvisory' id:2
  $albumadvisory
