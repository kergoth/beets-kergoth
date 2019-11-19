  $ export BEETSDIR="$PWD"

Verify that beets works
  $ beet version >/dev/null

Set up initial beets configuration

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > plugins: inconsistentalbumtracks
  > ui:
  >   color: no
  > inconsistentalbumtracks:
  >   ignored_fields: added genre
  > END

Import the album

  $ mkdir test
  $ cp "$TESTDIR/data/250-milliseconds-of-silence.mp3" test/test.mp3
  $ cp "$TESTDIR/data/250-milliseconds-of-silence.mp3" test/test2.mp3
  $ beet import -qCWA test
  .*/test (re)

Add inconsistency

  $ beet modify -yW id:2 album=wrong
  Modifying 1 items.
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    album: Blank Audio -> wrong

Check sanity

  $ beet ls -a
  Anar Software LLC - Blank Audio
  $ beet ls -f '$album'
  Blank Audio
  wrong

Identify the inconsistent album title

  $ beet inconsistent-album-tracks
  Anar Software LLC - wrong - 250 Milliseconds of Silence: field `album` has value `wrong` but album value is `Blank Audio`

Test ignored_fields

  $ beet modify -yWa genre=Silence
  Modifying 1 albums.
  Anar Software LLC - Blank Audio
    genre:  -> Silence
  $ beet modify -yW id:2 album='Blank Audio' genre=inconsistent >/dev/null
  $ beet inconsistent-album-tracks
