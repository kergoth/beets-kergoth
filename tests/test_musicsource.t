Verify that beets works

  $ beet version >/dev/null
  $ echo $?
  0

Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > plugins: musicsource
  > END

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3"
  error: No source specified, please include --set=source=SOURCE
  [1]
  $ beet import -qCWA --set=source=Foo "$TESTDIR/data/250-milliseconds-of-silence.mp3"
  /.*/250-milliseconds-of-silence.mp3 (re)
