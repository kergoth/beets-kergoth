  $ export BEETSDIR="$PWD"

Verify that beets works

  $ beet version >/dev/null

Set up initial beets configuration

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > plugins: crossquery
  > END

Init library

  $ beet import -qcWA "$TESTDIR/data/250-milliseconds-of-silence.mp3"
  (.*).mp3 (re)

album_has query with no matches

  $ beet ls album_has:missing_album_field:1

album_has query

  $ beet modify -ya id:1 new_album_field=foo
  Modifying 1 albums.
  Anar Software LLC - Blank Audio
    new_album_field: foo
  $ beet ls new_album_field:foo
  $ beet ls album_has:new_album_field:foo
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence

any_track_has query with no matches

  $ beet ls -a any_track_has:missing_field:1

any_track_has query

  $ beet modify -y id:1 new_item_field=foo
  Modifying 1 items.
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    new_item_field: foo
  $ beet ls -a any_track_has:new_item_field:foo
  Anar Software LLC - Blank Audio

all_tracks_have query with no matches

  $ beet ls -a all_tracks_have:missing_field:1

all_tracks_have query

  $ beet ls -a all_tracks_have:new_item_field:foo
  Anar Software LLC - Blank Audio

init library for multiple tracks

  $ rm library.db
  $ mkdir album
  $ cp "$TESTDIR/data/250-milliseconds-of-silence.mp3" album/test.mp3
  $ cp "$TESTDIR/data/250-milliseconds-of-silence.mp3" album/test2.mp3
  $ beet import -qcWA album
  (.*)/album (re)
  $ beet ls -f '$id'
  1
  2
  $ beet modify -y id:1 new_item_field=foo
  Modifying 1 items.
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    new_item_field: foo

any_track_has query with multiple tracks, 1 matching

  $ beet ls -a any_track_has:new_item_field:foo
  Anar Software LLC - Blank Audio

all_tracks_have query with multiple tracks, 1 matching

  $ beet ls -a all_tracks_have:new_item_field:foo
  $ beet ls -a all_tracks_have:track:1

all_tracks_have query with multiple tracks, all matching

  $ beet ls -a all_tracks_have:track:0
  Anar Software LLC - Blank Audio
