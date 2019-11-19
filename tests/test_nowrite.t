  $ export BEETSDIR="$PWD"

# Verify that beets works
  $ beet version >/dev/null

# Set up initial beets configuration

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > plugins: nowrite
  > END

Test nowrite

  $ beet import -qcWA "$TESTDIR/data/250-milliseconds-of-silence.mp3"
  .*/data/250-milliseconds-of-silence.mp3 (re)
  nowrite: ignoring attempt to move (.*) (re)
  $ beet ls -p
  (.*)/250-milliseconds-of-silence.mp3 (re)
  $ beet modify -yw id:1 title=foo >/dev/null
  nowrite: ignoring attempt to write (.*) (re)
  $ beet update -F title id:1
  Anar Software LLC - Blank Audio - foo
    title: foo -> 250 Milliseconds of Silence
