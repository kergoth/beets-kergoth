Verify that beets works

  $ beet version >/dev/null
  $ echo $?
  0

Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > plugins: modifytmpl the
  > END

Test with album

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1
  $ beet ls
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence

Test referencing other fields

  $ beet modifytmpl -yW id:1 artist_credit::'^$' artist_credit='$artist'
  Modifying 1 items.
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    artist_credit:  -> Anar Software LLC

Test use of a format function

  $ beet modify -yaW id:1 album='The Test'
  Modifying 1 albums.
  Anar Software LLC - Blank Audio
    album: Blank Audio -> The Test

  $ beet modifytmpl -yaW id:1 album_sort='%the{$album}'
  Modifying 1 albums.
  Anar Software LLC - The Test
    album_sort: Test, The
