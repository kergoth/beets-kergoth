  $ export BEETSDIR="$PWD"
  $ beet version >/dev/null

  $ cat >"$PWD/config.yaml" <<END
  > directory: library
  > ui:
  >   color: no
  > pluginpath:
  >   - $TESTDIR/beetsplug
  > plugins: mockedcandidate zero
  > zero:
  >   fields: year
  >   update_database: true
  > END

Zero does not zero album fields when it updates the database

  $ (echo y; echo a;) | beet import -S mocked "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null
  $ beet ls -f '$year'
  0000
  $ beet ls -a -f '$year'
  2019

Zero the album fields

  $ rm library.db
  $ echo 'plugins: mockedcandidate zero zeroalbum' >>config.yaml
  $ (echo y; echo a;) | beet import -S mocked "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null
  $ beet ls -f '$year'
  0000
  $ beet ls -a -f '$year'
  0000
