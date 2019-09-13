Verify that beets works

  $ beet version >/dev/null
  $ echo $?
  0

Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > plugins: saved_formats
  > album_formats:
  >   album_id: '\$id'
  > item_formats:
  >   artist_title: '\$artist - \$title'
  > END

Set up library

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1
  $ beet ls
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence

Album format

  $ beet ls -a -f '$id'
  1
  $ beet ls -a -f '$album_id'
  1

Item format

  $ beet ls -f '$artist_title'
  Anar Software LLC - 250 Milliseconds of Silence
