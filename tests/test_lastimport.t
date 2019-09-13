Verify that beets works

  $ beet version >/dev/null
  $ echo $?
  0

Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > plugins: last_import
  > END

Test with album

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1
  $ beet ls
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
  $ beet last-import
  $ beet last-import -a
  [^ ]+ [^ ]+ Anar Software LLC - Blank Audio (re)
  $ beet ls -a -f '$last_import'
  True

Test with singleton

  $ beet import -qscWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1
  $ beet ls
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
  $ beet last-import -a
  $ beet last-import
  [^ ]+ [^ ]+ Anar Software LLC - Blank Audio - 250 Milliseconds of Silence (re)
  $ beet ls -f '$last_import'
  1
