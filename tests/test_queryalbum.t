  $ export BEETSDIR="$PWD"

# Verify that beets works
  $ beet version >/dev/null

# Set up initial beets configuration

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > plugins: queryalbum
  > END

# Test

  $ beet import -qcWA "$TESTDIR/data/250-milliseconds-of-silence.mp3"
  (.*).mp3 (re)
  $ beet modify -ya id:1 new_album_field=foo
  Modifying 1 albums.
  Anar Software LLC - Blank Audio
    new_album_field: foo
  $ beet ls new_album_field:foo
  $ beet ls album_has:new_album_field:foo
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
